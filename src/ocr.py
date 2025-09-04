from typing import Any, List, Tuple, Union

from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
import base64


rapidocr_reader = RapidOCR()


def normalize_rapidocr_result(
    result: Tuple[List[List[Union[List[List[float]], str, float]]], Any]
) -> List[Tuple[List[List[float]], str, float]]:
    """Normalize RapidOCR result to a common tuple format."""
    if result[0] is None:
        return []
    detections = result[0]
    normalized = []
    for detection in detections:
        bbox = detection[0]
        text = detection[1]
        confidence = detection[2]
        normalized.append((bbox, text, confidence))
    return normalized


def decode_images_from_b64(images_b64: list[str]) -> list[Any]:
    imgdata = [base64.b64decode(data) for data in images_b64]
    images = [cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR) for data in imgdata]
    return images


def ocr_image(img: Any, ocr_engine: str = "rapidocr") -> list[tuple[list[list[float]], str, float]]:
    # Currently only RapidOCR is supported; keep structure for future engines
    result = rapidocr_reader(img)
    return normalize_rapidocr_result(result)


def ocr_images_b64(
    images_b64: list[str],
    ocr_engine: str = "rapidocr",
) -> list[list[tuple[list[list[float]], str, float]]]:
    images = decode_images_from_b64(images_b64)
    out = []
    for img in images:
        out.append(ocr_image(img, ocr_engine))
    return out

