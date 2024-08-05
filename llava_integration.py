from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import ollama
import cv2
import base64

class WorkerSignals(QObject):
    result = pyqtSignal(str, int)

class LlavaWorker(QRunnable):
    def __init__(self, image_data, image_index):
        super().__init__()
        self.image_data = image_data
        self.image_index = image_index
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            print(f"LlavaWorker: Starting analysis for image {self.image_index}")
            
            # Convert image data to base64
            _, buffer = cv2.imencode('.png', self.image_data)
            base64_image = base64.b64encode(buffer).decode('utf-8')

            print(f"LlavaWorker: Calling ollama.chat for image {self.image_index}")
            res = ollama.chat(
                model="llava-llama3",
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe the image: I want the data presented in this way: Name, HP, Card number',
                        'images': [base64_image]
                    }
                ]
            )
            content = res['message']['content']
            print(f"LlavaWorker: Analysis completed for image {self.image_index}")
            print(f"LlavaWorker: Result: {content[:100]}...")  # Print first 100 characters of the result
            self.signals.result.emit(content, self.image_index)
        except Exception as e:
            error_message = f"Error in Llava analysis for image {self.image_index}: {str(e)}"
            print(f"LlavaWorker: {error_message}")
            self.signals.result.emit(error_message, self.image_index)
        print(f"LlavaWorker: Task for image {self.image_index} finished")