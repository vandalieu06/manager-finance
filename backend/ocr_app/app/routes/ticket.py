from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import logging

from ..services.ocr_service import OCRService


logger = logging.getLogger(__name__)

ticket_bp = Blueprint("ticket", __name__)

_ocr_service = None


def get_ocr_service():
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service


@ticket_bp.route("/health", methods=["GET"])
def health():
    """Endpoint de salud."""
    return jsonify({"status": "ok"})


@ticket_bp.route("/process-ticket", methods=["POST"])
def process_ticket():
    """Procesa una imagen de ticket y retorna productos extraidos."""
    logger.info("=== INICIO process-ticket ===")
    
    if "image" not in request.files:
        logger.warning("No se proporcionó imagen en la request")
        return jsonify({"error": "No se proporcionó imagen"}), 400

    image_file = request.files["image"]
    logger.info(f"Archivo recibido: {image_file.filename}")

    img_array = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        logger.error("No se pudo decodificar la imagen")
        return jsonify({"error": "No se pudo decodificar la imagen"}), 400

    try:
        logger.info("Inicializando OCR service...")
        service = get_ocr_service()
        logger.info("Llamando a process_ticket...")
        productos = service.process_ticket(image)
        logger.info(f"Procesamiento completado. Productos encontrados: {len(productos)}")
        logger.info("=== FIN process-ticket ===")
        return jsonify(productos)
    except Exception as e:
        logger.exception(f"Error en process-ticket: {str(e)}")
        logger.info("=== FIN process-ticket (ERROR) ===")
        return jsonify({"error": str(e)}), 500


@ticket_bp.route("/extract-text", methods=["POST"])
def extract_text():
    """Extrae solo texto OCR de una imagen (sin LLM)."""
    logger.info("=== INICIO extract-text ===")
    
    if "image" not in request.files:
        logger.warning("No se proporcionó imagen en la request")
        return jsonify({"error": "No se proporcionó imagen"}), 400

    image_file = request.files["image"]
    logger.info(f"Archivo recibido: {image_file.filename}")

    img_array = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        logger.error("No se pudo decodificar la imagen")
        return jsonify({"error": "No se pudo decodificar la imagen"}), 400

    try:
        logger.info("Inicializando OCR service...")
        service = get_ocr_service()
        logger.info("Extrayendo texto con OCR...")
        texto = service.extract_text_only(image)
        logger.info(f"Texto extraído. Caracteres: {len(texto)}")
        logger.info("=== FIN extract-text ===")
        return jsonify({"text": texto})
    except Exception as e:
        logger.exception(f"Error en extract-text: {str(e)}")
        logger.info("=== FIN extract-text (ERROR) ===")
        return jsonify({"error": str(e)}), 500
