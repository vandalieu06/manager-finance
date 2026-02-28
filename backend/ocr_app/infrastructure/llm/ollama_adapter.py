import json
import logging
import re
from datetime import datetime

import requests

from core.entities.producto import Producto
from core.ports.llm_port import LLMPort

_logger = logging.getLogger(__name__)

time_init = datetime.now()
_logger.info(f'Se ha ejecutado el adapatador de ollama a las {time_init}')


class OllamaAdapter(LLMPort):
    """Adaptador que implementa LLMPort usando Ollama."""

    def __init__(self, model_name='llama3.2:1b', base_url='http://localhost:11434'):
        self.model_name = model_name
        self.base_url = base_url

    def extract_products(self, ocr_text):
        """Extrae productos del texto OCR usando Ollama."""
        _logger.info(f"OllamaAdapter: Recibido texto OCR ({len(ocr_text)} caracteres)")

        prompt = self._build_prompt(ocr_text)
        _logger.info(f"OllamaAdapter: Prompt construido ({len(prompt)} caracteres)")

        try:
            _logger.info(f"OllamaAdapter: Enviando solicitud a {self.base_url}/api/generate con modelo {self.model_name}")
            response = requests.post(
                f'{self.base_url}/api/generate',
                json={
                    'model': self.model_name,
                    'prompt': prompt,
                    'stream': False,
                    'format': 'json',
                },
                timeout=600,
            )
            _logger.info(f"OllamaAdapter: Respuesta recibida. Status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            _logger.info("OllamaAdapter: Parseando respuesta del LLM...")
            return self._parse_llm_response(result.get('response', '[]'))
        except requests.exceptions.RequestException as e:
            _logger.exception("OllamaAdapter: Error comunicando con Ollama")
            raise RuntimeError(f'Error comunicando con Ollama: {e}')

    def _build_prompt(self, ocr_text):
        return f"""Eres un asistente especializado en extraer información de tickets de compra en español.
                Del siguiente texto extraído de un ticket, extrae todos los productos comprados.
                Para cada producto proporciona:
                - nombre: nombre del producto
                - precio_total: precio total del producto (sin IVA)
                - cantidad: número de unidades (si aplica, si no usar 1)
                - precio_unitario: precio por unidad (si cantidad > 1)

                Responde ÚNICAMENTE con un array JSON válido, sin texto adicional.

                Texto del ticket:
                {ocr_text}

                Responde con el JSON:"""

    def _parse_llm_response(self, response):
        _logger.info(f"OllamaAdapter: Respuesta cruda del LLM (primeros 500 chars): {response[:500]}")
        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response)

            productos = []
            for item in data:
                producto = Producto(
                    item.get('nombre'),
                    self._parse_float(item.get('precio_total')),
                    self._parse_float(item.get('cantidad')),
                    self._parse_float(item.get('precio_unitario')),
                )
                if producto.nombre and producto.precio_total:
                    productos.append(producto)
            return productos
        except (json.JSONDecodeError, ValueError) as e:
            _logger.warning(f"OllamaAdapter: Error con json estándar, intentando con ast.literal_eval: {e}")
            try:
                import ast
                data = ast.literal_eval(response)
                productos = []
                for item in data:
                    producto = Producto(
                        item.get('nombre'),
                        self._parse_float(item.get('precio_total')),
                        self._parse_float(item.get('cantidad')),
                        self._parse_float(item.get('precio_unitario')),
                    )
                    if producto.nombre and producto.precio_total:
                        productos.append(producto)
                return productos
            except Exception as e2:
                raise RuntimeError(f'Error parseando respuesta de LLM: {e}')

    def _parse_float(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
