from __future__ import annotations

import re
import json
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

from .models import Producto


class TicketParser:
    """Extrae comercio, fecha, total y productos desde el OCR.

    Contrato TSV fijo v1:
    - VER\t1
    - H\t<store>\t<cif>\t<address>\t<postal_city>\t<phone>\t<datetime_iso>\t<op>\t<ticket_id>\t<currency>
    - L\t<desc>\t<qty>\t<unit_price>\t<line_total>\t<unit_optional>
    - T\t<total>
    - V\t<rate>\t<base>\t<amount> (opcional)
    - P\t<method>\t<amount> (opcional)
    """

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
        limpio = re.sub(r"[^\d,.\-]", "", texto.replace(" ", ""))
        if not re.search(r"\d", limpio):
            return None

        separador_decimal = None
        if "." in limpio and "," in limpio:
            separador_decimal = "," if limpio.rfind(",") > limpio.rfind(".") else "."
        elif "," in limpio:
            partes = limpio.split(",")
            if len(partes) >= 2 and 1 <= len(partes[-1]) <= 3:
                separador_decimal = ","
        elif "." in limpio:
            partes = limpio.split(".")
            if len(partes) >= 2 and 1 <= len(partes[-1]) <= 3:
                separador_decimal = "."

        if separador_decimal == ",":
            limpio = limpio.replace(".", "")
            limpio = limpio.replace(",", ".")
        elif separador_decimal == ".":
            limpio = limpio.replace(",", "")
        else:
            limpio = re.sub(r"[.,]", "", limpio)

        if limpio in {"", "-", ".", "-."}:
            return None
        try:
            return float(limpio)
        except ValueError:
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
        candidatos: List[tuple[int, float, int]] = []
        for indice, linea in enumerate(lineas):
            linea_upper = linea.upper()
            compacta = linea_upper.replace(" ", "")
            es_linea_total = bool(
                re.search(r"\b(TOTAL|TOTAI|A\s*PAGAR|IMPORTE\s*TOTAL)\b", linea_upper)
            )
            if not es_linea_total:
                continue

            es_total_iva = "TOTALIVA" in compacta or "CUOTAIVA" in compacta
            es_subtotal = "SUBTOTAL" in compacta
            solo_letras = re.sub(r"[^A-Z]", "", linea_upper)
            es_standalone = solo_letras in {"TOTAL", "TOTAI", "APAGAR", "IMPORTETOTAL"}
            for offset in range(indice, min(indice + 3, len(lineas))):
                for numero in self._extraer_precios(lineas[offset]):
                    if numero <= 0:
                        continue
                    score = 100 + offset + (30 if es_standalone else 0)
                    if es_total_iva:
                        score -= 80
                    if es_subtotal:
                        score -= 60
                    candidatos.append((score, numero, offset))

        if candidatos:
            candidatos.sort(key=lambda x: (x[0], x[2]), reverse=True)
            return candidatos[0][1]

        decimales_encontrados: List[float] = []
        for linea in lineas:
            if any(k in linea.upper() for k in ["IVA", "%", "TIPO", "BASE IMPONIBLE"]):
                continue
            for numero in self._extraer_precios(linea):
                if numero > 0.5:
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
        linea_strip = linea.strip()
        if not linea_strip:
            return False
        if linea_strip.upper() in {"KG", "UD", "U", "UN", "L", "ML"}:
            return True
        if len(linea_strip) < 2:
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
            "FECHA",
            "HORA",
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
        if len(solo_letras) < 2:
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
            return False
        letras = re.findall(r"[A-Za-zÀ-ÿ]", sin_espacios)
        digitos = re.findall(r"\d", sin_espacios)
        if re.search(r"^(CP|OP|ID)[:\-]?\d+$", sin_espacios.upper()):
            return True
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
            "TARGETA",
            "TARJETA",
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
        if re.search(r"\b(CP|OP|ID)\s*[:\-]\s*\d+\b", linea_upper):
            return []
        matches = re.findall(r"-?\d+(?:[.,]\d{2,3})", linea)
        precios: List[float] = []
        for match in matches:
            numero = self.normalizar_numero(match)
            if numero is not None:
                precios.append(numero)
        return precios

    def _lineas_a_texto(self, texto_ocr: str) -> List[str]:
        return [re.sub(r"\s+", " ", l).strip() for l in texto_ocr.splitlines() if l.strip()]

    def _normalizar_fecha_iso(self, valor: Optional[str]) -> str:
        if not valor:
            return ""
        valor = valor.strip()
        formatos = [
            "%d/%m/%Y %H:%M",
            "%d-%m-%Y %H:%M",
            "%d.%m.%Y %H:%M",
            "%d/%m/%y %H:%M",
            "%d-%m-%y %H:%M",
            "%d.%m.%y %H:%M",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%d/%m/%y",
            "%d-%m-%y",
            "%d.%m.%y",
        ]
        for formato in formatos:
            try:
                dt = datetime.strptime(valor, formato)
                return dt.isoformat(timespec="minutes")
            except ValueError:
                continue
        return ""

    def _extraer_cif(self, lineas: List[str]) -> str:
        patrones = [
            r"\b([A-Z]\d{8})\b",
            r"\b(\d{8}[A-Z])\b",
            r"\b([A-Z]\d{7}[A-Z0-9])\b",
        ]
        for linea in lineas[:20]:
            for patron in patrones:
                match = re.search(patron, linea.upper())
                if match:
                    return match.group(1)
        return ""

    def _extraer_telefono(self, lineas: List[str]) -> str:
        for linea in lineas[:25]:
            match = re.search(r"(?:\+34\s*)?(\d(?:[\s.-]?\d){8})", linea)
            if match:
                return re.sub(r"\D", "", match.group(1))
        return ""

    def _extraer_op(self, lineas: List[str]) -> str:
        for linea in lineas:
            match = re.search(r"\bOP\s*[:\-]?\s*([A-Z0-9]+)\b", linea.upper())
            if match:
                return match.group(1)
        return ""

    def _extraer_ticket_id(self, lineas: List[str]) -> str:
        patrones = [
            r"\b(?:TICKET|FACTURA)\s*(?:N[Oº°]\s*)?[:\-]?\s*([A-Z0-9\-]{4,})\b",
            r"\bN[Oº°]\s*[:\-]?\s*([A-Z0-9\-]{5,})\b",
        ]
        for linea in lineas:
            linea_upper = linea.upper()
            for patron in patrones:
                match = re.search(patron, linea_upper)
                if match:
                    return match.group(1)
        return ""

    def _extraer_address_postal(self, lineas: List[str]) -> tuple[str, str]:
        address = ""
        postal_city = ""
        for linea in lineas[:25]:
            if not address and self._es_linea_direccion(linea):
                address = linea.strip()
            if not postal_city and re.search(r"\b\d{5}\b", linea) and self._tiene_letras(linea):
                postal_city = linea.strip()
            if address and postal_city:
                break
        return address, postal_city

    def _extraer_iva(self, lineas: List[str]) -> List[Dict[str, float]]:
        resultados: List[Dict[str, float]] = []
        for linea in lineas:
            linea_upper = linea.upper()
            if "IVA" not in linea_upper:
                continue
            rate_match = re.search(r"(\d{1,2}(?:[.,]\d{1,2})?)\s*%", linea)
            numeros = [
                n
                for n in (
                    self.normalizar_numero(x)
                    for x in re.findall(r"-?\d+(?:[.,]\d{2,3})", linea)
                )
                if n is not None
            ]
            if len(numeros) < 2:
                continue
            base = numeros[-2]
            amount = numeros[-1]
            if base <= 0 or amount < 0:
                continue
            rate = self.normalizar_numero(rate_match.group(1)) if rate_match else None
            resultados.append(
                {
                    "rate": round(rate, 2) if rate is not None else 0.0,
                    "base": round(base, 2),
                    "amount": round(amount, 2),
                }
            )
        return resultados

    def _extraer_pagos(self, lineas: List[str]) -> List[Dict[str, Any]]:
        pagos: List[Dict[str, Any]] = []
        for linea in lineas:
            if not self._es_linea_pago(linea):
                continue
            precios = self._extraer_precios(linea)
            metodo = ""
            linea_upper = linea.upper()
            if "EFECT" in linea_upper:
                metodo = "EFECTIVO"
            elif any(k in linea_upper for k in ["TARJETA", "TARGETA", "VISA", "MASTERCARD", "MAESTRO"]):
                metodo = "TARJETA"
            if metodo and precios:
                pagos.append({"method": metodo, "amount": round(max(precios), 2)})
        return pagos

    def _ajustar_total_con_iva(
        self, total: Optional[float], iva: List[Dict[str, float]]
    ) -> Optional[float]:
        """Ajusta total para cliente final si se detecta total sin IVA."""
        if not iva:
            return round(total, 2) if total is not None else None

        base_total = round(sum(i.get("base", 0.0) for i in iva), 2)
        iva_total = round(sum(i.get("amount", 0.0) for i in iva), 2)
        if base_total <= 0 or iva_total <= 0:
            return round(total, 2) if total is not None else None

        total_con_iva = round(base_total + iva_total, 2)
        if total is None:
            return total_con_iva

        total_redondeado = round(total, 2)
        if abs(total_redondeado - base_total) <= 0.02:
            return total_con_iva
        return total_redondeado

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
        fecha_raw = self.extraer_fecha_y_hora_por_contexto(lineas) or self.extraer_fecha(
            texto_completo
        )
        address, postal_city = self._extraer_address_postal(lineas)
        iva = self._extraer_iva(lineas)
        total_base = self.extraer_total_por_contexto(lineas)
        productos = self.extraer_productos(lineas)
        productos = self.filtrar_productos_por_comercio(productos, comercio)

        return {
            "comercio": comercio,
            "fecha": fecha_raw,
            "datetime_iso": self._normalizar_fecha_iso(fecha_raw),
            "productos": productos,
            "total": self._ajustar_total_con_iva(total_base, iva),
            "moneda": "EUR",
            "cif": self._extraer_cif(lineas),
            "address": address,
            "postal_city": postal_city,
            "phone": self._extraer_telefono(lineas),
            "op": self._extraer_op(lineas),
            "ticket_id": self._extraer_ticket_id(lineas),
            "iva": iva,
            "payments": self._extraer_pagos(lineas),
            "raw_text": texto_completo,
            "num_lineas": len(lineas),
        }

    def parsear_a_tsv(self, texto_ocr: str) -> str:
        """Parsea texto OCR crudo y devuelve contrato TSV fijo v1."""
        ticket = self.parsear(self._lineas_a_texto(texto_ocr))
        return export_tsv(ticket)

    def parsear_a_productos_json(self, texto_ocr: str) -> str:
        """Parsea OCR crudo y devuelve array JSON [{name, price}]."""
        ticket = self.parsear(self._lineas_a_texto(texto_ocr))
        return export_productos_json(ticket)


def _safe_tsv(texto: Any) -> str:
    if texto is None:
        return ""
    return str(texto).replace("\t", " ").replace("\n", " ").strip()


def _fmt_num(valor: Any, decimales: int = 2) -> str:
    if valor is None or valor == "":
        return ""
    if isinstance(valor, (float, int)):
        return f"{float(valor):.{decimales}f}"
    return _safe_tsv(valor)


def export_tsv(ticket_obj: Dict[str, Any]) -> str:
    """Exporta un ticket parseado al contrato TSV fijo v1."""
    lineas: List[str] = ["VER\t1"]
    lineas.append(
        "\t".join(
            [
                "H",
                _safe_tsv(ticket_obj.get("comercio", "")),
                _safe_tsv(ticket_obj.get("cif", "")),
                _safe_tsv(ticket_obj.get("address", "")),
                _safe_tsv(ticket_obj.get("postal_city", "")),
                _safe_tsv(ticket_obj.get("phone", "")),
                _safe_tsv(ticket_obj.get("datetime_iso", "")),
                _safe_tsv(ticket_obj.get("op", "")),
                _safe_tsv(ticket_obj.get("ticket_id", "")),
                _safe_tsv(ticket_obj.get("moneda", "EUR") or "EUR"),
            ]
        )
    )

    for producto in ticket_obj.get("productos", []):
        qty = getattr(producto, "cantidad", None)
        line_total = getattr(producto, "precio_total", None)
        unit_price = None
        if qty and line_total:
            try:
                unit_price = float(line_total) / float(qty)
            except (ValueError, ZeroDivisionError):
                unit_price = None
        lineas.append(
            "\t".join(
                [
                    "L",
                    _safe_tsv(getattr(producto, "nombre", "")),
                    _fmt_num(qty, decimales=3),
                    _fmt_num(unit_price),
                    _fmt_num(line_total),
                    "",
                ]
            )
        )

    total = ticket_obj.get("total")
    lineas.append(f"T\t{_fmt_num(total)}")

    for iva in ticket_obj.get("iva", []):
        lineas.append(
            "\t".join(
                [
                    "V",
                    _fmt_num(iva.get("rate")),
                    _fmt_num(iva.get("base")),
                    _fmt_num(iva.get("amount")),
                ]
            )
        )

    for pago in ticket_obj.get("payments", []):
        lineas.append(
            "\t".join(
                [
                    "P",
                    _safe_tsv(pago.get("method", "")),
                    _fmt_num(pago.get("amount")),
                ]
            )
        )
    return "\n".join(lineas)


def export_productos_json(ticket_obj: Dict[str, Any]) -> str:
    """Exporta solo productos fisicos como JSON compacto [{name, price}]."""
    productos_json: List[Dict[str, Any]] = []
    for producto in ticket_obj.get("productos", []):
        nombre = _safe_tsv(getattr(producto, "nombre", ""))
        precio_total = getattr(producto, "precio_total", None)
        if not nombre or precio_total is None:
            continue
        if float(precio_total) <= 0:
            continue
        productos_json.append({"name": nombre, "price": round(float(precio_total), 2)})
    return json.dumps(productos_json, ensure_ascii=False, separators=(",", ":"))


def parsear_a_tsv(texto_ocr: str) -> str:
    """Funcion publica para parsear OCR crudo y devolver TSV v1."""
    return TicketParser().parsear_a_tsv(texto_ocr)


def parsear_a_productos_json(texto_ocr: str) -> str:
    """Funcion publica para parsear OCR crudo a JSON [{name, price}]."""
    return TicketParser().parsear_a_productos_json(texto_ocr)
