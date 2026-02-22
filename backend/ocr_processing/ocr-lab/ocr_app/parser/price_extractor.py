import re


class PriceExtractor:
    """Extrae importes monetarios evitando falsos positivos comunes."""

    def __init__(self, normalize_number_function):
        self.normalize_number_function = normalize_number_function

    def extract_prices(self, texto_linea_ocr):
        texto_linea_mayus = texto_linea_ocr.upper()

        if "%" in texto_linea_mayus or "IVA" in texto_linea_mayus:
            return []
        if re.search(r"\d+[.,]\d{2}\s*P\b", texto_linea_mayus):
            return []
        if re.search(r"\b(CP|OP|ID)\s*[:\-]\s*\d+\b", texto_linea_mayus):
            return []

        tokens_numericos = re.findall(r"-?\d+(?:[.,]\d{2,3})", texto_linea_ocr)
        candidatos_precio_normalizados = []
        for token_numerico in tokens_numericos:
            valor_normalizado = self.normalize_number_function(token_numerico)
            if valor_normalizado is not None:
                candidatos_precio_normalizados.append(valor_normalizado)
        return candidatos_precio_normalizados
