import re
from difflib import SequenceMatcher

from ..models import Producto


class ProductFilter:
    """Limpia falsos positivos de productos derivados del nombre del comercio."""

    def filter_by_store(self, extracted_products, detected_store):
        if not detected_store:
            return extracted_products

        normalized_store_name = re.sub(r"[^A-Za-zÀ-ÿ\s]", "", detected_store).upper().strip()
        store_name_words = set(normalized_store_name.split())

        filtered_products = []
        for extracted_product in extracted_products:
            normalized_product_name = re.sub(
                r"[^A-Za-zÀ-ÿ\s]", "", extracted_product.nombre
            ).upper().strip()
            full_name_similarity = SequenceMatcher(
                None, normalized_product_name, normalized_store_name
            ).ratio()
            if full_name_similarity >= 0.6:
                continue

            product_name_words = normalized_product_name.split()
            for prefix_word_count in range(min(3, len(product_name_words)), 0, -1):
                product_name_prefix = " ".join(product_name_words[:prefix_word_count])
                prefix_similarity = SequenceMatcher(
                    None, product_name_prefix, normalized_store_name
                ).ratio()
                prefix_words_match_store = (
                    prefix_word_count <= 2
                    and all(
                        any(
                            SequenceMatcher(None, product_word, store_word).ratio() > 0.7
                            for store_word in store_name_words
                        )
                        for product_word in product_name_words[:prefix_word_count]
                    )
                )

                if prefix_similarity >= 0.75 or prefix_words_match_store:
                    cleaned_name_without_store_prefix = " ".join(
                        product_name_words[prefix_word_count:]
                    ).strip()
                    if cleaned_name_without_store_prefix:
                        extracted_product = Producto(
                            nombre=cleaned_name_without_store_prefix,
                            precio_total=extracted_product.precio_total,
                            cantidad=extracted_product.cantidad,
                        )
                    break

            product_name_without_punctuation_edges = re.sub(
                r"^[<>.,;:!?\-]+\s*|\s*[<>.,;:!?\-]+$",
                "",
                extracted_product.nombre,
            ).strip()
            if product_name_without_punctuation_edges:
                extracted_product = Producto(
                    nombre=product_name_without_punctuation_edges,
                    precio_total=extracted_product.precio_total,
                    cantidad=extracted_product.cantidad,
                )

            if extracted_product.nombre:
                filtered_products.append(extracted_product)

        return filtered_products
