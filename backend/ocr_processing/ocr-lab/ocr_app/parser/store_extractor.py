import re
from difflib import SequenceMatcher

from .constants import KNOWN_STORES


class StoreExtractor:
    """Identifica comercio a partir de variantes conocidas y fuzzy match."""

    def __init__(self):
        self.known_stores = KNOWN_STORES

    def extract(self, ocr_lines):
        full_ocr_text = " ".join(ocr_lines).upper()
        for canonical_store_name, store_variants in self.known_stores.items():
            if any(store_variant in full_ocr_text for store_variant in store_variants):
                return canonical_store_name

        best_score = 0.0
        best_matching_store = None
        normalized_candidate_lines = [
            re.sub(r"[^A-Za-zÀ-ÿ\s]", "", ocr_line).upper().strip()
            for ocr_line in ocr_lines[:12]
        ]

        for canonical_store_name, store_variants in self.known_stores.items():
            for store_variant in store_variants:
                normalized_variant = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", store_variant).upper().strip()
                for normalized_candidate_line in normalized_candidate_lines:
                    if not normalized_candidate_line:
                        continue
                    similarity_score = SequenceMatcher(
                        None, normalized_candidate_line, normalized_variant
                    ).ratio()
                    if similarity_score > best_score:
                        best_score = similarity_score
                        best_matching_store = canonical_store_name

        if best_score >= 0.7:
            return best_matching_store

        for ocr_line in ocr_lines[:10]:
            line_text_without_symbols = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", ocr_line).strip()
            if 4 <= len(line_text_without_symbols) <= 30:
                return line_text_without_symbols.upper()

        return None
