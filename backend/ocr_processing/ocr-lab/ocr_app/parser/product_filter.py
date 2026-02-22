import re
from difflib import SequenceMatcher

from ..models import Producto


class ProductFilter:
    """Limpia falsos positivos de productos derivados del nombre del comercio."""

    def filter_by_store(self, productos_candidatos, nombre_comercio_detectado):
        if not nombre_comercio_detectado:
            return productos_candidatos

        nombre_comercio_normalizado = re.sub(
            r"[^A-Za-zÀ-ÿ\s]", "", nombre_comercio_detectado
        ).upper().strip()
        palabras_comercio_normalizadas = set(nombre_comercio_normalizado.split())

        productos_filtrados = []
        for producto_candidato in productos_candidatos:
            nombre_producto_normalizado = re.sub(
                r"[^A-Za-zÀ-ÿ\s]", "", producto_candidato.nombre
            ).upper().strip()
            score_similitud_nombre_completo = SequenceMatcher(
                None, nombre_producto_normalizado, nombre_comercio_normalizado
            ).ratio()
            if score_similitud_nombre_completo >= 0.6:
                continue

            palabras_nombre_producto = nombre_producto_normalizado.split()
            for cantidad_palabras_prefijo in range(
                min(3, len(palabras_nombre_producto)), 0, -1
            ):
                prefijo_nombre_producto = " ".join(
                    palabras_nombre_producto[:cantidad_palabras_prefijo]
                )
                score_similitud_prefijo = SequenceMatcher(
                    None, prefijo_nombre_producto, nombre_comercio_normalizado
                ).ratio()
                palabras_prefijo_coinciden_comercio = (
                    cantidad_palabras_prefijo <= 2
                    and all(
                        any(
                            SequenceMatcher(None, palabra_producto, palabra_comercio).ratio() > 0.7
                            for palabra_comercio in palabras_comercio_normalizadas
                        )
                        for palabra_producto in palabras_nombre_producto[:cantidad_palabras_prefijo]
                    )
                )

                if score_similitud_prefijo >= 0.75 or palabras_prefijo_coinciden_comercio:
                    nombre_limpio_sin_prefijo_comercio = " ".join(
                        palabras_nombre_producto[cantidad_palabras_prefijo:]
                    ).strip()
                    if nombre_limpio_sin_prefijo_comercio:
                        producto_candidato = Producto(
                            nombre=nombre_limpio_sin_prefijo_comercio,
                            precio_total=producto_candidato.precio_total,
                            cantidad=producto_candidato.cantidad,
                        )
                    break

            nombre_producto_sin_puntuacion_bordes = re.sub(
                r"^[<>.,;:!?\-]+\s*|\s*[<>.,;:!?\-]+$",
                "",
                producto_candidato.nombre,
            ).strip()
            if nombre_producto_sin_puntuacion_bordes:
                producto_candidato = Producto(
                    nombre=nombre_producto_sin_puntuacion_bordes,
                    precio_total=producto_candidato.precio_total,
                    cantidad=producto_candidato.cantidad,
                )

            if producto_candidato.nombre:
                productos_filtrados.append(producto_candidato)

        return productos_filtrados
