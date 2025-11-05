# 🎯 Decisões Técnicas - ForgeERP

## 📋 Visão Geral

Este documento registra as decisões técnicas importantes tomadas durante o desenvolvimento do ForgeERP MVP. Use este documento para entender o "porquê" por trás das escolhas arquiteturais.

**Última atualização:** 2025-11-05

---

## 🐳 Docker: Imagem Unificada

### Decisão

Uma única imagem Docker contém frontend (React), backend (FastAPI) e CLI.

### Motivação

1. **Simplicidade de deploy**: Usuário faz `docker pull` e `docker run`, pronto
2. **Sem necessidade de orquestração**: Não precisa de `docker-compose` em produção
3. **Inspiração**: Portainer (leve e simples)

### Alternativas Consideradas

1. **Múltiplas imagens** (frontend, backend separados)
   - ❌ Rejeitado: Requer orquestração e configuração mais complexa
2. **Frontend separado** (CDN ou serviço estático)
   - ❌ Rejeitado: Adiciona complexidade desnecessária para MVP

### Trade-offs

- ✅ **Prós**: Deploy simples, sem dependências externas
- ❌ **Contras**: Imagem maior (~500MB), mas aceitável para MVP

### Implementação

- Multi-stage Dockerfile: Stage 1 (frontend build) + Stage 2 (runtime)
- FastAPI serve arquivos estáticos do frontend
- SPA routing: catch-all route serve `index.html` para rotas não-API

---

## 💾 Banco de Dados: SQLite

### Decisão

Usar SQLite em vez de PostgreSQL ou MySQL.

### Motivação

1. **Deploy simples**: Não requer serviço de banco separado
2. **Leve**: Perfeito para MVP
3. **Fácil backup**: Um único arquivo (`data/forgeerp.db`)

### Alternativas Consideradas

1. **PostgreSQL**
   - ❌ Rejeitado: Requer serviço separado, complexifica deploy
2. **MySQL**
   - ❌ Rejeitado: Mesmo motivo do PostgreSQL

### Trade-offs

- ✅ **Prós**: Zero configuração, backup simples, leve
- ❌ **Contras**: Limitações de concorrência, mas suficiente para MVP

### Implementação

- Arquivo: `data/forgeerp.db` (volume Docker)
- Migrations: Alembic (SQLModel)
- Pode migrar para PostgreSQL no futuro se necessário

---

## 🧪 Testes: Documentação pelos Testes

### Decisão

Documentação visual gerada pelos próprios testes E2E, não por scripts separados.

### Motivação

1. **Documentação sempre atualizada**: Se o teste passa, a documentação está correta
2. **Testes como documentação**: Testes validam funcionalidade E geram docs
3. **Sem duplicação**: Um único código para testar e documentar

### Alternativas Consideradas

1. **Scripts separados** (`generate_docs.py`)
   - ❌ Rejeitado: Código duplicado, pode ficar desatualizado
2. **Documentação manual**
   - ❌ Rejeitado: Trabalhosa e sempre desatualizada

### Trade-offs

- ✅ **Prós**: Documentação sempre sincronizada, menos código para manter
- ❌ **Contras**: Testes podem ser mais lentos, mas aceitável

### Implementação

- Testes em `tests/e2e/test_documentation.py`
- Flag `--generate-docs` para gerar documentação
- Output: `docs/operacional/screenshots/` e `docs/operacional/GUIA_*.md`

---

## ⚛️ React: Utils Reutilizáveis para Espera

### Decisão

Criar funções utilitárias (`wait_for_react()`, `wait_for_navigation_complete()`) para esperar React hidratar.

### Motivação

1. **Problema recorrente**: Todo teste E2E precisa esperar React hidratar
2. **Evita duplicação**: Código repetido em todos os testes
3. **Manutenibilidade**: Uma mudança afeta todos os testes

### Alternativas Consideradas

1. **Esperas manuais** (`time.sleep()`, `page.wait_for_selector()`)
   - ❌ Rejeitado: Código duplicado, frágil
2. **Fixtures com espera automática**
   - ✅ Implementado: Fixtures já fazem espera automaticamente

### Trade-offs

- ✅ **Prós**: Código limpo, fácil de manter, consistente
- ❌ **Contras**: Mais uma camada de abstração, mas vale a pena

### Implementação

- `backend/tests/e2e/utils.py`: Funções `wait_for_react()` e `wait_for_navigation_complete()`
- Fixtures em `conftest.py` usam automaticamente
- Testes podem usar diretamente se necessário

---

## 🎨 Frontend: React + Vite

### Decisão

React 19 + TypeScript + Vite para frontend.

### Motivação

1. **Moderno**: React 19 com melhorias de performance
2. **TypeScript**: Type safety
3. **Vite**: Build rápido e leve

### Alternativas Consideradas

1. **Next.js**
   - ❌ Rejeitado: Overhead desnecessário para SPA simples
2. **Vue.js**
   - ❌ Rejeitado: Equipe já conhece React melhor

### Trade-offs

- ✅ **Prós**: Stack moderna, TypeScript, build rápido
- ❌ **Contras**: Necessário esperar React hidratar (resolvido com utils)

---

## 🚀 Backend: FastAPI + SQLModel

### Decisão

FastAPI com SQLModel (Pydantic + SQLAlchemy).

### Motivação

1. **Type safety**: Pydantic valida requests/responses
2. **ORM moderno**: SQLModel une Pydantic e SQLAlchemy
3. **Performance**: FastAPI é um dos frameworks mais rápidos

### Alternativas Consideradas

1. **Django**
   - ❌ Rejeitado: Muito pesado para MVP
2. **Flask**
   - ❌ Rejeitado: Menos type safety, mais verboso

### Trade-offs

- ✅ **Prós**: Type safety, performance, moderno
- ❌ **Contras**: Curva de aprendizado, mas aceitável

---

## 📦 CLI: Typer + Rich

### Decisão

CLI usando Typer (baseado em Click) + Rich para output colorido.

### Motivação

1. **Typer**: Type hints, menos boilerplate que Click
2. **Rich**: Output bonito e colorido
3. **Abstração**: Esconde `docker compose` dos usuários

### Alternativas Consideradas

1. **Click puro**
   - ❌ Rejeitado: Mais verboso, sem type hints
2. **argparse**
   - ❌ Rejeitado: Muito boilerplate

### Trade-offs

- ✅ **Prós**: Código limpo, output bonito, type safe
- ❌ **Contras**: Dependência adicional, mas vale a pena

---

## 🧪 Testes: Playwright

### Decisão

Playwright para testes E2E (não Selenium).

### Motivação

1. **Mais rápido**: 3-5x mais rápido que Selenium
2. **Espera automática**: Melhor espera de elementos
3. **API moderna**: Mais limpa que Selenium

### Alternativas Consideradas

1. **Selenium**
   - ❌ Rejeitado: Mais lento, API verbosa
2. **Cypress**
   - ❌ Rejeitado: Playwright é mais moderno e rápido

### Trade-offs

- ✅ **Prós**: Rápido, confiável, API limpa
- ❌ **Contras**: Requer instalar browsers, mas aceitável

---

## 📝 Documentação: Estrutura em 3 Camadas

### Decisão

Documentação dividida em `funcional/`, `tecnica/`, `operacional/`.

### Motivação

1. **Funcional**: Para usuários finais (GUI)
2. **Técnica**: Para desenvolvedores (GUI + CLI)
3. **Operacional**: Gerada automaticamente (screenshots, guias)

### Alternativas Consideradas

1. **Documentação única**
   - ❌ Rejeitado: Muito confuso misturar público-alvo
2. **Documentação por formato**
   - ❌ Rejeitado: Não reflete o propósito do conteúdo

### Trade-offs

- ✅ **Prós**: Organização clara, fácil de encontrar
- ❌ **Contras**: Mais pastas, mas mais organizado

---

## 🔄 CI/CD: GitHub Actions

### Decisão

GitHub Actions para CI/CD e geração de documentação.

### Motivação

1. **Integrado**: Já está no GitHub
2. **Self-hosted runners**: Máquinas Contabo (sem custo)
3. **Automatização**: Build e docs automáticos

### Alternativas Consideradas

1. **GitLab CI**
   - ❌ Rejeitado: Repo está no GitHub
2. **Jenkins**
   - ❌ Rejeitado: Overhead desnecessário

### Trade-offs

- ✅ **Prós**: Gratuito, integrado, self-hosted runners
- ❌ **Contras**: Limitado ao GitHub, mas aceitável

---

## 📚 Próximas Decisões Pendentes

### 1. Estrutura de Módulos
- Como implementar módulos Odoo-like?
- Como módulos modificam workflows?
- Sistema de herança de configurações?

### 2. Geração de Workflows
- Como módulos geram steps do GitHub Actions?
- Template engine (Jinja2)?
- Sistema de hooks?

### 3. Sistema de Permissões
- Como integrar com GitHub PRs?
- Validação de permissões?
- Sistema de roles?

### 4. Frontend Completo
- Componentes React para todas as funcionalidades?
- Estado global (Redux/Zustand)?
- Routing (React Router)?

---

**Nota**: Este documento deve ser atualizado conforme novas decisões são tomadas. Use como referência para entender o "porquê" das escolhas arquiteturais.

