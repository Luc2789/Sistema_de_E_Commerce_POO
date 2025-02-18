class Manga:
    def __init__(self, titulo, autor, categoria, quantidade_estoque):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.quantidade_estoque = quantidade_estoque

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.categoria}) | Estoque: {self.quantidade_estoque}"

class GerenciadorMangas:
    def __init__(self):
        self.mangas = []

    def cadastrar_manga(self, titulo, autor, categoria, quantidade_estoque):
        manga = Manga(titulo, autor, categoria, quantidade_estoque)
        self.mangas.append(manga)
        print(f"Mangá '{titulo}' cadastrado com sucesso!")

    def editar_manga(self, titulo, novo_titulo=None, novo_autor=None, nova_categoria=None, nova_quantidade_estoque=None):
        for manga in self.mangas:
            if manga.titulo == titulo:
                if novo_titulo:
                    manga.titulo = novo_titulo
                if novo_autor:
                    manga.autor = novo_autor
                if nova_categoria:
                    manga.categoria = nova_categoria
                if nova_quantidade_estoque is not None:
                    manga.quantidade_estoque = nova_quantidade_estoque
                print(f"Mangá '{titulo}' editado com sucesso!")
                return
        print(f"Mangá '{titulo}' não encontrado.")

    def excluir_manga(self, titulo):
        for manga in self.mangas:
            if manga.titulo == titulo:
                self.mangas.remove(manga)
                print(f"Mangá '{titulo}' excluído com sucesso!")
                return
        print(f"Mangá '{titulo}' não encontrado.")

    def listar_mangas(self):
        if not self.mangas:
            print("Nenhum mangá cadastrado.")
        else:
            for manga in self.mangas:
                print(manga)

    def listar_por_categoria(self, categoria):
        mangas_categoria = [manga for manga in self.mangas if manga.categoria == categoria]
        if not mangas_categoria:
            print(f"Nenhum mangá encontrado na categoria '{categoria}'.")
        else:
            for manga in mangas_categoria:
                print(manga)

    def verificar_estoque(self, titulo):
        for manga in self.mangas:
            if manga.titulo == titulo:
                print(f"Estoque de '{titulo}': {manga.quantidade_estoque}")
                return
        print(f"Mangá '{titulo}' não encontrado.")

# Exemplo de uso
gerenciador = GerenciadorMangas()

# Cadastrar mangás
gerenciador.cadastrar_manga("Naruto", "Masashi Kishimoto", "Shonen", 10)
gerenciador.cadastrar_manga("One Piece", "Eiichiro Oda", "Shonen", 15)
gerenciador.cadastrar_manga("Death Note", "Tsugumi Ohba", "Suspense", 5)

# Listar todos os mangás
print("\nLista de todos os mangás:")
gerenciador.listar_mangas()

# Editar um mangá
gerenciador.editar_manga("Naruto", novo_titulo="Naruto Shippuden", nova_quantidade_estoque=8)

# Listar mangás por categoria
print("\nLista de mangás Shonen:")
gerenciador.listar_por_categoria("Shonen")

# Verificar estoque
print("\nVerificando estoque:")
gerenciador.verificar_estoque("One Piece")

# Excluir um mangá
gerenciador.excluir_manga("Death Note")

# Listar todos os mangás após exclusão
print("\nLista de todos os mangás após exclusão:")
gerenciador.listar_mangas()