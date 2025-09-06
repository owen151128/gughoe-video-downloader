# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal


class BackgroundWorker(QThread):
    result_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.result_ready.emit(result)
        except BaseException as e:
            self.error_occurred.emit(str(e))
