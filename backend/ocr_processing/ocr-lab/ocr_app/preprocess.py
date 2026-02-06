from __future__ import annotations

import cv2
import numpy as np

from .config import OCRConfig


class Preprocessor:
    """Aplica distintas tecnicas de preprocesado a imagenes."""
    # Inicializa el preprocesador con configuracion compartida.
    def __init__(self, config: OCRConfig) -> None:
        """Inicializa el preprocesador con la configuracion dada."""
        self.config = config

    # Rota imagenes horizontales para mantener texto en vertical.
    def orientar_vertical_si_horizontal(self, imagen_bgr: np.ndarray) -> np.ndarray:
        """Rota imagenes si el ancho supera el alto."""
        alto, ancho = imagen_bgr.shape[:2]
        if ancho > alto:
            return cv2.rotate(imagen_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return imagen_bgr

    # Calcula factor de escalado objetivo segun ancho y limites.
    def _calcular_factor_escalado(self, imagen_gris: np.ndarray, factor_base: float) -> float:
        """Calcula el factor de escalado para acercarse al ancho objetivo."""
        alto, ancho = imagen_gris.shape[:2]
        ancho_deseado = self.config.ancho_objetivo_ocr
        factor_necesario = ancho_deseado / ancho
        return min(factor_base, max(1.0, factor_necesario))

    # Preprocesa con escalado inteligente y binarizacion adaptativa.
    def preprocesar_escalado_y_binarizacion_adaptativa(
        self, imagen_bgr: np.ndarray
    ) -> np.ndarray:
        """Aumenta resolucion y binariza para mejorar texto pequeno."""
        imagen_gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        factor = self._calcular_factor_escalado(imagen_gris, self.config.escalado_fuerte)
        imagen_escalada = cv2.resize(
            imagen_gris,
            None,
            fx=factor,
            fy=factor,
            interpolation=cv2.INTER_CUBIC,
        )
        imagen_suavizada = cv2.GaussianBlur(imagen_escalada, self.config.blur_suave, 0)
        imagen_binaria = cv2.adaptiveThreshold(
            imagen_suavizada,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            self.config.adaptive_block_size,
            self.config.adaptive_c,
        )
        return imagen_binaria

    # Preprocesa con CLAHE agresivo para bajo contraste.
    def preprocesar_clahe_agresivo(self, imagen_bgr: np.ndarray) -> np.ndarray:
        """Mejora contraste local y realza texto tenue."""
        imagen_gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        factor = self._calcular_factor_escalado(imagen_gris, self.config.escalado_medio)
        imagen_escalada = cv2.resize(
            imagen_gris,
            None,
            fx=factor,
            fy=factor,
            interpolation=cv2.INTER_CUBIC,
        )
        clahe = cv2.createCLAHE(
            clipLimit=self.config.clahe_clip_limit,
            tileGridSize=self.config.clahe_tile_grid,
        )
        imagen_con_contraste = clahe.apply(imagen_escalada)
        return imagen_con_contraste

    # Preprocesa con Otsu tras escalado inteligente.
    def preprocesar_otsu(self, imagen_bgr: np.ndarray) -> np.ndarray:
        """Aplica umbral Otsu tras escalar para fondo uniforme."""
        imagen_gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        factor = self._calcular_factor_escalado(imagen_gris, self.config.escalado_fuerte)
        imagen_escalada = cv2.resize(
            imagen_gris,
            None,
            fx=factor,
            fy=factor,
            interpolation=cv2.INTER_CUBIC,
        )
        imagen_suavizada = cv2.GaussianBlur(imagen_escalada, self.config.blur_fuerte, 0)
        _, imagen_binaria = cv2.threshold(
            imagen_suavizada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return imagen_binaria

    # Invierte la imagen si el fondo es oscuro y binariza.
    def preprocesar_invertir_si_fondo_oscuro(self, imagen_bgr: np.ndarray) -> np.ndarray:
        """Invierte colores cuando el fondo es oscuro y binariza."""
        imagen_gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        factor = self._calcular_factor_escalado(imagen_gris, self.config.escalado_fuerte)
        imagen_escalada = cv2.resize(
            imagen_gris,
            None,
            fx=factor,
            fy=factor,
            interpolation=cv2.INTER_CUBIC,
        )

        if np.mean(imagen_escalada) < self.config.umbral_fondo_oscuro:
            imagen_escalada = cv2.bitwise_not(imagen_escalada)

        imagen_binaria = cv2.adaptiveThreshold(
            imagen_escalada,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            self.config.adaptive_block_size,
            self.config.adaptive_c,
        )
        return imagen_binaria

    # Preprocesa fotos de movil con filtro bilateral, CLAHE y deskew.
    def preprocesar_foto_movil(self, imagen_bgr: np.ndarray) -> np.ndarray:
        """Reduce ruido de camara y corrige inclinacion ligera."""
        imagen_gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        factor = self._calcular_factor_escalado(imagen_gris, 2.0)
        imagen_escalada = cv2.resize(
            imagen_gris,
            None,
            fx=factor,
            fy=factor,
            interpolation=cv2.INTER_CUBIC,
        )
        imagen_filtrada = cv2.bilateralFilter(imagen_escalada, 9, 75, 75)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        imagen_contraste = clahe.apply(imagen_filtrada)

        imagen_invertida = cv2.bitwise_not(imagen_contraste)
        _, imagen_binaria_temp = cv2.threshold(
            imagen_invertida, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        coords = np.column_stack(np.where(imagen_binaria_temp > 0))
        if coords.size > 0:
            angulo = cv2.minAreaRect(coords)[-1]
            if angulo < -45:
                angulo = -(90 + angulo)
            else:
                angulo = -angulo
            if 0.5 < abs(angulo) < 15:
                alto, ancho = imagen_contraste.shape[:2]
                centro = (ancho // 2, alto // 2)
                M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
                imagen_contraste = cv2.warpAffine(
                    imagen_contraste,
                    M,
                    (ancho, alto),
                    flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )
        return imagen_contraste

    # Construye todas las variantes de preprocesado para OCR.
    def construir_versiones(self, imagen_bgr: np.ndarray) -> list[tuple[str, np.ndarray]]:
        """Devuelve lista de imagenes preprocesadas con nombre."""
        imagen_orientada = self.orientar_vertical_si_horizontal(imagen_bgr)
        return [
            (
                "Metodo 1: Escalado + Binarizacion",
                self.preprocesar_escalado_y_binarizacion_adaptativa(imagen_orientada),
            ),
            ("Metodo 2: CLAHE agresivo", self.preprocesar_clahe_agresivo(imagen_orientada)),
            ("Metodo 3: Otsu", self.preprocesar_otsu(imagen_orientada)),
            (
                "Metodo 4: Invertir si fondo oscuro",
                self.preprocesar_invertir_si_fondo_oscuro(imagen_orientada),
            ),
            (
                "Metodo 5: Foto movil (bilateral+CLAHE+deskew)",
                self.preprocesar_foto_movil(imagen_orientada),
            ),
        ]
