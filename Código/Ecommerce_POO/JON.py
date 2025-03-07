from PySide6.QtWidgets import QStackedWidget, QApplication
from screens.auth_screen import AuthScreen
from screens.menu_screen import MenuScreen
from screens.client_dashboard_screen import ClientDashboardScreen
from screens.product_management_screen import ProductManagementScreen
from screens.cart_screen import CartScreen
from screens.payment_screen import PaymentScreen
from screens.order_management_screen import OrderManagementScreen
from screens.reports_screen import ReportsScreen
from ui_data import UserSession

app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background-color: #ffffff;
    }
""")
stacked_widget = QStackedWidget()
session = UserSession()

# Inicializar as telas na ordem correta
menu_screen = MenuScreen(stacked_widget, session)
product_screen = ProductManagementScreen(stacked_widget, menu_screen, session)
client_dashboard_screen = ClientDashboardScreen(stacked_widget, None, None, None, None, session, product_screen)
auth_screen = AuthScreen(stacked_widget, menu_screen, client_dashboard_screen, session)
order_screen = OrderManagementScreen(stacked_widget, menu_screen, session)
reports_screen = ReportsScreen(stacked_widget, menu_screen, session)
cart_screen = CartScreen(stacked_widget, client_dashboard_screen, session, client_dashboard_screen)
payment_screen = PaymentScreen(stacked_widget, client_dashboard_screen, client_dashboard_screen, session)

# Atualizar dependências do ClientDashboardScreen
client_dashboard_screen.return_screen = auth_screen
client_dashboard_screen.auth_screen = auth_screen
client_dashboard_screen.payment_screen = payment_screen
client_dashboard_screen.cart_screen = cart_screen

# Adicionar referências ao stacked_widget
stacked_widget.auth_screen = auth_screen
stacked_widget.menu_screen = menu_screen
stacked_widget.product_screen = product_screen
stacked_widget.order_screen = order_screen
stacked_widget.reports_screen = reports_screen
stacked_widget.cart_screen = cart_screen
stacked_widget.payment_screen = payment_screen
stacked_widget.client_dashboard_screen = client_dashboard_screen

# Adicionar as telas ao stacked_widget
stacked_widget.addWidget(auth_screen)
stacked_widget.addWidget(menu_screen)
stacked_widget.addWidget(product_screen)
stacked_widget.addWidget(order_screen)
stacked_widget.addWidget(reports_screen)
stacked_widget.addWidget(cart_screen)
stacked_widget.addWidget(payment_screen)
stacked_widget.addWidget(client_dashboard_screen)

# Iniciar na tela de autenticação
stacked_widget.setCurrentWidget(auth_screen)

stacked_widget.show()
app.exec()