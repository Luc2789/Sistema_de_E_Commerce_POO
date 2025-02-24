import streamlit as st
import datetime
from models.usuario import Administrador, Cliente
from models.produto import Produto, Categoria
from models.endereco import Endereco
from models.pedido import Pedido
from models.pagamento import Pagamento

# Dicionário/banco de dados em memória só para DEMO
FAKE_USERS = {
    "admin@loja.com": Administrador(
        user_id=1, nome="Admin Master", email="admin@loja.com",
        senha="admin123", nivel_acesso="SUPER"
    ),
    "joao@example.com": Cliente(
        user_id=2, nome="João da Silva", email="joao@example.com",
        senha="123456", telefone="(11) 99999-9999"
    )
}

# Também criaremos alguns produtos em memória
categoria_livros = Categoria(categoria_id=10, nome="Livros", descricao="Livros diversos")
produto1 = Produto(
    produto_id=101, 
    nome="Livro POO em Python", 
    descricao="Aprenda OOP em Python", 
    preco=50.0, 
    estoque_atual=10, 
    categoria=categoria_livros
)
produto2 = Produto(
    produto_id=102, 
    nome="Livro Django", 
    descricao="Desenvolvimento Web com Django", 
    preco=60.0, 
    estoque_atual=5, 
    categoria=categoria_livros
)

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Minha Loja", layout="centered")

st.title("Minha Loja Online - Exemplo Streamlit")

# Usaremos a sessão do Streamlit para guardar dados como "usuário logado" e "carrinho"
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if "pedido_atual" not in st.session_state:
    st.session_state["pedido_atual"] = None

# SIDEBAR: Login ou Logout
st.sidebar.header("Autenticação")

if st.session_state["usuario_logado"] is None:
    # Exibir campos de login
    email = st.sidebar.text_input("Email")
    senha = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Login"):
        user = FAKE_USERS.get(email)
        if user and user.senha == senha:
            st.session_state["usuario_logado"] = user
            st.success(f"Bem-vindo(a), {user.nome}!")
        else:
            st.error("Credenciais inválidas!")
else:
    user = st.session_state["usuario_logado"]
    st.sidebar.write(f"Logado como: {user.nome}")
    if st.sidebar.button("Logout"):
        st.session_state["usuario_logado"] = None
        st.experimental_rerun()

# Se o usuário não estiver logado, não mostra o restante
if st.session_state["usuario_logado"] is None:
    st.stop()

# Caso haja um usuário logado
user = st.session_state["usuario_logado"]

# Verifica se é Administrador ou Cliente
if isinstance(user, Administrador):
    st.subheader("Área do Administrador")

    if st.button("Gerenciar Produtos"):
        st.info("Aqui você poderia mostrar formulários para incluir/alterar/excluir produtos.")
        user.gerenciarProdutos()

    if st.button("Gerar Relatórios"):
        st.info("Aqui poderia haver a seleção de tipo de relatório, datas, etc.")
        user.gerarRelatorios()

    if st.button("Gerenciar Estoque"):
        st.info("Aqui poderia haver a interface para atualizar estoque de cada produto.")
        user.gerenciarEstoque()

else:
    # Cliente
    st.subheader("Área do Cliente")
    
    # 1) Listar Produtos
    st.write("### Catálogo de Produtos")
    produtos_lista = categoria_livros.listarProdutos()  # Retorna [produto1, produto2, ...]
    
    # Exibe cada produto
    for prod in produtos_lista:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{prod.nome}** - R${prod.preco}")
            st.write(prod.descricao)
            st.write(f"Estoque: {prod.estoque_atual}")
        with col2:
            qtd = st.number_input(f"Qtd {prod.nome}", min_value=0, max_value=prod.estoque_atual, key=f"qtd_{prod.produto_id}")
        with col3:
            if st.button(f"Adicionar {prod.nome}", key=f"add_{prod.produto_id}"):
                if qtd > 0:
                    user.adicionarAoCarrinho(prod, qtd)
                else:
                    st.warning("Quantidade deve ser maior que zero.")
    
    st.write("### Seu Carrinho")
    # Lista itens do carrinho
    total = user.carrinho.calcularTotal()
    if len(user.carrinho.itens) == 0:
        st.info("Carrinho vazio!")
    else:
        for item in user.carrinho.itens:
            st.write(f"{item.quantidade} x {item.produto.nome} = R${item.getSubtotal()}")

        st.write(f"**Total:** R$ {total}")
        
        if st.button("Esvaziar Carrinho"):
            user.carrinho.esvaziar()
            st.info("Carrinho esvaziado!")

        # 2) Finalizar Compra
        st.write("### Endereço de Entrega (exemplo simples)")
        logradouro = st.text_input("Logradouro", value="Rua das Flores")
        numero = st.text_input("Número", value="123")
        complemento = st.text_input("Complemento", value="")
        bairro = st.text_input("Bairro", value="Centro")
        cidade = st.text_input("Cidade", value="São Paulo")
        estado = st.text_input("Estado", value="SP")
        cep = st.text_input("CEP", value="01000-000")

        if st.button("Finalizar Compra"):
            endereco_entrega = Endereco(
                endereco_id=999,
                logradouro=logradouro,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep
            )
            pedido = user.finalizarCompra(endereco_entrega=endereco_entrega)
            
            if pedido is not None:
                st.session_state["pedido_atual"] = pedido
                st.success(f"Pedido {pedido.pedido_id} criado! Status: {pedido.status}")

                # Simular pagamento rápido
                st.write("### Pagamento")
                valor = pedido.calcularTotal()
                metodo_pagamento = st.selectbox("Método de Pagamento", ["Cartão", "Boleto", "Pix"])
                if st.button("Processar Pagamento"):
                    pagamento = Pagamento(
                        pagamento_id=1,
                        pedido=pedido,
                        valor_total=valor,
                        metodo_pagamento=metodo_pagamento,
                        status_pagamento="PENDENTE"
                    )
                    sucesso = pagamento.processarPagamento()
                    if sucesso:
                        pagamento.confirmarPagamento()
                        pedido.atualizarStatus("PAGO")
                        st.success(f"Pagamento aprovado! Pedido {pedido.pedido_id} agora está como {pedido.status}.")
                    else:
                        pedido.atualizarStatus("CANCELADO")
                        st.error("Pagamento rejeitado. Pedido cancelado.")
            else:
                st.error("Houve algum problema ao finalizar a compra (estoque?).")
