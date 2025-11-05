# 🚧 O que Falta Implementar - ForgeERP MVP

## 📋 Status Atual

### ✅ Implementado

1. **Infraestrutura Base**
   - ✅ Imagem Docker unificada (frontend + backend + CLI)
   - ✅ SQLite database
   - ✅ FastAPI servindo frontend estático
   - ✅ CLI básico (`forge` commands)
   - ✅ Testes E2E com Playwright
   - ✅ Documentação gerada automaticamente

2. **Autenticação**
   - ✅ Login/logout via API
   - ✅ JWT tokens
   - ✅ Proteção de rotas API

3. **Frontend Básico**
   - ✅ Página de login
   - ✅ Dashboard básico
   - ✅ Componente de Configurações

4. **Backend Básico**
   - ✅ Models (Client, User, Configuration, Module)
   - ✅ API routes básicas (auth, clients, configurations)
   - ✅ Database setup

---

## 🚧 O que Falta (Fluxo Básico)

### 1. **Frontend Completo** 🔴 Crítico

#### Páginas Faltando
- [ ] **Clientes** - CRUD completo de clientes
  - Lista de clientes
  - Criar novo cliente
  - Editar cliente
  - Deletar cliente
  - Ver detalhes do cliente

- [ ] **Módulos** - Gerenciamento de módulos
  - Lista de módulos disponíveis
  - Instalar/desinstalar módulos
  - Ver módulos instalados por cliente

- [ ] **Ambientes** - Gerenciamento de ambientes (dev, hml, prod)
  - Lista de ambientes
  - Criar/editar ambiente
  - Ver status de cada ambiente

- [ ] **Configurações** - Melhorar componente existente
  - Validação de formulário
  - Filtros e busca
  - Paginação

- [ ] **Onboarding Wizard** - Wizard passo a passo
  - Passo 1: Criar primeiro cliente
  - Passo 2: Configurar módulos
  - Passo 3: Configurar ambientes
  - Passo 4: Gerar workflows

#### Componentes Faltando
- [ ] **Navegação** - Menu lateral ou topo
- [ ] **Formulários** - Componentes reutilizáveis
- [ ] **Tabelas** - Componentes de lista/tabela
- [ ] **Modais** - Para confirmações e forms
- [ ] **Notificações** - Toast/alert messages

#### Estado Global
- [ ] **Context/Redux** - Gerenciamento de estado
  - Estado do usuário
  - Estado de clientes
  - Estado de configurações
  - Cache de dados

---

### 2. **Backend - Rotas API** 🟡 Importante

#### Rotas Faltando
- [ ] **Módulos** - CRUD completo
  - `GET /api/v1/modules` - Lista módulos
  - `GET /api/v1/modules/{id}` - Detalhes módulo
  - `POST /api/v1/clients/{client_id}/modules` - Instalar módulo
  - `DELETE /api/v1/clients/{client_id}/modules/{module_id}` - Desinstalar

- [ ] **Ambientes** - CRUD completo
  - `GET /api/v1/clients/{client_id}/environments` - Lista ambientes
  - `POST /api/v1/clients/{client_id}/environments` - Criar ambiente
  - `PUT /api/v1/environments/{id}` - Atualizar ambiente
  - `DELETE /api/v1/environments/{id}` - Deletar ambiente

- [ ] **Workflows** - Geração de workflows
  - `POST /api/v1/clients/{client_id}/workflows/generate` - Gerar workflows
  - `GET /api/v1/clients/{client_id}/workflows` - Lista workflows gerados

- [ ] **GitHub** - Integração GitHub
  - `POST /api/v1/clients/{client_id}/github/fork` - Criar fork
  - `GET /api/v1/clients/{client_id}/github/prs` - Lista PRs
  - `POST /api/v1/clients/{client_id}/github/prs` - Criar PR

---

### 3. **Lógica de Negócio** 🟡 Importante

#### Geração de Workflows
- [ ] **GitHubWorkflowGenerator** - Implementação completa
  - Ler templates de workflows
  - Aplicar módulos instalados
  - Gerar workflows específicos por cliente
  - Salvar em `.github/workflows/`

#### Sistema de Módulos
- [ ] **ModuleManager** - Gerenciamento de módulos
  - Carregar módulos de `backend/addons/`
  - Registrar hooks de módulos
  - Aplicar módulos em workflows

#### Onboarding
- [ ] **OnboardingService** - Wizard de onboarding
  - Fluxo passo a passo
  - Validação de cada passo
  - Persistência de progresso
  - Finalização e geração de workflows

---

### 4. **Integração GitHub** 🟡 Importante

#### GitHub API
- [ ] **GitHubService** - Cliente GitHub completo
  - Criar fork do repositório
  - Criar branch
  - Criar PR
  - Verificar permissões
  - Validar PRs

#### Workflows GitHub Actions
- [ ] **Templates de Workflows** - Templates base
  - `setup-client.yml` - Setup inicial
  - `deploy-client.yml` - Deploy
  - `disaster-recovery.yml` - Disaster recovery
  - `diagnose-services.yml` - Diagnóstico
  - `fix-common-issues.yml` - Correção automática

---

### 5. **Sistema de Permissões** 🟢 Futuro

- [ ] **PermissionService** - Verificação de permissões
  - Roles (admin, user, viewer)
  - Permissões por recurso
  - Integração com GitHub PRs

---

## 📊 Priorização

### 🔴 Crítico (MVP não funciona sem)
1. Frontend - Página de Clientes (CRUD)
2. Backend - Rotas de Módulos e Ambientes
3. Geração básica de workflows

### 🟡 Importante (MVP funciona, mas incompleto)
1. Frontend - Páginas de Módulos e Ambientes
2. Backend - Integração GitHub básica
3. Onboarding wizard básico

### 🟢 Futuro (Pode esperar)
1. Sistema de permissões completo
2. Múltiplos provedores de infraestrutura
3. Monitoramento avançado

---

## 🎯 Próximos Passos Recomendados

### 1. Completar Frontend Básico
- Implementar página de Clientes (CRUD)
- Implementar navegação entre páginas
- Melhorar componentes existentes

### 2. Completar Backend Básico
- Implementar rotas de Módulos
- Implementar rotas de Ambientes
- Implementar geração básica de workflows

### 3. Integração GitHub
- Implementar GitHubService básico
- Criar templates de workflows
- Gerar workflows para clientes

### 4. Onboarding
- Implementar wizard básico
- Fluxo: Cliente → Módulos → Ambientes → Workflows

---

## 📝 Notas

- **Documentação visual**: Já está sendo gerada pelos testes E2E
- **Testes**: Estrutura de testes está pronta, falta cobrir funcionalidades
- **Infraestrutura**: Docker, banco, API base tudo funcionando
- **Foco**: Completar fluxo básico (Cliente → Módulos → Workflows) primeiro

---

**Última atualização**: 2025-11-05

