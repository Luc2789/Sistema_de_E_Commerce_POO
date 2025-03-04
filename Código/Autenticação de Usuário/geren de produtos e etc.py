from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QListWidget, QLineEdit, QHBoxLayout
import sys

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de Login"))
        self.setLayout(layout)

class ProductManagementScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.product_list = QListWidget()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Nome do Produto")
        
        btn_add = QPushButton("Adicionar Produto")
        btn_add.clicked.connect(self.add_product)
        
        btn_remove = QPushButton("Remover Produto")
        btn_remove.clicked.connect(self.remove_product)
        
        layout.addWidget(QLabel("Gerenciamento de Produtos"))
        layout.addWidget(self.product_list)
        layout.addWidget(self.input_field)
        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)
        
        self.setLayout(layout)
    
    def add_product(self):
        product_name = self.input_field.text().strip()
        if product_name:
            self.product_list.addItem(product_name)
            self.input_field.clear()
    
    def remove_product(self):
        selected_item = self.product_list.currentItem()
        if selected_item:
            self.product_list.takeItem(self.product_list.row(selected_item))

class OrderManagementScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gerenciamento de Pedidos"))
        self.setLayout(layout)

class ReportsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.comment_list = QListWidget()
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Adicionar comentário sobre pedidos...")
        
        btn_add_comment = QPushButton("Adicionar Comentário")
        btn_add_comment.clicked.connect(self.add_comment)
        
        layout.addWidget(QLabel("Relatórios"))
        layout.addWidget(self.comment_list)
        layout.addWidget(self.comment_input)
        layout.addWidget(btn_add_comment)
        
        self.setLayout(layout)
    
    def add_comment(self):
        comment = self.comment_input.text().strip()
        if comment:
            self.comment_list.addItem(comment)
            self.comment_input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-commerce de Mangas")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginScreen()
        self.product_screen = ProductManagementScreen()
        self.order_screen = OrderManagementScreen()
        self.reports_screen = ReportsScreen()

        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.product_screen)
        self.central_widget.addWidget(self.order_screen)
        self.central_widget.addWidget(self.reports_screen)

        self.show_main_menu()

    def show_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Menu Principal"))

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
