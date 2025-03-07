from abc import ABC, abstractmethod
from .carrinho import Carrinho, ItemCarrinho
import datetime

class Usuario(ABC):
    def __init__(self, user_id: int, nome: str, email: str, senha: str):
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.enderecos = []

    @abstractmethod
    def login(self) -> bool:
        pass

    def logout(self) -> None:
        print(f"{self.nome} fez logout.")

    def visualizarPerfil(self) -> None:
        print(f"=== Perfil de {self.nome} ===")
        print(f"UserID: {self.user_id}")
        print(f"Email:  {self.email}")

    def atualizarPerfil(self, novo_nome=None, novo_email=None) -> None:
        if novo_nome:
            self.nome = novo_nome
        if novo_email:
            self.email = novo_email
        print("Perfil atualizado com sucesso!")

    def adicionarEndereco(self, endereco) -> None:
        self.enderecos.append(endereco)
        print(f"Endereço adicionado para o usuário {self.nome}.")

class Administrador(Usuario):
    def __init__(self, user_id: int, nome: str, email: str, senha: str, nivel_acesso: str):
        super().__init__(user_id, nome, email, senha)
        self.nivel_acesso = nivel_acesso

    def login(self) -> bool:
        print(f"Administrador {self.nome} realizou login!")
        return True

    def gerenciarProdutos(self) -> None:
        print("Gerenciando produtos (incluir, atualizar, remover)...")

    def gerarRelatorios(self) -> None:
        print("Gerando relatórios de vendas, estoque, clientes etc.")

    def gerenciarEstoque(self) -> None:
        print("Gerenciando estoque...")

class Cliente(Usuario):
    def __init__(self, user_id: int, nome: str, email: str, senha: str, telefone: str):
        super().__init__(user_id, nome, email, senha)
        self.telefone = telefone
        self.carrinho = Carrinho()

    def login(self) -> bool:
        print(f"Cliente {self.nome} realizou login!")
        return True

    def adicionarAoCarrinho(self, prod, qtd: int) -> None:
        item = ItemCarrinho(produto=prod, quantidade=qtd, preco_unitario=prod.preco)
        self.carrinho.adicionarItem(item)
        print(f"Adicionado {qtd} x {prod.nome} ao carrinho de {self.nome}.")

    def removerDoCarrinho(self, item: ItemCarrinho) -> None:
        self.carrinho.removerItem(item)
        print(f"Removido item {item.produto.nome} do carrinho de {self.nome}.")

    def finalizarCompra(self, endereco_entrega=None):
        from .pedido import Pedido  # Import movido para dentro da função
        for item in self.carrinho.itens:
            if not item.produto.verificarDisponibilidade(item.quantidade):
                print(f"ERRO: Produto {item.produto.nome} sem estoque suficiente.")
                return None

        pedido = Pedido(
            pedido_id=1000 + self.user_id,
            cliente=self,
            data_criacao=datetime.datetime.now(),
            itens=[],
            endereco_entrega=endereco_entrega,
            status="PENDENTE"
        )

        for item_carrinho in self.carrinho.itens:
            pedido.addItemPedido(item_carrinho.produto, item_carrinho.quantidade, item_carrinho.preco_unitario)
            item_carrinho.produto.atualizarEstoque(-item_carrinho.quantidade)  # Atualizar estoque ao finalizar compra

        print(f"Pedido {pedido.pedido_id} criado com sucesso para o cliente {self.nome}.")
        self.carrinho.esvaziar()
        return pedido