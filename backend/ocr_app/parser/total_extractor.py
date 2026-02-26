import re


class TotalExtractor:
    """Calcula el total del ticket con estrategia de candidatos y fallback."""

    def __init__(self, price_extractor_service):
        self.price_extractor_service = price_extractor_service

    def extract(self, ocr_lines):
        candidatos_total_puntuados = self._find_total_candidates(ocr_lines)
        if candidatos_total_puntuados:
            candidatos_total_puntuados.sort(
                key=lambda entrada_candidata: (
                    entrada_candidata[0],
                    entrada_candidata[2],
                ),
                reverse=True,
            )
            return candidatos_total_puntuados[0][1]
        return self._find_largest_plausible_decimal(ocr_lines)

    def _find_total_candidates(self, ocr_lines):
        candidatos_puntuados = []

        for indice_linea_keyword, texto_linea_keyword in enumerate(ocr_lines):
            texto_linea_mayus = texto_linea_keyword.upper()
            if not re.search(
                r"\b(TOTAL|TOTAI|A\s*PAGAR|IMPORTE\s*TOTAL)\b", texto_linea_mayus
            ):
                continue

            texto_linea_compacto = texto_linea_mayus.replace(" ", "")
            es_linea_total_iva = (
                "TOTALIVA" in texto_linea_compacto or "CUOTAIVA" in texto_linea_compacto
            )
            es_subtotal = "SUBTOTAL" in texto_linea_compacto
            texto_linea_solo_letras = re.sub(r"[^A-Z]", "", texto_linea_mayus)
            es_total_aislado = texto_linea_solo_letras in {
                "TOTAL",
                "TOTAI",
                "APAGAR",
                "IMPORTETOTAL",
            }

            for indice_linea_candidata in range(
                indice_linea_keyword, min(indice_linea_keyword + 3, len(ocr_lines))
            ):
                precios_linea_candidata = self.price_extractor_service.extract_prices(
                    ocr_lines[indice_linea_candidata]
                )
                for precio_candidato in precios_linea_candidata:
                    if precio_candidato <= 0:
                        continue
                    puntuacion_candidata = self._score_candidate(
                        indice_linea_candidata,
                        es_total_aislado,
                        es_linea_total_iva,
                        es_subtotal,
                    )
                    candidatos_puntuados.append(
                        (puntuacion_candidata, precio_candidato, indice_linea_candidata)
                    )

        return candidatos_puntuados

    @staticmethod
    def _score_candidate(
        indice_linea_candidata, es_total_aislado, es_total_iva, es_subtotal
    ):
        puntuacion = 100 + indice_linea_candidata + (30 if es_total_aislado else 0)
        if es_total_iva:
            puntuacion -= 80
        if es_subtotal:
            puntuacion -= 60
        return puntuacion

    def _find_largest_plausible_decimal(self, ocr_lines):
        valores_numericos_plausibles = []
        for texto_linea_candidata in ocr_lines:
            if any(
                token_relacionado_iva in texto_linea_candidata.upper()
                for token_relacionado_iva in ["IVA", "%", "TIPO", "BASE IMPONIBLE"]
            ):
                continue
            precios_linea_candidata = self.price_extractor_service.extract_prices(
                texto_linea_candidata
            )
            for precio_candidato in precios_linea_candidata:
                if precio_candidato > 0.5:
                    valores_numericos_plausibles.append(precio_candidato)
        return (
            max(valores_numericos_plausibles) if valores_numericos_plausibles else None
        )
