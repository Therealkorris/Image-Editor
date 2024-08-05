from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import pytesseract
import easyocr
import torch

class OCRWorker(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, image, ocr_type):
        super().__init__()
        self.image = image
        self.ocr_type = ocr_type
        print(f"Initializing OCRWorker with {ocr_type}, image shape: {image.shape}")
        if ocr_type == 'EasyOCR':
            # Initialize EasyOCR with GPU support if available
            self.reader = easyocr.Reader(['en'], gpu=True)
        elif ocr_type == 'Tesseract':
            # Specify the path to Tesseract executable
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def run(self):
        print(f"Running OCR with {self.ocr_type}")
        try:
            if self.ocr_type == 'EasyOCR':
                # Perform OCR using EasyOCR
                ocr_text = self.reader.readtext(self.image, detail=0)
                result = '\n'.join(ocr_text)
            elif self.ocr_type == 'Tesseract':
                # Perform OCR using Tesseract
                result = pytesseract.image_to_string(self.image)
            print(f"OCR result: {result[:100] if result else 'None'}")
            self.finished.emit(result, self.ocr_type)
        except Exception as e:
            print(f"Error in OCR {self.ocr_type}: {str(e)}")
            self.finished.emit(f"Error: {str(e)}", self.ocr_type)