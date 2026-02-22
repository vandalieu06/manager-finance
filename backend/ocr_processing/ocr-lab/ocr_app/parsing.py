import json

from .parser.date_extractor import DateExtractor
from .parser.line_classifier import LineClassifier
from .parser.metadata_extractor import MetadataExtractor
from .parser.price_extractor import PriceExtractor
from .parser.constants import KNOWN_STORES
from .parser.store_extractor import StoreExtractor
from .parser.text_utils import (
    format_numeric_field,
    normalize_number,
    normalize_ocr_lines,
    sanitize_tsv_field,
)
from .parser.ticket_parser_refactored import TicketParserRefactored
from .parser.total_extractor import TotalExtractor


class TicketParser:
    """Fachada compatible con la API anterior basada en componentes SRP."""

    def __init__(self):
        self.refactored_parser = TicketParserRefactored()
        self.date_extractor = self.refactored_parser.date_extractor
        self.total_extractor = self.refactored_parser.total_extractor
        self.store_extractor = self.refactored_parser.store_extractor
        self.product_extractor = self.refactored_parser.product_extractor
        self.product_filter = self.refactored_parser.product_filter
        self.metadata_extractor = self.refactored_parser.metadata_extractor

    def normalizar_numero(self, raw_number_text):
        return normalize_number(raw_number_text)

    def extraer_fecha(self, raw_text):
        return self.date_extractor.extract_date(raw_text)

    def extraer_fecha_y_hora_por_contexto(self, ocr_lines):
        return self.date_extractor.extract_datetime_by_context(ocr_lines)

    def extraer_total_por_contexto(self, ocr_lines):
        return self.total_extractor.extract(ocr_lines)

    def extraer_comercio(self, ocr_lines):
        return self.store_extractor.extract(ocr_lines)

    def extraer_productos(self, ocr_lines):
        return self.product_extractor.extract(ocr_lines)

    def filtrar_productos_por_comercio(self, extracted_products, detected_store):
        return self.product_filter.filter_by_store(extracted_products, detected_store)

    def parsear(self, ocr_lines):
        return self.refactored_parser.parse_lines(ocr_lines)

    def _lineas_a_texto(self, raw_ocr_text):
        return normalize_ocr_lines(raw_ocr_text)

    def _normalizar_fecha_iso(self, raw_date_value):
        return self.date_extractor.normalize_iso_datetime(raw_date_value)

    def _extraer_cif(self, ocr_lines):
        return self.metadata_extractor.extract_cif(ocr_lines)

    def _extraer_telefono(self, ocr_lines):
        return self.metadata_extractor.extract_phone(ocr_lines)

    def _extraer_op(self, ocr_lines):
        return self.metadata_extractor.extract_op(ocr_lines)

    def _extraer_ticket_id(self, ocr_lines):
        return self.metadata_extractor.extract_ticket_id(ocr_lines)

    def _extraer_address_postal(self, ocr_lines):
        return self.metadata_extractor.extract_address_postal(ocr_lines)

    def _extraer_iva(self, ocr_lines):
        return self.metadata_extractor.extract_vat(ocr_lines)

    def _extraer_pagos(self, ocr_lines):
        return self.metadata_extractor.extract_payments(ocr_lines)

    def _ajustar_total_con_iva(self, extracted_total, extracted_vat_rows):
        return self.metadata_extractor.adjust_total_with_vat(
            extracted_total, extracted_vat_rows
        )

    def parsear_a_tsv(self, raw_ocr_text):
        parsed_ticket = self.parsear(self._lineas_a_texto(raw_ocr_text))
        return export_tsv(parsed_ticket)

    def parsear_a_productos_json(self, raw_ocr_text):
        parsed_ticket = self.parsear(self._lineas_a_texto(raw_ocr_text))
        return export_productos_json(parsed_ticket)


def export_tsv(parsed_ticket):
    """Exporta un ticket parseado al contrato TSV fijo v1."""
    output_tsv_lines = ["VER\t1"]
    output_tsv_lines.append(
        "\t".join(
            [
                "H",
                sanitize_tsv_field(parsed_ticket.get("comercio", "")),
                sanitize_tsv_field(parsed_ticket.get("cif", "")),
                sanitize_tsv_field(parsed_ticket.get("address", "")),
                sanitize_tsv_field(parsed_ticket.get("postal_city", "")),
                sanitize_tsv_field(parsed_ticket.get("phone", "")),
                sanitize_tsv_field(parsed_ticket.get("datetime_iso", "")),
                sanitize_tsv_field(parsed_ticket.get("op", "")),
                sanitize_tsv_field(parsed_ticket.get("ticket_id", "")),
                sanitize_tsv_field(parsed_ticket.get("moneda", "EUR") or "EUR"),
            ]
        )
    )

    for extracted_product in parsed_ticket.get("productos", []):
        extracted_quantity = getattr(extracted_product, "cantidad", None)
        extracted_line_total = getattr(extracted_product, "precio_total", None)
        calculated_unit_price = None
        if extracted_quantity and extracted_line_total:
            try:
                calculated_unit_price = float(extracted_line_total) / float(
                    extracted_quantity
                )
            except (ValueError, ZeroDivisionError):
                calculated_unit_price = None

        output_tsv_lines.append(
            "\t".join(
                [
                    "L",
                    sanitize_tsv_field(getattr(extracted_product, "nombre", "")),
                    format_numeric_field(extracted_quantity, decimals=3),
                    format_numeric_field(calculated_unit_price),
                    format_numeric_field(extracted_line_total),
                    "",
                ]
            )
        )

    extracted_total = parsed_ticket.get("total")
    output_tsv_lines.append(f"T\t{format_numeric_field(extracted_total)}")

    for vat_row in parsed_ticket.get("iva", []):
        output_tsv_lines.append(
            "\t".join(
                [
                    "V",
                    format_numeric_field(vat_row.get("rate")),
                    format_numeric_field(vat_row.get("base")),
                    format_numeric_field(vat_row.get("amount")),
                ]
            )
        )

    for payment_row in parsed_ticket.get("payments", []):
        output_tsv_lines.append(
            "\t".join(
                [
                    "P",
                    sanitize_tsv_field(payment_row.get("method", "")),
                    format_numeric_field(payment_row.get("amount")),
                ]
            )
        )

    return "\n".join(output_tsv_lines)


def export_productos_json(parsed_ticket):
    """Exporta solo productos fisicos como JSON compacto [{name, price}]."""
    output_json_products = []

    for extracted_product in parsed_ticket.get("productos", []):
        product_name = sanitize_tsv_field(getattr(extracted_product, "nombre", ""))
        product_total_price = getattr(extracted_product, "precio_total", None)
        if not product_name or product_total_price is None:
            continue
        if float(product_total_price) <= 0:
            continue
        output_json_products.append(
            {"name": product_name, "price": round(float(product_total_price), 2)}
        )

    return json.dumps(output_json_products, ensure_ascii=False, separators=(",", ":"))


def parsear_a_tsv(raw_ocr_text):
    """Funcion publica para parsear OCR crudo y devolver TSV v1."""
    return TicketParser().parsear_a_tsv(raw_ocr_text)


def parsear_a_productos_json(raw_ocr_text):
    """Funcion publica para parsear OCR crudo a JSON [{name, price}]."""
    return TicketParser().parsear_a_productos_json(raw_ocr_text)


__all__ = [
    "TicketParser",
    "KNOWN_STORES",
    "LineClassifier",
    "PriceExtractor",
    "StoreExtractor",
    "TotalExtractor",
    "MetadataExtractor",
    "DateExtractor",
    "parsear_a_tsv",
    "parsear_a_productos_json",
    "export_tsv",
    "export_productos_json",
]
