from __future__ import annotations

import argparse
import os
import sys
from typing import Union

import cv2

if __package__ in {None, ""}:
    # Permite ejecutar como script:
    # python /ruta/proyecto/ocr_app/main.py
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ocr_app.config import OCRConfig
    from ocr_app.ocr import OCREngine
    from ocr_app.parsing import TicketParser, export_productos_json, export_tsv
else:
    from .config import OCRConfig
    from .ocr import OCREngine
    from .parsing import TicketParser, export_productos_json, export_tsv


def imprimir_resultados(datos: dict) -> None:
    # Imprime el resumen de datos extraidos de forma legible.
    """Muestra por consola el resultado del OCR y parsing."""
    print("\n" + "=" * 60)
    print("DATOS EXTRAIDOS")
    print("=" * 60)
    print(f"  Tienda:   {datos['comercio'] or 'No detectada'}")
    print(f"  Fecha:    {datos['fecha'] or 'No detectada'}")
    if datos["total"]:
        print(f"  Total:    {datos['total']} {datos['moneda']}")
    else:
        print("  Total:    No detectado")

    if datos["productos"]:
        print(f"  Productos ({len(datos['productos'])}):")
        for producto in datos["productos"]:
            precio_str = f"{producto.precio_total:.2f} EUR" if producto.precio_total else "?"
            print(f"    - {producto.nombre}  -->  {precio_str}")
    print(f"  Lineas OCR: {datos['num_lineas']}")


def _parsear_argumentos(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OCR + parsing de tickets/facturas.")
    parser.add_argument(
        "ruta_imagen",
        nargs="?",
        default="amazon.jpg",
        help="Ruta de la factura/ticket a procesar.",
    )
    parser.add_argument(
        "--formato",
        choices=["dict", "tsv", "productos-json"],
        default="dict",
        help="Formato de salida del parseo.",
    )
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> Union[dict, str]:
    # Punto de entrada principal para ejecutar OCR + parsing.
    """Ejecuta el flujo completo OCR + parsing desde CLI."""
    argumentos = _parsear_argumentos(argv)
    config = OCRConfig(ruta_imagen=argumentos.ruta_imagen)

    imagen_original = cv2.imread(config.ruta_imagen)
    if imagen_original is None:
        raise RuntimeError("❌ No se pudo cargar la imagen. Revisa la ruta.")

    ocr = OCREngine(config)
    lineas_detectadas = ocr.ejecutar(imagen_original)

    parser = TicketParser()
    datos = parser.parsear(lineas_detectadas)

    if argumentos.formato == "tsv":
        salida_tsv = export_tsv(datos)
        print(salida_tsv)
        return salida_tsv

    if argumentos.formato == "productos-json":
        salida_json = export_productos_json(datos)
        print(salida_json)
        return salida_json

    imprimir_resultados(datos)

    return datos


if __name__ == "__main__":
    main(sys.argv)
