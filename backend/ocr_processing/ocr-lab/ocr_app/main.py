from __future__ import annotations

import argparse
import os
import sys
from typing import Any

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

RUTA_IMAGEN_HARDCODEADA = (
    "/home/adri/dev/github/manager-finance/backend/ocr_processing/ocr-lab/merc.jpg"
)


def _imprimir_resultados_consola(datos: dict[str, Any]) -> None:
    # TODO_REMOVE_CLI: salida visual temporal para pruebas manuales.
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
    # TODO_REMOVE_CLI: cuando se integre como servicio/API, eliminar argparse.
    parser = argparse.ArgumentParser(description="OCR + parsing de tickets/facturas.")
    parser.add_argument(
        "--formato",
        choices=["dict", "tsv", "productos-json"],
        default="dict",
        help="Formato de salida del parseo.",
    )
    return parser.parse_args(argv[1:])


def _cargar_imagen_desde_ruta() -> Any:
    """Carga la imagen de trabajo desde ruta hardcodeada."""
    imagen = cv2.imread(RUTA_IMAGEN_HARDCODEADA)
    if imagen is None:
        raise RuntimeError(
            f"❌ No se pudo cargar la imagen. Ruta intentada: {RUTA_IMAGEN_HARDCODEADA}"
        )
    return imagen


def procesar_ticket() -> dict[str, Any]:
    """Ejecuta OCR + parsing y devuelve un diccionario estructurado."""
    config = OCRConfig(ruta_imagen=RUTA_IMAGEN_HARDCODEADA)
    imagen_original = _cargar_imagen_desde_ruta()
    ocr = OCREngine(config)
    lineas_detectadas = ocr.ejecutar(imagen_original)
    parser = TicketParser()
    return parser.parsear(lineas_detectadas)


def main(argv: list[str]) -> dict[str, Any] | str:
    # TODO_REMOVE_CLI: punto de entrada temporal para uso por consola.
    argumentos = _parsear_argumentos(argv)
    datos = procesar_ticket()

    if argumentos.formato == "tsv":
        salida_tsv = export_tsv(datos)
        print(salida_tsv)
        return salida_tsv

    if argumentos.formato == "productos-json":
        salida_json = export_productos_json(datos)
        print(salida_json)
        return salida_json

    _imprimir_resultados_consola(datos)

    return datos


if __name__ == "__main__":
    main(sys.argv)
