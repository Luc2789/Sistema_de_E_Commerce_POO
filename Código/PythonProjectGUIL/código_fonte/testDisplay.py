
from  PySide6.QtWidgets import QLineEdit

class display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.displayConfig()

    def displayConfig(self):
        self.setStyleSheet('font-size: 15px')
        self.setMinimumHeight(30)
