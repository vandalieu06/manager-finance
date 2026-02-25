from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    """Representa un producto extraido del ticket."""
    nombre: str
    precio_total: Optional[float] = None
    cantidad: Optional[float] = None
    precio_unitario: Optional[float] = None

    def to_dict(self) -> dict:
        """Convierte el producto a diccionario."""
        return {
            "nombre": self.nombre,
            "precio_total": self.precio_total,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
        }
