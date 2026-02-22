from .date_extractor import DateExtractor
from .line_classifier import LineClassifier
from .metadata_extractor import MetadataExtractor
from .price_extractor import PriceExtractor
from .product_extractor import ProductExtractor
from .product_filter import ProductFilter
from .store_extractor import StoreExtractor
from .text_utils import normalize_number
from .total_extractor import TotalExtractor


class TicketParserRefactored:
    """Orquestador del parseo de tickets compuesto por extractores simples."""

    def __init__(self):
        self.date_extractor = DateExtractor()
        self.price_extractor = PriceExtractor(normalize_number)
        self.line_classifier = LineClassifier()
        self.total_extractor = TotalExtractor(self.price_extractor)
        self.store_extractor = StoreExtractor()
        self.product_extractor = ProductExtractor(self.line_classifier, self.price_extractor)
        self.product_filter = ProductFilter()
        self.metadata_extractor = MetadataExtractor(
            self.line_classifier,
            self.price_extractor,
            normalize_number,
        )

    def parse_lines(self, ocr_lines):
        full_ocr_text = "\n".join(ocr_lines)

        extracted_store = self.store_extractor.extract(ocr_lines)
        extracted_raw_date = self.date_extractor.extract_datetime_by_context(
            ocr_lines
        ) or self.date_extractor.extract_date(full_ocr_text)

        extracted_address, extracted_postal_city = self.metadata_extractor.extract_address_postal(
            ocr_lines
        )
        extracted_vat_rows = self.metadata_extractor.extract_vat(ocr_lines)
        extracted_base_total = self.total_extractor.extract(ocr_lines)
        extracted_products = self.product_extractor.extract(ocr_lines)
        filtered_products = self.product_filter.filter_by_store(
            extracted_products, extracted_store
        )

        return {
            "comercio": extracted_store,
            "fecha": extracted_raw_date,
            "datetime_iso": self.date_extractor.normalize_iso_datetime(extracted_raw_date),
            "productos": filtered_products,
            "total": self.metadata_extractor.adjust_total_with_vat(
                extracted_base_total, extracted_vat_rows
            ),
            "moneda": "EUR",
            "cif": self.metadata_extractor.extract_cif(ocr_lines),
            "address": extracted_address,
            "postal_city": extracted_postal_city,
            "phone": self.metadata_extractor.extract_phone(ocr_lines),
            "op": self.metadata_extractor.extract_op(ocr_lines),
            "ticket_id": self.metadata_extractor.extract_ticket_id(ocr_lines),
            "iva": extracted_vat_rows,
            "payments": self.metadata_extractor.extract_payments(ocr_lines),
            "raw_text": full_ocr_text,
            "num_lineas": len(ocr_lines),
        }

    def parse_products(self, ocr_lines, detected_store=None):
        extracted_products = self.product_extractor.extract(ocr_lines)
        return self.product_filter.filter_by_store(extracted_products, detected_store)
