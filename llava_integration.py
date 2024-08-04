from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import ollama
import os

class WorkerSignals(QObject):
    result = pyqtSignal(str, int)

class LlavaWorker(QRunnable):
    def __init__(self, image_path, image_index):
        super().__init__()
        self.image_path = image_path
        self.image_index = image_index
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            print(f"LlavaWorker: Starting analysis for image {self.image_index}: {self.image_path}")
            if not os.path.exists(self.image_path):
                raise FileNotFoundError(f"Image file not found: {self.image_path}")

            print(f"LlavaWorker: Calling ollama.chat for image {self.image_index}")
            res = ollama.chat(
                model="llava-llama3",
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe the image: I want the data presented in this way: Name, HP, Card number',
                        'images': [self.image_path]
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
