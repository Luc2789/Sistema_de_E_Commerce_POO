from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QScrollArea, QFrame, QPushButton, QDialog,
    QMessageBox, QHBoxLayout, QListWidget, QListWidgetItem, QComboBox, QTextEdit
)
from PySide6.QtGui import QPixmap, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QPoint
import sys
from variaveis import*

# Banco de dados simulado (em memória)
usuarios = []
carrinhos = {}
pedidos = []
mangas = [
    {"titulo": "One Piece", "capa": one, "preco": 50.0},
    {"titulo": "Naruto", "capa": naruto, "preco": 45.0},
    {"titulo": "Bleach", "capa": bleach, "preco": 40.0},
    {"titulo": "Attack on Titan", "capa": at, "preco": 60.0},
    {"titulo": "Death Note", "capa": no, "preco": 35.0},
    {"titulo": "Demon Slayer", "capa": de, "preco": 55.0},
]

# Janela de Login e Cadastro
class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login / Cadastro")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome (Cadastro)")
        self.nome_input.setVisible(False)
        
        self.botao_login = QPushButton("Login")
        self.botao_login.clicked.connect(self.fazer_login)
        
        self.botao_cadastro = QPushButton("Cadastrar")
        self.botao_cadastro.clicked.connect(self.mostrar_cadastro)
        
        self.botao_confirmar_cadastro = QPushButton("Confirmar Cadastro")
        self.botao_confirmar_cadastro.clicked.connect(self.fazer_cadastro)
        self.botao_confirmar_cadastro.setVisible(False)
        
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(self.nome_input)
        layout.addWidget(self.botao_login)
        layout.addWidget(self.botao_cadastro)
        layout.addWidget(self.botao_confirmar_cadastro)
        
        self.setLayout(layout)
    
    def fazer_login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()
        
        # Verifica se é o administrador
        if email == "wesley" or email == "luciano" or email == "abrahao" or email == "jonathan" or email == "fabricio" and senha == "123":
            self.parent().usuario_logado = {"nome": "Admin", "email": email, "senha": "123", "admin": True}
            self.parent().atualizar_interface()
            QMessageBox.information(self, "Sucesso", "Login como administrador realizado com sucesso!")
            self.close()
            return
        
        for usuario in usuarios:
            if usuario["email"] == email and usuario["senha"] == senha:
                QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
                self.parent().usuario_logado = usuario
                self.parent().atualizar_interface()
                self.close()
                return
        
        QMessageBox.warning(self, "Erro", "E-mail ou senha inválidos.")
    
    def mostrar_cadastro(self):
        self.nome_input.setVisible(True)
        self.botao_confirmar_cadastro.setVisible(True)
        self.botao_login.setVisible(False)
        self.botao_cadastro.setVisible(False)
    
    def fazer_cadastro(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        senha = self.senha_input.text()
        
        if not nome or not email or not senha:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return
        
        for usuario in usuarios:
            if usuario["email"] == email:
                QMessageBox.warning(self, "Erro", "E-mail já cadastrado.")
                return
        
        novo_usuario = {"nome": nome, "email": email, "senha": senha, "admin": False}
        usuarios.append(novo_usuario)
        carrinhos[email] = []
        QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
        self.close()

# Janela do Carrinho de Compras
class CarrinhoWindow(QDialog):
    def __init__(self, usuario_logado, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Carrinho de Compras")
        self.setGeometry(200, 200, 400, 300)
        
        self.usuario_logado = usuario_logado
        self.carrinho = carrinhos[usuario_logado["email"]]
        
        layout = QVBoxLayout()
        
        self.lista_carrinho = QListWidget()
        self.atualizar_lista_carrinho()
        
        self.botao_remover = QPushButton("Remover Item")
        self.botao_remover.clicked.connect(self.remover_item)
        
        self.botao_finalizar = QPushButton("Finalizar Compra")
        self.botao_finalizar.clicked.connect(self.finalizar_compra)
        
        layout.addWidget(self.lista_carrinho)
        layout.addWidget(self.botao_remover)
        layout.addWidget(self.botao_finalizar)
        
        self.setLayout(layout)
    
    def atualizar_lista_carrinho(self):
        self.lista_carrinho.clear()
        for item in self.carrinho:
            self.lista_carrinho.addItem(QListWidgetItem(f"{item['titulo']} - R${item['preco']:.2f}"))
    
    def remover_item(self):
        item_selecionado = self.lista_carrinho.currentItem()
        if item_selecionado:
            titulo = item_selecionado.text().split(" - ")[0]
            self.carrinho = [item for item in self.carrinho if item["titulo"] != titulo]
            carrinhos[self.usuario_logado["email"]] = self.carrinho
            self.atualizar_lista_carrinho()
    
    def finalizar_compra(self):
        if not self.carrinho:
            QMessageBox.warning(self, "Erro", "O carrinho está vazio.")
            return
        
        self.finalizar_window = FinalizarCompraWindow(self.usuario_logado, self.carrinho, self)
        self.finalizar_window.exec()

# Janela de Finalização de Compra
class FinalizarCompraWindow(QDialog):
    def __init__(self, usuario_logado, carrinho, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Finalizar Compra")
        self.setGeometry(200, 200, 400, 300)
        
        self.usuario_logado = usuario_logado
        self.carrinho = carrinho
        
        layout = QVBoxLayout()
        
        self.endereco_input = QTextEdit()
        self.endereco_input.setPlaceholderText("Digite seu endereço completo")
        
        self.forma_pagamento = QComboBox()
        self.forma_pagamento.addItems(["Cartão de Crédito", "Boleto", "Pix"])
        
        self.botao_confirmar = QPushButton("Confirmar Compra")
        self.botao_confirmar.clicked.connect(self.confirmar_compra)
        
        layout.addWidget(QLabel("Endereço de Entrega:"))
        layout.addWidget(self.endereco_input)
        layout.addWidget(QLabel("Forma de Pagamento:"))
        layout.addWidget(self.forma_pagamento)
        layout.addWidget(self.botao_confirmar)
        
        self.setLayout(layout)
    
    def confirmar_compra(self):
        endereco = self.endereco_input.toPlainText()
        forma_pagamento = self.forma_pagamento.currentText()
        
        if not endereco:
            QMessageBox.warning(self, "Erro", "O endereço é obrigatório.")
            return
        
        total = sum(item["preco"] for item in self.carrinho)
        pedido = {
            "usuario": self.usuario_logado["email"],
            "itens": self.carrinho,
            "endereco": endereco,
            "forma_pagamento": forma_pagamento,
            "total": total,
            "status": "Processando"
        }
        pedidos.append(pedido)
        carrinhos[self.usuario_logado["email"]] = []
        QMessageBox.information(self, "Sucesso", "Compra finalizada com sucesso!")
        self.close()

# Janela de Status de Pedidos
class StatusPedidosWindow(QDialog):
    def __init__(self, usuario_logado, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Meus Pedidos")
        self.setGeometry(200, 200, 500, 400)
        
        self.usuario_logado = usuario_logado
        
        layout = QVBoxLayout()
        
        self.lista_pedidos = QListWidget()
        self.atualizar_lista_pedidos()
        
        layout.addWidget(self.lista_pedidos)
        
        self.setLayout(layout)
    
    def atualizar_lista_pedidos(self):
        self.lista_pedidos.clear()
        for pedido in pedidos:
            if pedido["usuario"] == self.usuario_logado["email"]:
                itens = ", ".join(item["titulo"] for item in pedido["itens"])
                status = pedido["status"]
                self.lista_pedidos.addItem(QListWidgetItem(f"Itens: {itens}\nStatus: {status}"))

# Janela de Administração
class AdminWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Painel de Administração")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        self.lista_pedidos = QListWidget()
        self.atualizar_lista_pedidos()
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Processando", "Saiu para entrega", "Entregue"])
        
        self.botao_atualizar_status = QPushButton("Atualizar Status")
        self.botao_atualizar_status.clicked.connect(self.atualizar_status)
        
        self.botao_adicionar_manga = QPushButton("Adicionar Mangá")
        self.botao_adicionar_manga.clicked.connect(self.adicionar_manga)
        
        layout.addWidget(QLabel("Pedidos:"))
        layout.addWidget(self.lista_pedidos)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_combo)
        layout.addWidget(self.botao_atualizar_status)
        layout.addWidget(self.botao_adicionar_manga)
        
        self.setLayout(layout)
    
    def atualizar_lista_pedidos(self):
        self.lista_pedidos.clear()
        for pedido in pedidos:
            self.lista_pedidos.addItem(QListWidgetItem(f"{pedido['usuario']} - R${pedido['total']:.2f} - {pedido['status']}"))
    
    def atualizar_status(self):
        pedido_selecionado = self.lista_pedidos.currentItem()
        if pedido_selecionado:
            index = self.lista_pedidos.row(pedido_selecionado)
            pedidos[index]["status"] = self.status_combo.currentText()
            self.atualizar_lista_pedidos()
    
    def adicionar_manga(self):
        self.adicionar_manga_window = AdicionarMangaWindow(self)
        self.adicionar_manga_window.exec()
        
    def atualizar_mangas(self):
        # Atualiza a lista de mangás na interface
        self.parent().display_mangas()

# Janela para Adicionar Mangá
class AdicionarMangaWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Mangá")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título")
        
        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço")
        
        self.botao_confirmar = QPushButton("Adicionar")
        self.botao_confirmar.clicked.connect(self.confirmar_adicao)
        
        layout.addWidget(self.titulo_input)
        layout.addWidget(self.preco_input)
        layout.addWidget(self.botao_confirmar)
        
        self.setLayout(layout)
    
    def confirmar_adicao(self):
        titulo = self.titulo_input.text()
        preco = self.preco_input.text()
        
        if not titulo or not preco:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return
        
        try:
            preco = float(preco)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço inválido.")
            return
        
        novo_manga = {"titulo": titulo, "capa": "default.jpg", "preco": preco}
        mangas.append(novo_manga)
        
        # Atualiza a tela principal após adicionar o mangá
        self.parent().atualizar_mangas()
        
        QMessageBox.information(self, "Sucesso", "Mangá adicionado com sucesso!")
        self.close()

# Janela Principal (MangaSearchApp)
class MangaSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planeta Mangá")
        self.setGeometry(100, 100, 1000, 600)
        
        self.usuario_logado = None
        
        # Definir um gradiente de fundo para a janela
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        gradient.setColorAt(0, QColor(100, 150, 255))  # Azul claro
        gradient.setColorAt(1, QColor(150, 100, 255))  # Roxo claro
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Barra de pesquisa
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Pesquisar mangá...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.textChanged.connect(self.filter_mangas)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #ff7f50;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #ff4500;
            }
        """)
        layout.addWidget(self.search_bar)
        
        # Botão de Login
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.login_button.clicked.connect(self.abrir_janela_login)
        layout.addWidget(self.login_button)
        
        # Botão do Carrinho
        self.carrinho_button = QPushButton("Carrinho")
        self.carrinho_button.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.carrinho_button.clicked.connect(self.abrir_carrinho)
        self.carrinho_button.setVisible(False)
        layout.addWidget(self.carrinho_button)
        
        # Botão de Meus Pedidos
        self.pedidos_button = QPushButton("Meus Pedidos")
        self.pedidos_button.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.pedidos_button.clicked.connect(self.abrir_status_pedidos)
        self.pedidos_button.setVisible(False)
        layout.addWidget(self.pedidos_button)
        
        # Botão de Administração
        self.admin_button = QPushButton("Admin")
        self.admin_button.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.admin_button.clicked.connect(self.abrir_admin)
        self.admin_button.setVisible(False)
        layout.addWidget(self.admin_button)
        
        # Botão de Logoff
        self.logoff_button = QPushButton("Logoff")
        self.logoff_button.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        self.logoff_button.clicked.connect(self.fazer_logoff)
        self.logoff_button.setVisible(False)
        layout.addWidget(self.logoff_button)
        
        # Área de rolagem para os mangás
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
        
        # Exibir mangás
        self.display_mangas()
    
    def display_mangas(self, filtered_mangas=None):
        # Remove widgets anteriores
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        mangas_to_display = filtered_mangas if filtered_mangas else mangas
        
        for index, manga in enumerate(mangas_to_display):
            row, col = divmod(index, 3)
            manga_widget = self.create_manga_widget(manga)
            self.grid_layout.addWidget(manga_widget, row, col)
    
    def create_manga_widget(self, manga):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #ddd;
            }
            QFrame:hover {
                border: 2px solid #ff7f50;
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ff7f50, stop: 1 #ff4500
                );
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container.setLayout(container_layout)
        
        # Imagem da capa
        label_image = QLabel()
        pixmap = QPixmap(manga["capa"])
        if pixmap.isNull():
            pixmap = QPixmap(100, 150)
            pixmap.fill(Qt.darkGray)
        label_image.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_image.setAlignment(Qt.AlignCenter)
        
        # Título do mangá
        label_title = QLabel(manga["titulo"])
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)
        
        # Preço do mangá
        label_preco = QLabel(f"R${manga['preco']:.2f}")
        label_preco.setAlignment(Qt.AlignCenter)
        label_preco.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
            }
        """)
        
        # Botão para adicionar ao carrinho
        botao_adicionar = QPushButton("Adicionar ao Carrinho")
        botao_adicionar.clicked.connect(lambda _, m=manga: self.adicionar_ao_carrinho(m))
        botao_adicionar.setStyleSheet("""
            QPushButton {
                background-color: #ff7f50;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff4500;
            }
        """)
        
        container_layout.addWidget(label_image)
        container_layout.addWidget(label_title)
        container_layout.addWidget(label_preco)
        container_layout.addWidget(botao_adicionar)
        
        return container
    
    def filter_mangas(self):
        text = self.search_bar.text().lower()
        filtered = [manga for manga in mangas if text in manga["titulo"].lower()]
        self.display_mangas(filtered)
    
    def abrir_janela_login(self):
        self.login_window = LoginWindow(self)
        self.login_window.exec()
    
    def abrir_carrinho(self):
        if self.usuario_logado:
            self.carrinho_window = CarrinhoWindow(self.usuario_logado, self)
            self.carrinho_window.exec()
    
    def abrir_status_pedidos(self):
        if self.usuario_logado:
            self.status_pedidos_window = StatusPedidosWindow(self.usuario_logado, self)
            self.status_pedidos_window.exec()
    
    def abrir_admin(self):
        if self.usuario_logado and self.usuario_logado["admin"]:
            self.admin_window = AdminWindow(self)
            self.admin_window.exec()
    
    def fazer_logoff(self):
        self.usuario_logado = None
        self.atualizar_interface()
        QMessageBox.information(self, "Logoff", "Você foi desconectado.")
    
    def adicionar_ao_carrinho(self, manga):
        if self.usuario_logado:
            carrinhos[self.usuario_logado["email"]].append(manga)
            QMessageBox.information(self, "Sucesso", f"{manga['titulo']} adicionado ao carrinho!")
        else:
            QMessageBox.warning(self, "Erro", "Faça login para adicionar itens ao carrinho.")
    
    def atualizar_interface(self):
        if self.usuario_logado:
            self.login_button.setVisible(False)
            self.carrinho_button.setVisible(True)
            self.pedidos_button.setVisible(True)
            self.logoff_button.setVisible(True)
            if self.usuario_logado["admin"]:
                self.admin_button.setVisible(True)
        else:
            self.login_button.setVisible(True)
            self.carrinho_button.setVisible(False)
            self.pedidos_button.setVisible(False)
            self.admin_button.setVisible(False)
            self.logoff_button.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MangaSearchApp()
    window.show()
    sys.exit(app.exec())