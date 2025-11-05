# 📖 Guia Passo a Passo - ForgeERP

Este guia foi gerado automaticamente pelos testes E2E.

**Gerado em:** 05/11/2025 11:08:06

---

## 📋 Índice

1. [Acessar a aplicação](#passo-1-acessar-a-aplicação)
2. [Preencher campo de usuário](#passo-2-preencher-campo-de-usuário)
3. [Preencher campo de senha](#passo-3-preencher-campo-de-senha)
4. [Clicar em 'Entrar'](#passo-4-clicar-em-'entrar')
5. [Visualizar Dashboard](#passo-5-visualizar-dashboard)
6. [Navegar para página de Clientes](#passo-6-navegar-para-página-de-clientes)
7. [Clicar em 'Novo Cliente'](#passo-7-clicar-em-'novo-cliente')
8. [Preencher dados do cliente](#passo-8-preencher-dados-do-cliente)
9. [Salvar cliente](#passo-9-salvar-cliente)
10. [Visualizar lista de clientes](#passo-10-visualizar-lista-de-clientes)
11. [Editar cliente](#passo-11-editar-cliente)
12. [Navegar para Configurações](#passo-12-navegar-para-configurações)
13. [Fazer logout](#passo-13-fazer-logout)

---

## Passo 1: Acessar a aplicação

![01_acessar_aplicacao](operacional/screenshots/01_acessar_aplicacao.png)

### O que fazer:

1. Abra o navegador e acesse: http://localhost:8000
2. A página de login será exibida automaticamente
3. Você verá o formulário de login com campos para usuário e senha

---

## Passo 2: Preencher campo de usuário

![02_preencher_usuario](operacional/screenshots/02_preencher_usuario.png)

### O que fazer:

1. No campo 'Usuário', digite: **admin**
2. Este é o usuário padrão do sistema
3. O campo aceita apenas texto

---

## Passo 3: Preencher campo de senha

![03_preencher_senha](operacional/screenshots/03_preencher_senha.png)

### O que fazer:

1. No campo 'Senha', digite: **admin**
2. Esta é a senha padrão do sistema
3. A senha é ocultada por segurança (aparece como ••••••••)

---

## Passo 4: Clicar em 'Entrar'

![04_login_sucesso](operacional/screenshots/04_login_sucesso.png)

### O que fazer:

1. Clique no botão **'Entrar'**
2. O sistema irá validar suas credenciais
3. Se corretas, você será redirecionado para o dashboard

---

## Passo 5: Visualizar Dashboard

![05_dashboard](operacional/screenshots/05_dashboard.png)

### O que fazer:

1. Após fazer login, você verá o **Dashboard**
2. No topo, há um menu de navegação com: Dashboard, Clientes, Configurações
3. No centro, você verá estatísticas e uma lista de clientes recentes

---

## Passo 6: Navegar para página de Clientes

![06_pagina_clientes](operacional/screenshots/06_pagina_clientes.png)

### O que fazer:

1. Clique na aba **'Clientes'** no menu superior
2. Você será redirecionado para a página de gerenciamento de clientes
3. Aqui você pode criar, editar e excluir clientes

---

## Passo 7: Clicar em 'Novo Cliente'

![07_formulario_criar_cliente](operacional/screenshots/07_formulario_criar_cliente.png)

### O que fazer:

1. Clique no botão **'+ Novo Cliente'** no topo da página
2. Um formulário será exibido para criar um novo cliente

---

## Passo 8: Preencher dados do cliente

![08_preencher_dados_cliente](operacional/screenshots/08_preencher_dados_cliente.png)

### O que fazer:

1. No campo **'Nome'**, digite: Cliente Exemplo
2. No campo **'Código'**, digite: cliente-exemplo
3. O código deve ser único e não pode ser alterado após criação
4. Preencha também Email, Domínio e Prefixo do Namespace (opcionais)

---

## Passo 9: Salvar cliente

![09_cliente_criado](operacional/screenshots/09_cliente_criado.png)

### O que fazer:

1. Clique no botão **'Criar'**
2. O cliente será salvo no banco de dados
3. Você será redirecionado para a lista de clientes

---

## Passo 10: Visualizar lista de clientes

![10_lista_clientes](operacional/screenshots/10_lista_clientes.png)

### O que fazer:

1. Na página de Clientes, você verá uma tabela com todos os clientes cadastrados
2. A tabela mostra: Nome, Código, Email, Domínio, Status e Ações
3. Você pode editar ou excluir clientes clicando nos botões correspondentes

---

## Passo 11: Editar cliente

![11_editar_cliente](operacional/screenshots/11_editar_cliente.png)

### O que fazer:

1. Clique no botão **'Editar'** na linha do cliente desejado
2. O formulário será preenchido com os dados do cliente
3. Você pode modificar os campos (exceto o código)
4. Clique em **'Atualizar'** para salvar as alterações

---

## Passo 12: Navegar para Configurações

![12_pagina_configuracoes](operacional/screenshots/12_pagina_configuracoes.png)

### O que fazer:

1. Clique na aba **'Configurações'** no menu superior
2. Você será redirecionado para a página de configurações
3. Aqui você pode gerenciar configurações globais do sistema

---

## Passo 13: Fazer logout

![13_logout](operacional/screenshots/13_logout.png)

### O que fazer:

1. Clique no botão **'Sair'** no canto superior direito
2. Você será deslogado e redirecionado para a página de login
3. Para acessar novamente, você precisará fazer login novamente

---

