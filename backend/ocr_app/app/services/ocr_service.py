from typing import List

from config import OCRConfig
from core.entities.producto import Producto
from core.ports.ocr_port import OCRPort
from core.ports.llm_port import LLMPort
from infrastructure.ocr import EasyOCRAdapter
from infrastructure.llm import OllamaAdapter


class OCRService:
    """Servicio que orquesta OCR + LLM para extraer productos de tickets."""

    def __init__(
        self,
        ocr_adapter: OCRPort = None,
        llm_adapter: LLMPort = None,
        config: OCRConfig = None
    ):
        self._ocr_adapter = ocr_adapter or EasyOCRAdapter(config)
        self._llm_adapter = llm_adapter or OllamaAdapter()

    def process_ticket(self, image) -> List[dict]:
        """Procesa una imagen de ticket y retorna array de productos."""
        ocr_lines = self._ocr_adapter.extract_text(image)
        ocr_text = "\n".join(ocr_lines)

        productos = self._llm_adapter.extract_products(ocr_text)

        return [p.to_dict() for p in productos]

    def extract_text_only(self, image) -> List[str]:
        """Extrae solo texto OCR sin procesamiento LLM."""
        return self._ocr_adapter.extract_text(image)
