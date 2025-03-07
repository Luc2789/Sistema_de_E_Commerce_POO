from dataclasses import dataclass
from typing import Optional
from models.usuario import Cliente, Administrador
from models.pedido import Pedido
from models.produto import Produto  # Importando Produto explicitamente

@dataclass
class UserSession:
    user: Optional[Cliente | Administrador] = None

@dataclass
class ProductUI:
    title: str
    author: str
    category: str
    stock: int
    price: float
    imagem: str = None  # Adicionando suporte para imagem
    product: Optional[Produto] = None  # Usando tipo Produto importado

@dataclass
class OrderUI:
    order_id: int
    customer: str
    status: str
    total: float
    order: Optional[Pedido] = None  # Tornando opcional para maior flexibilidade