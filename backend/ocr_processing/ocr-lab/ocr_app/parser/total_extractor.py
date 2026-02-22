import re


class TotalExtractor:
    """Calcula el total del ticket con estrategia de candidatos y fallback."""

    def __init__(self, price_extractor_service):
        self.price_extractor_service = price_extractor_service

    def extract(self, ocr_lines):
        total_candidates = self._find_total_candidates(ocr_lines)
        if total_candidates:
            total_candidates.sort(
                key=lambda candidate_tuple: (candidate_tuple[0], candidate_tuple[2]),
                reverse=True,
            )
            return total_candidates[0][1]
        return self._find_largest_plausible_decimal(ocr_lines)

    def _find_total_candidates(self, ocr_lines):
        total_candidates = []

        for line_index, line_text in enumerate(ocr_lines):
            upper_line_text = line_text.upper()
            if not re.search(r"\b(TOTAL|TOTAI|A\s*PAGAR|IMPORTE\s*TOTAL)\b", upper_line_text):
                continue

            compact_line_text = upper_line_text.replace(" ", "")
            is_vat_total = "TOTALIVA" in compact_line_text or "CUOTAIVA" in compact_line_text
            is_subtotal = "SUBTOTAL" in compact_line_text
            line_text_letters_only = re.sub(r"[^A-Z]", "", upper_line_text)
            is_standalone_total = line_text_letters_only in {
                "TOTAL",
                "TOTAI",
                "APAGAR",
                "IMPORTETOTAL",
            }

            for candidate_line_index in range(line_index, min(line_index + 3, len(ocr_lines))):
                extracted_prices = self.price_extractor_service.extract_prices(
                    ocr_lines[candidate_line_index]
                )
                for extracted_price in extracted_prices:
                    if extracted_price <= 0:
                        continue
                    candidate_score = self._score_candidate(
                        candidate_line_index,
                        is_standalone_total,
                        is_vat_total,
                        is_subtotal,
                    )
                    total_candidates.append(
                        (candidate_score, extracted_price, candidate_line_index)
                    )

        return total_candidates

    @staticmethod
    def _score_candidate(candidate_line_index, is_standalone_total, is_vat_total, is_subtotal):
        score = 100 + candidate_line_index + (30 if is_standalone_total else 0)
        if is_vat_total:
            score -= 80
        if is_subtotal:
            score -= 60
        return score

    def _find_largest_plausible_decimal(self, ocr_lines):
        plausible_numeric_values = []
        for line_text in ocr_lines:
            if any(vat_related_token in line_text.upper() for vat_related_token in ["IVA", "%", "TIPO", "BASE IMPONIBLE"]):
                continue
            extracted_prices = self.price_extractor_service.extract_prices(line_text)
            for extracted_price in extracted_prices:
                if extracted_price > 0.5:
                    plausible_numeric_values.append(extracted_price)
        return max(plausible_numeric_values) if plausible_numeric_values else None
