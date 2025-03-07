from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QListWidget,
                               QLineEdit, QHBoxLayout, QMessageBox, QStackedWidget, QWidget)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Administrador
from models.relatorio import Relatorio
from datetime import datetime

class ReportsScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget, session):
        super().__init__(stacked_widget, return_screen, session)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title_label = QLabel("Relatórios")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.comment_list = QListWidget()
        self.comment_list.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 5px; color: #333;")

        self.title_input = QLineEdit(placeholderText="Título do Relatório")
        self.title_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

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
        layout.addWidget(self.title_input)
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

        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Erro", "Por favor, insira um título para o relatório")
            return

        report = Relatorio(1, title, datetime.now(), datetime.now(), datetime.now())
        report.gerarRelatorio()

        report_content = f"Relatório: {title}\n"
        report_content += f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        report_content += "Comentários:\n"
        for i in range(self.comment_list.count()):
            report_content += f"{self.comment_list.item(i).text()}\n"

        current_date = datetime.now().strftime('%d_%m_%Y')
        filename = f"{title}_{current_date}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            self.comment_list.addItem(
                f"Relatório '{title}' gerado e salvo como {filename} em {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            self.title_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar o relatório: {str(e)}")