import re


class PriceExtractor:
    """Extrae importes monetarios evitando falsos positivos comunes."""

    def __init__(self, normalize_number_function):
        self.normalize_number_function = normalize_number_function

    def extract_prices(self, line_text):
        upper_line_text = line_text.upper()

        if "%" in upper_line_text or "IVA" in upper_line_text:
            return []
        if re.search(r"\d+[.,]\d{2}\s*P\b", upper_line_text):
            return []
        if re.search(r"\b(CP|OP|ID)\s*[:\-]\s*\d+\b", upper_line_text):
            return []

        matched_numeric_tokens = re.findall(r"-?\d+(?:[.,]\d{2,3})", line_text)
        extracted_prices = []
        for numeric_token in matched_numeric_tokens:
            normalized_number = self.normalize_number_function(numeric_token)
            if normalized_number is not None:
                extracted_prices.append(normalized_number)
        return extracted_prices
