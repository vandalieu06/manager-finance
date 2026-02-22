from .config import OCRConfig
from .models import Producto
from .parsing import (
    TicketParser,
    export_productos_json,
    export_tsv,
    parsear_a_productos_json,
    parsear_a_tsv,
)

try:
    from .ocr import OCREngine
except ModuleNotFoundError:
    # pragma: no cover - entorno sin dependencias OCR opcionales
    OCREngine = None

__all__ = [
    "OCRConfig",
    "Producto",
    "OCREngine",
    "TicketParser",
    "export_productos_json",
    "export_tsv",
    "parsear_a_productos_json",
    "parsear_a_tsv",
]
