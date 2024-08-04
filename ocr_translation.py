from PyQt5.QtCore import QThread, pyqtSignal

class TranslationWorker(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, text, target_lang):
        super().__init__()
        self.text = text
        self.target_lang = target_lang

    def run(self):
        try:
            # Mock translation (replace this with actual translation if possible)
            translated_text = f"Translated to {self.target_lang}: {self.text}"
            self.finished.emit(translated_text, 'success')
        except Exception as e:
            self.finished.emit(str(e), 'error')

def perform_translation(parent):
    target_lang = parent.target_lang_combo.currentText()

    for translation_result in parent.translation_results:
        for result in translation_result:
            result.clear()

    for worker in parent.translation_workers:
        if worker.isRunning():
            worker.terminate()
    parent.translation_workers.clear()

    for i, ocr_result in enumerate(parent.ocr_results):
        for j, result in enumerate(ocr_result):
            text = result.toPlainText()
            if text:
                worker = TranslationWorker(text, target_lang)
                worker.finished.connect(lambda translated_text, status, idx=i, ocr_idx=j: 
                                        parent.update_translation_result(translated_text, status, idx, ocr_idx))
                worker.start()
                parent.translation_workers.append(worker)