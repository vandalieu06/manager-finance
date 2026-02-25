from abc import ABC, abstractmethod

from ..entities.producto import Producto


class LLMPort(ABC):
    """Puerto (interfaz) para el modelo LLM."""

    @abstractmethod
    def extract_products(self, ocr_text):
        """Extrae productos del texto OCR usando LLM."""
        pass
