from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        # definindo o widget central e o layout
        self.central_widget = QWidget()
        self.grade_Layout = QGridLayout()
        # setando o layout
        self.central_widget.setLayout(self.grade_Layout)

        self.setCentralWidget(self.central_widget)


        #titulo
        self.setWindowTitle('Planeta Mangá')

