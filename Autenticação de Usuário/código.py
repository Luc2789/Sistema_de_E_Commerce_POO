class Usuario:
    def __init__ (self, user_id: int, nome: str, email: str, senha: str):
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def login(self):
        print(f"Usuário {self.nome} logado.")
    
    def logout(self):
        print(f"Usuário {self.nome} deslogado.")

    def view_profile(self):
        print(f"""Perfil do Usuário
              Usuário: {self.nome} ID: {self.user_id}
              E-mail: {self.email}
              """)
        
    def atualizar_Perfil(self):
        pass #sujeito a adição

class Administrador(Usuario):
    def __init__(self, user_id: int, nome: str, email: str, senha: str, cargo: str):
        super().__init__(user_id, nome, email, senha)
        self.cargo = cargo
    
    def gerenProd(self):
        pass

    def gerarRelat(self):
        pass

    def gerenEstoque(self):
        pass

class Endereco:
    def __init__(self, endereco_id: int, logradouro: str, num: str, compl: str, bairro: str, cidade: str, estado: str, cep: str):
        self.endereco_id = endereco_id
        self.logradouro = logradouro
        self.num = num
        self.compl = compl
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def ender_completo(self):
        return f"""Dados de Endereço
        Estado: {self.estado}
        Cidade: {self.cidade}
        Bairro: {self.bairro}
        Logradouro: {self.logradouro}
        Número: {self.num}
        Complemento: {self.compl}
        CEP: {self.cep}
        """

class cliente:
    def __init__(self, telefone: str, carrinho):
        self.telefone = telefone
        self.carrinho = carrinho
    
    def addatCarrinho(self, produto, quant: int):
        pass
    def removeCarrinho(self, item):
        pass
