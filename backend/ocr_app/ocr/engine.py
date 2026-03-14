import json
import os

os.environ['FLAGS_use_onednn'] = '0'
os.environ['FLAGS_enable_pir_api'] = '0'
os.environ['FLAGS_enable_executor_unittests'] = '0'
os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'

import paddle
from paddleocr import PaddleOCR

paddle.set_flags({'FLAGS_fraction_of_cpu_memory_to_use': 0.5})


ocr_instance = None


def get_ocr_model():
    global ocr_instance
    if ocr_instance is None:
        ocr_instance = PaddleOCR(
            text_detection_model_name='PP-OCRv5_mobile_det',
            text_recognition_model_name='latin_PP-OCRv5_mobile_rec',
            enable_mkldnn=False,
        )
    return ocr_instance


class OCREngine:
    def __init__(self, config):
        self.config = config
        self.lector = get_ocr_model()

    def ejecutar(self, imagen_bgr):
        if self.lector is not None:
            result = self.lector.predict(input=imagen_bgr)
            text = result[0].get('rec_texts', '')
            text_clean = json.dumps(text, indent=2)
            return text_clean
