from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

class BaseScreen(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, return_screen: QWidget | None, session):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.return_screen = return_screen
        self.session = session

    def go_back(self):
        if self.return_screen:
            self.stacked_widget.setCurrentWidget(self.return_screen)
        else:
            # Se não houver tela de retorno definida, voltar para a tela de autenticação
            if hasattr(self.stacked_widget, 'auth_screen'):
                self.stacked_widget.setCurrentWidget(self.stacked_widget.auth_screen)
            else:
                print("Nenhuma tela de retorno definida!")