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

    def is_product_candidate(self, line_text):
        stripped_line_text = line_text.strip()
        if not stripped_line_text:
            return False
        if stripped_line_text.upper() in {"KG", "UD", "U", "UN", "L", "ML"}:
            return True
        if len(stripped_line_text) < 2:
            return False
        if any(non_product_hint in stripped_line_text.upper() for non_product_hint in NON_PRODUCT_HINTS):
            return False
        return has_letters(stripped_line_text)

    def is_header_line(self, line_text):
        upper_line_text = line_text.upper()
        if any(header_keyword in upper_line_text for header_keyword in PRODUCT_HEADER_KEYWORDS):
            return True
        if "IMPORT" in upper_line_text and any(
            table_hint in upper_line_text for table_hint in ["P.UNIT", "PREU", "CANT", "QUANTITAT"]
        ):
            return True
        return False

    def is_discard_line(self, line_text):
        return any(discard_keyword in line_text.upper() for discard_keyword in DISCARDED_LINE_KEYWORDS)

    def is_code_line(self, line_text):
        compact_line_text = re.sub(r"\s+", "", line_text)
        if len(compact_line_text) < 5:
            return False

        extracted_letters = re.findall(r"[A-Za-zÀ-ÿ]", compact_line_text)
        extracted_digits = re.findall(r"\d", compact_line_text)

        if re.search(r"^(CP|OP|ID)[:\-]?\d+$", compact_line_text.upper()):
            return True
        if len(extracted_digits) >= 5 and len(extracted_letters) <= 2:
            return True
        return False

    def is_payment_line(self, line_text):
        return any(payment_keyword in line_text.upper() for payment_keyword in PAYMENT_SECTION_KEYWORDS)

    def is_address_line(self, line_text):
        if re.search(r"\b\d{5}\b", line_text) and has_letters(line_text):
            return True
        return any(address_keyword in line_text.upper() for address_keyword in ADDRESS_HINT_KEYWORDS)
