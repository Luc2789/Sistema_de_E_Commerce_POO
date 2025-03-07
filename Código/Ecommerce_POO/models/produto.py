from enum import Enum
from .estoque import Estoque
from .categoria import Categoria

class Produto:
    def __init__(self, produto_id: int, nome: str, descricao: str, preco: float, categoria: Categoria, imagem: str = None):
        self.produto_id = produto_id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.imagem = imagem
        self.estoque = Estoque(
            estoque_id=produto_id,
            produto=self,
            quantidade_atual=0,
            localizacao="Armazém 1"
        )

    def atualizarEstoque(self, quantidade: int) -> None:
        self.estoque.atualizarQuantidade(quantidade)

    def verificarDisponibilidade(self, quantidade: int) -> bool:
        return self.estoque.quantidade_atual >= quantidade

    def getPreco(self) -> float:
        return self.preco