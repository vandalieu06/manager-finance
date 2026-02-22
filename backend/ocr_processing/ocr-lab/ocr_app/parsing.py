import json

from .parser.constants import KNOWN_STORES
from .parser.text_utils import (
    format_numeric_field,
    normalize_ocr_lines,
    sanitize_tsv_field,
)
from .parser.ticket_parser_refactored import TicketParserRefactored


class TicketParser:
    """Fachada ligera para parsear lineas OCR en un ticket estructurado."""

    def __init__(self):
        self.refactored_parser = TicketParserRefactored()

    def parsear(self, ocr_lines):
        """Parsea lineas OCR ya normalizadas."""
        return self.refactored_parser.parse_lines(ocr_lines)

    # TODO_REMOVE_COMPAT: wrapper de compatibilidad temporal para OCR crudo.
    def parsear_texto_crudo(self, raw_ocr_text: str):
        return self.parsear(normalize_ocr_lines(raw_ocr_text))


def export_tsv(parsed_ticket: dict) -> str:
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


def export_productos_json(parsed_ticket: dict) -> str:
    """Exporta solo productos fisicos como JSON compacto [{name, price}]."""
    output_json_products: list[dict[str, float | str]] = []

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


def _parsear_desde_texto(raw_ocr_text: str) -> dict:
    parsed_lines = normalize_ocr_lines(raw_ocr_text)
    return TicketParser().parsear(parsed_lines)


def parsear_a_tsv(raw_ocr_text: str) -> str:
    """Funcion publica para parsear OCR crudo y devolver TSV v1."""
    return export_tsv(_parsear_desde_texto(raw_ocr_text))


def parsear_a_productos_json(raw_ocr_text: str) -> str:
    """Funcion publica para parsear OCR crudo a JSON [{name, price}]."""
    return export_productos_json(_parsear_desde_texto(raw_ocr_text))


__all__ = [
    "TicketParser",
    "KNOWN_STORES",
    "parsear_a_tsv",
    "parsear_a_productos_json",
    "export_tsv",
    "export_productos_json",
]
