from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QListWidget,
                               QHBoxLayout, QMessageBox, QInputDialog, QStackedWidget, QWidget)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Cliente

class CartScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, session, client_dashboard_screen: QWidget):
        super().__init__(stacked_widget, return_screen, session)
        self.client_dashboard_screen = client_dashboard_screen
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
        btn_back.clicked.connect(self.go_back_to_dashboard)

        layout.addWidget(title_label)
        layout.addWidget(self.cart_list)
        btn_layout.addWidget(btn_add_product)
        btn_layout.addWidget(btn_remove_product)
        btn_layout.addWidget(btn_checkout)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.update_cart_list()

    def go_back_to_dashboard(self):
        if self.client_dashboard_screen:
            self.stacked_widget.setCurrentWidget(self.client_dashboard_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela do cliente não encontrada!")

    def add_product_to_cart(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        product_name, ok = QInputDialog.getText(self, "Adicionar Produto", "Nome do Produto:")
        if ok and product_name:
            product = next((p.product for p in getattr(self.stacked_widget, 'product_screen', {}).get('products', []) if p.title == product_name), None)
            if product:
                quantity, ok = QInputDialog.getInt(self, "Quantidade", "Quantidade:", 1, 1, 999)
                if ok:
                    self.session.user.adicionarAoCarrinho(product, quantity)
                    self.update_cart_list()
            else:
                QMessageBox.warning(self, "Erro", "Produto não encontrado!")

    def remove_product_from_cart(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        current_row = self.cart_list.currentRow()
        if current_row >= 0:
            item_text = self.cart_list.item(current_row).text()
            product_name = item_text.split(" x ")[0]
            product = next((p.product for p in getattr(self.stacked_widget, 'product_screen', {}).get('products', []) if p.title == product_name), None)
            if product:
                item = next((i for i in self.session.user.carrinho.itens if i.produto == product), None)
                if item:
                    self.session.user.removerDoCarrinho(item)
                    self.update_cart_list()
            else:
                QMessageBox.warning(self, "Erro", "Produto não encontrado!")

    def checkout(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        if not self.session.user.carrinho.itens:
            QMessageBox.warning(self, "Erro", "Seu carrinho está vazio!")
            return
        if hasattr(self.stacked_widget, 'payment_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.payment_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela de pagamento não encontrada!")

    def update_cart_list(self):
        self.cart_list.clear()
        if self.session.user and isinstance(self.session.user, Cliente):
            for item in self.session.user.carrinho.itens:
                self.cart_list.addItem(f"{item.produto.nome} x {item.quantidade} - R${item.getSubtotal():.2f}")