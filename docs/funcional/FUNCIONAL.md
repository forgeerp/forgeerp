# 📘 Documentação Funcional (GUI)

Guia funcional para uso do ForgeERP pela interface web, focado nas atividades do dia a dia.

## 🔐 Login

- Acesse: http://localhost:3000
- Informe usuário e senha
- Usuário padrão (dev): `admin` / `admin`

## 🏠 Dashboard

- Visão geral do ambiente
- Indicadores principais: quantidade de clientes, status do usuário, estado do sistema
- Acesso às seções através da barra de navegação

## ⚙️ Configurações (Chave/Valor)

Permite gerenciar variáveis operacionais do ForgeERP e integrações:
- Criar nova configuração: informe `Chave`, `Valor`, `Tipo` e `Descrição`
- Editar configuração existente
- Deletar configuração (ação irreversível)
- Tipos suportados: string, json, integer, boolean

Boas práticas:
- Use nomes de chave descritivos (ex.: `github_token`, `database_url`)
- Documente no campo `Descrição` o objetivo do parâmetro

## 👥 Clientes

- Listagem de clientes gerenciados pelo ForgeERP
- Ações previstas: visualizar, criar, editar, inativar (conforme evolução do MVP)

## ⚙️ Geração de Workflows (GitHub Actions)

- A geração efetiva acontece no seu fork, em `.github/workflows/`
- O sistema considera os módulos instalados para compor os workflows
- Para o usuário final, a ação é solicitar a geração (pela GUI) e acompanhar o status

## 🔒 Permissões

- O ForgeERP adota papéis mínimos (admin/usuário)
- A integração com PRs do GitHub restringe alterações críticas a quem tem permissão

## 🧩 Módulos

- O ForgeERP é modular (estilo Odoo). Módulos habilitados estendem capacidades
- Exemplos: `backup`, `diagnosis`, `fix`, `hetzner`, `postgresql`, `ssl`
- A interface mostrará funcionalidades conforme módulos ativos

## 🧾 Auditoria e Registros (futuro imediato)

- Logs básicos nos workflows e no backend
- Registros de ações de usuários relevantes

## ❓Dúvidas Comuns

- “Onde vejo os workflows?” → No seu fork GitHub, em `.github/workflows/`
- “Por que não aparecem workflows aqui?” → O repo principal não versiona workflows de clientes; eles vivem no fork
- “Como altero parâmetros?” → Em Configurações, atualize os valores correspondentes

---

Para detalhes técnicos e comandos, veja a Documentação Técnica.

