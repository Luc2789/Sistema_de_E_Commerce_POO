class Usuario:
    def __init__(self, user_id: int, nome: str, email: str, senha: str):
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.senha = senha

    def verificar_senha(self, senha: str) -> bool:
        return self.senha == senha


class Perfil(Usuario):
    def __init__(self, user_id: int, nome: str, email: str, senha: str, telefone: str, endereco: str):
        super().__init__(user_id, nome, email, senha)
        self.telefone = telefone
        self.endereco = endereco

    def view_profile(self):
        return (f"""Perfil do Usuário
Usuário: {self.nome} | ID: {self.user_id}
E-mail: {self.email}
Telefone: {self.telefone}
Endereço: {self.endereco}
""")


class Login:
    def __init__(self, email: str, senha: str, usuarios_cadastro: list):
        usuario = next((u for u in usuarios_cadastro if u.email == email), None)
        if usuario:
            self.usuario = usuario
            self.senha_fornecida = senha
        else:
            raise ValueError("Usuário não encontrado")

    def fazer_login(self) -> bool:
        if self.usuario.verificar_senha(self.senha_fornecida):
            print(f"Login bem-sucedido! Usuário: {self.usuario.nome}.")
            return True
        else:
            print("Senha incorreta! Tente novamente.")
            return False


class RegisUsuario(Usuario):
    _contador_id = 1  # Variável de classe para gerar IDs automaticamente

    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(RegisUsuario._contador_id, nome, email, senha)
        RegisUsuario._contador_id += 1  # Incrementa o ID automaticamente

    def registrar(self, usuarios_cadastro: list) -> bool:
        usuarios_cadastro.append(self)
        print(f"Usuário {self.nome} registrado com sucesso!")
        return True

# # Lista para armazenar usuários cadastrados
# usuarios_cadastrados = []

# # Registrando um novo usuário
# novo_usuario = RegisUsuario("João Silva", "joao@example.com", "senha123")
# novo_usuario.registrar(usuarios_cadastrados)

# # Tentando fazer login com um usuário cadastrado
# try:
#     login = Login("joao@example.com", "senha123", usuarios_cadastrados)
#     login.fazer_login()
# except ValueError as e:
#     print(e)

# # Tentando fazer login com senha incorreta
# try:
#     login = Login("joao@example.com", "senha_errada", usuarios_cadastrados)
#     login.fazer_login()
# except ValueError as e:
#     print(e)

# # Tentando fazer login com um usuário não cadastrado
# try:
#     login = Login("ana@example.com", "senha456", usuarios_cadastrados)
#     login.fazer_login()
# except ValueError as e:
#     print(e)
