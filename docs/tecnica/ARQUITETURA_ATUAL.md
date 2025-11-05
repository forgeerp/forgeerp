# 🏗️ Arquitetura Atual - ForgeERP

## 📋 Visão Geral

Este documento descreve a arquitetura atual do ForgeERP após as refatorações e decisões técnicas implementadas. Use este documento como referência para entender o estado atual do projeto.

**Última atualização:** 2025-11-05

---

## 🎯 Princípios Arquiteturais

### 1. Imagem Docker Unificada
- **Decisão**: Uma única imagem Docker contém frontend, backend e CLI
- **Benefício**: Deploy simples com `docker pull` e `docker run`
- **Estrutura**:
  - Frontend: Build estático (React + Vite) servido pelo FastAPI
  - Backend: FastAPI servindo API + arquivos estáticos
  - CLI: Pacote pip instalado na imagem

### 2. Banco de Dados Leve
- **Decisão**: SQLite para facilitar deploy
- **Benefício**: Não requer serviço de banco separado
- **Localização**: `data/forgeerp.db` (volume Docker)

### 3. Estrutura de Testes Integrada
- **Decisão**: Documentação gerada pelos próprios testes E2E
- **Benefício**: Documentação sempre atualizada e testes como documentação
- **Comando**: `make docs-e2e` ou `pytest tests/e2e/test_documentation.py --generate-docs`

### 4. Utils Reutilizáveis para React
- **Decisão**: Funções utilitárias para esperar React hidratar
- **Benefício**: Evita duplicação e problemas de timing em todos os testes
- **Localização**: `backend/tests/e2e/utils.py`

---

## 📁 Estrutura do Projeto

```
forgeerp/
├── backend/                    # Backend FastAPI
│   ├── forgeerp/
│   │   ├── main.py            # FastAPI app (serve API + static frontend)
│   │   ├── core/
│   │   │   ├── database/      # Models e database
│   │   │   ├── api/           # Rotas API
│   │   │   └── ...
│   │   └── ...
│   ├── tests/
│   │   ├── e2e/
│   │   │   ├── utils.py       # Utils para esperar React
│   │   │   ├── conftest.py    # Fixtures E2E
│   │   │   ├── test_documentation.py  # Testes que geram docs
│   │   │   └── ...
│   │   └── ...
│   └── requirements.txt
│
├── frontend/                   # Frontend React + Vite
│   ├── src/
│   └── vite.config.ts
│
├── cli/                        # CLI ForgeERP
│   └── forgeerp/
│       └── cli/
│           └── main.py
│
├── docs/
│   ├── funcional/             # Documentação funcional (GUI)
│   ├── tecnica/               # Documentação técnica (GUI + CLI)
│   └── operacional/           # Documentação gerada automaticamente
│       └── screenshots/       # Screenshots gerados pelos testes
│
├── Dockerfile                  # Multi-stage: frontend build + backend
├── docker-compose.yml          # Para desenvolvimento local
└── README.md
```

---

## 🐳 Docker

### Imagem Unificada

**Stage 1: Frontend Build**
- Base: `node:20-alpine`
- Build do frontend React com Vite
- Output: `/app/frontend/dist`

**Stage 2: Runtime**
- Base: `python:3.11-slim`
- Dependências do sistema (incluindo Playwright browser dependencies)
- Backend Python + dependências
- Playwright browsers instalados (chromium para testes e documentação)
- CLI instalado via pip
- Frontend estático copiado de Stage 1 para `/app/static`
- WORKDIR: `/app/backend`
- PYTHONPATH: `/app/backend`

### Comandos

```bash
# Build local
docker build -t forgeerp:local .

# Usar imagem do GHCR (produção)
docker pull ghcr.io/forgeerp/forgeerp:latest
docker run -p 8000:8000 -v ./data:/app/data ghcr.io/forgeerp/forgeerp:latest

# Desenvolvimento
docker compose up --profile dev --build
```

---

## 🔧 FastAPI - Servindo Frontend Estático

### Estrutura de Rotas

```python
# Ordem de registro é importante:
# 1. API routes primeiro
app.include_router(auth_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
# ... outros routers

# 2. Health check
app.get("/health")

# 3. Static files (assets)
app.mount("/static", StaticFiles(directory="/app/static/static"))

# 4. SPA catch-all (por último)
app.get("/{full_path:path}")  # Serve index.html para todas outras rotas
```

### Caminhos

- **Static files**: `/app/static` (copiado do build do frontend)
- **Index HTML**: `/app/static/index.html`
- **Assets**: `/app/static/static/` (JS, CSS, imagens)

---

## 🧪 Testes E2E

### Utils Reutilizáveis

**`wait_for_react(page)`**
- Espera React root element (`#root`)
- Espera `document.readyState === 'complete'`
- Aguarda elementos renderizados
- Deve ser usado após `page.goto()`

**`wait_for_navigation_complete(page)`**
- Espera `networkidle`
- Chama `wait_for_react()`
- Deve ser usado após cliques que disparam navegação

### Fixtures

**`page`**: Página limpa do navegador
- Já chama `wait_for_react()` após `goto()`

**`authenticated_page`**: Página com usuário autenticado
- Login via API + localStorage
- Chama `wait_for_react()` após reload

**`clean_page`**: Página limpa sem autenticação
- Limpa localStorage
- Chama `wait_for_react()` após reload

### Geração de Documentação

**Testes de documentação**: `test_documentation.py`
- Testes normais do pytest
- Geram screenshots e markdown quando executados com `--generate-docs`
- Output: `docs/operacional/screenshots/` e `docs/operacional/GUIA_*.md`

**Comando**:
```bash
# Via Makefile
make docs-e2e

# Diretamente
pytest tests/e2e/test_documentation.py --generate-docs -v
```

---

## 📦 CLI

### Estrutura

- **Pacote pip**: `cli/forgeerp/`
- **Instalado na imagem**: `pip install -e ./cli`
- **Comando**: `forge`

### Comandos Principais

```bash
forge up          # Subir aplicação (docker compose up)
forge down        # Parar aplicação
forge status      # Status dos serviços
forge logs        # Ver logs
forge test        # Executar testes
forge user        # Criar usuário admin
```

### Integração com Docker

- CLI abstrai `docker compose` commands
- Usuários não precisam usar `docker compose` diretamente
- CLI verifica se Docker está instalado

---

## 🔄 Fluxo de Desenvolvimento

### Local

1. **Desenvolvimento frontend**: `cd frontend && npm run dev`
2. **Desenvolvimento backend**: `cd backend && uvicorn forgeerp.main:app --reload`
3. **Docker Compose**: `docker compose up --profile dev`

### Produção

1. **Build imagem**: `.github/workflows/build-images.yml`
2. **Push para GHCR**: Automático em push para `main`
3. **Deploy**: `docker pull ghcr.io/forgeerp/forgeerp:latest && docker run ...`

---

## 📝 Documentação

### Estrutura

- **`docs/funcional/`**: Uso diário pela GUI
- **`docs/tecnica/`**: Uso técnico (GUI + CLI)
- **`docs/operacional/`**: Documentação gerada automaticamente

### Geração Automática

- **Workflow**: `.github/workflows/generate-docs.yml`
- **Testes**: `tests/e2e/test_documentation.py`
- **Comando**: `make docs-e2e`
- **Output**: Screenshots e markdown em `docs/operacional/`

---

## 🚀 Decisões Técnicas Importantes

### 1. Imagem Unificada vs Múltiplas Imagens

**Decisão**: Imagem única
- **Razão**: Facilita deploy (apenas `docker pull` e `docker run`)
- **Trade-off**: Imagem maior, mas simplifica muito o deploy

### 2. SQLite vs PostgreSQL

**Decisão**: SQLite
- **Razão**: Não requer serviço de banco separado
- **Trade-off**: Limitações de concorrência, mas suficiente para MVP

### 3. Documentação por Testes vs Scripts Separados

**Decisão**: Documentação gerada pelos testes
- **Razão**: Documentação sempre atualizada, testes como documentação
- **Trade-off**: Testes podem ser mais lentos, mas valida funcionalidade

### 4. Utils Reutilizáveis vs Código Duplicado

**Decisão**: Utils reutilizáveis (`utils.py`)
- **Razão**: Evita duplicação e problemas de timing
- **Trade-off**: Mais uma camada de abstração, mas muito mais manutenível

---

## 🔍 Pontos de Atenção

### 1. Ordem de Rotas no FastAPI
- API routes devem ser registradas ANTES do catch-all SPA route
- Se não, o catch-all intercepta requisições da API

### 2. Caminhos do Static
- Frontend build: `/app/frontend/dist`
- Static copiado: `/app/static`
- Assets: `/app/static/static/`
- Verificar caminhos se mudar estrutura de build do Vite

### 3. PYTHONPATH e WORKDIR
- WORKDIR: `/app/backend` (para imports funcionarem)
- PYTHONPATH: `/app/backend` (para encontrar módulos)
- Scripts executados de `/app/backend` devem usar caminhos relativos

### 4. Espera do React
- SEMPRE usar `wait_for_react()` após `page.goto()`
- SEMPRE usar `wait_for_navigation_complete()` após cliques que disparam navegação
- Fixtures já fazem isso automaticamente

---

## 📚 Próximos Passos

### Arquitetura a Revisar

1. **Estrutura de módulos**: Módulos Odoo-like ainda não implementados
2. **Geração de workflows**: GitHub Actions workflows ainda não implementados
3. **Sistema de permissões**: Integração com GitHub PRs ainda não implementada
4. **Frontend completo**: Componentes React ainda não completos

### Arquivos a Revisar/Descartar

- Scripts antigos de documentação (já removidos)
- Documentação desatualizada em `docs/tecnica/`
- Testes que não fazem mais sentido
- Fixtures que não são mais usadas

---

## 🔗 Referências

- **Dockerfile**: Multi-stage build para imagem unificada
- **docker-compose.yml**: Configuração para desenvolvimento
- **backend/tests/e2e/utils.py**: Utils para esperar React
- **backend/tests/e2e/conftest.py**: Fixtures E2E
- **backend/tests/e2e/test_documentation.py**: Testes que geram documentação
- **backend/forgeerp/main.py**: FastAPI app servindo frontend estático

---

**Nota**: Este documento deve ser atualizado conforme a arquitetura evolui. Use como referência para entender o estado atual do projeto.

