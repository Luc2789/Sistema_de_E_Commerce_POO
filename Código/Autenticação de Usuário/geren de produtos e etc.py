from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QListWidget, QLineEdit, QHBoxLayout
import sys
from datetime import datetime

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tela de Login"))
        self.setLayout(layout)

class ProductManagementScreen(QWidget):
    def __init__(self, stacked_widget, menu_screen):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.menu_screen = menu_screen
        
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
        btn_back.clicked.connect(self.go_back)
        
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

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.menu_screen)

class OrderManagementScreen(QWidget):
    def __init__(self, stacked_widget, menu_screen):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.menu_screen = menu_screen

        self.order = []

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gerenciamento de Pedidos"))
        
        self.order_list = QListWidget()
        layout.addWidget(self.order_list)

        self.input_cliente = QLineEdit()
        self.input_cliente.setPlaceholderText("Nome do Cliente")
        layout.addWidget(self.input_cliente)

        self.input_endereco = QLineEdit()
        self.input_endereco.setPlaceholderText("Endereçe do Cliente")
        layout.addWidget(self.input_endereco)

        self.input_status = QLineEdit()
        self.input_status.setPlaceholderText("Status do Pedido")
        layout.addWidget(self.input_status)

        btn_add_pedido = QPushButton("Adicionar Pedido")
        btn_add_pedido.clicked.connect(self.add_order)
        layout.addWidget(btn_add_pedido)

        btn_update_status = QPushButton("Atualizar Status")
        btn_update_status.clicked.connect(self.update_status)
        layout.addWidget(btn_update_status)

        btn_calculate_total = QPushButton("Calcular Total")
        btn_calculate_total.clicked.connect(self.calculate_total)
        layout.addWidget(btn_calculate_total)

        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)
        
        self.setLayout(layout)

    def add_order(self):
        cliente = self.input_cliente.text()
        endereco = self.input_endereco.text()
        status = self.input_status.text()

        if cliente and endereco and status:
            order = {
                "pedidold": len(self.order) + 1,
                "cliente": cliente,
                "dataCriacao": datetime.now(),
                "enderecoEntrega": endereco,
                "status": status,
                "itens": []
            }
            self.order.append(order)
            self.order_list.addItem(f"Pedido {order['pedidold']} - {cliente} - {status}")
            self.input_cliente.clear()
            self.input_endereco.clear()
            self.input_status.clear()

    def update_status(self):
        selected_item = self.order_list.currentItem()
        if selected_item:
            order_id = int(selected_item.text().split()[1])
            new_status = self.input_status.text()
            if new_status:
                for order in self.order:
                    if order["pedidold"] == order_id:
                        order["status"] = new_status
                        selected_item.setText(f"Pedido {order['pedidold']} - {order['cliente']} - {new_status}")
                        self.input_status.clear()
                        break

    def calculate_total(self):
        selected_item = self.order_list.currentItem()
        if selected_item:
            order_id = int(selected_item.text().split()[1])
            for order in self.order:
                if order["pedidold"] == order_id:
                    total = sum(item["preco"] * item["quantidade"] for item in order["itens"])
                    self.order_list.addItem(f"Total do Pedido {order_id}: R${total:.2f}")
                    break

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.menu_screen)

class ReportsScreen(QWidget):
    def __init__(self, stacked_widget, menu_screen):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.menu_screen = menu_screen

        layout = QVBoxLayout()
        
        self.comment_list = QListWidget()
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Adicionar comentário sobre pedidos...")
        
        btn_add_comment = QPushButton("Adicionar Comentário")
        btn_add_comment.clicked.connect(self.add_comment)
        
        btn_back = QPushButton("Voltar")
        btn_back.clicked.connect(self.go_back)
        
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
        self.stacked_widget.setCurrentWidget(self.menu_screen)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-commerce de Mangas")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.menu_screen = self.create_main_menu()

        self.login_screen = LoginScreen()
        self.product_screen = ProductManagementScreen(self.central_widget, self.menu_screen)
        self.order_screen = OrderManagementScreen(self.central_widget, self.menu_screen)
        self.reports_screen = ReportsScreen(self.central_widget, self.menu_screen)

        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.menu_screen)
        self.central_widget.addWidget(self.product_screen)
        self.central_widget.addWidget(self.order_screen)
        self.central_widget.addWidget(self.reports_screen)

        self.central_widget.setCurrentWidget(self.menu_screen)

    def create_main_menu(self):
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
        return menu_widget
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
