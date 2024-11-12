import pytesseract
from PIL import Image
import os

def perform_ocr(frame_folder):
    text_data = []
    for frame_name in sorted(os.listdir(frame_folder)):
        frame_path = os.path.join(frame_folder, frame_name)
        image = Image.open(frame_path)
        text = pytesseract.image_to_string(image)
        text_data.append(text)
    return text_data
