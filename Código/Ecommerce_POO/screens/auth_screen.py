from PySide6.QtWidgets import (QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox, QStackedWidget, QWidget)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from models.usuario import Cliente, Administrador

class AuthScreen(BaseScreen):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget | None, client_dashboard_screen: QWidget, session):
        super().__init__(stacked_widget, return_screen, session)
        self.client_dashboard_screen = client_dashboard_screen
        self.users = [
            Cliente(1, "Cliente", "client@example.com", "client123", "123456789"),
            Administrador(2, "Admin", "admin@example.com", "admin123", "987654321")
        ]  # Lista de usuários para simular um "banco de dados"
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Lado Esquerdo - Fazer Login
        login_widget = QWidget()
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignTop)

        login_title = QLabel("Fazer Login")
        login_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")

        login_subtitle = QLabel("Clientes Registrados")
        login_subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")

        login_desc = QLabel("Se você tiver uma conta, acesse com seu endereço de e-mail e senha.")
        login_desc.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 20px;")

        self.email_input = QLineEdit(placeholderText="E-mail *")
        self.password_input = QLineEdit(placeholderText="Senha *")
        self.password_input.setEchoMode(QLineEdit.Password)

        for field in (self.email_input, self.password_input):
            field.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        show_password = QPushButton("Mostrar Senha?")
        show_password.setStyleSheet("font-size: 12px; color: #e74c3c; background: none; border: none; text-decoration: underline;")
        show_password.clicked.connect(lambda: self.toggle_password())

        btn_login = QPushButton("Entrar")
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: #fff;
                padding: 10px;
                border: none;
                border-radius: 4px;
                width: 100%;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        btn_login.clicked.connect(self.login)

        forgot_password = QLabel("<a href='#' style='color: #e74c3c;'>Esqueceu a sua senha?</a>")
        forgot_password.setOpenExternalLinks(False)
        forgot_password.linkActivated.connect(lambda: QMessageBox.information(self, "Info", "Funcionalidade não implementada!"))

        login_layout.addWidget(login_title)
        login_layout.addWidget(login_subtitle)
        login_layout.addWidget(login_desc)
        login_layout.addWidget(self.email_input)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(show_password)
        login_layout.addWidget(btn_login)
        login_layout.addWidget(forgot_password)
        login_layout.addStretch()
        login_widget.setLayout(login_layout)
        login_widget.setStyleSheet("background-color: #fff; padding: 20px; border: none;")  # Removido a borda

        # Lado Direito - Novos Clientes
        register_widget = QWidget()
        register_layout = QVBoxLayout()
        register_layout.setAlignment(Qt.AlignTop)

        register_title = QLabel("Novos Clientes")
        register_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")

        register_desc = QLabel("Criar uma nova conta tem muitos benefícios: fechar pedidos mais rapidamente, registrar mais endereços, acompanhar pedidos e muito mais.")
        register_desc.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 20px;")

        self.register_name = QLineEdit(placeholderText="Nome *")
        self.register_email = QLineEdit(placeholderText="E-mail *")
        self.register_password = QLineEdit(placeholderText="Senha *")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_cpf = QLineEdit(placeholderText="CPF *")

        for field in (self.register_name, self.register_email, self.register_password, self.register_cpf):
            field.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 4px; color: #333;")

        btn_register = QPushButton("Criar Conta")
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: #000;
                color: #fff;
                padding: 10px;
                border: none;
                border-radius: 4px;
                width: 100%;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        btn_register.clicked.connect(self.register)

        register_layout.addWidget(register_title)
        register_layout.addWidget(register_desc)
        register_layout.addWidget(self.register_name)
        register_layout.addWidget(self.register_email)
        register_layout.addWidget(self.register_password)
        register_layout.addWidget(self.register_cpf)
        register_layout.addWidget(btn_register)
        register_layout.addStretch()
        register_widget.setLayout(register_layout)
        register_widget.setStyleSheet("background-color: #fff; padding: 20px; border: none;")  # Removido a borda

        layout.addWidget(login_widget)
        layout.addWidget(register_widget)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ffffff;")  # Fundo branco para toda a janela

    def toggle_password(self):
        self.password_input.setEchoMode(QLineEdit.Normal if self.password_input.echoMode() == QLineEdit.Password else QLineEdit.Password)

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        user = next((u for u in self.users if u.email == email and u.senha == password), None)

        if user:
            self.session.user = user
            if isinstance(user, Cliente) and self.client_dashboard_screen:
                self.stacked_widget.setCurrentWidget(self.client_dashboard_screen)
            elif isinstance(user, Administrador) and self.return_screen:
                self.stacked_widget.setCurrentWidget(self.return_screen)
            else:
                QMessageBox.warning(self, "Erro", "Tela de destino não encontrada!")
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha incorretos!")

    def register(self):
        name = self.register_name.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()
        cpf = self.register_cpf.text().strip()

        if not all([name, email, password, cpf]):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")
            return

        if any(u.email == email for u in self.users):
            QMessageBox.warning(self, "Erro", "Email já cadastrado!")
            return

        new_user = Cliente(len(self.users) + 1, name, email, password, cpf)
        self.users.append(new_user)
        QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso! Faça login para continuar.")
        self.register_name.clear()
        self.register_email.clear()
        self.register_password.clear()
        self.register_cpf.clear()