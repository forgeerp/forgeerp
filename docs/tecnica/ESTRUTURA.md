# Estrutura do Projeto ForgeERP

## 📁 Estrutura Completa

```
forgeerp/
├── backend/                          # Backend FastAPI
│   ├── forgeerp/                      # Módulos core
│   │   ├── core/                     # Módulo core
│   │   │   ├── database/
│   │   │   │   ├── models/          # SQLModel models
│   │   │   │   ├── schemas/         # Pydantic schemas
│   │   │   │   └── migrations/      # Alembic migrations
│   │   │   ├── api/
│   │   │   │   └── routes/          # FastAPI routes
│   │   │   ├── engine/
│   │   │   │   └── github_generator/  # Gerador de .github/
│   │   │   └── services/            # Serviços (auth, encryption, etc)
│   │   ├── web/                      # Servir frontend estático
│   │   ├── cli/                      # Comandos CLI
│   │   └── main.py                   # Entry point FastAPI
│   ├── addons/                       # Módulos opcionais
│   │   ├── providers/               # Padrões de provedores
│   │   ├── database/                 # Padrões de database
│   │   ├── hetzner/                  # Implementação Hetzner
│   │   ├── postgresql/               # Implementação PostgreSQL
│   │   ├── kubernetes/               # Implementação Kubernetes
│   │   ├── ssl/                      # Implementação SSL
│   │   ├── backup/                   # Implementação Backup
│   │   ├── diagnosis/                # Implementação Diagnóstico
│   │   └── fix/                      # Implementação Correção
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                         # Frontend React + Vite
│   ├── src/
│   │   ├── components/               # Componentes React
│   │   ├── pages/                    # Páginas
│   │   └── lib/                      # Utilitários
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── cli/                               # CLI Typer (separado)
│   ├── forgeerp/
│   │   └── cli/
│   │       └── main.py
│   ├── pyproject.toml
│   └── Dockerfile
├── addons/                            # Módulos opcionais (alternativa)
│   └── (mesma estrutura de backend/addons)
├── data/                              # SQLite database
├── docker-compose.yml
└── README.md
```

## 📝 Notas

- **Backend**: `backend/forgeerp/` contém os módulos core
- **Addons**: Podem estar em `backend/addons/` ou `addons/` (escolha uma estrutura)
- **Frontend**: Separado em `frontend/`
- **CLI**: Separado em `cli/` (mas também há `backend/forgeerp/cli/`)
- **Data**: Diretório para SQLite database

## 🔧 Estrutura Planejada vs Implementada

### ✅ Implementado Corretamente
- `backend/forgeerp/core/` - Módulo core
- `backend/forgeerp/core/database/models/` - Modelos SQLModel
- `backend/forgeerp/core/api/routes/` - Rotas FastAPI
- `backend/forgeerp/core/engine/github_generator/` - Gerador de .github/
- `backend/forgeerp/core/services/` - Serviços
- `frontend/` - Frontend React + Vite
- `cli/` - CLI Typer separado

### ⚠️ Ajustes Necessários
- `backend/forgeerp/web/` - Criado, mas precisa implementação
- `backend/forgeerp/cli/` - Criado, mas precisa implementação
- `backend/addons/` - Criado, mas precisa implementação dos módulos
- `backend/forgeerp/core/database/migrations/` - Criado, mas precisa configuração Alembic

