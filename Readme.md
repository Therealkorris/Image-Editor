# Advanced Image Processor

This project is an advanced image processing application built with PyQt5. It provides functionalities for image uploading, OCR (Optical Character Recognition), translation, and Llava analysis. The application is designed to handle multiple images and perform various operations on them.

## Features

- **Image Uploading**: Upload and manage multiple images.
- **OCR**: Perform OCR on selected regions of images.
- **Translation**: Translate OCR results into different languages.
- **Llava Analysis**: Analyze images using the Llava model to extract specific data.

## Project Structure

### Key Components

- **ImageProcessor**: Main class for handling the UI and image processing logic.
- **LlavaWorker**: Handles the Llava analysis for images.
- **OCRWorker**: Manages OCR operations.
- **UI Components**: Contains functions to create UI panels and components.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/advanced-image-processor.git
    cd advanced-image-processor
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python main.py
    ```

## Usage

1. **Upload Images**: Use the upload button to add images to the application.
2. **Perform OCR**: Select regions of the image and click the OCR button to extract text.
3. **Translate Text**: Use the translate button to translate the extracted text.
4. **Llava Analysis**: Click the Llava analysis button to analyze images and extract specific data.

## Code Overview

### [`image_processor.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fimage_processor.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "e:\Image Editor\image_processor.py")

This file contains the [`ImageProcessor`](command:_github.copilot.openSymbolFromReferences?%5B%22ImageProcessor%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cimage_processor.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fimage_processor.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fimage_processor.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A6%7D%7D%5D%5D "Go to definition") class, which is the main class for the application. It handles the UI setup and various image processing operations.

### [`llava_integration.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fllava_integration.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "e:\Image Editor\llava_integration.py")

This file contains the [`LlavaWorker`](command:_github.copilot.openSymbolFromReferences?%5B%22LlavaWorker%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cimage_processor.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fimage_processor.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fimage_processor.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A30%7D%7D%2C%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cllava_integration.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fllava_integration.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fllava_integration.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A6%7D%7D%5D%5D "Go to definition") class, which performs Llava analysis on images. It uses the [`ollama.chat`](command:_github.copilot.openSymbolFromReferences?%5B%22ollama.chat%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cllava_integration.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fllava_integration.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fllava_integration.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A1%2C%22character%22%3A7%7D%7D%5D%5D "Go to definition") API to analyze images and extract data.

### [`ocr_worker.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Focr_worker.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "e:\Image Editor\ocr_worker.py")

This file contains the [`OCRWorker`](command:_github.copilot.openSymbolFromReferences?%5B%22OCRWorker%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cimage_processor.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fimage_processor.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fimage_processor.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A23%7D%7D%5D%5D "Go to definition") class, which handles OCR operations on images.

### [`ui_components.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fui_components.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "e:\Image Editor\ui_components.py")

This file contains functions to create UI panels and components used in the [`ImageProcessor`](command:_github.copilot.openSymbolFromReferences?%5B%22ImageProcessor%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5CImage%20Editor%5C%5Cimage_processor.py%22%2C%22_sep%22%3A1%2C%22external%22%3A%22file%3A%2F%2F%2Fe%253A%2FImage%2520Editor%2Fimage_processor.py%22%2C%22path%22%3A%22%2Fe%3A%2FImage%20Editor%2Fimage_processor.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A6%7D%7D%5D%5D "Go to definition") class.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [OpenCV](https://opencv.org/) for image processing.
- [ollama](https://ollama.com/) for the Llava model API.

---
