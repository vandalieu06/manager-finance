from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto extraido del ticket."""

    nombre = None
    precio_total = None
    cantidad = None
    precio_unitario = None

    def to_dict(self):
        """Convierte el producto a diccionario."""
        return {
            "nombre": self.nombre,
            "precio_total": self.precio_total,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
        }
