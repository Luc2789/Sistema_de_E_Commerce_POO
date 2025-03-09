
#Essa classe manga é um exemplo que melhor se trabalha na adição de itens no carrinho(em relação aos seus atributos e metodos)
class Manga:
    def __init__(self, titulo, autor, preco, estoque):
        self.titulo = titulo
        self.autor = autor
        self.preco = preco
        self.estoque = estoque

    def atualizar_estoque(self, quantidade):# ex: manga1.atualizar_estoque(10)
        self.estoque += quantidade

    def vender(self, quantidade): #é usada na classe Carrinho para não permitir que sejam adicionados mais produtos do que o estoque
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return True
        else:
            print("Estoque insuficiente!")
            return False
        
    def reduzir_estoque(self, quantidade): #é usada na classe Pagamento para diminuir a quantidade do estoque quando finalizar o pagamento
        self.estoque -= quantidade

    def mostrar_info(self): #mostra as informações do manga
        print(f"Título: {self.titulo}, Autor: {self.autor}, Preço: {self.preco}, Estoque: {self.estoque}")

        """Classe para manipulação de carrinhos"""
class Carrinho:
    def __init__(self):
        """lista que armazena os itens do carrinho"""
        self.itens = []

    def adicionar_produto(self, produto, quantidade):#o parâmetro deve ser o produto adicionado e a quantidade(ex: carrinho.adicionar_produto(manga1, 3))
        if produto.vender(quantidade):
            """serão adicionados o título e preço que estão na classe Manga, e a quantidade"""
            self.itens.append({"produto": produto, "nome": produto.titulo, "preco": produto.preco, "quantidade": quantidade})

    def remover_produto(self, nome):# parâmetro deve ser o nome do produto "Naruto" para excluir(ex: carrinho.remover_produto("Naruto"))
        self.itens = [item for item in self.itens if item["nome"] != nome]

    def mostrar_produtos(self):
        """exibe todos os itens do carrinho"""
        print("\t\tProdutos no carrinho:")
        for item in self.itens:
            print(f"Produto: {item['nome']}, Preço: {item['preco']}, Quantidade: {item['quantidade']}")

    """Classe para manipulação de pagamentos"""
class Pagamento:
    def __init__(self, frete=20):#frete padrão 0(pode ser alterado para qualquer valor)
        self.frete = frete

    """função que calculo somente o valor dos produtos sem frete e cupons"""
    def mostrar_valor_produtos(self, carrinho):#O  valor deve ser atribuido a uma variável(ex: valor_produto = pagamento.mostrar_valor_produtos(carrinho))
        return sum(item["preco"] * item["quantidade"] for item in carrinho.itens)

    """função que calculo o valor total de produtos + frete pré-definido"""
    def mostrar_valor_total(self, carrinho): #O  valor deve ser atribuido a uma variável(ex: valor_total = pagamento.mostrar_valor_total(carrinho))
        return self.mostrar_valor_produtos(carrinho) + self.frete

    def inserir_cupom(self, carrinho, codigo_cupom, desconto):#O  valor deve ser atribuido a uma variável(ex: valor_com_desconto = pagamento.inserir_cupom(carrinho, "desconto10", desconto))
        valor_total = self.mostrar_valor_total(carrinho)
        """verifica se o cupom existe e aplica o desconto"""
        if codigo_cupom in desconto.cupons:
            valor_desconto = desconto.cupons[codigo_cupom]
            
            if valor_desconto == "frete":
                valor_total -= self.frete  # Remove o frete se for frete grátis
            else:
                valor_total -= valor_desconto  # Aplica o desconto numérico
                
            return max(0, valor_total)  # Garante que o total não seja negativo
        else:
            print("Cupom inválido!")
            return valor_total
        
    def finalizar_pagamento(self, carrinho, historico, forma_pagamento):
        for item in carrinho.itens:
            item["produto"].reduzir_estoque(item["quantidade"])
        print(f"Pagamento realizado com {forma_pagamento}.")
        historico.adicionar_compra(carrinho.itens) #A compra é adicionada no histórico quando o pagmanento é realizado
        historico.definir_status("Pedido Aprovado, aguarde a entrega.") #Atualiza o status do pedido no histórico de compras

class Desconto:
    def __init__(self):
        """dicionário que armazena os cupons"""
        self.cupons = {}

    def inserir_cupom(self, codigo, valor):# Os parâmetros devem  ser o nome do cupom e o valor do cupom(ex: desconto.inserir_cupom("desconto10", 10))
        self.cupons[codigo] = valor

    def excluir_cupom(self, codigo):# Os parâmetros devem  ser o nome do cupom(ex: desconto.excluir_cupom("desconto10"))
        if codigo in self.cupons:
            del self.cupons[codigo]

    def mostrar_cupons(self):
        print("\t\tCupons de desconto:")
        print(f"{self.cupons}")

"""Classe para armazenar o histórico de compras"""
class Historico:
    def __init__(self):
        self.status = "Pedido realizado"
        self.compras = []# dicionário para armazenar as compras

    def definir_status(self, novo_status):# Basta definir o novo status ex: historico.definir_status("Pedido entregue")
        self.status = novo_status

    def mostrar_status(self): #ex: historico.mostrar_status()
        print(f"Status do pedido: {self.status}")

    def adicionar_compra(self, itens): # O paramentro deve ser uma lista de itens(ex: historico.adicionar_compra(carrinho.itens))
        self.compras.append(itens)

    def mostrar_compras(self): #ex: historico.mostrar_compras()
        if not self.compras:
            print("Nenhuma compra realizada ainda.")
        for i, compra in enumerate(self.compras, 1):
            print(f" {i}º compra:")
            for item in compra:
                print(f" - Produto: {item['nome']}, Quantidade: {item['quantidade']}, Preço unitário: {item['preco']}")

                """Exemplo de teste"""
#cadastro dos itens na classe Manga
manga1 = Manga("Naruto", "Masashi Kishimoto", 19.90, 10)
manga2 = Manga("One Piece", "Eiichiro Oda", 29.90, 10)
#Manga.mostrar_info(manga)

"""Inicializa/cria o carrinho de compras"""
carrinho = Carrinho()
#adiciona os itens no carrinho(manga1 = Naruto, manga2 = One Piece)
carrinho.adicionar_produto(manga1, 3)
carrinho.adicionar_produto(manga2, 2)
#mostra os itens do carrinho
carrinho.mostrar_produtos()

"""inicializar o pagamento"""
pagamento = Pagamento()
#mostrar o valor total dos produtos(sem desconto e frete)
valor_produto = pagamento.mostrar_valor_produtos(carrinho)
print(f"Valor dos produtos: {valor_produto}")

#mostrar o valor total dos produtos(incluindo frete, sem desconto)
valor_total = pagamento.mostrar_valor_total(carrinho)
print(f"Valor total incluindo frete: {valor_total}")

"""criar cupons de desconto"""
desconto = Desconto()
desconto.inserir_cupom("desconto10", 10)
desconto.mostrar_cupons()

#diminuir o valor do produto com o desconto
valor_com_desconto = pagamento.inserir_cupom(carrinho, "desconto10", desconto)
print(f"Valor com desconto: {valor_com_desconto}")

"""inicializar/cria o historico de compras"""
historico =Historico()

#historico.definir_status("Pedido em andamento")
#Finaliza o pagamento
pagamento.finalizar_pagamento(carrinho, historico, "cartão de crédito")
#mostra o status do pedido
historico.mostrar_status()
#mostra as compras
historico.mostrar_compras()
