from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget, QWidget, QMessageBox, QFormLayout, QListWidget, QFileDialog)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.produto import Produto, Categoria
from ui_data import ProductUI

class ProductManagementScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, session):
        super().__init__(stacked_widget, return_screen, session)
        self.products = []
        self.categories = [Categoria(i, f"Cat{i}", f"Descrição {i}") for i in range(1, 4)]
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

        self.imagem_label = QLabel("Nenhuma imagem selecionada")
        self.imagem_label.setStyleSheet("color: #666; font-size: 14px;")
        self.imagem_path = None
        btn_select_image = QPushButton("Selecionar Imagem")
        btn_select_image.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_select_image.clicked.connect(self.select_image)

        for field in self.input_fields.values():
            field.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        for label, field in [
            ("Título", self.input_fields['title']),
            ("Autor", self.input_fields['author']),
            ("Categoria", self.input_fields['category']),
            ("Estoque", self.input_fields['stock']),
            ("Preço", self.input_fields['price']),
        ]:
            form_layout.addRow(QLabel(label), field)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.imagem_label)
        image_layout.addWidget(btn_select_image)
        form_layout.addRow(QLabel("Imagem"), image_layout)

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

        layout.addWidget(title_label)
        layout.addWidget(self.product_list)
        layout.addLayout(form_layout)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "",
                                                   "Imagens (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.imagem_path = file_name
            self.imagem_label.setText(file_name.split("\\")[-1])
        else:
            self.imagem_label.setText("Nenhuma imagem selecionada")
            self.imagem_path = None

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
                              f"Descrição de {product_data['title']}", price, category, self.imagem_path)
            product.atualizarEstoque(stock)
            product_ui = ProductUI(product_data['title'], product_data['author'],
                                   product_data['category'], stock, price, self.imagem_path, product)
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

    def format_product_display(self, product) -> str:
        return f"{product.title} - {product.author} ({product.category}) | Estoque: {product.stock} | Preço: R${product.price:.2f}"

    def clear_inputs(self):
        for field in self.input_fields.values():
            field.clear()
        self.imagem_label.setText("Nenhuma imagem selecionada")
        self.imagem_path = None