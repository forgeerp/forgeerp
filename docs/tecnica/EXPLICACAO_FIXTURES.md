# 🔧 O que são Fixtures no Pytest?

## 📖 Definição

Uma **fixture** no pytest é uma função decorada com `@pytest.fixture` que fornece dados, configurações ou recursos que podem ser usados por múltiplos testes. É uma forma de **setup e teardown** reutilizável.

## 🎯 Por que usar Fixtures?

1. **Reutilização**: Evita duplicação de código de setup
2. **Isolamento**: Cada teste recebe uma instância limpa
3. **Organização**: Código de setup centralizado
4. **Flexibilidade**: Fixtures podem depender de outras fixtures

## 📝 Exemplo Básico

```python
import pytest

@pytest.fixture
def user():
    """Cria um usuário para testes"""
    return {
        "username": "test_user",
        "email": "test@example.com"
    }

def test_user_creation(user):
    """Testa criação de usuário usando a fixture user"""
    assert user["username"] == "test_user"
    assert user["email"] == "test@example.com"
```

## 🔄 Fixtures no ForgeERP

### 1. `session` - Banco de Dados de Teste

```python
@pytest.fixture(name="session")
def session_fixture():
    """Cria uma sessão de banco de dados de teste"""
    engine = create_engine("sqlite:///:memory:")  # Banco em memória
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  # Fornece a sessão para o teste
    # Após o teste, o banco é limpo automaticamente
```

**Uso:**
```python
def test_create_client(session: Session):
    client = Client(name="Test", code="test")
    session.add(client)
    session.commit()
    assert client.id is not None
```

### 2. `client` - Cliente de Teste FastAPI

```python
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cria um cliente de teste FastAPI"""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()  # Limpa após o teste
```

**Uso:**
```python
def test_api_endpoint(client: TestClient):
    response = client.get("/api/v1/clients")
    assert response.status_code == 200
```

### 3. `admin_user` - Usuário Admin para Testes

```python
@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session):
    """Cria um usuário admin para testes"""
    user = User(
        username="admin",
        email="admin@test.com",
        password_hash=get_password_hash("admin"),
        role="superuser",
        is_active=True
    )
    session.add(user)
    session.commit()
    return user
```

**Uso:**
```python
def test_admin_permission(admin_user: User):
    assert check_permission(admin_user, "client_create") is True
```

### 4. `auth_headers_admin` - Headers de Autenticação

```python
@pytest.fixture(name="auth_headers_admin")
def auth_headers_admin_fixture(client: TestClient, admin_user: User):
    """Headers de autenticação para admin"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

**Uso:**
```python
def test_protected_endpoint(client: TestClient, auth_headers_admin):
    response = client.get(
        "/api/v1/clients",
        headers=auth_headers_admin
    )
    assert response.status_code == 200
```

### 5. `github_repo_dir` - Repositório Git Temporário

```python
@pytest.fixture(name="github_repo_dir")
def github_repo_dir_fixture():
    """Cria um repositório Git temporário para testes"""
    temp_dir = tempfile.mkdtemp()
    repo_path = Path(temp_dir) / "test-repo"
    repo_path.mkdir(parents=True)
    
    # Inicializa git
    subprocess.run(["git", "init"], cwd=repo_path)
    
    yield repo_path
    
    # Limpa após o teste
    shutil.rmtree(temp_dir)
```

**Uso:**
```python
def test_workflow_generation(github_repo_dir):
    generator = GitHubWorkflowGenerator(github_repo_dir)
    generator.generate_workflow("test.yml", {...})
    assert (github_repo_dir / ".github" / "workflows" / "test.yml").exists()
```

## 🔗 Dependências entre Fixtures

Fixtures podem depender de outras fixtures:

```python
@pytest.fixture
def session():
    # Setup do banco
    yield session

@pytest.fixture
def admin_user(session):  # Depende de session
    # Usa session para criar usuário
    user = User(...)
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def auth_headers(client, admin_user):  # Depende de client e admin_user
    # Usa client e admin_user para fazer login
    response = client.post("/api/v1/auth/login", ...)
    return {"Authorization": f"Bearer {token}"}
```

## 📍 Onde ficam as Fixtures?

### `conftest.py`
- **Local**: `tests/conftest.py` - Fixtures disponíveis para todos os testes
- **Específico**: `tests/github_actions/conftest.py` - Fixtures apenas para testes de GitHub Actions

### Escopo das Fixtures

```python
@pytest.fixture(scope="function")  # Padrão - uma por teste
@pytest.fixture(scope="class")   # Uma por classe
@pytest.fixture(scope="module")  # Uma por módulo
@pytest.fixture(scope="session") # Uma por sessão de testes
```

## 💡 Vantagens

1. **Código Limpo**: Testes focam na lógica, não no setup
2. **Reutilização**: Mesmo setup para múltiplos testes
3. **Isolamento**: Cada teste tem dados limpos
4. **Manutenção**: Mudanças em um lugar afetam todos os testes

## 🎯 Exemplo Completo

```python
# conftest.py
@pytest.fixture
def session():
    """Banco de dados de teste"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    """Cliente FastAPI de teste"""
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)

@pytest.fixture
def admin_user(session):
    """Usuário admin"""
    user = User(username="admin", password_hash=hash("admin"), ...)
    session.add(user)
    session.commit()
    return user

# test_clients.py
def test_create_client(client, admin_user):
    """Testa criação de cliente"""
    # client e admin_user são injetados automaticamente
    response = client.post(
        "/api/v1/clients",
        json={"name": "Test", "code": "test"},
        headers=get_auth_headers(client, admin_user)
    )
    assert response.status_code == 201
```

## 📚 Recursos

- [Pytest Fixtures Documentation](https://docs.pytest.org/en/stable/fixture.html)
- [Fixture Best Practices](https://docs.pytest.org/en/stable/fixture.html#fixture-best-practices)

