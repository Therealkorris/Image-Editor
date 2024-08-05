import sys
from PyQt5.QtWidgets import QApplication
from image_processor import ImageProcessor
import warnings

# Suppress specific FutureWarning from torch
warnings.filterwarnings("ignore", category=FutureWarning, module="easyocr.detection")

# Suppress warnings from ollama
warnings.filterwarnings("ignore", category=UserWarning, module="ollama")

if __name__ == '__main__':
    main_app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(main_app.exec_())