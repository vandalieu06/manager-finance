from abc import ABC, abstractmethod
from typing import List


class OCRPort(ABC):
    """Puerto (interfaz) para el motor OCR."""

    @abstractmethod
    def extract_text(self, image) -> List[str]:
        """Extrae texto de una imagen."""
        pass
