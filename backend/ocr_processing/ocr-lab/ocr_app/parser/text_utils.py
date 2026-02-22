import re


def normalize_number(raw_number_text):
    """Convierte texto con comas/puntos a float tolerante a OCR."""
    sanitized_number_text = re.sub(r"[^\d,.\-]", "", raw_number_text.replace(" ", ""))
    if not re.search(r"\d", sanitized_number_text):
        return None

    decimal_separator = None
    if "." in sanitized_number_text and "," in sanitized_number_text:
        decimal_separator = (
            ","
            if sanitized_number_text.rfind(",") > sanitized_number_text.rfind(".")
            else "."
        )
    elif "," in sanitized_number_text:
        comma_split_parts = sanitized_number_text.split(",")
        if len(comma_split_parts) >= 2 and 1 <= len(comma_split_parts[-1]) <= 3:
            decimal_separator = ","
    elif "." in sanitized_number_text:
        dot_split_parts = sanitized_number_text.split(".")
        if len(dot_split_parts) >= 2 and 1 <= len(dot_split_parts[-1]) <= 3:
            decimal_separator = "."

    if decimal_separator == ",":
        sanitized_number_text = sanitized_number_text.replace(".", "")
        sanitized_number_text = sanitized_number_text.replace(",", ".")
    elif decimal_separator == ".":
        sanitized_number_text = sanitized_number_text.replace(",", "")
    else:
        sanitized_number_text = re.sub(r"[.,]", "", sanitized_number_text)

    if sanitized_number_text in {"", "-", ".", "-."}:
        return None

    try:
        return float(sanitized_number_text)
    except ValueError:
        return None


def normalize_ocr_lines(raw_ocr_text):
    """Normaliza OCR crudo en lineas limpias sin vacios."""
    return [
        re.sub(r"\s+", " ", raw_ocr_line).strip()
        for raw_ocr_line in raw_ocr_text.splitlines()
        if raw_ocr_line.strip()
    ]


def has_letters(candidate_text):
    """Indica si hay suficiente contenido textual para tratar la linea como texto."""
    return len(re.findall(r"[A-Za-zÀ-ÿ]", candidate_text)) >= 2


def sanitize_tsv_field(raw_field_value):
    """Evita romper el contrato TSV por tabs o saltos de linea."""
    if raw_field_value is None:
        return ""
    return str(raw_field_value).replace("\t", " ").replace("\n", " ").strip()


def format_numeric_field(raw_numeric_value, decimals=2):
    """Formatea numeros para salida TSV respetando campos opcionales."""
    if raw_numeric_value is None or raw_numeric_value == "":
        return ""
    if isinstance(raw_numeric_value, (float, int)):
        return f"{float(raw_numeric_value):.{decimals}f}"
    return sanitize_tsv_field(raw_numeric_value)
