from abc import ABC, abstractmethod


class OCRPort(ABC):
    """Puerto (interfaz) para el motor OCR."""

    @abstractmethod
    def extract_text(self, image):
        """Extrae texto de una imagen."""
        pass
