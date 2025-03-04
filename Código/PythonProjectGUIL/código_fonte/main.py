import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMainWindow, QLineEdit
from window import MainWindow
from testDisplay import display
from PySide6.QtCore import Qt
from quadros import quadro
from PySide6.QtWidgets import QSpacerItem, QSizePolicy


if __name__ == '__main__':
     app = QApplication()
     window = MainWindow()
     
     # barra_pesquisa
     dis = display()
     dis.setPlaceholderText('pesquise aqui')
   

# Adicionando a barra de pesquisa
     window.grade_Layout.addWidget(dis, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
     lista_manga = [ 'Naruto', 'Dororo', 'Noragame', 'One piece']
     botoes_manga = []
     for i in range(len(lista_manga)):
          variavel = quadro(lista_manga[i])
          botoes_manga.append(variavel)
     linhas, colunas = len(botoes_manga), 3
     for k in range(linhas):
          for h in range(colunas):
               window.grade_Layout.addWidget(botoes_manga[k], k, h)
     
     carrinho = quadro('carrinho')
     window.grade_Layout.addWidget(carrinho, 0, 1)
     
     usuario = quadro('usuário')
     window.grade_Layout.addWidget(usuario, 1, 1)
     
     
     
               
          
     
          
# Adicionando o quadro logo após a barra de pesquisa
     

     window.show()
     app.exec()
