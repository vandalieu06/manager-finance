from config import OCRConfig
from core.ports.ocr_port import OCRPort
from ocr import OCREngine


class EasyOCRAdapter(OCRPort):
    """Adaptador que implementa OCRPort usando EasyOCR."""

    def __init__(self, config=None):
        self.config = config or OCRConfig()
        self._engine = None

    @property
    def engine(self):
        """Inicializa el motor OCR lazily."""
        if self._engine is None:
            self._engine = OCREngine(self.config)
        return self._engine

    def extract_text(self, image):
        """Extrae texto de una imagen usando EasyOCR."""
        return self.engine.ejecutar(image)
