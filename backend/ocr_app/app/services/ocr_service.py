from infrastructure.llm import OllamaAdapter
from infrastructure.ocr import EasyOCRAdapter
import logging


logger = logging.getLogger(__name__)


class OCRService:
    """Servicio que orquesta OCR + LLM para extraer productos de tickets."""

    def __init__(self, ocr_adapter=None, llm_adapter=None, config=None):
        self._ocr_adapter = ocr_adapter or EasyOCRAdapter(config)
        self._llm_adapter = llm_adapter or OllamaAdapter()

    def process_ticket(self, image):
        """Procesa una imagen de ticket y retorna array de productos."""
        logger.info("OCRService: Extrayendo texto de la imagen...")
        ocr_lines = self._ocr_adapter.extract_text(image)
        ocr_text = '\n'.join(ocr_lines)
        logger.info(f"OCRService: Texto OCR extraído ({len(ocr_lines)} líneas)")

        logger.info("OCRService: Enviando texto al LLM para extracción de productos...")
        productos = self._llm_adapter.extract_products(ocr_text)
        logger.info(f"OCRService: Productos extraídos: {len(productos)}")

        return [p.to_dict() for p in productos]

    def extract_text_only(self, image):
        """Extrae solo texto OCR sin procesamiento LLM."""
        return self._ocr_adapter.extract_text(image)
