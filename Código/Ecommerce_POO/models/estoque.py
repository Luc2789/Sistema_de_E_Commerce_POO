# models/estoque.py
class Estoque:
    def __init__(self, estoque_id: int, produto, quantidade_atual: int, localizacao: str):
        self.estoque_id = estoque_id
        self.produto = produto
        self.quantidade_atual = quantidade_atual
        self.localizacao = localizacao

    def reservarQuantidade(self, qtd: int) -> bool:
        """Tenta reservar 'qtd' do produto (decrementando)."""
        if qtd < 0:
            raise ValueError("Quantidade a reservar não pode ser negativa")
        if self.quantidade_atual >= qtd:
            self.quantidade_atual -= qtd
            print(f"[Estoque] Reservado {qtd} de {self.produto.nome}. Restante: {self.quantidade_atual}.")
            return True
        print(f"[Estoque] Falha: não há estoque suficiente de {self.produto.nome}.")
        return False

    def liberarQuantidade(self, qtd: int) -> bool:
        """Libera 'qtd' de volta ao estoque."""
        if qtd < 0:
            raise ValueError("Quantidade a liberar não pode ser negativa")
        self.quantidade_atual += qtd
        print(f"[Estoque] Liberado {qtd} de {self.produto.nome}. Total: {self.quantidade_atual}.")
        return True

    def atualizarQuantidade(self, qtd: int) -> None:
        """Soma 'qtd' ao estoque atual (pode ser positivo ou negativo)."""
        if self.quantidade_atual + qtd < 0:
            raise ValueError(f"Quantidade não pode ser negativa. Estoque atual: {self.quantidade_atual}, tentativa: {qtd}")
        self.quantidade_atual += qtd
        print(f"[Estoque] Quantidade do produto {self.produto.nome} agora é {self.quantidade_atual}.")