from __future__ import annotations  # Adicione esta linha
import datetime
from enum import Enum
from .endereco import Endereco
from .pagamento import Pagamento
from .entrega import Entrega

class StatusPedido(Enum):
    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class ItemPedido:
    def __init__(self, produto, quantidade: int, preco_unitario: float):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def getSubtotal(self) -> float:
        return self.quantidade * self.preco_unitario

class Pedido:
    def __init__(self, pedido_id: int, cliente: 'Cliente', data_criacao: datetime.datetime, itens: list, endereco_entrega: Endereco, status: str):
        self.pedido_id = pedido_id
        self.cliente = cliente
        self.data_criacao = data_criacao
        self.itens = itens
        self.endereco_entrega = endereco_entrega
        self.status = StatusPedido(status).value  # Usar enum
        self.pagamento = None  # Novo atributo
        self.entrega = None    # Novo atributo

    def addItemPedido(self, produto, quantidade, preco_unitario):
        item = ItemPedido(produto, quantidade, preco_unitario)
        self.itens.append(item)

    def calcularTotal(self) -> float:
        return sum(item.getSubtotal() for item in self.itens)

    def atualizarStatus(self, novo_status: str) -> None:
        novo_status_enum = StatusPedido(novo_status)
        if novo_status_enum == StatusPedido.ENVIADO and self.status != StatusPedido.PAGO.value:
            print(f"ERRO: Pedido {self.pedido_id} não pode ser enviado pois não está PAGO.")
            return
        if novo_status_enum == StatusPedido.ENTREGUE and self.status != StatusPedido.ENVIADO.value:
            print(f"ERRO: Pedido {self.pedido_id} não pode ser entregue pois não foi enviado.")
            return
        self.status = novo_status_enum.value
        print(f"Status do pedido {self.pedido_id} atualizado para {self.status}.")

    def setPagamento(self, pagamento: Pagamento):
        self.pagamento = pagamento

    def setEntrega(self, entrega: Entrega):
        self.entrega = entrega

    def exibirPedido(self):
        print(f"==== Detalhes do Pedido {self.pedido_id} ====")
        print(f"Cliente: {self.cliente.nome}")
        if self.endereco_entrega:
            print(f"Entrega: {self.endereco_entrega.obterEnderecoCompleto()}")
        print(f"Status: {self.status}")
        for item in self.itens:
            print(f"  - {item.quantidade} x {item.produto.nome} @ {item.preco_unitario} = {item.getSubtotal()}")
        print(f"Total: R$ {self.calcularTotal()}")