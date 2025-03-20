import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)
from PyQt6.QtCore import QThread, pyqtSignal
from Backend.LLM.LLM_Class import get_llm_response

class LLMWorker(QThread):
    finished = pyqtSignal(str)  # Signal to send the LLM response back to the main thread
    error = pyqtSignal(str)     # Signal to send error messages

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            # Call the LLM function to get the response
            response = get_llm_response(self.prompt)
            self.finished.emit(response)  # Emit the response when done
        except Exception as e:
            self.error.emit(str(e))  # Emit the error message if something goes wrong