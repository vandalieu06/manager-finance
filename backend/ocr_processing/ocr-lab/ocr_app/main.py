from __future__ import annotations

import os
import sys

import cv2

from .config import OCRConfig
from .ocr_engine import OCREngine
from .parsing import TicketParser


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


def main(argv: list[str]) -> dict:
    # Punto de entrada principal para ejecutar OCR + parsing.
    """Ejecuta el flujo completo OCR + parsing desde CLI."""
    ruta_imagen = argv[1] if len(argv) > 1 else "ticket2.jpg"
    config = OCRConfig(ruta_imagen=ruta_imagen)

    print("=" * 60)
    print("OCR MEJORADO PARA TICKETS")
    print("=" * 60)
    print(f"CWD: {os.getcwd()}")
    print(f"Leyendo: {os.path.abspath(config.ruta_imagen)}")

    imagen_original = cv2.imread(config.ruta_imagen)
    if imagen_original is None:
        raise RuntimeError("❌ No se pudo cargar la imagen. Revisa la ruta.")

    print(f"Tamano original: {imagen_original.shape}")

    ocr = OCREngine(config)
    lineas_detectadas = ocr.ejecutar(imagen_original)

    print("\n" + "=" * 60)
    print("TEXTO DETECTADO")
    print("=" * 60)
    for indice, linea in enumerate(lineas_detectadas, 1):
        print(f"{indice:3d}. {linea}")

    parser = TicketParser()
    datos = parser.parsear(lineas_detectadas)
    imprimir_resultados(datos)

    if not datos["total"]:
        print("\n⚠️  No se pudo extraer el total. Revisa manualmente el texto detectado.")

    return datos


if __name__ == "__main__":
    main(sys.argv)
