# Advanced Image Processor

## Description

The Advanced Image Processor is a powerful Python-based application that provides a comprehensive suite of image processing, OCR (Optical Character Recognition), translation, and AI-powered image analysis tools. Built with PyQt5, this desktop application offers an intuitive graphical user interface for manipulating and analyzing images.
=======
This project is an advanced image-processing application built with PyQt5. It provides functionalities for image uploading, OCR (Optical Character Recognition), translation, and Llava image analysis. The application is designed to handle multiple images and perform various operations on them.

## Features

1. **Image Processing**
   - Adjust brightness, contrast, saturation, hue, and gamma
   - Apply blur, sharpen, and noise effects
   - Perform edge detection
   - Convert to greyscale, invert colors, or apply sepia tone
   - Rotate and flip images

2. **Color Balance**
   - Fine-tune red, green, and blue color channels

3. **OCR (Optical Character Recognition)**
   - Perform text extraction using both EasyOCR and Tesseract
   - Support for multiple languages
   - Automatic OCR option

4. **Translation**
   - Translate extracted text to various languages
   - Support for multiple target languages

5. **AI-powered Image Analysis**
   - Utilize Llava (Large Language and Vision Assistant) for advanced image analysis

6. **Selection Tools**
   - Rectangle and triangle selection modes for targeted processing both for OCR and image analysis

7. **File Operations**
   - Upload multiple images
   - Save processed images

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Therealkorris/Image-Editor
   cd Image-Editor
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR:
   - For Windows: Download and install from [GitHub Tesseract OCR repository](https://github.com/UB-Mannheim/tesseract/wiki)
   - For macOS: `brew install tesseract`
   - For Linux: `sudo apt-get install tesseract-ocr`

5. Install Ollama for Llava integration:
   - Follow the instructions at [Ollama's official website](https://ollama.com/)
   - "Ollama pull Llava-llama3" or any other multi-model

6. Install Cuda and CuDNN for faster GPU processing:
   - Follow the instructions at [NVIDIA's official website](https://developer.nvidia.com/cuda-downloads)
   - Install the required packages:
     ```
     pip install torch torchvision
     ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Use the "Upload Images" button to load images into the application.

3. Adjust image processing parameters using the sliders and checkboxes in the left panel.

4. Use the selection tools to focus on specific areas of the image for processing or analysis.

5. Perform OCR by clicking the "Perform OCR" button or enabling "Auto OCR".

6. Translate extracted text by selecting a target language and clicking "Show/Hide Translation".

7. Conduct AI-powered image analysis using the "Perform Llava Analysis" button.

8. Save processed images using the "Save Image" button.

## Project Structure

- `main.py`: Entry point of the application
- `image_processor.py`: Main application logic and UI
- `image_frame.py`: Custom widget for displaying and interacting with images
- `image_processing.py`: Image processing functions
- `ocr_worker.py`: Worker class for OCR operations
- `ocr_translation.py`: Translation functionality
- `llava_integration.py`: Integration with Llava for AI-powered image analysis
- `ui_components.py`: UI component creation and layout

## Dependencies

See `requirements.txt` for a full list of dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- EasyOCR
- Tesseract OCR
- PyQt5
- OpenCV
- Ollama
- Llava (Large Language and Vision Assistant)

