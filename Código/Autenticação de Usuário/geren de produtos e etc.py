from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,QLabel, QStackedWidget
import sys

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de Login"))
        self.setLayout(layout)

class ProdManScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gerenciamento de Produtos"))
        self.setLayout(layout)

class OrdenManSreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gerenciamento de Pedidos"))
        self.setLayout(layout)

class ReportSreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Relatórios"))
        self.setLayout(layout)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-commerce de Mangas")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginScreen()
        self.product_screen = ProdManScreen()
        self.order_screen = OrdenManSreen()
        self.reports_screen = ReportSreen()
        
        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.product_screen)
        self.central_widget.addWidget(self.order_screen)
        self.central_widget.addWidget(self.reports_screen)

        self.show_main_menu()

    def show_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Menu principal"))

        btn_products = QPushButton("Gerenciar Produtos")
        btn_products.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.product_screen))
        
        btn_orders = QPushButton("Gerenciar Pedidos")
        btn_orders.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.order_screen))
        
        btn_reports = QPushButton("Relatórios")
        btn_reports.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.reports_screen))

        layout.addWidget(btn_products)
        layout.addWidget(btn_orders)
        layout.addWidget(btn_reports)

        menu_widget.setLayout(layout)
        self.central_widget.addWidget(menu_widget)
        self.central_widget.setCurrentWidget(menu_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
