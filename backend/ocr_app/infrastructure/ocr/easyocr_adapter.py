from typing import List

from core.ports.ocr_port import OCRPort
from ocr import OCREngine
from config import OCRConfig


class EasyOCRAdapter(OCRPort):
    """Adaptador que implementa OCRPort usando EasyOCR."""

    def __init__(self, config: OCRConfig = None):
        self.config = config or OCRConfig(ruta_imagen="")
        self._engine = None

    @property
    def engine(self) -> OCREngine:
        """Inicializa el motor OCR lazily."""
        if self._engine is None:
            self._engine = OCREngine(self.config)
        return self._engine

    def extract_text(self, image) -> List[str]:
        """Extrae texto de una imagen usando EasyOCR."""
        return self.engine.ejecutar(image)
