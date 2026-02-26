from flask import Blueprint, request, jsonify
import cv2
import numpy as np

from ..services.ocr_service import OCRService


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
    if "image" not in request.files:
        return jsonify({"error": "No se proporcionó imagen"}), 400

    image_file = request.files["image"]

    img_array = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "No se pudo decodificar la imagen"}), 400

    try:
        service = get_ocr_service()
        productos = service.process_ticket(image)
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ticket_bp.route("/extract-text", methods=["POST"])
def extract_text():
    """Extrae solo texto OCR de una imagen (sin LLM)."""
    if "image" not in request.files:
        return jsonify({"error": "No se proporcionó imagen"}), 400

    image_file = request.files["image"]

    img_array = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "No se pudo decodificar la imagen"}), 400

    try:
        service = get_ocr_service()
        texto = service.extract_text_only(image)
        return jsonify({"text": texto})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
