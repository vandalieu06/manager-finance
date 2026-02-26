from __future__ import annotations

import cv2
import easyocr

from ocr.preprocess import Preprocessor


class OCREngine:
    """Orquesta preprocesado y OCR multi-estrategia."""

    # Inicializa el motor OCR con preprocesado y lector.
    def __init__(self, config):
        """Crea el motor OCR y carga el lector una sola vez."""
        self.config = config
        self.preprocessor = Preprocessor(config)
        self.lector = easyocr.Reader(config.lenguajes_ocr, gpu=config.usa_gpu)

    # Ejecuta OCR sobre una imagen preprocesada.
    def _ejecutar_ocr(self, imagen_preprocesada, nombre_estrategia):
        """Devuelve lineas y confianza para una estrategia concreta."""

        resultados_ocr = self.lector.readtext(
            imagen_preprocesada,
            detail=1,
            paragraph=False,
            decoder="greedy",
            batch_size=4,
        )
        lineas_filtradas_con_confianza = []
        for _, texto_detectado, confianza in resultados_ocr:
            if (
                texto_detectado
                and texto_detectado.strip()
                and float(confianza) >= self.config.umbral_min_confianza
            ):
                texto_normalizado = " ".join(texto_detectado.split())
                lineas_filtradas_con_confianza.append(
                    (texto_normalizado, float(confianza))
                )
        return lineas_filtradas_con_confianza

    # Calcula puntuacion combinada por cantidad y confianza.
    def _puntuacion(self, resultado_metodo):
        """Calcula una puntuacion para elegir la mejor estrategia."""
        _, lineas_con_confianza = resultado_metodo
        if not lineas_con_confianza:
            return 0.0
        lineas_significativas = [
            texto for texto, _ in lineas_con_confianza if len(texto.strip()) > 3
        ]
        confianza_media = sum(c for _, c in lineas_con_confianza) / len(
            lineas_con_confianza
        )
        return len(lineas_significativas) * 0.7 + confianza_media * 30

    # Reintenta OCR agrupando por parrafos cuando hay solo caracteres sueltos.
    def _reintentar_con_paragraph(self, versiones_preprocesadas):
        """Reintenta OCR con paragraph=True si el texto es muy pobre."""
        _, imagen_con_mejor_nitidez = max(
            versiones_preprocesadas, key=lambda x: cv2.Laplacian(x[1], cv2.CV_64F).var()
        )
        resultados_ocr = self.lector.readtext(
            imagen_con_mejor_nitidez,
            detail=1,
            paragraph=True,
            decoder="beamsearch",
        )
        lineas_detectadas = []

        for bloque_resultado in resultados_ocr:
            if len(bloque_resultado) == 3:
                _, texto_detectado, confianza = bloque_resultado
            elif len(bloque_resultado) == 2:
                _, texto_detectado = bloque_resultado
                confianza = 1.0
            else:
                continue
            if (
                texto_detectado
                and texto_detectado.strip()
                and float(confianza) >= self.config.umbral_min_confianza
            ):
                lineas_detectadas.append(" ".join(texto_detectado.split()))
        return lineas_detectadas

    # Ejecuta OCR multi-estrategia y devuelve lineas de texto.
    def ejecutar(self, imagen_bgr):
        """Ejecuta OCR con varias estrategias y retorna el mejor texto."""
        versiones_preprocesadas = self.preprocessor.construir_versiones(imagen_bgr)

        resultados_por_estrategia = []
        for nombre_estrategia, imagen_preprocesada in versiones_preprocesadas:
            lineas_extraidas = self._ejecutar_ocr(
                imagen_preprocesada, nombre_estrategia
            )
            resultados_por_estrategia.append((nombre_estrategia, lineas_extraidas))

        mejor_estrategia, lineas_mejor_estrategia = max(
            resultados_por_estrategia, key=self._puntuacion
        )

        lineas_texto_finales = [texto for texto, _ in lineas_mejor_estrategia]
        if lineas_texto_finales and all(
            len(linea) <= 3 for linea in lineas_texto_finales
        ):
            lineas_texto_finales = self._reintentar_con_paragraph(
                versiones_preprocesadas
            )
        return lineas_texto_finales
