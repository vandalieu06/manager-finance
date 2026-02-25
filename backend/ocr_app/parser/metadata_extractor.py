import re

from .text_utils import has_letters


class MetadataExtractor:
    """Extrae metadatos de cabecera y fiscalidad/pagos."""

    def __init__(self, line_classifier, price_extractor_service, normalize_number_function):
        self.line_classifier = line_classifier
        self.price_extractor_service = price_extractor_service
        self.normalize_number_function = normalize_number_function

    def extract_cif(self, ocr_lines):
        patrones_cif = [
            r"\b([A-Z]\d{8})\b",
            r"\b(\d{8}[A-Z])\b",
            r"\b([A-Z]\d{7}[A-Z0-9])\b",
        ]

        for texto_linea_candidata in ocr_lines[:20]:
            for patron_cif in patrones_cif:
                coincidencia_cif = re.search(patron_cif, texto_linea_candidata.upper())
                if coincidencia_cif:
                    return coincidencia_cif.group(1)
        return ""

    def extract_phone(self, ocr_lines):
        for texto_linea_candidata in ocr_lines[:25]:
            coincidencia_telefono = re.search(
                r"(?:\+34\s*)?(\d(?:[\s.-]?\d){8})", texto_linea_candidata
            )
            if coincidencia_telefono:
                return re.sub(r"\D", "", coincidencia_telefono.group(1))
        return ""

    def extract_op(self, ocr_lines):
        for texto_linea_candidata in ocr_lines:
            coincidencia_codigo_operacion = re.search(
                r"\bOP\s*[:\-]?\s*([A-Z0-9]+)\b", texto_linea_candidata.upper()
            )
            if coincidencia_codigo_operacion:
                return coincidencia_codigo_operacion.group(1)
        return ""

    def extract_ticket_id(self, ocr_lines):
        patrones_regex_ticket_id = [
            r"\b(?:TICKET|FACTURA)\s*(?:N[Oº°]\s*)?[:\-]?\s*([A-Z0-9\-]{4,})\b",
            r"\bN[Oº°]\s*[:\-]?\s*([A-Z0-9\-]{5,})\b",
        ]

        for texto_linea_candidata in ocr_lines:
            texto_linea_mayus = texto_linea_candidata.upper()
            for patron_ticket_id in patrones_regex_ticket_id:
                coincidencia_ticket_id = re.search(patron_ticket_id, texto_linea_mayus)
                if coincidencia_ticket_id:
                    return coincidencia_ticket_id.group(1)
        return ""

    def extract_address_postal(self, ocr_lines):
        linea_direccion_extraida = ""
        linea_postal_ciudad_extraida = ""

        for texto_linea_candidata in ocr_lines[:25]:
            if (
                not linea_direccion_extraida
                and self.line_classifier.is_address_line(texto_linea_candidata)
            ):
                linea_direccion_extraida = texto_linea_candidata.strip()
            if (
                not linea_postal_ciudad_extraida
                and re.search(r"\b\d{5}\b", texto_linea_candidata)
                and has_letters(texto_linea_candidata)
            ):
                linea_postal_ciudad_extraida = texto_linea_candidata.strip()
            if linea_direccion_extraida and linea_postal_ciudad_extraida:
                break

        return linea_direccion_extraida, linea_postal_ciudad_extraida

    def extract_vat(self, ocr_lines):
        filas_iva = []

        for texto_linea_candidata in ocr_lines:
            if "IVA" not in texto_linea_candidata.upper():
                continue

            coincidencia_tasa_iva = re.search(
                r"(\d{1,2}(?:[.,]\d{1,2})?)\s*%", texto_linea_candidata
            )
            tokens_numericos_normalizados = [
                valor_token_normalizado
                for valor_token_normalizado in (
                    self.normalize_number_function(token_numerico_crudo)
                    for token_numerico_crudo in re.findall(
                        r"-?\d+(?:[.,]\d{2,3})", texto_linea_candidata
                    )
                )
                if valor_token_normalizado is not None
            ]

            if len(tokens_numericos_normalizados) < 2:
                continue

            importe_base_iva = tokens_numericos_normalizados[-2]
            importe_cuota_iva = tokens_numericos_normalizados[-1]

            if importe_base_iva <= 0 or importe_cuota_iva < 0:
                continue

            tasa_iva_normalizada = (
                self.normalize_number_function(coincidencia_tasa_iva.group(1))
                if coincidencia_tasa_iva
                else None
            )
            filas_iva.append(
                {
                    "rate": round(tasa_iva_normalizada, 2)
                    if tasa_iva_normalizada is not None
                    else 0.0,
                    "base": round(importe_base_iva, 2),
                    "amount": round(importe_cuota_iva, 2),
                }
            )

        return filas_iva

    def extract_payments(self, ocr_lines):
        filas_pago_extraidas = []

        for texto_linea_candidata in ocr_lines:
            if not self.line_classifier.is_payment_line(texto_linea_candidata):
                continue

            candidatos_importe_linea = self.price_extractor_service.extract_prices(
                texto_linea_candidata
            )
            metodo_pago = self._infer_payment_method(texto_linea_candidata)
            if metodo_pago and candidatos_importe_linea:
                filas_pago_extraidas.append(
                    {"method": metodo_pago, "amount": round(max(candidatos_importe_linea), 2)}
                )

        return filas_pago_extraidas

    @staticmethod
    def adjust_total_with_vat(importe_total_base, filas_iva):
        if not filas_iva:
            return round(importe_total_base, 2) if importe_total_base is not None else None

        suma_bases_iva = round(sum(fila_iva.get("base", 0.0) for fila_iva in filas_iva), 2)
        suma_cuotas_iva = round(
            sum(fila_iva.get("amount", 0.0) for fila_iva in filas_iva), 2
        )

        if suma_bases_iva <= 0 or suma_cuotas_iva <= 0:
            return round(importe_total_base, 2) if importe_total_base is not None else None

        total_ajustado_con_iva = round(suma_bases_iva + suma_cuotas_iva, 2)
        if importe_total_base is None:
            return total_ajustado_con_iva

        total_base_redondeado = round(importe_total_base, 2)
        if abs(total_base_redondeado - suma_bases_iva) <= 0.02:
            return total_ajustado_con_iva
        return total_base_redondeado

    @staticmethod
    def _infer_payment_method(texto_linea_pago):
        texto_linea_mayus = texto_linea_pago.upper()
        if "EFECT" in texto_linea_mayus:
            return "EFECTIVO"
        if any(
            token_pago in texto_linea_mayus
            for token_pago in ["TARJETA", "TARGETA", "VISA", "MASTERCARD", "MAESTRO"]
        ):
            return "TARJETA"
        return ""
