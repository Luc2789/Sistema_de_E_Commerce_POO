from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QLabel, QStackedWidget, QListWidget,
                               QLineEdit, QHBoxLayout, QMessageBox, QFormLayout, QInputDialog)
from PySide6.QtCore import Qt
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# Importando os modelos
from models.usuario import Cliente, Administrador
from models.produto import Produto, Categoria
from models.pedido import Pedido, ItemPedido
from models.carrinho import Carrinho, ItemCarrinho
from models.pagamento import Pagamento
from models.estoque import Estoque
from models.entrega import Entrega
from models.endereco import Endereco
from models.relatorio import Relatorio

@dataclass
class UserSession:
    user: Optional[Cliente | Administrador] = None

# Data Models para a interface (mantidos para compatibilidade)
@dataclass
class ProductUI:
    title: str
    author: str
    category: str
    stock: int
    price: float
    product: Produto = None  # Referência ao objeto Produto

@dataclass
class OrderUI:
    order_id: int
    customer: str
    status: str
    total: float
    order: Pedido = None  # Referência ao objeto Pedido

class BaseScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.menu_screen = menu_screen
        self.session = session

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.menu_screen)

class LoginScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__(stacked_widget, menu_screen, session)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Tela de Login")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.email_input = QLineEdit(placeholderText="Email")
        self.password_input = QLineEdit(placeholderText="Senha")
        self.password_input.setEchoMode(QLineEdit.Password)

        for field in (self.email_input, self.password_input):
            field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_login = QPushButton("Login")
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
        """)
        btn_login.clicked.connect(self.login)

        layout.addWidget(title_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(btn_login)
        layout.addStretch()

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Simulação simplificada de login (substitua por lógica real)
        if email == "admin@example.com" and password == "admin123":
            self.session.user = Administrador(1, "Admin", email, password, "admin")
            if self.menu_screen and self.menu_screen in self.stacked_widget.children():
                self.stacked_widget.setCurrentWidget(self.menu_screen)
            else:
                QMessageBox.warning(self, "Erro", "Menu principal não encontrado!")
        elif email == "client@example.com" and password == "client123":
            self.session.user = Cliente(2, "Cliente", email, password, "1234567890")
            if self.menu_screen and self.menu_screen in self.stacked_widget.children():
                self.stacked_widget.setCurrentWidget(self.menu_screen)
            else:
                QMessageBox.warning(self, "Erro", "Menu principal não encontrado!")
        else:
            QMessageBox.warning(self, "Erro", "Credenciais inválidas!")

class ProductManagementScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__(stacked_widget, menu_screen, session)
        self.products: List[ProductUI] = []
        self.categories: List[Categoria] = [Categoria(i, f"Cat{i}", f"Descrição {i}") for i in range(1, 4)]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Gerenciamento de Produtos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.product_list = QListWidget()
        self.product_list.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 5px; color: #333;")

        form_layout = QFormLayout()
        self.input_fields = {
            'title': QLineEdit(placeholderText="Título do Mangá"),
            'author': QLineEdit(placeholderText="Autor"),
            'category': QLineEdit(placeholderText="Categoria"),
            'stock': QLineEdit(placeholderText="Quantidade em Estoque"),
            'price': QLineEdit(placeholderText="Preço (R$)")
        }
        for field in self.input_fields.values():
            field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Produto")
        btn_remove = QPushButton("Remover Produto")
        btn_back = QPushButton("Voltar")

        for btn in (btn_add, btn_remove, btn_back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)

        btn_add.clicked.connect(self.add_product)
        btn_remove.clicked.connect(self.remove_product)
        btn_back.clicked.connect(self.go_back)

        for label, field in [
            ("Título", self.input_fields['title']),
            ("Autor", self.input_fields['author']),
            ("Categoria", self.input_fields['category']),
            ("Estoque", self.input_fields['stock']),
            ("Preço", self.input_fields['price'])
        ]:
            form_layout.addRow(QLabel(label), field)

        layout.addWidget(title_label)
        layout.addWidget(self.product_list)
        layout.addLayout(form_layout)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_product(self):
        try:
            product_data = {key: field.text().strip() for key, field in self.input_fields.items()}
            if not all(product_data.values()):
                raise ValueError("Todos os campos devem ser preenchidos")
            stock = int(product_data['stock'])
            price = float(product_data['price'])
            if stock < 0 or price < 0:
                raise ValueError("Estoque e preço não podem ser negativos")

            category = next((cat for cat in self.categories if cat.nome == product_data['category']), None)
            if not category:
                category = Categoria(len(self.categories) + 1, product_data['category'], "Descrição")
                self.categories.append(category)

            product = Produto(len(self.products) + 1, product_data['title'],
                              f"Descrição de {product_data['title']}", price, stock, category)
            estoque = Estoque(len(self.products) + 1, product, stock, "Armazém 1")
            product_ui = ProductUI(product_data['title'], product_data['author'],
                                   product_data['category'], stock, price, product)
            self.products.append(product_ui)
            self.product_list.addItem(self.format_product_display(product_ui))
            self.clear_inputs()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def remove_product(self):
        current_row = self.product_list.currentRow()
        if current_row >= 0:
            del self.products[current_row]
            self.product_list.takeItem(current_row)

    def format_product_display(self, product: ProductUI) -> str:
        return f"{product.title} - {product.author} ({product.category}) | Estoque: {product.stock} | Preço: R${product.price:.2f}"

    def clear_inputs(self):
        for field in self.input_fields.values():
            field.clear()

class OrderManagementScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__(stacked_widget, menu_screen, session)
        self.orders: List[OrderUI] = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Gerenciamento de Pedidos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.order_list = QListWidget()
        self.order_list.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 5px; color: #333;")

        form_layout = QFormLayout()
        self.input_fields = {
            'customer': QLineEdit(placeholderText="Nome do Cliente"),
            'address': QLineEdit(placeholderText="Endereço (ex: Rua X, 123)"),
            'status': QLineEdit(placeholderText="Status do Pedido")
        }
        for field in self.input_fields.values():
            field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Pedido")
        btn_update = QPushButton("Atualizar Status")
        btn_calculate = QPushButton("Calcular Total")
        btn_back = QPushButton("Voltar")

        for btn in (btn_add, btn_update, btn_calculate, btn_back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1e87db;
                }
            """)

        btn_add.clicked.connect(self.add_order)
        btn_update.clicked.connect(self.update_status)
        btn_calculate.clicked.connect(self.calculate_total)
        btn_back.clicked.connect(self.go_back)

        for label, field in [
            ("Cliente", self.input_fields['customer']),
            ("Endereço", self.input_fields['address']),
            ("Status", self.input_fields['status'])
        ]:
            form_layout.addRow(QLabel(label), field)

        layout.addWidget(title_label)
        layout.addWidget(self.order_list)
        layout.addLayout(form_layout)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_calculate)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_order(self):
        try:
            if not self.session.user or not isinstance(self.session.user, Cliente):
                raise ValueError("Usuário não logado ou não é cliente")

            order_data = {key: field.text().strip() for key, field in self.input_fields.items()}
            if not all(order_data.values()):
                raise ValueError("Todos os campos devem ser preenchidos")

            address = Endereco(len(self.orders) + 1, order_data['address'], "123", "", "Bairro", "Cidade", "Estado",
                               "12345-678")
            order = Pedido(len(self.orders) + 1, self.session.user, datetime.now(), [], address, "PENDENTE")
            order_ui = OrderUI(order.pedido_id, order_data['customer'], order_data['status'], 0.0, order)
            self.orders.append(order_ui)
            self.order_list.addItem(self.format_order_display(order_ui))
            self.clear_inputs()
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def update_status(self):
        current_item = self.order_list.currentItem()
        if current_item:
            new_status = self.input_fields['status'].text().strip()
            if not new_status:
                QMessageBox.warning(self, "Erro", "Digite um novo status")
                return
            order_id = int(current_item.text().split()[1])
            order_ui = next((o for o in self.orders if o.order_id == order_id), None)
            if order_ui and order_ui.order:
                order_ui.order.atualizarStatus(new_status)
                order_ui.status = new_status
                current_item.setText(self.format_order_display(order_ui))
                self.input_fields['status'].clear()

    def calculate_total(self):
        current_item = self.order_list.currentItem()
        if current_item:
            order_id = int(current_item.text().split()[1])
            order_ui = next((o for o in self.orders if o.order_id == order_id), None)
            if order_ui and order_ui.order:
                total = order_ui.order.calcularTotal()
                order_ui.total = total
                QMessageBox.information(self, "Total", f"Total do Pedido {order_id}: R${total:.2f}")

    def format_order_display(self, order: OrderUI) -> str:
        return f"Pedido {order.order_id} - {order.customer} - {order.status}"

    def clear_inputs(self):
        for field in self.input_fields.values():
            field.clear()

class CartScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__(stacked_widget, menu_screen, session)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Carrinho de Compras")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.cart_list = QListWidget()
        self.cart_list.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 5px; color: #333;")

        btn_layout = QHBoxLayout()
        btn_add_product = QPushButton("Adicionar Produto")
        btn_remove_product = QPushButton("Remover Produto")
        btn_checkout = QPushButton("Finalizar Compra")
        btn_back = QPushButton("Voltar")

        for btn in (btn_add_product, btn_remove_product, btn_checkout, btn_back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #8e24aa;
                }
            """)

        btn_add_product.clicked.connect(self.add_product_to_cart)
        btn_remove_product.clicked.connect(self.remove_product_from_cart)
        btn_checkout.clicked.connect(self.checkout)
        btn_back.clicked.connect(self.go_back)

        layout.addWidget(title_label)
        layout.addWidget(self.cart_list)
        btn_layout.addWidget(btn_add_product)
        btn_layout.addWidget(btn_remove_product)
        btn_layout.addWidget(btn_checkout)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_product_to_cart(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        product_name, ok = QInputDialog.getText(self, "Adicionar Produto", "Nome do Produto:")
        if ok and product_name:
            product = next((p.product for p in self.stacked_widget.product_screen.products if p.title == product_name),
                           None)
            if product:
                quantity, ok = QInputDialog.getInt(self, "Quantidade", "Quantidade:", 1, 1, 999)
                if ok:
                    self.session.user.adicionarAoCarrinho(product, quantity)
                    self.update_cart_list()

    def remove_product_from_cart(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        current_row = self.cart_list.currentRow()
        if current_row >= 0:
            item_text = self.cart_list.item(current_row).text()
            product_name = item_text.split(" x ")[0]
            product = next((p.product for p in self.stacked_widget.product_screen.products if p.title == product_name),
                           None)
            if product:
                item = next((i for i in self.session.user.carrinho.itens if i.produto == product), None)
                if item:
                    self.session.user.removerDoCarrinho(item)
                    self.update_cart_list()

    def checkout(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        address, ok = QInputDialog.getText(self, "Endereço de Entrega", "Endereço:")
        if ok and address:
            pedido = self.session.user.finalizarCompra(
                Endereco(1, address, "123", "", "Bairro", "Cidade", "Estado", "12345-678"))
            if pedido:
                order_ui = OrderUI(pedido.pedido_id, self.session.user.nome, "PENDENTE", pedido.calcularTotal(), pedido)
                self.stacked_widget.order_screen.orders.append(order_ui)
                self.stacked_widget.order_screen.order_list.addItem(
                    self.stacked_widget.order_screen.format_order_display(order_ui))
                QMessageBox.information(self, "Sucesso", f"Pedido {pedido.pedido_id} criado com sucesso!")
                self.update_cart_list()

    def update_cart_list(self):
        self.cart_list.clear()
        if self.session.user and isinstance(self.session.user, Cliente):
            for item in self.session.user.carrinho.itens:
                self.cart_list.addItem(f"{item.produto.nome} x {item.quantidade} - R${item.getSubtotal():.2f}")

class ReportsScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, menu_screen: QWidget, session: UserSession):
        super().__init__(stacked_widget, menu_screen, session)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Relatórios")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.comment_list = QListWidget()
        self.comment_list.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 5px; color: #333;")

        self.comment_input = QLineEdit(placeholderText="Adicionar comentário sobre pedidos...")
        self.comment_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Comentário")
        btn_generate = QPushButton("Gerar Relatório")
        btn_back = QPushButton("Voltar")

        for btn in (btn_add, btn_generate, btn_back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #8e24aa;
                }
            """)

        btn_add.clicked.connect(self.add_comment)
        btn_generate.clicked.connect(self.generate_report)
        btn_back.clicked.connect(self.go_back)

        layout.addWidget(title_label)
        layout.addWidget(self.comment_list)
        layout.addWidget(self.comment_input)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_generate)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_comment(self):
        comment = self.comment_input.text().strip()
        if comment:
            self.comment_list.addItem(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {comment}")
            self.comment_input.clear()

    def generate_report(self):
        if not self.session.user or not isinstance(self.session.user, Administrador):
            QMessageBox.warning(self, "Erro", "Apenas administradores podem gerar relatórios")
            return
        report = Relatorio(1, "VENDAS", datetime.now(), datetime.now(), datetime.now())
        report.gerarRelatorio()
        self.comment_list.addItem(f"Relatório gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-commerce de Mangás")
        self.setMinimumSize(800, 600)

        self.session = UserSession()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Criar todas as telas primeiro, incluindo o menu_screen
        self.menu_screen = self.create_main_menu()  # Criar o menu imediatamente
        self.login_screen = LoginScreen(self.central_widget, self.menu_screen, self.session)
        self.product_screen = ProductManagementScreen(self.central_widget, self.menu_screen, self.session)
        self.order_screen = OrderManagementScreen(self.central_widget, self.menu_screen, self.session)
        self.cart_screen = CartScreen(self.central_widget, self.menu_screen, self.session)
        self.reports_screen = ReportsScreen(self.central_widget, self.menu_screen, self.session)

        # Adicionar todos os widgets ao QStackedWidget
        self.central_widget.addWidget(self.login_screen)
        self.central_widget.addWidget(self.menu_screen)
        self.central_widget.addWidget(self.product_screen)
        self.central_widget.addWidget(self.order_screen)
        self.central_widget.addWidget(self.cart_screen)
        self.central_widget.addWidget(self.reports_screen)

        self.central_widget.setCurrentWidget(self.login_screen)  # Começa na tela de login

        self.apply_styles()

    def create_main_menu(self) -> QWidget:
        menu_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        title_label = QLabel("Menu Principal")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")

        btn_products = QPushButton("Gerenciar Produtos")
        btn_orders = QPushButton("Gerenciar Pedidos")
        btn_cart = QPushButton("Carrinho")
        btn_reports = QPushButton("Relatórios")
        btn_logout = QPushButton("Logout")

        for btn in (btn_products, btn_orders, btn_cart, btn_reports, btn_logout):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF5722;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #e64a19;
                }
            """)
            btn.setMinimumHeight(50)

        btn_products.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.product_screen))
        btn_orders.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.order_screen))
        btn_cart.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.cart_screen))
        btn_reports.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.reports_screen))
        btn_logout.clicked.connect(self.logout)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(btn_products)
        layout.addWidget(btn_orders)
        layout.addWidget(btn_cart)
        layout.addWidget(btn_reports)
        layout.addWidget(btn_logout)
        layout.addStretch()

        menu_widget.setLayout(layout)
        return menu_widget

    def logout(self):
        self.session.user = None
        self.central_widget.setCurrentWidget(self.login_screen)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #ffffff;
                color: #333;
            }
            QStackedWidget {
                background-color: #ffffff;
                color: #333;
            }
            QMessageBox {
                background-color: #ffffff;
                color: #333;
            }
            QLabel {
                color: #333;
            }
            QListWidget {
                color: #333;
            }
            QLineEdit {
                color: #333;
            }
        """)
        self.menu_screen.setStyleSheet("background-color: #3F51B5;")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Erro crítico na aplicação: {str(e)}")
