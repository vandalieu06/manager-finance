from typing import List

from core.entities.producto import Producto
from core.ports.llm_port import LLMPort

import requests



class OllamaAdapter(LLMPort):
    """Adaptador que implementa LLMPort usando Ollama."""

    def __init__(self, model_name: str = "llama3.2:1b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def extract_products(self, ocr_text: str) -> List[Producto]:
        """Extrae productos del texto OCR usando Ollama."""

        prompt = self._build_prompt(ocr_text)

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return self._parse_llm_response(result.get("response", "[]"))
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error comunicando con Ollama: {e}")

    def _build_prompt(self, ocr_text: str) -> str:
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

    def _parse_llm_response(self, response: str) -> List[Producto]:
        import json
        import re

        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(response)

            productos = []
            for item in data:
                producto = Producto(
                    nombre=item.get("nombre", ""),
                    precio_total=self._parse_float(item.get("precio_total")),
                    cantidad=self._parse_float(item.get("cantidad")),
                    precio_unitario=self._parse_float(item.get("precio_unitario"))
                )
                if producto.nombre and producto.precio_total:
                    productos.append(producto)
            return productos
        except (json.JSONDecodeError, ValueError) as e:
            raise RuntimeError(f"Error parseando respuesta de LLM: {e}")

    def _parse_float(self, value) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
