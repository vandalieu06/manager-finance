from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional

from .models import Producto


class TicketParser:
    """Extrae comercio, fecha, total y productos desde el OCR."""

    # Inicializa el parser con lista de comercios conocidos.
    def __init__(self) -> None:
        """Carga comercios conocidos y configura el parser."""
        self.comercios_conocidos = {
            "BON PREU": ["BON PREU", "BONPREU", "BON-PREU"],
            "ESCLAT": ["ESCLAT", "ESCIAT"],
            "MERCADONA": ["MERCADONA"],
            "CARREFOUR": ["CARREFOUR"],
            "DIA": ["DIA %", "DIA MARKET"],
            "LIDL": ["LIDL"],
            "ALDI": ["ALDI"],
            "MEDIA MARKT": ["MEDIA MARKT", "MEDIAMARKT", "MEDIA MARKT SATURN"],
        }

    # Normaliza numeros con coma o punto decimal.
    def normalizar_numero(self, texto: str) -> Optional[float]:
        """Convierte numeros con coma/punto en float normalizado."""
        limpio = texto.replace(" ", "").replace(",", ".")
        match = re.search(r"(\d+)[.,](\d{2})", limpio)
        if match:
            return float(f"{match.group(1)}.{match.group(2)}")
        if limpio.isdigit():
            return float(limpio)
        return None

    # Extrae fechas en formatos habituales o con OCR corrupto.
    def extraer_fecha(self, texto: str) -> Optional[str]:
        """Extrae fechas con varios patrones y tolerancia a OCR."""
        patrones = [
            r"\b(\d{2}[-/\.]\d{2}[-/\.]\d{2,4})\b",
            r"\b(\d{1,2}\s+(?:ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC)[A-Z]*\s+\d{2,4})\b",
            r"\b(\d{4}-\d{2})\b",
            r"\b(\d{2})(\d{2})(\d{2,4})\b",
        ]
        for patron in patrones[:2]:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return match.group(1)
        match = re.search(patrones[2], texto)
        if match:
            s = match.group(1)
            return f"{s[:2]}-{s[2:4]}-{s[5:]}" if len(s) >= 5 else s
        return None

    # Busca fecha/hora con contexto alrededor de palabras clave.
    def extraer_fecha_y_hora_por_contexto(self, lineas: List[str]) -> Optional[str]:
        """Busca fecha/hora cercana a etiquetas como 'Fecha de factura'."""
        prioridad_alta = ["FECHA DE FACTURA", "FECHA DE COMPRA", "FECHA FACTURA"]
        prioridad_media = ["FECHA DE PAGO", "FECHA PAGO", "FECHA DE ENTREGA"]
        prioridad_baja = ["DATA", "TICKET", "FECHA", "HORA"]

        for grupo_claves in [prioridad_alta, prioridad_media, prioridad_baja]:
            for indice, linea in enumerate(lineas):
                linea_upper = linea.upper()
                if any(clave in linea_upper for clave in grupo_claves):
                    fragmento = " ".join(lineas[indice : indice + 6])
                    fecha = self.extraer_fecha(fragmento)
                    hora = re.search(r"\b(\d{1,2}:\d{2})\b", fragmento)
                    if fecha and hora:
                        return f"{fecha} {hora.group(1)}"
                    if fecha:
                        return fecha
                    fecha_corta = re.search(r"\b(\d{2}[-/\.]\d{2})\b", fragmento)
                    if fecha_corta:
                        return fecha_corta.group(1)
        return None

    # Extrae el total priorizando el resumen de IVA y luego TOTAL.
    def extraer_total_por_contexto(self, lineas: List[str]) -> Optional[float]:
        """Obtiene el total priorizando el resumen final de IVA."""
        indice_resumen = None
        for i, linea in enumerate(lineas):
            linea_upper = linea.upper()
            if "TIPO IVA" in linea_upper or "BASE IMPONIBLE" in linea_upper:
                if i > len(lineas) * 0.5:
                    indice_resumen = i
                    break

        if indice_resumen is not None:
            for i in range(indice_resumen, min(indice_resumen + 10, len(lineas))):
                linea_upper = lineas[i].upper().replace(" ", "")
                if "TOTAL" in linea_upper:
                    for offset in range(i, min(i + 4, len(lineas))):
                        matches = re.findall(r"(\d+[.,]\d{2})", lineas[offset])
                        if matches:
                            numero = self.normalizar_numero(matches[-1])
                            if numero is not None and numero > 0:
                                return numero

        palabras_clave_total = ["TOTAL", "TOTAI", "A PAGAR", "IMPORTE TOTAL"]
        candidatos_total: List[tuple[int, float, bool]] = []
        for indice, linea in enumerate(lineas):
            linea_sin_espacios = linea.replace(" ", "").upper()
            if any(clave in linea_sin_espacios for clave in palabras_clave_total):
                solo_letras = re.sub(r"[^A-Za-z]", "", linea).upper()
                es_standalone = solo_letras in ["TOTAL", "TOTAI", "APAGAR"]
                for offset in range(indice, min(indice + 5, len(lineas))):
                    matches = re.findall(r"(\d+[.,]\d{2})", lineas[offset])
                    if matches:
                        for m in matches:
                            numero = self.normalizar_numero(m)
                            if numero is not None and numero > 0:
                                candidatos_total.append((indice, numero, es_standalone))

        if candidatos_total:
            standalone = [c for c in candidatos_total if c[2]]
            if standalone:
                standalone.sort(key=lambda x: x[0], reverse=True)
                return standalone[0][1]
            candidatos_total.sort(key=lambda x: x[0], reverse=True)
            return candidatos_total[0][1]

        decimales_encontrados: List[float] = []
        for linea in lineas:
            matches = re.findall(r"(\d+[.,]\d{2})\s*(?:EUR|€|E)?", linea)
            for match in matches:
                numero = self.normalizar_numero(match)
                if numero is not None and numero > 0.50:
                    decimales_encontrados.append(numero)

        if decimales_encontrados:
            return max(decimales_encontrados)
        return None

    # Detecta el comercio con lista conocida + fuzzy en cabecera.
    def extraer_comercio(self, lineas: List[str]) -> Optional[str]:
        """Identifica el comercio usando coincidencia exacta y fuzzy."""
        texto_completo = " ".join(lineas).upper()
        for nombre_comercio, variantes in self.comercios_conocidos.items():
            if any(variante in texto_completo for variante in variantes):
                return nombre_comercio

        mejor_puntaje = 0.0
        mejor_comercio: Optional[str] = None
        lineas_normalizadas = [
            re.sub(r"[^A-Za-zÀ-ÿ\s]", "", linea).upper().strip()
            for linea in lineas[:12]
        ]
        for nombre_comercio, variantes in self.comercios_conocidos.items():
            for variante in variantes:
                variante_norm = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", variante).upper().strip()
                for candidato in lineas_normalizadas:
                    if not candidato:
                        continue
                    puntaje = SequenceMatcher(None, candidato, variante_norm).ratio()
                    if puntaje > mejor_puntaje:
                        mejor_puntaje = puntaje
                        mejor_comercio = nombre_comercio
        if mejor_puntaje >= 0.7:
            return mejor_comercio

        for linea in lineas[:10]:
            solo_letras = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", linea).strip()
            if 4 <= len(solo_letras) <= 30:
                return solo_letras.upper()
        return None

    # Filtra lineas que no parecen nombres de producto.
    def _es_linea_candidata_producto(self, linea: str) -> bool:
        """Determina si la linea parece un nombre de producto."""
        linea_upper = linea.upper()
        if len(linea.strip()) < 5:
            return False
        palabras_excluir = [
            "TOTAL",
            "TARGETES",
            " CANVI",
            "CANVI:",
            "DESGLOSSAMENT",
            "DESGLOSAMENT",
            "DESGLOSSPMENT",
            "D'IVA",
            "ARTICLES",
            "IVA",
            "BASE IMPOSABLE",
            "DATA",
            "TICKET",
            "NIF",
            "BON PREU",
            "ESCLAT",
            "MERCADONA",
            "CARREFOUR",
            "LIDL",
            "ALDI",
            "DIA",
            "GRACIES",
            "GRÀCIES",
            "FACTURA",
            "CLIENTE",
            "DIRECCION",
            "PAGO",
            "CUPON",
            "CUPÓN",
            "DESCUENTO",
            "ENVIO",
            "GASTOS",
            "TIPO IVA",
            "BASE IMPONIBLE",
            "CUOTA IVA",
            "TRIBUTARIA",
            "POR UNIDAD",
            "UNITARIO",
            "UNIDAD",
            "MEDIA MARKT",
            "SATURN",
            "UNIPERSONAL",
            "REGISTRO",
            "MERCANTIL",
            "PAGINA",
            "PEDIDO",
            "REFERENCIA",
            "METODO",
            "NUMERO",
            "IDENTIFICACION",
            "RECOGIDA",
            "TIENDA",
            "ENTREGA",
            "TELEFONO",
            "TELÉFONO",
            "TELÈFON",
            "EMAIL",
            "REEMPLAZA",
            "LOY_",
            "APP",
            "CAIXERA",
            "CAIXA",
            "ATES PER",
            "ATESA PER",
            # Seccion de pago (catalan y espanol)
            "TARGETA",
            "TARJETA",
            "BANCARIA",
            "BANCÀRIA",
            "VERIFICAT",
            "DISPOSITIU",
            "VISA",
            "DEBIT",
            "MASTERCARD",
            "MAESTRO",
            "EFECTIU",
            "EFECTIVO",
            "QUOTA",
            "AID:",
            # Direccion / cabecera
            "RONDA DE ",
            "CARRER ",
            "AVINGUDA",
            "PASSEIG",
            "PLAÇA",
            "P.UNIT",
            "OP:",
        ]
        if any(palabra in linea_upper for palabra in palabras_excluir):
            return False
        solo_letras = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", linea).strip()
        if len(solo_letras) < 4:
            return False
        return True

    # Detecta encabezados de la tabla de productos.
    def _es_linea_header(self, linea: str) -> bool:
        """Detecta encabezados de columnas de la tabla."""
        linea_upper = linea.upper()
        keywords = [
            "DESCRIP",
            "PRODUCTO",
            "CANT.",
            "P.V.P",
            "PVP",
            "UNITARIO",
            "TRIBUTARIA",
            "POR UNIDAD",
            "BASE IMPONIBLE",
            "CUOTA IVA",
            "TIPO IVA",
            "FACTURA",
            "P.UNIT",
        ]
        if any(k in linea_upper for k in keywords):
            return True
        # Combinacion de cabecera catalan de Mercadona
        if "IMPORT" in linea_upper and any(
            k in linea_upper for k in ["P.UNIT", "PREU", "CANT", "QUANTITAT"]
        ):
            return True
        return False

    # Detecta lineas de descuento/cupon/envio para ignorar.
    def _es_linea_descartar(self, linea: str) -> bool:
        """Marca lineas de descuentos/cupones/envios."""
        linea_upper = linea.upper()
        keywords = [
            "DESCUENTO",
            "CUPON",
            "CUPÓN",
            "LOY_",
            "APP",
            "GASTOS",
            "ENVIO",
            "ENVÍO",
        ]
        return any(k in linea_upper for k in keywords)

    # Detecta codigos o SKU con muchos digitos.
    def _es_linea_codigo(self, linea: str) -> bool:
        """Detecta lineas que parecen codigos numericos."""
        sin_espacios = re.sub(r"\s+", "", linea)
        if len(sin_espacios) < 5:
            return True
        letras = re.findall(r"[A-Za-zÀ-ÿ]", sin_espacios)
        digitos = re.findall(r"\d", sin_espacios)
        if len(digitos) >= 5 and len(letras) <= 2:
            return True
        return False

    # Detecta lineas de la seccion de pago del ticket.
    def _es_linea_pago(self, linea: str) -> bool:
        """Detecta lineas de pago, tarjetas, verificacion."""
        linea_upper = linea.upper()
        keywords = [
            "TARGETA BANCARIA",
            "TARJETA BANCARIA",
            "TARG. BANCARIA",
            "TARG BANCARIA",
            "TARGETA BANCÀRIA",
            "TARJETA BANCÀRIA",
            "EFECTIU",
            "EFECTIVO",
            "CANVI:",
            "CAMBIO:",
            "VERIFICAT PER",
            "VERIFICADO POR",
            "VISA DEBIT",
            "VISA CREDIT",
            "MASTERCARD",
            "MAESTRO",
            "AID:",
            "AID ",
        ]
        return any(k in linea_upper for k in keywords)

    # Detecta lineas de direccion o cabecera del comercio.
    def _es_linea_direccion(self, linea: str) -> bool:
        """Detecta lineas de direccion postal o telefono."""
        # Codigo postal (5 digitos) junto con texto
        if re.search(r"\b\d{5}\b", linea):
            if len(re.findall(r"[A-Za-zÀ-ÿ]", linea)) >= 3:
                return True
        linea_upper = linea.upper()
        keywords = [
            "TELÈFON",
            "TELEFON",
            "TELÉFONO",
            "TEL.",
            "RONDA DE ",
            "CARRER ",
            "AVINGUDA ",
            "PASSEIG ",
            "PLAÇA ",
            "CALLE ",
            "AVDA.",
            "PLAZA ",
            "C/ ",
        ]
        return any(k in linea_upper for k in keywords)

    # Comprueba que el texto tiene suficientes letras.
    def _tiene_letras(self, texto: str) -> bool:
        """Devuelve True si el texto tiene al menos 2 letras."""
        return len(re.findall(r"[A-Za-zÀ-ÿ]", texto)) >= 2

    # Extrae precios con decimales descartando IVA/%.
    def _extraer_precios(self, linea: str) -> List[float]:
        """Extrae valores con decimales evitando IVA/porcentaje."""
        linea_upper = linea.upper()
        if "%" in linea_upper or "IVA" in linea_upper:
            return []
        if re.search(r"\d+[.,]\d{2}\s*P\b", linea_upper):
            return []
        matches = re.findall(r"-?\d+[.,]\d{2}", linea)
        precios: List[float] = []
        for match in matches:
            numero = self.normalizar_numero(match)
            if numero is not None:
                precios.append(numero)
        return precios

    # Extrae lista de productos agrupando nombres y precios.
    def extraer_productos(self, lineas: List[str]) -> List[Producto]:
        """Devuelve productos extraidos linea a linea con sus precios."""
        productos: List[Producto] = []

        # --- Detectar inicio de la zona de productos ---
        inicio = 0
        for i, linea in enumerate(lineas):
            linea_upper = linea.upper()
            # Cabeceras de tabla (espanol y catalan)
            if any(k in linea_upper for k in ["DESCRIP", "P.V.P", "PVP", "P.UNIT"]):
                contexto = " ".join(lineas[max(0, i - 2) : i + 6]).upper()
                if any(
                    k in contexto
                    for k in [
                        "CANT",
                        "PRODUCTO",
                        "TOTAL",
                        "UNITARIO",
                        "P.UNIT",
                        "IMPORT",
                    ]
                ):
                    inicio = i + 1
                    while inicio < len(lineas) and self._es_linea_header(
                        lineas[inicio]
                    ):
                        inicio += 1
                    break
            # Marcadores de fin de cabecera (catalan: OP, CAIXA)
            if re.search(r"\bOP:\s*\d", linea_upper) or re.search(
                r"\bCAIXA\s*:\s*\d", linea_upper
            ):
                inicio = i + 1
                break

        # --- Detectar fin de la zona de productos ---
        fin = len(lineas)
        for i in range(max(inicio, int(len(lineas) * 0.3)), len(lineas)):
            linea_upper = lineas[i].upper().replace(" ", "")
            # Espanol: resumen IVA
            if "TIPOIVA" in linea_upper and "BASEIMPONIBLE" in " ".join(
                lineas[i : i + 3]
            ).upper().replace(" ", ""):
                fin = i
                break
            # Catalan: desglose IVA
            if "DESGLOSSAMENT" in linea_upper or "DESGLOSAMENT" in linea_upper:
                fin = i
                break
            # TOTAL standalone (linea que empieza por TOTAL)
            if re.match(r"^\s*TOTAL\b", lineas[i], re.IGNORECASE):
                fin = i
                break
            # Seccion de pago
            if self._es_linea_pago(lineas[i]):
                fin = i
                break
            # Catalan: ARTICLES: N
            if re.match(r"^\s*ARTICLES\s*:", lineas[i], re.IGNORECASE):
                fin = i
                break

        # --- Extraer productos linea a linea ---
        nombre_buffer: List[str] = []
        precio_actual: Optional[float] = None

        def _guardar():
            nonlocal nombre_buffer, precio_actual
            if nombre_buffer and precio_actual is not None and precio_actual > 0:
                nombre = " ".join(nombre_buffer).strip()
                # Limpiar cantidad al inicio (ej: "2 BIFIDUS" -> "BIFIDUS")
                nombre_sin_cantidad = re.sub(r"^\d+\s+", "", nombre)
                if len(nombre_sin_cantidad) >= 3:
                    nombre = nombre_sin_cantidad
                nombre = nombre.upper()
                if len(nombre) >= 3:
                    productos.append(
                        Producto(nombre=nombre, precio_total=precio_actual)
                    )
            nombre_buffer = []
            precio_actual = None

        for linea in lineas[inicio:fin]:
            linea_limpia = re.sub(r"\s+", " ", linea).strip()
            if not linea_limpia:
                continue

            # Saltar lineas que no son productos
            if self._es_linea_descartar(linea_limpia):
                _guardar()
                continue
            if self._es_linea_header(linea_limpia):
                _guardar()
                continue
            if self._es_linea_pago(linea_limpia):
                _guardar()
                continue
            if self._es_linea_direccion(linea_limpia):
                _guardar()
                continue

            # Comprobar precios en esta linea
            precios = self._extraer_precios(linea_limpia)

            if precios:
                positivos = [p for p in precios if p > 0]
                precio = max(positivos) if positivos else None

                # Extraer parte de texto (nombre) quitando los numeros decimales
                nombre_parte = re.sub(r"-?\d+[.,]\d{2}", "", linea_limpia)
                nombre_parte = re.sub(r"\s+", " ", nombre_parte).strip()
                # Limpiar numeros sueltos y puntuacion al inicio/final
                nombre_parte = re.sub(
                    r"^[\s\d.,*×xX-]+\s*|\s*[\s\d.,*×xX-]+$", "", nombre_parte
                ).strip()

                if (
                    nombre_parte
                    and len(nombre_parte) >= 3
                    and self._tiene_letras(nombre_parte)
                ):
                    # Linea con nombre + precio: guardar anterior y crear nuevo
                    if nombre_buffer and precio_actual is not None:
                        _guardar()
                    if nombre_buffer:
                        nombre_buffer.append(nombre_parte)
                    else:
                        nombre_buffer = [nombre_parte]
                    precio_actual = precio
                    _guardar()
                else:
                    # Linea solo con precio(s)
                    if nombre_buffer:
                        precio_actual = precio
                        _guardar()
                    # Si no hay nombre en buffer, precio huerfano -> ignorar
            else:
                # Linea sin precio (solo texto)
                if self._es_linea_codigo(linea_limpia):
                    continue
                if not self._es_linea_candidata_producto(linea_limpia):
                    _guardar()
                    continue

                # Si ya teniamos nombre + precio, guardar primero
                if nombre_buffer and precio_actual is not None:
                    _guardar()

                nombre_buffer.append(linea_limpia)

        _guardar()
        return productos

    # Elimina falsos positivos comparando con el nombre del comercio.
    def filtrar_productos_por_comercio(
        self, productos: List[Producto], comercio: Optional[str]
    ) -> List[Producto]:
        """Limpia productos que se parecen al nombre del comercio."""
        if not comercio:
            return productos
        comercio_norm = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", comercio).upper().strip()
        comercio_words = set(comercio_norm.split())

        filtrados: List[Producto] = []
        for producto in productos:
            nombre_norm = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", producto.nombre).upper().strip()
            similitud = SequenceMatcher(None, nombre_norm, comercio_norm).ratio()
            if similitud >= 0.6:
                continue

            palabras = nombre_norm.split()
            for n_prefijo in range(min(3, len(palabras)), 0, -1):
                prefijo = " ".join(palabras[:n_prefijo])
                sim_prefijo = SequenceMatcher(None, prefijo, comercio_norm).ratio()
                if sim_prefijo >= 0.75 or (
                    n_prefijo <= 2
                    and all(
                        any(
                            SequenceMatcher(None, p, cw).ratio() > 0.7
                            for cw in comercio_words
                        )
                        for p in palabras[:n_prefijo]
                    )
                ):
                    nombre_limpio = " ".join(palabras[n_prefijo:]).strip()
                    if nombre_limpio:
                        producto = Producto(
                            nombre=nombre_limpio,
                            precio_total=producto.precio_total,
                            cantidad=producto.cantidad,
                        )
                    break

            nombre_final = re.sub(
                r"^[<>.,;:!?\-]+\s*|\s*[<>.,;:!?\-]+$", "", producto.nombre
            ).strip()
            if nombre_final:
                producto = Producto(
                    nombre=nombre_final,
                    precio_total=producto.precio_total,
                    cantidad=producto.cantidad,
                )

            if producto.nombre:
                filtrados.append(producto)
        return filtrados

    # Parseo completo: comercio, fecha, productos, total.
    def parsear(self, lineas: List[str]) -> Dict[str, object]:
        """Parsea lineas OCR y devuelve datos estructurados."""
        texto_completo = "\n".join(lineas)
        comercio = self.extraer_comercio(lineas)
        productos = self.extraer_productos(lineas)
        productos = self.filtrar_productos_por_comercio(productos, comercio)

        return {
            "comercio": comercio,
            "fecha": self.extraer_fecha_y_hora_por_contexto(lineas)
            or self.extraer_fecha(texto_completo),
            "productos": productos,
            "total": self.extraer_total_por_contexto(lineas),
            "moneda": "EUR",
            "raw_text": texto_completo,
            "num_lineas": len(lineas),
        }
