import re
from datetime import datetime


class DateExtractor:
    """Extrae fecha/hora del ticket con heuristicas tolerantes a OCR."""

    def extract_date(self, source_text):
        date_patterns = [
            r"\b(\d{2}[-/\.]\d{2}[-/\.]\d{2,4})\b",
            r"\b(\d{1,2}\s+(?:ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC)[A-Z]*\s+\d{2,4})\b",
            r"\b(\d{4}-\d{2})\b",
            r"\b(\d{2})(\d{2})(\d{2,4})\b",
        ]

        for date_pattern in date_patterns[:2]:
            matched_date = re.search(date_pattern, source_text, re.IGNORECASE)
            if matched_date:
                return matched_date.group(1)

        matched_yyyy_mm = re.search(date_patterns[2], source_text)
        if matched_yyyy_mm:
            extracted_date_text = matched_yyyy_mm.group(1)
            if len(extracted_date_text) >= 5:
                return f"{extracted_date_text[:2]}-{extracted_date_text[2:4]}-{extracted_date_text[5:]}"
            return extracted_date_text
        return None

    def extract_datetime_by_context(self, ocr_lines):
        prioritized_keyword_groups = [
            ["FECHA DE FACTURA", "FECHA DE COMPRA", "FECHA FACTURA"],
            ["FECHA DE PAGO", "FECHA PAGO", "FECHA DE ENTREGA"],
            ["DATA", "TICKET", "FECHA", "HORA"],
        ]

        for keyword_group in prioritized_keyword_groups:
            for line_index, line_text in enumerate(ocr_lines):
                if not any(keyword in line_text.upper() for keyword in keyword_group):
                    continue

                nearby_context_text = " ".join(ocr_lines[line_index : line_index + 6])
                extracted_date_value = self.extract_date(nearby_context_text)
                matched_hour = re.search(r"\b(\d{1,2}:\d{2})\b", nearby_context_text)

                if extracted_date_value and matched_hour:
                    return f"{extracted_date_value} {matched_hour.group(1)}"
                if extracted_date_value:
                    return extracted_date_value

                matched_short_date = re.search(r"\b(\d{2}[-/\.]\d{2})\b", nearby_context_text)
                if matched_short_date:
                    return matched_short_date.group(1)

        return None

    def normalize_iso_datetime(self, raw_date_value):
        if not raw_date_value:
            return ""

        accepted_input_formats = [
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

        for input_format in accepted_input_formats:
            try:
                parsed_datetime = datetime.strptime(raw_date_value.strip(), input_format)
                return parsed_datetime.isoformat(timespec="minutes")
            except ValueError:
                continue
        return ""
