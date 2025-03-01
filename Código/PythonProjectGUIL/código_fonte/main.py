import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMainWindow, QLineEdit
from window import MainWindow
from testDisplay import display
from PySide6.QtCore import Qt

if __name__ == '__main__':
     app = QApplication()
     window = MainWindow()

     dis = display()
     dis.setPlaceholderText('pesquise aqui')
     window.grade_Layout.addWidget(dis, 0, 0, alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

     window.show()
     app.exec()
