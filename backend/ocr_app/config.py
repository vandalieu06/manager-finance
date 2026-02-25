from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OCRConfig:
    """Configuracion general para el OCR y preprocesado."""

    ruta_imagen = './'
    umbral_min_confianza = 0.25
    lenguajes_ocr = None
    usa_gpu = False

    # Preprocesado
    escalado_fuerte = 4.0
    escalado_medio = 3.5
    blur_suave = (3, 3)
    blur_fuerte = (5, 5)
    adaptive_block_size = 11
    adaptive_c = 2
    clahe_clip_limit = 3.0
    clahe_tile_grid = (8, 8)
    umbral_fondo_oscuro = 127
    ancho_objetivo_ocr = 2000

    # Asigna lenguajes por defecto si no se pasan.
    def __post_init__(self):
        """Completa valores por defecto para la configuracion."""
        if self.lenguajes_ocr is None:
            object.__setattr__(self, 'lenguajes_ocr', ['es'])
