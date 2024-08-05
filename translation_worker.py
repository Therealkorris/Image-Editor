from PyQt5.QtCore import QThread, pyqtSignal
from translate import Translator

class TranslationWorker(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, text, dest='en'):
        super().__init__()
        self.text = text
        self.dest = dest
        self.translator = Translator(to_lang=self.dest)

    def run(self):
        try:
            translated = self.translator.translate(self.text)
            self.finished.emit(translated, 'success')
        except Exception as e:
            self.finished.emit(str(e), 'error')
