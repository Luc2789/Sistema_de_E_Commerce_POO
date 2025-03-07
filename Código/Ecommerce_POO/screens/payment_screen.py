from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QFormLayout,
                               QLineEdit, QComboBox, QMessageBox, QStackedWidget, QWidget, QHBoxLayout)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Cliente
from models.endereco import Endereco
from models.pagamento import Pagamento
from models.entrega import Entrega
from datetime import datetime, timedelta
from ui_data import OrderUI

class PaymentScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, client_dashboard_screen: QWidget, session):
        super().__init__(stacked_widget, return_screen, session)
        self.client_dashboard_screen = client_dashboard_screen
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Finalizar Compra")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")

        form_layout = QFormLayout()
        self.cep_input = QLineEdit(placeholderText="CEP (ex: 12345-678)")
        self.logradouro_type_input = QLineEdit(placeholderText="Tipo de Logradouro (ex: Rua)")
        self.logradouro_input = QLineEdit(placeholderText="Logradouro (ex: Avenida Brasil)")
        self.bairro_input = QLineEdit(placeholderText="Bairro")
        self.estado_input = QLineEdit(placeholderText="Estado (ex: SP)")
        self.municipio_input = QLineEdit(placeholderText="Município")

        for field in (self.cep_input, self.logradouro_type_input, self.logradouro_input, self.bairro_input,
                      self.estado_input, self.municipio_input):
            field.setStyleSheet("padding: 8px; border: 2px solid #3498db; border-radius: 5px; color: #2c3e50; background-color: #ecf0f1;")

        self.payment_method = QComboBox()
        self.payment_method.addItems(["PIX", "Boleto", "Cartão"])
        self.payment_method.setStyleSheet("padding: 8px; border: 2px solid #3498db; border-radius: 5px; color: #2c3e50; background-color: #ecf0f1;")

        btn_layout = QHBoxLayout()
        btn_confirm = QPushButton("Confirmar Pagamento")
        btn_back = QPushButton("Voltar")

        for btn in (btn_confirm, btn_back):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: #ffffff;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)

        btn_confirm.clicked.connect(self.confirm_payment)
        btn_back.clicked.connect(self.go_back_to_dashboard)

        form_layout.addRow(QLabel("CEP:"), self.cep_input)
        form_layout.addRow(QLabel("Tipo de Logradouro:"), self.logradouro_type_input)
        form_layout.addRow(QLabel("Logradouro:"), self.logradouro_input)
        form_layout.addRow(QLabel("Bairro:"), self.bairro_input)
        form_layout.addRow(QLabel("Estado:"), self.estado_input)
        form_layout.addRow(QLabel("Município:"), self.municipio_input)
        form_layout.addRow(QLabel("Método de Pagamento:"), self.payment_method)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        btn_layout.addWidget(btn_confirm)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f9f9f9;")

    def go_back_to_dashboard(self):
        if self.client_dashboard_screen:
            self.stacked_widget.setCurrentWidget(self.client_dashboard_screen)
        else:
            QMessageBox.warning(self, "Erro", "Tela do cliente não encontrada!")

    def confirm_payment(self):
        if not self.session.user or not isinstance(self.session.user, Cliente):
            QMessageBox.warning(self, "Erro", "Usuário não logado ou não é cliente")
            return
        if not self.session.user.carrinho.itens:
            QMessageBox.warning(self, "Erro", "Seu carrinho está vazio!")
            return

        cep = self.cep_input.text().strip()
        logradouro_type = self.logradouro_type_input.text().strip()
        logradouro = self.logradouro_input.text().strip()
        bairro = self.bairro_input.text().strip()
        estado = self.estado_input.text().strip()
        municipio = self.municipio_input.text().strip()
        payment_method = self.payment_method.currentText()

        if not all([cep, logradouro_type, logradouro, bairro, estado, municipio]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos de endereço!")
            return

        endereco = Endereco(1, logradouro, cep, logradouro_type, bairro, municipio, estado, cep)
        pedido = self.session.user.finalizarCompra(endereco)
        if pedido:
            pagamento = Pagamento(1, pedido, pedido.calcularTotal(), payment_method, "PENDENTE")
            entrega = Entrega(1, pedido, datetime.now(), datetime.now() + timedelta(days=5), "", "AGUARDANDO_ENVIO")
            pedido.setPagamento(pagamento)
            pedido.setEntrega(entrega)

            if payment_method == "PIX":
                pagamento.processarPagamento(approved=True)
                pedido.atualizarStatus("PAGO")
                entrega.atualizarStatusEntrega("EM_TRANSITO")
                QMessageBox.information(self, "Sucesso", f"Pagamento via PIX aprovado! Pedido {pedido.pedido_id} criado.")
            else:
                pagamento.processarPagamento(approved=False)
                pedido.atualizarStatus("PENDENTE")
                QMessageBox.information(self, "Sucesso", f"Pagamento via {payment_method} pendente. Aguardando aprovação do administrador. Pedido {pedido.pedido_id} criado.")

            if hasattr(self.stacked_widget, 'order_screen') and hasattr(self.stacked_widget.order_screen, 'orders'):
                order_ui = OrderUI(pedido.pedido_id, self.session.user.nome, pedido.status, pedido.calcularTotal(), pedido)
                self.stacked_widget.order_screen.orders.append(order_ui)
                if hasattr(self.stacked_widget.order_screen, 'order_list') and hasattr(self.stacked_widget.order_screen, 'format_order_display'):
                    self.stacked_widget.order_screen.order_list.addItem(self.stacked_widget.order_screen.format_order_display(order_ui))
            self.stacked_widget.setCurrentWidget(self.client_dashboard_screen)