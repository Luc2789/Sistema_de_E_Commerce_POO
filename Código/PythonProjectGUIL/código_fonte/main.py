from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QScrollArea, QFrame, QPushButton, QDialog
from PySide6.QtGui import QPixmap, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QPoint
import sys
from variaveis import *



# Janela de Login (simples)
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 300, 150)
        
        layout = QVBoxLayout()
        
        # Exemplo de conteúdo da janela de login
        label = QLabel("Faça login para continuar")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        self.setLayout(layout)

# Janela Principal (MangaSearchApp)
class MangaSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planeta Mangá")
        self.setGeometry(100, 100, 1000, 600)
        
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
        
        # Lista de mangás (simulada)
        self.mangas = [
            ("One Piece", one),
            ("Naruto", naruto),
            ("Bleach", bleach),
            ("Attack on Titan", at),
            ("Death Note", no),
            ("Demon Slayer", de)
        ]
        
        self.display_mangas()
    
    def display_mangas(self, filtered_mangas=None):
        # Remove widgets anteriores
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        mangas_to_display = filtered_mangas if filtered_mangas else self.mangas
        
        for index, (title, cover) in enumerate(mangas_to_display):
            row, col = divmod(index, 3)
            manga_widget = self.create_manga_widget(title, cover)
            self.grid_layout.addWidget(manga_widget, row, col)
    
    def create_manga_widget(self, title, cover_path):
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
        pixmap = QPixmap(str(cover_path))  # Converte Path para string para evitar problemas
        if pixmap.isNull():
            pixmap = QPixmap(100, 150)
            pixmap.fill(Qt.darkGray)
        label_image.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_image.setAlignment(Qt.AlignCenter)
        
        # Título do mangá
        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)
        
        container_layout.addWidget(label_image)
        container_layout.addWidget(label_title)
        
        return container
    
    def filter_mangas(self):
        text = self.search_bar.text().lower()
        filtered = [(title, cover) for title, cover in self.mangas if text in title.lower()]
        self.display_mangas(filtered)
    
    def abrir_janela_login(self):
        # Abre a janela de login
        self.login_window = LoginWindow()
        self.login_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MangaSearchApp()
    window.show()
    sys.exit(app.exec())