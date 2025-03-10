class Produto:
    def __init__(self, nome, descricao, preco, estoque_atual, categoria):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque_atual = estoque_atual
        self.categoria = categoria

    def verificar_disponibilidade(self):
        return self.estoque_atual > 0

    def atualizar_estoque(self, quantidade):
        if self.estoque_atual + quantidade >= 0:
            self.estoque_atual += quantidade
        else:
            print("Erro: Estoque não pode ser negativo.")

    def __str__(self):
        return (f"Produto: {self.nome}\n"
                f"Descrição: {self.descricao}\n"
                f"Preço: R${self.preco:.2f}\n"
                f"Estoque Atual: {self.estoque_atual}\n"
                f"Categoria: {self.categoria}\n"
                f"Disponível: {'Sim' if self.verificar_disponibilidade() else 'Não'}")

class GerenciadorProdutos:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        print(f"Produto '{produto.nome}' adicionado com sucesso!")

    def remover_produto(self, nome):
        for produto in self.produtos:
            if produto.nome == nome:
                self.produtos.remove(produto)
                print(f"Produto '{nome}' removido com sucesso!")
                return
        print(f"Produto '{nome}' não encontrado.")

    def buscar_produto(self, nome):
        for produto in self.produtos:
            if produto.nome == nome:
                return produto
        return None

    def listar_produtos(self):
        if not self.produtos:
            print("Nenhum produto cadastrado.")
        else:
            for produto in self.produtos:
                print(produto)
                print("-" * 30)

    def atualizar_estoque_produto(self, nome, quantidade):
        produto = self.buscar_produto(nome)
        if produto:
            produto.atualizar_estoque(quantidade)
            print(f"Estoque do produto '{nome}' atualizado para {produto.estoque_atual}.")
        else:
            print(f"Produto '{nome}' não encontrado.")

def exibir_menu():
    print("\n--- Gerenciador de Produtos ---")
    print("1. Adicionar Produto")
    print("2. Remover Produto")
    print("3. Buscar Produto")
    print("4. Listar Produtos")
    print("5. Atualizar Estoque")
    print("6. Sair")

if __name__ == "__main__":
    gerenciador = GerenciadorProdutos()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            descricao = input("Descrição do produto: ")
            preco = float(input("Preço do produto: "))
            estoque = int(input("Estoque inicial: "))
            categoria = input("Categoria do produto: ")
            produto = Produto(nome, descricao, preco, estoque, categoria)
            gerenciador.adicionar_produto(produto)

        elif opcao == "2":
            nome = input("Nome do produto a ser removido: ")
            gerenciador.remover_produto(nome)

        elif opcao == "3":
            nome = input("Nome do produto a ser buscado: ")
            produto = gerenciador.buscar_produto(nome)
            if produto:
                print(produto)
            else:
                print("Produto não encontrado.")

        elif opcao == "4":
            gerenciador.listar_produtos()

        elif opcao == "5":
            nome = input("Nome do produto para atualizar estoque: ")
            quantidade = int(input("Quantidade a adicionar/remover (use negativo para remover): "))
            gerenciador.atualizar_estoque_produto(nome, quantidade)

        elif opcao == "6":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")