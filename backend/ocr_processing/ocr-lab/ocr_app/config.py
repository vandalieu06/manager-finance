from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class OCRConfig:
    """Configuracion general para el OCR y preprocesado."""

    ruta_imagen: str
    umbral_min_confianza: float = 0.25
    lenguajes_ocr: List[str] = None
    usa_gpu: bool = False

    # Debug
    prefijo_debug_preprocesado: str = "debug_metodo_"

    # Preprocesado
    escalado_fuerte: float = 4.0
    escalado_medio: float = 3.5
    blur_suave: tuple[int, int] = (3, 3)
    blur_fuerte: tuple[int, int] = (5, 5)
    adaptive_block_size: int = 11
    adaptive_c: int = 2
    clahe_clip_limit: float = 3.0
    clahe_tile_grid: tuple[int, int] = (8, 8)
    umbral_fondo_oscuro: int = 127
    ancho_objetivo_ocr: int = 2000

    # Asigna lenguajes por defecto si no se pasan.
    def __post_init__(self):
        """Completa valores por defecto para la configuracion."""
        if self.lenguajes_ocr is None:
            object.__setattr__(self, "lenguajes_ocr", ["es"])
