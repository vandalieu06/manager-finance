import re

from .constants import (
    ADDRESS_HINT_KEYWORDS,
    DISCARDED_LINE_KEYWORDS,
    NON_PRODUCT_HINTS,
    PAYMENT_SECTION_KEYWORDS,
    PRODUCT_HEADER_KEYWORDS,
)
from .text_utils import has_letters


class LineClassifier:
    """Clasifica lineas OCR para separar productos, metadatos y ruido."""

    def is_product_candidate(self, texto_linea_ocr):
        texto_linea_limpio = texto_linea_ocr.strip()
        if not texto_linea_limpio:
            return False
        if texto_linea_limpio.upper() in {"KG", "UD", "U", "UN", "L", "ML"}:
            return True
        if len(texto_linea_limpio) < 2:
            return False
        if any(
            pista_no_producto in texto_linea_limpio.upper()
            for pista_no_producto in NON_PRODUCT_HINTS
        ):
            return False
        return has_letters(texto_linea_limpio)

    def is_header_line(self, texto_linea_ocr):
        texto_linea_mayus = texto_linea_ocr.upper()
        if any(
            keyword_cabecera in texto_linea_mayus
            for keyword_cabecera in PRODUCT_HEADER_KEYWORDS
        ):
            return True
        if "IMPORT" in texto_linea_mayus and any(
            pista_tabla in texto_linea_mayus
            for pista_tabla in ["P.UNIT", "PREU", "CANT", "QUANTITAT"]
        ):
            return True
        return False

    def is_discard_line(self, texto_linea_ocr):
        return any(
            keyword_descartar in texto_linea_ocr.upper()
            for keyword_descartar in DISCARDED_LINE_KEYWORDS
        )

    def is_code_line(self, texto_linea_ocr):
        texto_linea_compacto = re.sub(r"\s+", "", texto_linea_ocr)
        if len(texto_linea_compacto) < 5:
            return False

        tokens_letras = re.findall(r"[A-Za-zÀ-ÿ]", texto_linea_compacto)
        tokens_digitos = re.findall(r"\d", texto_linea_compacto)

        if re.search(r"^(CP|OP|ID)[:\-]?\d+$", texto_linea_compacto.upper()):
            return True
        if len(tokens_digitos) >= 5 and len(tokens_letras) <= 2:
            return True
        return False

    def is_payment_line(self, texto_linea_ocr):
        return any(
            keyword_pago in texto_linea_ocr.upper()
            for keyword_pago in PAYMENT_SECTION_KEYWORDS
        )

    def is_address_line(self, texto_linea_ocr):
        if re.search(r"\b\d{5}\b", texto_linea_ocr) and has_letters(texto_linea_ocr):
            return True
        return any(
            keyword_direccion in texto_linea_ocr.upper()
            for keyword_direccion in ADDRESS_HINT_KEYWORDS
        )
