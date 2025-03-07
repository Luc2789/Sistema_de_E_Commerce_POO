# models/endereco.py

class Endereco:
    def __init__(self, endereco_id: int, logradouro: str, numero: str,
                 complemento: str, bairro: str, cidade: str, estado: str, cep: str):
        self.endereco_id = endereco_id
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def obterEnderecoCompleto(self) -> str:
        return (
            f"{self.logradouro}, {self.numero}, "
            f"{self.bairro}, {self.cidade}-{self.estado}, CEP: {self.cep}"
        )
