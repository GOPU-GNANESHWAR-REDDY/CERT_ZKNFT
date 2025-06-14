# api/qr_utils.py

import qrcode
import os
import re

def sanitize_filename(name: str) -> str:
    """
    Replace invalid filename characters (like /, \, :, etc.) with _
    """
    return re.sub(r"[^\w\-_.]", "_", name)

def generate_qr(data: str, filename: str = "qr_token.png") -> str:
    """
    Generate a QR code image from data.
    Saves it to ./static/qr/ folder.
    """
    os.makedirs("./static/qr", exist_ok=True)
    clean_filename = sanitize_filename(filename)
    path = f"./static/qr/{clean_filename}"
    img = qrcode.make(data)
    img.save(path)
    return path
