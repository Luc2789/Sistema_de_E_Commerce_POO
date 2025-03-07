# models/carrinho.py

class ItemCarrinho:
    def __init__(self, produto, quantidade: int, preco_unitario: float):
        self.produto = produto      # Tipo: Produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def getSubtotal(self) -> float:
        return self.quantidade * self.preco_unitario
        
class Carrinho:
    def __init__(self):
        self.itens = []  # Lista de ItemCarrinho

    def adicionarItem(self, item: ItemCarrinho) -> None:
        self.itens.append(item)

    def removerItem(self, item: ItemCarrinho) -> None:
        if item in self.itens:
            self.itens.remove(item)

    def calcularTotal(self) -> float:
        return sum(item.getSubtotal() for item in self.itens)

    def esvaziar(self) -> None:
        self.itens.clear()
