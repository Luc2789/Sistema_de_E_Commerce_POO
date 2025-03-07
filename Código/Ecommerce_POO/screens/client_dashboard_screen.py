from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QHBoxLayout,
                               QLineEdit, QScrollArea, QWidget, QMessageBox, QInputDialog, QStackedWidget)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from .base_screen import BaseScreen
from models.usuario import Cliente
from ui_data import ProductUI

class ClientDashboardScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, auth_screen: QWidget, payment_screen: QWidget, cart_screen: QWidget, session, product_management_screen):
        super().__init__(stacked_widget, return_screen, session)
        self.auth_screen = auth_screen
        self.payment_screen = payment_screen
        self.cart_screen = cart_screen
        self.product_management_screen = product_management_screen
        self.current_page = 0
        self.page_size = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_page)
        self.timer.start(10000)  # 10 segundos
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Cabeçalho
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)
        header.setStyleSheet("background-color: #FFC107;")  # Amarelo

        logo_label = QLabel("Loja de Revistas")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000;")
        header_layout.addWidget(logo_label)

        search_input = QLineEdit(placeholderText="Pesquisa em toda a loja...")
        search_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333; width: 300px;")
        header_layout.addWidget(search_input)

        header_layout.addStretch()

        btn_account = QPushButton("Minha Conta")
        btn_orders = QPushButton("Meus Pedidos")
        btn_cart = QPushButton("Carrinho")
        btn_cart.clicked.connect(self.view_cart)

        for btn in (btn_account, btn_orders, btn_cart):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #000;
                    padding: 5px 10px;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)

        header_layout.addWidget(btn_account)
        header_layout.addWidget(btn_orders)
        header_layout.addWidget(btn_cart)
        header.setLayout(header_layout)

        # Área de Produtos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.products_container = QWidget()
        self.products_layout = QHBoxLayout()
        self.products_layout.setSpacing(15)
        self.products_layout.setContentsMargins(15, 15, 15, 15)

        self.products_container.setLayout(self.products_layout)
        scroll.setWidget(self.products_container)
        scroll.setStyleSheet("background-color: #ffffff; border: none;")

        # Navegação de Páginas
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)
        self.page_buttons = []
        products = self.product_management_screen.products if self.product_management_screen else []
        num_pages = (len(products) + self.page_size - 1) // self.page_size if products else 1
        for i in range(num_pages):
            btn = QPushButton()
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ccc;
                    border-radius: 50%;
                    width: 10px;
                    height: 10px;
                    margin: 5px;
                    border: none;
                }
                QPushButton:checked {
                    background-color: #000;
                }
            """)
            btn.setCheckable(True)
            if i == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self.go_to_page(idx))
            self.page_buttons.append(btn)
            nav_layout.addWidget(btn)

        # Rodapé
        footer = QWidget()
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(20, 10, 20, 10)
        footer.setStyleSheet("background-color: #F5F5F5;")  # Cinza claro

        delivery_label = QLabel("ENTREGA\nEnviamos para todo o Brasil")
        exchange_label = QLabel("TROCA DE PRODUTOS\nFale conosco")
        installment_label = QLabel("EM ATÉ 3X SEM JUROS\nPara compras acima de R$150")
        payment_label = QLabel("BOLETO E PIX\nPague com toda comodidade")

        for label in (delivery_label, exchange_label, installment_label, payment_label):
            label.setStyleSheet("font-size: 12px; color: #666; text-align: center;")

        footer_layout.addWidget(delivery_label)
        footer_layout.addWidget(exchange_label)
        footer_layout.addWidget(installment_label)
        footer_layout.addWidget(payment_label)
        footer.setLayout(footer_layout)

        main_layout.addWidget(header)
        main_layout.addWidget(scroll)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)
        self.load_products()

    def load_products(self):
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        products = self.product_management_screen.products if self.product_management_screen else []
        if not products:
            no_products_label = QLabel("Nenhum produto cadastrado.")
            no_products_label.setStyleSheet("font-size: 16px; color: #666; text-align: center;")
            self.products_layout.addWidget(no_products_label)
            return

        start_idx = self.current_page * self.page_size
        end_idx = min((self.current_page + 1) * self.page_size, len(products))
        for product_ui in products[start_idx:end_idx]:
            product_widget = self.create_product_widget(product_ui)
            self.products_layout.addWidget(product_widget)

        # Atualizar botões de navegação
        num_pages = (len(products) + self.page_size - 1) // self.page_size
        for btn in self.page_buttons:
            btn.deleteLater()
        self.page_buttons.clear()
        for i in range(num_pages):
            btn = QPushButton()
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ccc;
                    border-radius: 50%;
                    width: 10px;
                    height: 10px;
                    margin: 5px;
                    border: none;
                }
                QPushButton:checked {
                    background-color: #000;
                }
            """)
            btn.setCheckable(True)
            if i == self.current_page:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self.go_to_page(idx))
            self.page_buttons.append(btn)
            self.layout().itemAt(2).layout().addWidget(btn)

    def create_product_widget(self, product_ui):
        product_widget = QWidget()
        product_layout = QVBoxLayout()
        product_layout.setSpacing(5)

        # Etiqueta de Promoção
        discount = 0.15  # 15% de desconto (pode ser ajustado no futuro pelo admin)
        promo_label = QLabel(f"Promoção {int(discount * 100)}% OFF")
        promo_label.setStyleSheet("font-size: 12px; color: #fff; background-color: #27ae60; padding: 4px 8px; border-radius: 3px; text-align: center;")

        # Imagem
        image_label = QLabel()
        if product_ui.imagem:
            pixmap = QPixmap(product_ui.imagem).scaled(100, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Sem imagem")
            image_label.setFixedSize(100, 140)
            image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9; color: #666; text-align: center;")

        # Título
        title_label = QLabel(product_ui.title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333; text-align: center;")
        title_label.setWordWrap(True)  # Permite que o texto quebre em várias linhas se necessário

        # Preços
        original_price = product_ui.price
        discounted_price = original_price * (1 - discount)
        price_label = QLabel(f"De R${original_price:.2f} por <b>R${discounted_price:.2f}</b>")
        price_label.setStyleSheet("font-size: 14px; color: #e74c3c; text-align: center;")

        # Informações de Parcelamento
        extra_info = QLabel(f"1x de R${discounted_price:.2f} sem juros")
        extra_info.setStyleSheet("font-size: 12px; color: #666; text-align: center;")

        # Botão Adicionar ao Carrinho
        add_button = QPushButton("Adicionar ao Carrinho")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #fff;
                padding: 6px;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        add_button.clicked.connect(lambda: self.add_to_cart(product_ui))

        product_layout.addWidget(promo_label)
        product_layout.addWidget(image_label)
        product_layout.addWidget(title_label)
        product_layout.addWidget(price_label)
        product_layout.addWidget(extra_info)
        product_layout.addWidget(add_button)

        product_widget.setLayout(product_layout)
        product_widget.setStyleSheet("background-color: #fff; padding: 5px;")  # Removidas bordas e sombra
        return product_widget

    def next_page(self):
        products = self.product_management_screen.products if self.product_management_screen else []
        if not products:
            return
        self.current_page = (self.current_page + 1) % ((len(products) + self.page_size - 1) // self.page_size)
        self.load_products()
        for i, btn in enumerate(self.page_buttons):
            btn.setChecked(i == self.current_page)

    def go_to_page(self, page):
        self.current_page = page
        self.load_products()
        for i, btn in enumerate(self.page_buttons):
            btn.setChecked(i == self.current_page)
        self.timer.stop()
        self.timer.start(10000)

    def add_to_cart(self, product_ui):
        if product_ui.stock <= 0:
            QMessageBox.warning(self, "Erro", "Produto fora de estoque!")
            return

        quantity, ok = QInputDialog.getInt(self, "Quantidade", "Quantidade:", 1, 1, product_ui.stock)
        if ok:
            self.session.user.adicionarAoCarrinho(product_ui.product, quantity)
            product_ui.stock -= quantity
            self.load_products()
            QMessageBox.information(self, "Sucesso", f"{quantity}x {product_ui.title} adicionado ao carrinho!")

    def view_cart(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        if hasattr(self.stacked_widget, 'cart_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.cart_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela do carrinho não encontrada!")