from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QLabel, QMainWindow, QGridLayout, QWidget


class quadro(QPushButton):
    def __init__(self, nome):
        super().__init__()
        
        self.setText(nome)
        self.setStyleSheet('font-size: 15px; color: red;')

        
                
            