# Testes - ForgeERP Backend

## 📋 Estrutura de Testes

```
tests/
├── conftest.py          # Configuração e fixtures do pytest
├── test_auth.py         # Testes de autenticação
├── test_clients.py      # Testes de clientes
├── test_permissions.py  # Testes de permissões
└── README.md            # Este arquivo
```

## 🚀 Como Executar

### Executar todos os testes

```bash
cd backend
pytest
```

### Executar testes específicos

```bash
# Testes de autenticação
pytest tests/test_auth.py

# Testes de clientes
pytest tests/test_clients.py

# Testes de permissões
pytest tests/test_permissions.py
```

### Executar com verbosidade

```bash
pytest -v
```

### Executar com cobertura

```bash
pytest --cov=forgeerp --cov-report=html
```

## 📝 Tipos de Testes

### Unit Tests
Testes unitários de funções e classes individuais.

### Integration Tests
Testes de integração entre componentes.

### E2E Tests
Testes end-to-end de fluxos completos.

## 🔧 Fixtures Disponíveis

### `session`
Sessão de banco de dados de teste (SQLite em memória).

### `client`
Cliente de teste FastAPI.

### `admin_user`
Usuário admin para testes.

### `regular_user`
Usuário regular para testes.

### `auth_headers_admin`
Headers de autenticação para admin.

### `auth_headers_user`
Headers de autenticação para usuário regular.

## 📊 Cobertura de Testes

- ✅ Autenticação (login, logout, get current user)
- ✅ Clientes (CRUD completo)
- ✅ Permissões (verificação básica)

## 🔄 Próximos Testes

- ⏳ Testes de módulos
- ⏳ Testes de configurações
- ⏳ Testes de integração com GitHub
- ⏳ Testes de geração de .github/

