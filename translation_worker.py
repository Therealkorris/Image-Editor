from PyQt5.QtCore import QThread, pyqtSignal
from googletrans import Translator

class TranslationWorker(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, text, dest='en'):
        super().__init__()
        self.text = text
        self.dest = dest
        self.translator = Translator()

    def run(self):
        try:
            translated = self.translator.translate(self.text, dest=self.dest)
            self.finished.emit(translated.text, 'success')
        except Exception as e:
            self.finished.emit(str(e), 'error')