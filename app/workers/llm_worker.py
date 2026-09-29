from PySide6.QtCore import QObject, Signal

from llm.llama_qwen_4b import LlamaEngine


class LLMWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, text):
        super().__init__()

        self.text = text

    def run(self):
        try:
            engine = LlamaEngine()

            if not engine.is_available():
                raise RuntimeError(
                    "AI engine is not running.\n\n"
                    "Please start llama-server and try again."
                )

            normalized_text = engine.clean_text(self.text)

            self.finished.emit(normalized_text)

        except Exception as e:
            self.error.emit(str(e))