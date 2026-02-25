import re


def normalize_number(texto_numero_crudo):
    """Convierte texto con comas/puntos a float tolerante a OCR."""
    texto_numero_limpio = re.sub(r"[^\d,.\-]", "", texto_numero_crudo.replace(" ", ""))
    if not re.search(r"\d", texto_numero_limpio):
        return None

    separador_decimal_detectado = None
    if "." in texto_numero_limpio and "," in texto_numero_limpio:
        separador_decimal_detectado = (
            ","
            if texto_numero_limpio.rfind(",") > texto_numero_limpio.rfind(".")
            else "."
        )
    elif "," in texto_numero_limpio:
        segmentos_con_coma = texto_numero_limpio.split(",")
        if len(segmentos_con_coma) >= 2 and 1 <= len(segmentos_con_coma[-1]) <= 3:
            separador_decimal_detectado = ","
    elif "." in texto_numero_limpio:
        segmentos_con_punto = texto_numero_limpio.split(".")
        if len(segmentos_con_punto) >= 2 and 1 <= len(segmentos_con_punto[-1]) <= 3:
            separador_decimal_detectado = "."

    if separador_decimal_detectado == ",":
        texto_numero_limpio = texto_numero_limpio.replace(".", "")
        texto_numero_limpio = texto_numero_limpio.replace(",", ".")
    elif separador_decimal_detectado == ".":
        texto_numero_limpio = texto_numero_limpio.replace(",", "")
    else:
        texto_numero_limpio = re.sub(r"[.,]", "", texto_numero_limpio)

    if texto_numero_limpio in {"", "-", ".", "-."}:
        return None

    try:
        return float(texto_numero_limpio)
    except ValueError:
        return None


def normalize_ocr_lines(texto_ocr_crudo):
    """Normaliza OCR crudo en lineas limpias sin vacios."""
    return [
        re.sub(r"\s+", " ", texto_linea_crudo).strip()
        for texto_linea_crudo in texto_ocr_crudo.splitlines()
        if texto_linea_crudo.strip()
    ]


def has_letters(texto_candidato):
    """Indica si hay suficiente contenido textual para tratar la linea como texto."""
    return len(re.findall(r"[A-Za-zÀ-ÿ]", texto_candidato)) >= 2


def sanitize_tsv_field(valor_campo_crudo):
    """Evita romper el contrato TSV por tabs o saltos de linea."""
    if valor_campo_crudo is None:
        return ""
    return str(valor_campo_crudo).replace("\t", " ").replace("\n", " ").strip()


def format_numeric_field(valor_numerico_crudo, decimals=2):
    """Formatea numeros para salida TSV respetando campos opcionales."""
    if valor_numerico_crudo is None or valor_numerico_crudo == "":
        return ""
    if isinstance(valor_numerico_crudo, (float, int)):
        return f"{float(valor_numerico_crudo):.{decimals}f}"
    return sanitize_tsv_field(valor_numerico_crudo)
