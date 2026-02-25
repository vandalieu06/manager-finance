import re
from difflib import SequenceMatcher

from .constants import KNOWN_STORES


class StoreExtractor:
    """Identifica comercio a partir de variantes conocidas y fuzzy match."""

    def __init__(self):
        self.known_stores = KNOWN_STORES

    def extract(self, ocr_lines):
        texto_ocr_completo_mayus = " ".join(ocr_lines).upper()
        for nombre_comercio_canonico, variantes_comercio_conocidas in self.known_stores.items():
            if any(
                variante_comercio in texto_ocr_completo_mayus
                for variante_comercio in variantes_comercio_conocidas
            ):
                return nombre_comercio_canonico

        mejor_score_similitud = 0.0
        mejor_nombre_comercio = None
        lineas_candidatas_cabecera_normalizadas = [
            re.sub(r"[^A-Za-zÀ-ÿ\s]", "", linea_cabecera).upper().strip()
            for linea_cabecera in ocr_lines[:12]
        ]

        for nombre_comercio_canonico, variantes_comercio_conocidas in self.known_stores.items():
            for variante_comercio in variantes_comercio_conocidas:
                variante_comercio_normalizada = re.sub(
                    r"[^A-Za-zÀ-ÿ\s]", "", variante_comercio
                ).upper().strip()
                for linea_cabecera_normalizada in lineas_candidatas_cabecera_normalizadas:
                    if not linea_cabecera_normalizada:
                        continue
                    score_similitud = SequenceMatcher(
                        None, linea_cabecera_normalizada, variante_comercio_normalizada
                    ).ratio()
                    if score_similitud > mejor_score_similitud:
                        mejor_score_similitud = score_similitud
                        mejor_nombre_comercio = nombre_comercio_canonico

        if mejor_score_similitud >= 0.7:
            return mejor_nombre_comercio

        for linea_ocr_temprana in ocr_lines[:10]:
            candidato_comercio_fallback = re.sub(
                r"[^A-Za-zÀ-ÿ\s]", "", linea_ocr_temprana
            ).strip()
            if 4 <= len(candidato_comercio_fallback) <= 30:
                return candidato_comercio_fallback.upper()

        return None
