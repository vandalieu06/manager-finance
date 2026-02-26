import re

from ..models import Producto
from .text_utils import has_letters


class ProductExtractor:
    """Extrae productos del bloque central del ticket."""

    def __init__(self, line_classifier, price_extractor_service):
        self.line_classifier = line_classifier
        self.price_extractor_service = price_extractor_service

    def extract(self, ocr_lines):
        productos_extraidos = []
        indice_inicio_bloque_productos = self._detect_products_start(ocr_lines)
        indice_fin_bloque_productos = self._detect_products_end(
            ocr_lines, indice_inicio_bloque_productos
        )

        partes_nombre_producto_en_buffer = []
        precio_total_producto_en_buffer = None

        def guardar_producto_buffer_si_completo():
            nonlocal partes_nombre_producto_en_buffer, precio_total_producto_en_buffer
            if (
                partes_nombre_producto_en_buffer
                and precio_total_producto_en_buffer is not None
                and precio_total_producto_en_buffer > 0
            ):
                nombre_producto_normalizado = self._clean_product_name(
                    " ".join(partes_nombre_producto_en_buffer)
                )
                if len(nombre_producto_normalizado) >= 3:
                    productos_extraidos.append(
                        Producto(
                            nombre=nombre_producto_normalizado,
                            precio_total=precio_total_producto_en_buffer,
                        )
                    )
            partes_nombre_producto_en_buffer = []
            precio_total_producto_en_buffer = None

        for texto_linea_ocr_crudo in ocr_lines[
            indice_inicio_bloque_productos:indice_fin_bloque_productos
        ]:
            texto_linea_normalizado = re.sub(r"\s+", " ", texto_linea_ocr_crudo).strip()
            if not texto_linea_normalizado:
                continue

            if (
                self.line_classifier.is_discard_line(texto_linea_normalizado)
                or self.line_classifier.is_header_line(texto_linea_normalizado)
                or self.line_classifier.is_payment_line(texto_linea_normalizado)
                or self.line_classifier.is_address_line(texto_linea_normalizado)
            ):
                guardar_producto_buffer_si_completo()
                continue

            candidatos_precio_linea = self.price_extractor_service.extract_prices(
                texto_linea_normalizado
            )

            if candidatos_precio_linea:
                candidatos_precio_positivos = [
                    precio_linea
                    for precio_linea in candidatos_precio_linea
                    if precio_linea > 0
                ]
                precio_total_linea_seleccionado = (
                    max(candidatos_precio_positivos)
                    if candidatos_precio_positivos
                    else None
                )

                texto_linea_sin_tokens_precio = re.sub(
                    r"-?\d+[.,]\d{2}", "", texto_linea_normalizado
                )
                texto_linea_sin_tokens_precio = re.sub(
                    r"\s+", " ", texto_linea_sin_tokens_precio
                ).strip()
                texto_linea_sin_tokens_precio = re.sub(
                    r"^[\s\d.,*×xX-]+\s*|\s*[\s\d.,*×xX-]+$",
                    "",
                    texto_linea_sin_tokens_precio,
                ).strip()

                if (
                    texto_linea_sin_tokens_precio
                    and len(texto_linea_sin_tokens_precio) >= 3
                    and has_letters(texto_linea_sin_tokens_precio)
                ):
                    if (
                        partes_nombre_producto_en_buffer
                        and precio_total_producto_en_buffer is not None
                    ):
                        guardar_producto_buffer_si_completo()
                    if partes_nombre_producto_en_buffer:
                        partes_nombre_producto_en_buffer.append(
                            texto_linea_sin_tokens_precio
                        )
                    else:
                        partes_nombre_producto_en_buffer = [
                            texto_linea_sin_tokens_precio
                        ]
                    precio_total_producto_en_buffer = precio_total_linea_seleccionado
                    guardar_producto_buffer_si_completo()
                elif partes_nombre_producto_en_buffer:
                    precio_total_producto_en_buffer = precio_total_linea_seleccionado
                    guardar_producto_buffer_si_completo()
            else:
                if self.line_classifier.is_code_line(texto_linea_normalizado):
                    continue
                if not self.line_classifier.is_product_candidate(
                    texto_linea_normalizado
                ):
                    guardar_producto_buffer_si_completo()
                    continue

                if (
                    partes_nombre_producto_en_buffer
                    and precio_total_producto_en_buffer is not None
                ):
                    guardar_producto_buffer_si_completo()
                partes_nombre_producto_en_buffer.append(texto_linea_normalizado)

        guardar_producto_buffer_si_completo()
        return productos_extraidos

    def _detect_products_start(self, ocr_lines):
        for indice_linea, texto_linea in enumerate(ocr_lines):
            texto_linea_mayus = texto_linea.upper()
            if any(
                keyword_tabla in texto_linea_mayus
                for keyword_tabla in ["DESCRIP", "P.V.P", "PVP", "P.UNIT"]
            ):
                texto_contexto_cercano = " ".join(
                    ocr_lines[max(0, indice_linea - 2) : indice_linea + 6]
                ).upper()
                if any(
                    keyword_contexto in texto_contexto_cercano
                    for keyword_contexto in [
                        "CANT",
                        "PRODUCTO",
                        "TOTAL",
                        "UNITARIO",
                        "P.UNIT",
                        "IMPORT",
                    ]
                ):
                    indice_primera_linea_datos = indice_linea + 1
                    while indice_primera_linea_datos < len(
                        ocr_lines
                    ) and self.line_classifier.is_header_line(
                        ocr_lines[indice_primera_linea_datos]
                    ):
                        indice_primera_linea_datos += 1
                    return indice_primera_linea_datos
            if re.search(r"\bOP:\s*\d", texto_linea_mayus) or re.search(
                r"\bCAIXA\s*:\s*\d", texto_linea_mayus
            ):
                return indice_linea + 1
        return 0

    def _detect_products_end(self, ocr_lines, indice_inicio_productos):
        indice_inicio_escaneo = max(indice_inicio_productos, int(len(ocr_lines) * 0.3))
        for indice_linea in range(indice_inicio_escaneo, len(ocr_lines)):
            texto_linea_compacto = ocr_lines[indice_linea].upper().replace(" ", "")
            texto_contexto_cercano = (
                " ".join(ocr_lines[indice_linea : indice_linea + 3])
                .upper()
                .replace(" ", "")
            )

            if (
                "TIPOIVA" in texto_linea_compacto
                and "BASEIMPONIBLE" in texto_contexto_cercano
            ):
                return indice_linea
            if (
                "DESGLOSSAMENT" in texto_linea_compacto
                or "DESGLOSAMENT" in texto_linea_compacto
            ):
                return indice_linea
            if re.match(r"^\s*TOTAL\b", ocr_lines[indice_linea], re.IGNORECASE):
                return indice_linea
            if self.line_classifier.is_payment_line(ocr_lines[indice_linea]):
                return indice_linea
            if re.match(r"^\s*ARTICLES\s*:", ocr_lines[indice_linea], re.IGNORECASE):
                return indice_linea

        return len(ocr_lines)

    @staticmethod
    def _clean_product_name(texto_nombre_producto_crudo):
        nombre_producto_limpio = texto_nombre_producto_crudo.strip()
        nombre_producto_sin_prefijo_cantidad = re.sub(
            r"^\d+\s+", "", nombre_producto_limpio
        )
        if len(nombre_producto_sin_prefijo_cantidad) >= 3:
            nombre_producto_limpio = nombre_producto_sin_prefijo_cantidad
        return nombre_producto_limpio.upper()
