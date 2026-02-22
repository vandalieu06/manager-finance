import re

from .text_utils import has_letters


class MetadataExtractor:
    """Extrae metadatos de cabecera y fiscalidad/pagos."""

    def __init__(self, line_classifier, price_extractor_service, normalize_number_function):
        self.line_classifier = line_classifier
        self.price_extractor_service = price_extractor_service
        self.normalize_number_function = normalize_number_function

    def extract_cif(self, ocr_lines):
        cif_patterns = [
            r"\b([A-Z]\d{8})\b",
            r"\b(\d{8}[A-Z])\b",
            r"\b([A-Z]\d{7}[A-Z0-9])\b",
        ]

        for line_text in ocr_lines[:20]:
            for cif_pattern in cif_patterns:
                matched_cif = re.search(cif_pattern, line_text.upper())
                if matched_cif:
                    return matched_cif.group(1)
        return ""

    def extract_phone(self, ocr_lines):
        for line_text in ocr_lines[:25]:
            matched_phone = re.search(r"(?:\+34\s*)?(\d(?:[\s.-]?\d){8})", line_text)
            if matched_phone:
                return re.sub(r"\D", "", matched_phone.group(1))
        return ""

    def extract_op(self, ocr_lines):
        for line_text in ocr_lines:
            matched_operation_code = re.search(
                r"\bOP\s*[:\-]?\s*([A-Z0-9]+)\b", line_text.upper()
            )
            if matched_operation_code:
                return matched_operation_code.group(1)
        return ""

    def extract_ticket_id(self, ocr_lines):
        ticket_id_patterns = [
            r"\b(?:TICKET|FACTURA)\s*(?:N[Oº°]\s*)?[:\-]?\s*([A-Z0-9\-]{4,})\b",
            r"\bN[Oº°]\s*[:\-]?\s*([A-Z0-9\-]{5,})\b",
        ]

        for line_text in ocr_lines:
            upper_line_text = line_text.upper()
            for ticket_id_pattern in ticket_id_patterns:
                matched_ticket_id = re.search(ticket_id_pattern, upper_line_text)
                if matched_ticket_id:
                    return matched_ticket_id.group(1)
        return ""

    def extract_address_postal(self, ocr_lines):
        detected_address = ""
        detected_postal_city = ""

        for line_text in ocr_lines[:25]:
            if not detected_address and self.line_classifier.is_address_line(line_text):
                detected_address = line_text.strip()
            if (
                not detected_postal_city
                and re.search(r"\b\d{5}\b", line_text)
                and has_letters(line_text)
            ):
                detected_postal_city = line_text.strip()
            if detected_address and detected_postal_city:
                break

        return detected_address, detected_postal_city

    def extract_vat(self, ocr_lines):
        extracted_vat_rows = []

        for line_text in ocr_lines:
            if "IVA" not in line_text.upper():
                continue

            matched_vat_rate = re.search(r"(\d{1,2}(?:[.,]\d{1,2})?)\s*%", line_text)
            normalized_line_numbers = [
                normalized_number
                for normalized_number in (
                    self.normalize_number_function(raw_number_token)
                    for raw_number_token in re.findall(r"-?\d+(?:[.,]\d{2,3})", line_text)
                )
                if normalized_number is not None
            ]

            if len(normalized_line_numbers) < 2:
                continue

            vat_base_amount = normalized_line_numbers[-2]
            vat_quota_amount = normalized_line_numbers[-1]

            if vat_base_amount <= 0 or vat_quota_amount < 0:
                continue

            normalized_vat_rate = (
                self.normalize_number_function(matched_vat_rate.group(1))
                if matched_vat_rate
                else None
            )
            extracted_vat_rows.append(
                {
                    "rate": round(normalized_vat_rate, 2)
                    if normalized_vat_rate is not None
                    else 0.0,
                    "base": round(vat_base_amount, 2),
                    "amount": round(vat_quota_amount, 2),
                }
            )

        return extracted_vat_rows

    def extract_payments(self, ocr_lines):
        extracted_payments = []

        for line_text in ocr_lines:
            if not self.line_classifier.is_payment_line(line_text):
                continue

            line_prices = self.price_extractor_service.extract_prices(line_text)
            inferred_payment_method = self._infer_payment_method(line_text)
            if inferred_payment_method and line_prices:
                extracted_payments.append(
                    {"method": inferred_payment_method, "amount": round(max(line_prices), 2)}
                )

        return extracted_payments

    @staticmethod
    def adjust_total_with_vat(extracted_total, extracted_vat_rows):
        if not extracted_vat_rows:
            return round(extracted_total, 2) if extracted_total is not None else None

        vat_base_total = round(sum(vat_row.get("base", 0.0) for vat_row in extracted_vat_rows), 2)
        vat_quota_total = round(
            sum(vat_row.get("amount", 0.0) for vat_row in extracted_vat_rows), 2
        )

        if vat_base_total <= 0 or vat_quota_total <= 0:
            return round(extracted_total, 2) if extracted_total is not None else None

        adjusted_total_with_vat = round(vat_base_total + vat_quota_total, 2)
        if extracted_total is None:
            return adjusted_total_with_vat

        rounded_extracted_total = round(extracted_total, 2)
        if abs(rounded_extracted_total - vat_base_total) <= 0.02:
            return adjusted_total_with_vat
        return rounded_extracted_total

    @staticmethod
    def _infer_payment_method(line_text):
        upper_line_text = line_text.upper()
        if "EFECT" in upper_line_text:
            return "EFECTIVO"
        if any(
            payment_token in upper_line_text
            for payment_token in ["TARJETA", "TARGETA", "VISA", "MASTERCARD", "MAESTRO"]
        ):
            return "TARJETA"
        return ""
