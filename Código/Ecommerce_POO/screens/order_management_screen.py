from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QListWidget,
                               QFormLayout, QMessageBox, QStackedWidget, QWidget, QLineEdit, QHBoxLayout)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Cliente, Administrador
from models.endereco import Endereco
from datetime import datetime
from ui_data import OrderUI

class OrderManagementScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, session):
        super().__init__(stacked_widget, return_screen, session)
        self.orders = []
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
            'status': QLineEdit(placeholderText="Status do Pedido"),
            'payment_status': QLineEdit(placeholderText="Status do Pagamento")
        }
        for field in self.input_fields.values():
            field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Pedido")
        btn_update_status = QPushButton("Atualizar Status")
        btn_approve_payment = QPushButton("Aprovar Pagamento")
        btn_reject_payment = QPushButton("Rejeitar Pagamento")
        btn_calculate = QPushButton("Calcular Total")
        btn_back = QPushButton("Voltar")

        for btn in (btn_add, btn_update_status, btn_approve_payment, btn_reject_payment, btn_calculate, btn_back):
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
        btn_update_status.clicked.connect(self.update_status)
        btn_approve_payment.clicked.connect(self.approve_payment)
        btn_reject_payment.clicked.connect(self.reject_payment)
        btn_calculate.clicked.connect(self.calculate_total)
        btn_back.clicked.connect(self.go_back)

        for label, field in [
            ("Cliente", self.input_fields['customer']),
            ("Endereço", self.input_fields['address']),
            ("Status", self.input_fields['status']),
            ("Status Pagamento", self.input_fields['payment_status'])
        ]:
            form_layout.addRow(QLabel(label), field)

        layout.addWidget(title_label)
        layout.addWidget(self.order_list)
        layout.addLayout(form_layout)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update_status)
        btn_layout.addWidget(btn_approve_payment)
        btn_layout.addWidget(btn_reject_payment)
        btn_layout.addWidget(btn_calculate)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_order(self):
        try:
            if not self.session.user or not isinstance(self.session.user, Administrador):
                raise ValueError("Apenas administradores podem adicionar pedidos")

            order_data = {key: field.text().strip() for key, field in self.input_fields.items()}
            if not all(order_data.values()):
                raise ValueError("Todos os campos devem ser preenchidos")

            cliente_temp = Cliente(0, order_data['customer'], f"{order_data['customer']}@example.com", "123", "0000000000")
            address = Endereco(len(self.orders) + 1, order_data['address'], "123", "", "Bairro", "Cidade", "Estado", "12345-678")
            from models.pedido import Pedido
            order = Pedido(len(self.orders) + 1, cliente_temp, datetime.now(), [], address, order_data['status'])
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

    def approve_payment(self):
        current_item = self.order_list.currentItem()
        if current_item:
            order_id = int(current_item.text().split()[1])
            order_ui = next((o for o in self.orders if o.order_id == order_id), None)
            if order_ui and order_ui.order and hasattr(order_ui.order, 'pagamento'):
                if order_ui.order.pagamento.status_pagamento == "PENDENTE":
                    order_ui.order.pagamento.processarPagamento(approved=True)
                    order_ui.order.atualizarStatus("PAGO")
                    order_ui.status = "PAGO"
                    current_item.setText(self.format_order_display(order_ui))
                    QMessageBox.information(self, "Sucesso", f"Pagamento do Pedido {order_id} aprovado!")
                else:
                    QMessageBox.warning(self, "Erro", "O pagamento já foi processado!")
            else:
                QMessageBox.warning(self, "Erro", "Nenhum pagamento associado a este pedido!")

    def reject_payment(self):
        current_item = self.order_list.currentItem()
        if current_item:
            order_id = int(current_item.text().split()[1])
            order_ui = next((o for o in self.orders if o.order_id == order_id), None)
            if order_ui and order_ui.order and hasattr(order_ui.order, 'pagamento'):
                if order_ui.order.pagamento.status_pagamento == "PENDENTE":
                    order_ui.order.pagamento.processarPagamento(approved=False)
                    order_ui.order.atualizarStatus("CANCELADO")
                    order_ui.status = "CANCELADO"
                    current_item.setText(self.format_order_display(order_ui))
                    QMessageBox.information(self, "Sucesso", f"Pagamento do Pedido {order_id} rejeitado!")
                else:
                    QMessageBox.warning(self, "Erro", "O pagamento já foi processado!")
            else:
                QMessageBox.warning(self, "Erro", "Nenhum pagamento associado a este pedido!")

    def calculate_total(self):
        current_item = self.order_list.currentItem()
        if current_item:
            order_id = int(current_item.text().split()[1])
            order_ui = next((o for o in self.orders if o.order_id == order_id), None)
            if order_ui and order_ui.order:
                total = order_ui.order.calcularTotal()
                order_ui.total = total
                QMessageBox.information(self, "Total", f"Total do Pedido {order_id}: R${total:.2f}")
            else:
                QMessageBox.warning(self, "Erro", "Pedido não encontrado!")

    def format_order_display(self, order) -> str:
        payment_status = order.order.pagamento.status_pagamento if hasattr(order.order, 'pagamento') and order.order.pagamento else "N/A"
        return f"Pedido {order.order_id} - {order.customer} - {order.status} (Pagamento: {payment_status})"

    def clear_inputs(self):
        for field in self.input_fields.values():
            field.clear()