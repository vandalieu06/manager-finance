from __future__ import annotations

from typing import List, Tuple

import cv2
import easyocr

from .config import OCRConfig
from .preprocess import Preprocessor


class OCREngine:
    """Orquesta preprocesado y OCR multi-estrategia."""
    # Inicializa el motor OCR con preprocesado y lector.
    def __init__(self, config: OCRConfig) -> None:
        """Crea el motor OCR y carga el lector una sola vez."""
        self.config = config
        self.preprocessor = Preprocessor(config)
        self.lector = easyocr.Reader(config.lenguajes_ocr, gpu=config.usa_gpu)

    # Ejecuta OCR sobre una imagen preprocesada.
    def _ejecutar_ocr(self, imagen, nombre_estrategia: str) -> List[Tuple[str, float]]:
        """Devuelve lineas y confianza para una estrategia concreta."""
        print(f"\n>>> Probando {nombre_estrategia}...")
        resultados = self.lector.readtext(
            imagen,
            detail=1,
            paragraph=False,
            decoder="greedy",
            batch_size=4,
        )
        lineas_validas: List[Tuple[str, float]] = []
        for _, texto, confianza in resultados:
            if texto and texto.strip() and float(confianza) >= self.config.umbral_min_confianza:
                texto_limpio = " ".join(texto.split())
                lineas_validas.append((texto_limpio, float(confianza)))
        print(
            f"    -> Detectadas {len(lineas_validas)} lineas con confianza >= {self.config.umbral_min_confianza}"
        )
        return lineas_validas

    # Calcula puntuacion combinada por cantidad y confianza.
    def _puntuacion(self, resultado: Tuple[str, List[Tuple[str, float]]]) -> float:
        """Calcula una puntuacion para elegir la mejor estrategia."""
        _, lineas = resultado
        if not lineas:
            return 0.0
        lineas_significativas = [t for t, _ in lineas if len(t.strip()) > 3]
        confianza_media = sum(c for _, c in lineas) / len(lineas)
        return len(lineas_significativas) * 0.7 + confianza_media * 30

    # Reintenta OCR agrupando por parrafos cuando hay solo caracteres sueltos.
    def _reintentar_con_paragraph(
        self, versiones: List[Tuple[str, object]]
    ) -> List[str]:
        """Reintenta OCR con paragraph=True si el texto es muy pobre."""
        print(
            "\n⚠️  Solo se detectaron caracteres sueltos. Reintentando con paragraph=True..."
        )
        _, imagen_mas_nitida = max(
            versiones, key=lambda x: cv2.Laplacian(x[1], cv2.CV_64F).var()
        )
        resultados = self.lector.readtext(
            imagen_mas_nitida,
            detail=1,
            paragraph=True,
            decoder="beamsearch",
        )
        lineas: List[str] = []
        for resultado in resultados:
            if len(resultado) == 3:
                _, texto, confianza = resultado
            elif len(resultado) == 2:
                _, texto = resultado
                confianza = 1.0
            else:
                continue
            if texto and texto.strip() and float(confianza) >= self.config.umbral_min_confianza:
                lineas.append(" ".join(texto.split()))
        return lineas

    # Ejecuta OCR multi-estrategia y devuelve lineas de texto.
    def ejecutar(self, imagen_bgr) -> List[str]:
        """Ejecuta OCR con varias estrategias y retorna el mejor texto."""
        versiones = self.preprocessor.construir_versiones(imagen_bgr)
        for indice, (_, imagen) in enumerate(versiones, start=1):
            cv2.imwrite(f"{self.config.prefijo_debug_preprocesado}{indice}.png", imagen)

        print("\n=== PROBANDO MULTIPLES ESTRATEGIAS DE OCR ===")

        resultados_por_metodo: List[Tuple[str, List[Tuple[str, float]]]] = []
        for nombre, imagen_preprocesada in versiones:
            lineas = self._ejecutar_ocr(imagen_preprocesada, nombre)
            resultados_por_metodo.append((nombre, lineas))

        mejor_metodo, mejor_resultado = max(resultados_por_metodo, key=self._puntuacion)
        print(f"\n✓ MEJOR METODO: {mejor_metodo} ({len(mejor_resultado)} lineas)")

        lineas_texto = [texto for texto, _ in mejor_resultado]
        if lineas_texto and all(len(linea) <= 3 for linea in lineas_texto):
            lineas_texto = self._reintentar_con_paragraph(versiones)
        return lineas_texto
