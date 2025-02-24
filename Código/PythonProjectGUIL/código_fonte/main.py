import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMainWindow
from window import MainWindow
if __name__ == '__main__':
     app = QApplication()
     window = MainWindow()

     window.show()
     app.exec()
