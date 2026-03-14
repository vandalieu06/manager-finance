import json
import logging
import os
from datetime import datetime

from openai import OpenAI

from core.entities.producto import Producto
from core.ports.llm_port import LLMPort

_logger = logging.getLogger(__name__)

time_init = datetime.now()
_logger.info(f'Se ha ejecutado el adapatador de ollama a las {time_init}')


class OllamaAdapter(LLMPort):
    """Adaptador que implementa LLMPort usando Ollama."""

    def __init__(self):
        self.model = os.getenv('MODEL_AI', 'sample')
        self.base_url = os.getenv('OPENROUTER_URL_API', 'sample')
        self.key = os.getenv('OPENROUTER_KEY', 'sample')

    def extract_products(self, ocr_text):
        """Extrae productos del texto OCR usando OpenRouter"""

        system_instructions = (
            'Eres un extractor de datos experto. Tu objetivo es convertir texto de tickets en JSON.\n'
            'Reglas estrictas:\n'
            '1. Extrae: nombre, precio_total (float), cantidad (int), precio_unitario (float).\n'
            '2. Si el precio unitario no aparece, calcúlalo como precio_total / cantidad.\n'
            '3. No incluyas impuestos (IVA) en el precio si puedes identificarlo.\n'
            '4. Responde EXCLUSIVAMENTE con el objeto JSON, sin Markdown, sin explicaciones.'
        )
        user_input = f'Texto del ticket:\n{ocr_text}\n\nGenera el JSON siguiendo el esquema solicitado.'

        try:
            client = OpenAI(base_url=self.base_url, api_key=self.key)

            response = client.chat.completions.create(
                model=self.model,
                stream=False,
                messages=[
                    {'role': 'system', 'content': system_instructions},
                    {
                        'role': 'user',
                        'content': user_input,
                    },
                ],
                response_format={'type': 'json_object'},
            )

            raw_res = response.choices[0].message.content

            return self._parse_llm_response(raw_res)

        except Exception as e:
            _logger.error(f'Error en la extracción de productos: {e}')
            return []

    def _parse_llm_response(self, raw_response):
        """Convierte el string JSON del LLM en una lista de entidades Producto."""

        if not raw_response:
            return []

        try:
            clean_res = raw_response.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_res)

            items = []

            if isinstance(data, dict):
                items = (
                    data.get('productos', []) if 'productos' in data else data.values()
                )
            elif isinstance(data, list):
                items = data

            productos_validados = []

            for item in items:
                if not isinstance(item, dict):
                    continue

                nuevo_producto = Producto(
                    nombre=str(item.get('nombre', 'Desconocido')),
                    precio_total=self._parse_float(item.get('precio_total')),
                    cantidad=self._parse_float(item.get('cantidad', 1)),
                    precio_unitario=self._parse_float(item.get('precio_unitario')),
                )

                if nuevo_producto.nombre and nuevo_producto.precio_total is not None:
                    productos_validados.append(nuevo_producto)

            return productos_validados

        except json.JSONDecodeError as e:
            _logger.error(f'Error al decodificar JSON del LLM: {e}')
            return []

    def _parse_float(self, value):
        if value is None:
            return None
        try:
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return None
