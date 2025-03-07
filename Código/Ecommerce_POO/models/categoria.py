# models/categoria.py
class Categoria:
    def __init__(self, categoria_id: int, nome: str, descricao: str):
        self.categoria_id = categoria_id
        self.nome = nome
        self.descricao = descricao
        self._produtos = []  # poderia ser List[Produto]

    def listarProdutos(self):
        """Retorna a lista de produtos desta categoria."""
        return self._produtos

    def adicionarProduto(self, produto):
        """Adiciona um produto a esta categoria."""
        self._produtos.append(produto)