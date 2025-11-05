# Arquitetura de Testes - ForgeERP

## 📋 Visão Geral

A arquitetura de testes do ForgeERP segue as melhores práticas de testing para FastAPI, incluindo:

- **Testes Unitários**: Testes de funções e classes individuais
- **Testes de Integração**: Testes de integração entre componentes
- **Testes E2E**: Testes end-to-end de fluxos completos
- **Fixtures**: Configuração reutilizável para testes

## 🏗️ Estrutura

```
backend/
├── tests/
│   ├── conftest.py              # Configuração e fixtures do pytest
│   ├── test_auth.py             # Testes de autenticação
│   ├── test_clients.py          # Testes de clientes
│   ├── test_permissions.py      # Testes de permissões
│   ├── unit/                     # Testes unitários
│   │   ├── test_authentication.py
│   │   └── ...
│   ├── integration/             # Testes de integração
│   │   ├── test_client_workflow.py
│   │   └── ...
│   ├── github_actions/          # Testes de GitHub Actions
│   │   ├── conftest.py          # Fixtures para act
│   │   ├── test_workflow_generation.py
│   │   ├── test_workflow_execution.py
│   │   ├── test_actions_generation.py
│   │   └── README.md
│   └── README.md
├── pytest.ini                    # Configuração do pytest
└── Makefile                      # Comandos úteis para testes
```

## 🚀 Como Executar

### Executar todos os testes

```bash
cd backend
pytest
```

### Executar tipos específicos de testes

```bash
# Apenas testes unitários
pytest tests/unit

# Apenas testes de integração
pytest tests/integration

# Testes de GitHub Actions (sem act - apenas validação YAML)
pytest tests/github_actions/ -m "not act"

# Testes de GitHub Actions com act (requer act instalado)
pytest tests/github_actions/ -m act

# Testes específicos
pytest tests/test_auth.py
```

### Executar com cobertura

```bash
pytest --cov=forgeerp --cov-report=html
```

### Usando Makefile

```bash
# Executar todos os testes
make test

# Executar apenas testes unitários
make test-unit

# Executar apenas testes de integração
make test-integration

# Executar com cobertura
make test-coverage

# Testes de GitHub Actions (sem act)
make test-github-actions

# Testes de GitHub Actions com act (requer act instalado)
make test-github-actions-act

# Verificar se act está instalado
make check-act

# Limpar artefatos de teste
make clean
```

## 🔧 Fixtures Disponíveis

### `session`
Sessão de banco de dados de teste (SQLite em memória).

```python
def test_example(session: Session):
    # Usar session para criar dados de teste
    user = User(...)
    session.add(user)
    session.commit()
```

### `client`
Cliente de teste FastAPI.

```python
def test_example(client: TestClient):
    response = client.get("/api/v1/endpoint")
    assert response.status_code == 200
```

### `admin_user`
Usuário admin para testes.

```python
def test_example(client: TestClient, admin_user: User):
    # Usar admin_user para testes que requerem admin
    pass
```

### `regular_user`
Usuário regular para testes.

```python
def test_example(client: TestClient, regular_user: User):
    # Usar regular_user para testes que requerem usuário comum
    pass
```

### `auth_headers_admin`
Headers de autenticação para admin.

```python
def test_example(client: TestClient, auth_headers_admin):
    response = client.get(
        "/api/v1/protected",
        headers=auth_headers_admin
    )
```

### `auth_headers_user`
Headers de autenticação para usuário regular.

```python
def test_example(client: TestClient, auth_headers_user):
    response = client.get(
        "/api/v1/protected",
        headers=auth_headers_user
    )
```

## 📊 Cobertura de Testes

### ✅ Implementado

- **Autenticação**: Login, logout, get current user
- **Clientes**: CRUD completo (create, read, update, delete)
- **Permissões**: Verificação básica de permissões
- **Integração**: Workflows completos de clientes
- **GitHub Actions**: Geração e validação de workflows
  - ✅ Geração de workflows (setup-client, deploy-client)
  - ✅ Validação de sintaxe YAML
  - ✅ Execução de workflows com `act`
  - ✅ Geração de actions reutilizáveis

### ⏳ Pendente

- Testes de módulos
- Testes de configurações
- Testes de integração com GitHub API
- Testes de workflows específicos (disaster-recovery, diagnose-services)
- Testes de modificação de workflows (xpath-like)

## 🎯 Estratégia de Testes

### Testes Unitários
- Testam funções e classes isoladamente
- Rápidos e focados
- Exemplos: `test_authentication.py`

### Testes de Integração
- Testam interação entre componentes
- Usam banco de dados de teste
- Exemplos: `test_client_workflow.py`

### Testes E2E
- Testam fluxos completos do usuário
- Mais lentos e complexos
- A ser implementado

## 📝 Boas Práticas

1. **Isolamento**: Cada teste deve ser independente
2. **Fixtures**: Use fixtures para setup e teardown
3. **Nomenclatura**: Use nomes descritivos para testes
4. **Assertions**: Use assertions claras e específicas
5. **Cobertura**: Mantenha alta cobertura de código
6. **Velocidade**: Mantenha testes rápidos quando possível

## 🔄 CI/CD

Os testes devem ser executados automaticamente no CI/CD:

```yaml
# .github/workflows/test.yml (a ser criado)
- name: Run tests
  run: |
    cd backend
    pytest --cov=forgeerp --cov-report=xml
    
- name: Run GitHub Actions tests (without act)
  run: |
    cd backend
    pytest tests/github_actions/ -m "not act"
```

## 📦 Testes com act

Para testes que executam workflows GitHub Actions localmente, usamos `act`:

### Instalação do act

```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Verificar instalação
act --version
```

### Executar testes com act

```bash
# Testes que requerem act
pytest tests/github_actions/ -m act

# Ou usando Makefile
make test-github-actions-act
```

Veja [INSTALAR_ACT.md](INSTALAR_ACT.md) para mais detalhes sobre instalação e uso do act.

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLModel Testing](https://sqlmodel.tiangolo.com/)

