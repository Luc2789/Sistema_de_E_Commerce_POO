# Sistema de E-commerce em Python com PySide6

Este documento descreve a estrutura básica de um sistema de e-commerce desenvolvido em Python utilizando a biblioteca PySide6 para a interface gráfica.

## Estrutura do Projeto

### Classes Principais

#### Produto
- **Atributos:**
  - `id: int`
  - `nome: str`
  - `descricao: str`
  - `preco: float`
  - `quantidade_estoque: int`

- **Métodos:**
  - `atualizar_estoque(quantidade: int): void`
  - `obter_detalhes(): str`

#### Carrinho
- **Atributos:**
  - `itens: List[ItemCarrinho]`
  - `total: float`

- **Métodos:**
  - `adicionar_item(produto: Produto, quantidade: int): void`
  - `remover_item(produto_id: int): void`
  - `calcular_total(): float`
  - `finalizar_compra(): void`

#### ItemCarrinho
- **Atributos:**
  - `produto: Produto`
  - `quantidade: int`

- **Métodos:**
  - `calcular_subtotal(): float`

#### Usuario
- **Atributos:**
  - `id: int`
  - `nome: str`
  - `email: str`
  - `senha: str`
  - `endereco: Endereco`

- **Métodos:**
  - `fazer_login(email: str, senha: str): bool`
  - `fazer_logout(): void`
  - `atualizar_perfil(nome: str, email: str, senha: str): void`

#### Endereco
- **Atributos:**
  - `rua: str`
  - `cidade: str`
  - `estado: str`
  - `cep: str`
  - `pais: str`

#### Pedido
- **Atributos:**
  - `id: int`
  - `usuario: Usuario`
  - `itens: List[ItemCarrinho]`
  - `data_pedido: datetime`
  - `status: str`

- **Métodos:**
  - `atualizar_status(novo_status: str): void`
  - `gerar_nota_fiscal(): str`

### Interface Gráfica

#### Janela Principal
- **Componentes:**
  - Lista de produtos
  - Carrinho de compras
  - Botões de navegação (Login, Perfil, Finalizar Compra)

#### Janela de Login
- **Componentes:**
  - Campos de entrada para email e senha
  - Botão de login
  - Link para registro de novo usuário

#### Janela de Perfil
- **Componentes:**
  - Campos para edição de nome, email e senha
  - Botão de salvar alterações

#### Janela de Finalização de Compra
- **Componentes:**
  - Resumo do pedido
  - Campos para entrada de endereço de entrega
  - Botão de confirmar compra

### Funcionalidades

- **Gerenciamento de Produtos:**
  - Adicionar, remover e atualizar produtos.

- **Gerenciamento de Usuários:**
  - Registro, login e atualização de perfil.

- **Carrinho de Compras:**
  - Adicionar e remover itens, calcular total e finalizar compra.

- **Pedidos:**
  - Acompanhamento de status e geração de nota fiscal.

## Considerações Finais

Este sistema de e-commerce foi desenvolvido para fornecer uma experiência de usuário simples e eficiente, com uma interface gráfica intuitiva criada com PySide6. O código foi estruturado para facilitar a manutenção e a adição de novas funcionalidades no futuro.