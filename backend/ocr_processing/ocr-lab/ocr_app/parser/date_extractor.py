import re
from datetime import datetime


class DateExtractor:
    """Extrae fecha/hora del ticket con heuristicas tolerantes a OCR."""

    def extract_date(self, texto_crudo):
        patrones_fecha_regex = [
            r"\b(\d{2}[-/\.]\d{2}[-/\.]\d{2,4})\b",
            r"\b(\d{1,2}\s+(?:ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC)[A-Z]*\s+\d{2,4})\b",
            r"\b(\d{4}-\d{2})\b",
            r"\b(\d{2})(\d{2})(\d{2,4})\b",
        ]

        for patron_fecha in patrones_fecha_regex[:2]:
            coincidencia_fecha = re.search(patron_fecha, texto_crudo, re.IGNORECASE)
            if coincidencia_fecha:
                return coincidencia_fecha.group(1)

        coincidencia_ano_mes = re.search(patrones_fecha_regex[2], texto_crudo)
        if coincidencia_ano_mes:
            texto_fecha_detectado = coincidencia_ano_mes.group(1)
            if len(texto_fecha_detectado) >= 5:
                return (
                    f"{texto_fecha_detectado[:2]}-"
                    f"{texto_fecha_detectado[2:4]}-"
                    f"{texto_fecha_detectado[5:]}"
                )
            return texto_fecha_detectado
        return None

    def extract_datetime_by_context(self, ocr_lines):
        grupos_keywords_priorizados = [
            ["FECHA DE FACTURA", "FECHA DE COMPRA", "FECHA FACTURA"],
            ["FECHA DE PAGO", "FECHA PAGO", "FECHA DE ENTREGA"],
            ["DATA", "TICKET", "FECHA", "HORA"],
        ]

        for keywords_de_contexto in grupos_keywords_priorizados:
            for indice_linea_contexto, texto_linea_contexto in enumerate(ocr_lines):
                if not any(
                    keyword_contexto in texto_linea_contexto.upper()
                    for keyword_contexto in keywords_de_contexto
                ):
                    continue

                texto_ventana_contexto = " ".join(
                    ocr_lines[indice_linea_contexto : indice_linea_contexto + 6]
                )
                fecha_detectada = self.extract_date(texto_ventana_contexto)
                coincidencia_hora = re.search(
                    r"\b(\d{1,2}:\d{2})\b", texto_ventana_contexto
                )

                if fecha_detectada and coincidencia_hora:
                    return f"{fecha_detectada} {coincidencia_hora.group(1)}"
                if fecha_detectada:
                    return fecha_detectada

                coincidencia_fecha_corta = re.search(
                    r"\b(\d{2}[-/\.]\d{2})\b", texto_ventana_contexto
                )
                if coincidencia_fecha_corta:
                    return coincidencia_fecha_corta.group(1)

        return None

    def normalize_iso_datetime(self, texto_fecha_hora_crudo):
        if not texto_fecha_hora_crudo:
            return ""

        formatos_fecha_hora_aceptados = [
            "%d/%m/%Y %H:%M",
            "%d-%m-%Y %H:%M",
            "%d.%m.%Y %H:%M",
            "%d/%m/%y %H:%M",
            "%d-%m-%y %H:%M",
            "%d.%m.%y %H:%M",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%d/%m/%y",
            "%d-%m-%y",
            "%d.%m.%y",
        ]

        for formato_fecha_hora in formatos_fecha_hora_aceptados:
            try:
                fecha_hora_parseada = datetime.strptime(
                    texto_fecha_hora_crudo.strip(), formato_fecha_hora
                )
                return fecha_hora_parseada.isoformat(timespec="minutes")
            except ValueError:
                continue
        return ""
