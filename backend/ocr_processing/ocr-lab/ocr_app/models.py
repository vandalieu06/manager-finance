from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    """Representa un producto extraido del ticket."""
    nombre: str
    precio_total: Optional[float] = None
    cantidad: Optional[float] = None
