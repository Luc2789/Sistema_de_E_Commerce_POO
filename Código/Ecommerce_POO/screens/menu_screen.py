from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QStackedWidget, QWidget, QMessageBox, QLineEdit)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Administrador

class MenuScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, session):
        super().__init__(stacked_widget, None, session)
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

        logo_label = QLabel("Comic Book Shop")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #000;")
        header_layout.addWidget(logo_label)

        search_input = QLineEdit(placeholderText="Pesquisa em toda a loja...")
        search_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333; width: 300px;")
        header_layout.addWidget(search_input)

        header_layout.addStretch()

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        btn_logout.setStyleSheet("""
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
        header_layout.addWidget(btn_logout)
        header.setLayout(header_layout)

        # Área Principal
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Menu Principal - Administrador")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")

        btn_products = QPushButton("Gerenciar Produtos")
        btn_orders = QPushButton("Gerenciar Pedidos")
        btn_reports = QPushButton("Relatórios")

        for btn in (btn_products, btn_orders, btn_reports):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)

        btn_products.clicked.connect(self.go_to_products)
        btn_orders.clicked.connect(self.go_to_orders)
        btn_reports.clicked.connect(self.go_to_reports)

        content_layout.addWidget(title_label)
        content_layout.addWidget(btn_products)
        content_layout.addWidget(btn_orders)
        content_layout.addWidget(btn_reports)
        content_layout.addStretch()

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
        main_layout.addLayout(content_layout)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def go_to_products(self):
        if not self.session.user or not isinstance(self.session.user, Administrador):
            QMessageBox.warning(self, "Erro", "Apenas administradores podem acessar esta tela!")
            return
        if hasattr(self.stacked_widget, 'product_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.product_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela de gerenciamento de produtos não encontrada!")

    def go_to_orders(self):
        if not self.session.user or not isinstance(self.session.user, Administrador):
            QMessageBox.warning(self, "Erro", "Apenas administradores podem acessar esta tela!")
            return
        if hasattr(self.stacked_widget, 'order_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.order_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela de gerenciamento de pedidos não encontrada!")

    def go_to_reports(self):
        if not self.session.user or not isinstance(self.session.user, Administrador):
            QMessageBox.warning(self, "Erro", "Apenas administradores podem acessar esta tela!")
            return
        if hasattr(self.stacked_widget, 'reports_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.reports_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela de relatórios não encontrada!")

    def logout(self):
        self.session.user = None
        if hasattr(self.stacked_widget, 'auth_screen'):
            self.stacked_widget.setCurrentWidget(self.stacked_widget.auth_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela de autenticação não encontrada!")