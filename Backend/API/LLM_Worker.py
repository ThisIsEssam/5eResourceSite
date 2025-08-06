from PyQt6.QtCore import QThread, pyqtSignal
from LLM_Class import get_llm_response

class LLMWorker(QThread):
    finished = pyqtSignal(str)  # Signal to emit the assistant's response as a string
    error = pyqtSignal(str)     # Signal to emit error messages

    def __init__(self, prompt, chat_history, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.chat_history = chat_history

    def run(self):
        try:
            # Call the get_llm_response function
            assistant_response, self.chat_history = get_llm_response(self.prompt, self.chat_history)

            # Emit only the assistant's response
            self.finished.emit(assistant_response)
        except Exception as e:
            # Emit the error message if an exception occurs
            self.error.emit(str(e))