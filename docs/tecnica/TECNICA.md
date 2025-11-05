# 🛠️ Documentação Técnica (GUI + CLI)

Detalhes técnicos para operar o ForgeERP via GUI e CLI, além de integrações e automações.

## 📦 Instalação e Dependências

- Requisitos: Docker, Git, GitHub CLI, Python 3.11+, Node 18+
- Instalação detalhada: veja `INSTALACAO.md`
- Scripts de instalação: `scripts/install-ubuntu.sh`, `scripts/install-fedora.sh`, `scripts/install-macos.sh`

## 🚀 Subida e Parada (CLI)

```bash
forge up       # sobe serviços
forge down     # para serviços
forge status   # status dos serviços
forge logs -f  # logs em tempo real
```

> Observação: `docker compose` é usado internamente pelo CLI.

## 👤 Usuários

```bash
forge user --username admin --password admin --email admin@exemplo.com
```

## 🧪 Testes

```bash
forge test --unit
forge test --integration
forge test --e2e
forge test --coverage
```

## 🔧 Limpeza e Atualização

```bash
forge clean
forge update
```

## 🗄️ Banco de Dados

- Padrão: SQLite em `data/`
- Variável: `DATABASE_URL` (suporta Postgres conforme evolução)

## 🔐 Configuração de Secrets (GitHub)

- Use `forge github secrets` (interativo) ou consulte `.github/SECRETS.md`
- Armazene tokens (ex.: `GITHUB_TOKEN`) com segurança

## 🏃 Runners Self-Hosted

- Script: `scripts/setup_runners.sh`
- Requer credenciais e labels (ex.: `contabo`, `linux`, `x64`)

## 🤖 Workflows (GitHub Actions)

- Gerador escreve no fork do usuário em `.github/workflows/`
- Módulos ativos influenciam os jobs/steps gerados
- Workflow auxiliar: `.github/workflows/generate-workflows.yml`

## 🌐 GUI (Técnico)

- Frontend (React + Vite): `frontend/`
- Variável de API: `VITE_API_URL` (fallback: `http://localhost:8000`)
- Autenticação: token em `localStorage` após login

## 🧩 Módulos e Extensões

- Estrutura modular em `backend/addons/`
- `manifest.yaml` por módulo (exposição/controle de features)

## 📸 Documentação Operacional (Automática)

- Scripts internos: `backend/scripts/generate_docs*.py`
- Workflow de geração: `.github/workflows/generate-docs.yml`

## 🔗 Referências

- `README.md` (visão geral)
- `DAILY_USAGE.md` (uso diário por CLI)
- `INSTALAR_ACT.md` (testar Actions localmente)
- `TESTES.md` e `ARQUITETURA_TESTES.md` (testes)
- `DOCUMENTACAO_VISUAL.md` (docs automáticas)

