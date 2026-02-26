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
        self.product_extractor = ProductExtractor(
            self.line_classifier, self.price_extractor
        )
        self.product_filter = ProductFilter()
        self.metadata_extractor = MetadataExtractor(
            self.line_classifier,
            self.price_extractor,
            normalize_number,
        )

    def parse_lines(self, ocr_lines):
        texto_ocr_completo = "\n".join(ocr_lines)

        nombre_comercio_extraido = self.store_extractor.extract(ocr_lines)
        fecha_hora_cruda_extraida = self.date_extractor.extract_datetime_by_context(
            ocr_lines
        ) or self.date_extractor.extract_date(texto_ocr_completo)

        linea_direccion_extraida, linea_postal_ciudad_extraida = (
            self.metadata_extractor.extract_address_postal(ocr_lines)
        )
        filas_iva_extraidas = self.metadata_extractor.extract_vat(ocr_lines)
        importe_total_base_extraido = self.total_extractor.extract(ocr_lines)
        productos_extraidos = self.product_extractor.extract(ocr_lines)
        productos_filtrados = self.product_filter.filter_by_store(
            productos_extraidos, nombre_comercio_extraido
        )

        return {
            "comercio": nombre_comercio_extraido,
            "fecha": fecha_hora_cruda_extraida,
            "datetime_iso": self.date_extractor.normalize_iso_datetime(
                fecha_hora_cruda_extraida
            ),
            "productos": productos_filtrados,
            "total": self.metadata_extractor.adjust_total_with_vat(
                importe_total_base_extraido, filas_iva_extraidas
            ),
            "moneda": "EUR",
            "cif": self.metadata_extractor.extract_cif(ocr_lines),
            "address": linea_direccion_extraida,
            "postal_city": linea_postal_ciudad_extraida,
            "phone": self.metadata_extractor.extract_phone(ocr_lines),
            "op": self.metadata_extractor.extract_op(ocr_lines),
            "ticket_id": self.metadata_extractor.extract_ticket_id(ocr_lines),
            "iva": filas_iva_extraidas,
            "payments": self.metadata_extractor.extract_payments(ocr_lines),
            "raw_text": texto_ocr_completo,
            "num_lineas": len(ocr_lines),
        }

    def parse_products(self, ocr_lines, nombre_comercio_detectado=None):
        productos_extraidos = self.product_extractor.extract(ocr_lines)
        return self.product_filter.filter_by_store(
            productos_extraidos, nombre_comercio_detectado
        )
