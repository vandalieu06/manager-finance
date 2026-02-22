import re

from ..models import Producto
from .text_utils import has_letters


class ProductExtractor:
    """Extrae productos del bloque central del ticket."""

    def __init__(self, line_classifier, price_extractor_service):
        self.line_classifier = line_classifier
        self.price_extractor_service = price_extractor_service

    def extract(self, ocr_lines):
        extracted_products = []
        products_start_index = self._detect_products_start(ocr_lines)
        products_end_index = self._detect_products_end(ocr_lines, products_start_index)

        product_name_buffer = []
        buffered_product_price = None

        def save_if_complete():
            nonlocal product_name_buffer, buffered_product_price
            if product_name_buffer and buffered_product_price is not None and buffered_product_price > 0:
                normalized_product_name = self._clean_product_name(" ".join(product_name_buffer))
                if len(normalized_product_name) >= 3:
                    extracted_products.append(
                        Producto(nombre=normalized_product_name, precio_total=buffered_product_price)
                    )
            product_name_buffer = []
            buffered_product_price = None

        for raw_line_text in ocr_lines[products_start_index:products_end_index]:
            normalized_line_text = re.sub(r"\s+", " ", raw_line_text).strip()
            if not normalized_line_text:
                continue

            if (
                self.line_classifier.is_discard_line(normalized_line_text)
                or self.line_classifier.is_header_line(normalized_line_text)
                or self.line_classifier.is_payment_line(normalized_line_text)
                or self.line_classifier.is_address_line(normalized_line_text)
            ):
                save_if_complete()
                continue

            line_prices = self.price_extractor_service.extract_prices(normalized_line_text)

            if line_prices:
                positive_prices = [line_price for line_price in line_prices if line_price > 0]
                selected_price = max(positive_prices) if positive_prices else None

                line_text_without_prices = re.sub(r"-?\d+[.,]\d{2}", "", normalized_line_text)
                line_text_without_prices = re.sub(r"\s+", " ", line_text_without_prices).strip()
                line_text_without_prices = re.sub(
                    r"^[\s\d.,*×xX-]+\s*|\s*[\s\d.,*×xX-]+$",
                    "",
                    line_text_without_prices,
                ).strip()

                if (
                    line_text_without_prices
                    and len(line_text_without_prices) >= 3
                    and has_letters(line_text_without_prices)
                ):
                    if product_name_buffer and buffered_product_price is not None:
                        save_if_complete()
                    if product_name_buffer:
                        product_name_buffer.append(line_text_without_prices)
                    else:
                        product_name_buffer = [line_text_without_prices]
                    buffered_product_price = selected_price
                    save_if_complete()
                elif product_name_buffer:
                    buffered_product_price = selected_price
                    save_if_complete()
            else:
                if self.line_classifier.is_code_line(normalized_line_text):
                    continue
                if not self.line_classifier.is_product_candidate(normalized_line_text):
                    save_if_complete()
                    continue

                if product_name_buffer and buffered_product_price is not None:
                    save_if_complete()
                product_name_buffer.append(normalized_line_text)

        save_if_complete()
        return extracted_products

    def _detect_products_start(self, ocr_lines):
        for line_index, line_text in enumerate(ocr_lines):
            upper_line_text = line_text.upper()
            if any(table_keyword in upper_line_text for table_keyword in ["DESCRIP", "P.V.P", "PVP", "P.UNIT"]):
                nearby_context_text = " ".join(ocr_lines[max(0, line_index - 2) : line_index + 6]).upper()
                if any(
                    context_keyword in nearby_context_text
                    for context_keyword in ["CANT", "PRODUCTO", "TOTAL", "UNITARIO", "P.UNIT", "IMPORT"]
                ):
                    first_product_index = line_index + 1
                    while first_product_index < len(ocr_lines) and self.line_classifier.is_header_line(
                        ocr_lines[first_product_index]
                    ):
                        first_product_index += 1
                    return first_product_index
            if re.search(r"\bOP:\s*\d", upper_line_text) or re.search(r"\bCAIXA\s*:\s*\d", upper_line_text):
                return line_index + 1
        return 0

    def _detect_products_end(self, ocr_lines, products_start_index):
        for line_index in range(max(products_start_index, int(len(ocr_lines) * 0.3)), len(ocr_lines)):
            compact_line_text = ocr_lines[line_index].upper().replace(" ", "")
            nearby_context_text = " ".join(ocr_lines[line_index : line_index + 3]).upper().replace(" ", "")

            if "TIPOIVA" in compact_line_text and "BASEIMPONIBLE" in nearby_context_text:
                return line_index
            if "DESGLOSSAMENT" in compact_line_text or "DESGLOSAMENT" in compact_line_text:
                return line_index
            if re.match(r"^\s*TOTAL\b", ocr_lines[line_index], re.IGNORECASE):
                return line_index
            if self.line_classifier.is_payment_line(ocr_lines[line_index]):
                return line_index
            if re.match(r"^\s*ARTICLES\s*:", ocr_lines[line_index], re.IGNORECASE):
                return line_index

        return len(ocr_lines)

    @staticmethod
    def _clean_product_name(raw_product_name):
        cleaned_product_name = raw_product_name.strip()
        product_name_without_quantity_prefix = re.sub(r"^\d+\s+", "", cleaned_product_name)
        if len(product_name_without_quantity_prefix) >= 3:
            cleaned_product_name = product_name_without_quantity_prefix
        return cleaned_product_name.upper()
