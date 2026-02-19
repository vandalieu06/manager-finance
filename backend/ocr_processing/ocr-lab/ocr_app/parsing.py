from __future__ import annotations

import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

from .models import Producto

# Mantener estas listas como constantes evita "magia" repartida por el código.
# También facilita ampliar reglas sin tocar la lógica principal.
KNOWN_STORES = {
    "BON PREU": ["BON PREU", "BONPREU", "BON-PREU"],
    "ESCLAT": ["ESCLAT", "ESCIAT"],
    "MERCADONA": ["MERCADONA"],
    "CARREFOUR": ["CARREFOUR"],
    "DIA": ["DIA %", "DIA MARKET"],
    "LIDL": ["LIDL"],
    "ALDI": ["ALDI"],
    "MEDIA MARKT": ["MEDIA MARKT", "MEDIAMARKT", "MEDIA MARKT SATURN"],
}

PRODUCT_HEADER_KEYWORDS = [
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

DISCARDED_LINE_KEYWORDS = [
    "DESCUENTO",
    "CUPON",
    "CUPÓN",
    "LOY_",
    "APP",
    "GASTOS",
    "ENVIO",
    "ENVÍO",
]

PAYMENT_SECTION_KEYWORDS = [
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

ADDRESS_HINT_KEYWORDS = [
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

NON_PRODUCT_HINTS = [
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
    "RONDA DE ",
    "CARRER ",
    "AVINGUDA",
    "PASSEIG",
    "PLAÇA",
    "P.UNIT",
    "OP:",
]


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

    def __init__(self) -> None:
        self.comercios_conocidos = KNOWN_STORES

    def normalizar_numero(self, texto: str) -> Optional[float]:
        """Convierte texto con formato europeo o anglosajón a float.

        OCR mezcla símbolos, separadores y espacios. Este método prioriza tolerancia:
        intenta rescatar el número más probable y descarta lo ambiguo.
        """
        numero_limpio = re.sub(r"[^\d,.\-]", "", texto.replace(" ", ""))
        if not re.search(r"\d", numero_limpio):
            return None

        separador_decimal = None
        if "." in numero_limpio and "," in numero_limpio:
            separador_decimal = (
                "," if numero_limpio.rfind(",") > numero_limpio.rfind(".") else "."
            )
        elif "," in numero_limpio:
            partes = numero_limpio.split(",")
            if len(partes) >= 2 and 1 <= len(partes[-1]) <= 3:
                separador_decimal = ","
        elif "." in numero_limpio:
            partes = numero_limpio.split(".")
            if len(partes) >= 2 and 1 <= len(partes[-1]) <= 3:
                separador_decimal = "."

        if separador_decimal == ",":
            numero_limpio = numero_limpio.replace(".", "")
            numero_limpio = numero_limpio.replace(",", ".")
        elif separador_decimal == ".":
            numero_limpio = numero_limpio.replace(",", "")
        else:
            numero_limpio = re.sub(r"[.,]", "", numero_limpio)

        if numero_limpio in {"", "-", ".", "-."}:
            return None
        try:
            return float(numero_limpio)
        except ValueError:
            return None

    def extraer_fecha(self, texto: str) -> Optional[str]:
        """Extrae fecha en formatos frecuentes de ticket.

        Se prueban primero formatos completos y luego alternativas con OCR defectuoso.
        """
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

    def extraer_fecha_y_hora_por_contexto(self, lineas: List[str]) -> Optional[str]:
        """Busca fecha/hora cerca de etiquetas semánticas.

        En OCR, la fecha puede no estar limpia; mirar el contexto mejora acierto.
        """
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

    def extraer_total_por_contexto(self, lineas: List[str]) -> Optional[float]:
        """Obtiene el total aplicando una estrategia por puntuación.

        Primero se priorizan líneas que semánticamente indican TOTAL.
        Si no hay coincidencias claras, se usa fallback con el mayor decimal plausible.
        """
        candidatos_total = self._buscar_candidatos_total(lineas)
        if candidatos_total:
            candidatos_total.sort(key=lambda x: (x[0], x[2]), reverse=True)
            return candidatos_total[0][1]
        return self._buscar_total_por_fallback(lineas)

    def _buscar_candidatos_total(
        self, lineas: List[str]
    ) -> List[tuple[int, float, int]]:
        candidatos: List[tuple[int, float, int]] = []
        for indice, linea in enumerate(lineas):
            linea_upper = linea.upper()
            if not re.search(r"\b(TOTAL|TOTAI|A\s*PAGAR|IMPORTE\s*TOTAL)\b", linea_upper):
                continue

            linea_compacta = linea_upper.replace(" ", "")
            es_total_iva = "TOTALIVA" in linea_compacta or "CUOTAIVA" in linea_compacta
            es_subtotal = "SUBTOTAL" in linea_compacta
            solo_letras = re.sub(r"[^A-Z]", "", linea_upper)
            es_linea_aislada = solo_letras in {"TOTAL", "TOTAI", "APAGAR", "IMPORTETOTAL"}

            for indice_candidato in range(indice, min(indice + 3, len(lineas))):
                for precio in self._extraer_precios(lineas[indice_candidato]):
                    if precio <= 0:
                        continue
                    score = self._puntuar_candidato_total(
                        indice_candidato=indice_candidato,
                        es_linea_aislada=es_linea_aislada,
                        es_total_iva=es_total_iva,
                        es_subtotal=es_subtotal,
                    )
                    candidatos.append((score, precio, indice_candidato))
        return candidatos

    def _puntuar_candidato_total(
        self,
        indice_candidato: int,
        es_linea_aislada: bool,
        es_total_iva: bool,
        es_subtotal: bool,
    ) -> int:
        """Asigna prioridad a números candidatos a total.

        Reglas:
        - Línea "TOTAL" sola recibe extra de confianza.
        - Totales de IVA y subtotales se penalizan para evitar falsos positivos.
        """
        score = 100 + indice_candidato + (30 if es_linea_aislada else 0)
        if es_total_iva:
            score -= 80
        if es_subtotal:
            score -= 60
        return score

    def _buscar_total_por_fallback(self, lineas: List[str]) -> Optional[float]:
        """Fallback: devolver el mayor valor decimal que parezca monetario."""
        decimales_validos: List[float] = []
        for linea in lineas:
            if any(k in linea.upper() for k in ["IVA", "%", "TIPO", "BASE IMPONIBLE"]):
                continue
            for numero in self._extraer_precios(linea):
                if numero > 0.5:
                    decimales_validos.append(numero)
        return max(decimales_validos) if decimales_validos else None

    def extraer_comercio(self, lineas: List[str]) -> Optional[str]:
        """Identifica comercio por coincidencia exacta y fuzzy matching.

        Se intenta:
        1) match exacto por variantes conocidas (rápido y fiable),
        2) fuzzy en cabecera (tolerante a OCR),
        3) fallback con primera línea plausible.
        """
        texto_completo = " ".join(lineas).upper()
        for nombre_comercio, variantes in self.comercios_conocidos.items():
            if any(variante in texto_completo for variante in variantes):
                return nombre_comercio

        mejor_puntaje = 0.0
        mejor_candidato: Optional[str] = None
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
                        mejor_candidato = nombre_comercio
        if mejor_puntaje >= 0.7:
            return mejor_candidato

        for linea in lineas[:10]:
            solo_letras = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", linea).strip()
            if 4 <= len(solo_letras) <= 30:
                return solo_letras.upper()
        return None

    def _es_linea_candidata_producto(self, linea: str) -> bool:
        """Filtra ruido y conserva texto que sí puede ser producto.

        Mala práctica corregida:
        Antes esta validación mezclaba reglas de cabecera, pago y dirección sin
        dejar claro el objetivo. Ahora se centra en una única pregunta:
        "¿esta línea puede ser nombre de producto?".
        """
        texto = linea.strip()
        if not texto:
            return False
        if texto.upper() in {"KG", "UD", "U", "UN", "L", "ML"}:
            return True
        if len(texto) < 2:
            return False
        if any(hint in texto.upper() for hint in NON_PRODUCT_HINTS):
            return False
        solo_letras = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", texto).strip()
        if len(solo_letras) < 2:
            return False
        return True

    def _es_linea_header(self, linea: str) -> bool:
        """Detecta cabeceras de columnas de productos."""
        linea_upper = linea.upper()
        if any(k in linea_upper for k in PRODUCT_HEADER_KEYWORDS):
            return True
        if "IMPORT" in linea_upper and any(
            k in linea_upper for k in ["P.UNIT", "PREU", "CANT", "QUANTITAT"]
        ):
            return True
        return False

    def _es_linea_descartar(self, linea: str) -> bool:
        """Marca líneas no-producto (descuentos, cupones, envío)."""
        return any(k in linea.upper() for k in DISCARDED_LINE_KEYWORDS)

    def _es_linea_codigo(self, linea: str) -> bool:
        """Detecta líneas que parecen códigos internos o SKU."""
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

    def _es_linea_pago(self, linea: str) -> bool:
        """Detecta líneas de pago para separar fin de productos."""
        return any(k in linea.upper() for k in PAYMENT_SECTION_KEYWORDS)

    def _es_linea_direccion(self, linea: str) -> bool:
        """Detecta líneas de dirección/teléfono de cabecera."""
        if re.search(r"\b\d{5}\b", linea):
            if len(re.findall(r"[A-Za-zÀ-ÿ]", linea)) >= 3:
                return True
        return any(k in linea.upper() for k in ADDRESS_HINT_KEYWORDS)

    def _tiene_letras(self, texto: str) -> bool:
        """Valida que hay suficiente información textual."""
        return len(re.findall(r"[A-Za-zÀ-ÿ]", texto)) >= 2

    def _extraer_precios(self, linea: str) -> List[float]:
        """Extrae precios decimales descartando patrones no monetarios."""
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
        """Normaliza texto OCR a lista de líneas sin vacíos."""
        return [re.sub(r"\s+", " ", l).strip() for l in texto_ocr.splitlines() if l.strip()]

    def _normalizar_fecha_iso(self, valor: Optional[str]) -> str:
        """Convierte fecha libre detectada a ISO-8601 minutos."""
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
        """Extrae CIF/NIF fiscal si aparece en cabecera."""
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
        """Extrae teléfono español normalizando a dígitos."""
        for linea in lineas[:25]:
            match = re.search(r"(?:\+34\s*)?(\d(?:[\s.-]?\d){8})", linea)
            if match:
                return re.sub(r"\D", "", match.group(1))
        return ""

    def _extraer_op(self, lineas: List[str]) -> str:
        """Extrae código OP (operación/caja) si existe."""
        for linea in lineas:
            match = re.search(r"\bOP\s*[:\-]?\s*([A-Z0-9]+)\b", linea.upper())
            if match:
                return match.group(1)
        return ""

    def _extraer_ticket_id(self, lineas: List[str]) -> str:
        """Extrae identificador de ticket/factura."""
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
        """Busca dirección y línea postal en cabecera."""
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
        """Extrae desglose IVA con rate/base/cuota."""
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
        """Extrae pagos con método e importe desde sección de cobro."""
        pagos: List[Dict[str, Any]] = []
        for linea in lineas:
            if not self._es_linea_pago(linea):
                continue
            precios = self._extraer_precios(linea)
            metodo = self._inferir_metodo_pago(linea)
            if metodo and precios:
                pagos.append({"method": metodo, "amount": round(max(precios), 2)})
        return pagos

    def _inferir_metodo_pago(self, linea: str) -> str:
        linea_upper = linea.upper()
        if "EFECT" in linea_upper:
            return "EFECTIVO"
        if any(k in linea_upper for k in ["TARJETA", "TARGETA", "VISA", "MASTERCARD", "MAESTRO"]):
            return "TARJETA"
        return ""

    def _ajustar_total_con_iva(
        self, total: Optional[float], iva: List[Dict[str, float]]
    ) -> Optional[float]:
        """Ajusta total cuando OCR captura base imponible en lugar de total final.

        Mala práctica corregida:
        devolver números sin normalizar producía salidas inconsistentes.
        Aquí siempre devolvemos redondeo homogéneo a 2 decimales.
        """
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

    def extraer_productos(self, lineas: List[str]) -> List[Producto]:
        """Extrae productos recorriendo la zona útil del ticket.

        Flujo:
        1) detectar inicio/fin del bloque de líneas de compra,
        2) acumular nombre en buffer hasta encontrar precio,
        3) guardar producto cuando se completa el par nombre+precio.
        """
        productos: List[Producto] = []
        inicio = self._detectar_inicio_productos(lineas)
        fin = self._detectar_fin_productos(lineas, inicio)

        nombre_buffer: List[str] = []
        precio_actual: Optional[float] = None

        def guardar_producto_si_completo() -> None:
            nonlocal nombre_buffer, precio_actual
            if nombre_buffer and precio_actual is not None and precio_actual > 0:
                nombre_final = self._limpiar_nombre_producto(" ".join(nombre_buffer))
                if len(nombre_final) >= 3:
                    productos.append(Producto(nombre=nombre_final, precio_total=precio_actual))
            nombre_buffer = []
            precio_actual = None

        for linea in lineas[inicio:fin]:
            linea_limpia = re.sub(r"\s+", " ", linea).strip()
            if not linea_limpia:
                continue

            if self._es_linea_descartar(linea_limpia):
                guardar_producto_si_completo()
                continue
            if self._es_linea_header(linea_limpia):
                guardar_producto_si_completo()
                continue
            if self._es_linea_pago(linea_limpia):
                guardar_producto_si_completo()
                continue
            if self._es_linea_direccion(linea_limpia):
                guardar_producto_si_completo()
                continue

            precios = self._extraer_precios(linea_limpia)

            if precios:
                positivos = [p for p in precios if p > 0]
                precio = max(positivos) if positivos else None
                nombre_parte = re.sub(r"-?\d+[.,]\d{2}", "", linea_limpia)
                nombre_parte = re.sub(r"\s+", " ", nombre_parte).strip()
                nombre_parte = re.sub(
                    r"^[\s\d.,*×xX-]+\s*|\s*[\s\d.,*×xX-]+$", "", nombre_parte
                ).strip()

                if (
                    nombre_parte
                    and len(nombre_parte) >= 3
                    and self._tiene_letras(nombre_parte)
                ):
                    if nombre_buffer and precio_actual is not None:
                        guardar_producto_si_completo()
                    if nombre_buffer:
                        nombre_buffer.append(nombre_parte)
                    else:
                        nombre_buffer = [nombre_parte]
                    precio_actual = precio
                    guardar_producto_si_completo()
                else:
                    if nombre_buffer:
                        precio_actual = precio
                        guardar_producto_si_completo()
            else:
                if self._es_linea_codigo(linea_limpia):
                    continue
                if not self._es_linea_candidata_producto(linea_limpia):
                    guardar_producto_si_completo()
                    continue

                if nombre_buffer and precio_actual is not None:
                    guardar_producto_si_completo()

                nombre_buffer.append(linea_limpia)

        guardar_producto_si_completo()
        return productos

    def _detectar_inicio_productos(self, lineas: List[str]) -> int:
        """Calcula dónde empieza la sección de productos."""
        for indice, linea in enumerate(lineas):
            linea_upper = linea.upper()
            if any(k in linea_upper for k in ["DESCRIP", "P.V.P", "PVP", "P.UNIT"]):
                contexto = " ".join(lineas[max(0, indice - 2) : indice + 6]).upper()
                if any(
                    k in contexto
                    for k in ["CANT", "PRODUCTO", "TOTAL", "UNITARIO", "P.UNIT", "IMPORT"]
                ):
                    inicio = indice + 1
                    while inicio < len(lineas) and self._es_linea_header(lineas[inicio]):
                        inicio += 1
                    return inicio
            if re.search(r"\bOP:\s*\d", linea_upper) or re.search(r"\bCAIXA\s*:\s*\d", linea_upper):
                return indice + 1
        return 0

    def _detectar_fin_productos(self, lineas: List[str], inicio: int) -> int:
        """Calcula dónde termina la sección de productos."""
        for indice in range(max(inicio, int(len(lineas) * 0.3)), len(lineas)):
            linea_compacta = lineas[indice].upper().replace(" ", "")
            if "TIPOIVA" in linea_compacta and "BASEIMPONIBLE" in " ".join(
                lineas[indice : indice + 3]
            ).upper().replace(" ", ""):
                return indice
            if "DESGLOSSAMENT" in linea_compacta or "DESGLOSAMENT" in linea_compacta:
                return indice
            if re.match(r"^\s*TOTAL\b", lineas[indice], re.IGNORECASE):
                return indice
            if self._es_linea_pago(lineas[indice]):
                return indice
            if re.match(r"^\s*ARTICLES\s*:", lineas[indice], re.IGNORECASE):
                return indice
        return len(lineas)

    def _limpiar_nombre_producto(self, nombre_crudo: str) -> str:
        """Limpia prefijos de cantidad y estandariza nombre del producto."""
        nombre = nombre_crudo.strip()
        nombre_sin_cantidad = re.sub(r"^\d+\s+", "", nombre)
        if len(nombre_sin_cantidad) >= 3:
            nombre = nombre_sin_cantidad
        return nombre.upper()

    def filtrar_productos_por_comercio(
        self, productos: List[Producto], comercio: Optional[str]
    ) -> List[Producto]:
        """Elimina falsos positivos similares al nombre del comercio."""
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

    def parsear(self, lineas: List[str]) -> Dict[str, object]:
        """Orquesta parseo completo del ticket OCR.

        Diseño: este método coordina, no implementa detalles.
        Cada extracción vive en helpers con responsabilidad única.
        """
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
    """Evita romper formato TSV por saltos de línea o tabuladores."""
    if texto is None:
        return ""
    return str(texto).replace("\t", " ").replace("\n", " ").strip()


def _fmt_num(valor: Any, decimales: int = 2) -> str:
    """Formatea números de salida respetando campos opcionales."""
    if valor is None or valor == "":
        return ""
    if isinstance(valor, (float, int)):
        return f"{float(valor):.{decimales}f}"
    return _safe_tsv(valor)


def export_tsv(ticket_obj: Dict[str, Any]) -> str:
    """Exporta un ticket parseado al contrato TSV fijo v1."""
    lineas_tsv: List[str] = ["VER\t1"]
    lineas_tsv.append(
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
        cantidad = getattr(producto, "cantidad", None)
        total_linea = getattr(producto, "precio_total", None)
        precio_unitario = None
        if cantidad and total_linea:
            try:
                precio_unitario = float(total_linea) / float(cantidad)
            except (ValueError, ZeroDivisionError):
                precio_unitario = None
        lineas_tsv.append(
            "\t".join(
                [
                    "L",
                    _safe_tsv(getattr(producto, "nombre", "")),
                    _fmt_num(cantidad, decimales=3),
                    _fmt_num(precio_unitario),
                    _fmt_num(total_linea),
                    "",
                ]
            )
        )

    total = ticket_obj.get("total")
    lineas_tsv.append(f"T\t{_fmt_num(total)}")

    for iva_item in ticket_obj.get("iva", []):
        lineas_tsv.append(
            "\t".join(
                [
                    "V",
                    _fmt_num(iva_item.get("rate")),
                    _fmt_num(iva_item.get("base")),
                    _fmt_num(iva_item.get("amount")),
                ]
            )
        )

    for pago_item in ticket_obj.get("payments", []):
        lineas_tsv.append(
            "\t".join(
                [
                    "P",
                    _safe_tsv(pago_item.get("method", "")),
                    _fmt_num(pago_item.get("amount")),
                ]
            )
        )
    return "\n".join(lineas_tsv)


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
