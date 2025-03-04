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
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Titulo do Mangá")
        
        self.input_autor = QLineEdit()
        self.input_autor.setPlaceholderText("Autor")

        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("Categoria")

        self.input_quantidade = QLineEdit()
        self.input_quantidade.setPlaceholderText("Quantidade em Estoque")

        btn_add = QPushButton("Adicionar Produto")
        btn_add.clicked.connect(self.add_product)
        
        btn_remove = QPushButton("Remover Produto")
        btn_remove.clicked.connect(self.remove_product)
        
        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        
        layout.addWidget(QLabel("Gerenciamento de Produtos"))
        layout.addWidget(self.product_list)
        layout.addWidget(self.input_title)
        layout.addWidget(self.input_autor)
        layout.addWidget(self.input_categoria)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)
        layout.addWidget(btn_back)
        
        self.setLayout(layout)
    
    def add_product(self):
        title = self.input_title.text()
        autor = self.input_autor.text()
        categoria = self.input_categoria.text()
        quantidade = self.input_quantidade.text()

        if title and autor and categoria and quantidade:
            produto_info = f"{title} - {autor} ({categoria}) | Estoque: {quantidade}"
            self.product_list.addItem(produto_info)
            self.input_title.clear()
            self.input_autor.clear()
            self.input_categoria.clear()
            self.input_quantidade.clear()
    
    def remove_product(self):
        selected_item = self.product_list.currentItem()
        if selected_item:
            self.product_list.takeItem(self.product_list.row(selected_item))

class OrderManagementScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gerenciamento de Pedidos"))
        
        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        layout.addWidget(btn_back)
        
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
        
        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        
        layout.addWidget(QLabel("Relatórios"))
        layout.addWidget(self.comment_list)
        layout.addWidget(self.comment_input)
        layout.addWidget(btn_add_comment)
        layout.addWidget(btn_back)
        
        self.setLayout(layout)
    
    def add_comment(self):
        comment = self.comment_input.text().strip()
        if comment:
            self.comment_list.addItem(comment)
            self.comment_input.clear()
    
    def go_back(self):
        self.parentWidget().setCurrentIndex(0)

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
