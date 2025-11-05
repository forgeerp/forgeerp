# 🧪 Test-Driven Development (TDD) no ForgeERP

## ✅ Sim, posso trabalhar com TDD!

Posso trabalhar com **Test-Driven Development (TDD)** seguindo o ciclo Red-Green-Refactor.

## 🔄 Ciclo TDD

### 1. 🔴 **RED** - Escrever Teste que Falha
Primeiro, escrevo um teste para a funcionalidade que ainda não existe.

### 2. 🟢 **GREEN** - Fazer o Teste Passar
Implemento o mínimo de código necessário para o teste passar.

### 3. 🔵 **REFACTOR** - Melhorar o Código
Refatoro o código mantendo os testes passando.

## 📋 Como Funciona TDD no ForgeERP

### Exemplo: Criar Funcionalidade de Módulos

#### Passo 1: 🔴 RED - Escrever Teste

```python
# tests/test_modules.py
def test_list_modules(client, auth_headers_admin):
    """Testa listagem de módulos"""
    response = client.get(
        "/api/v1/modules",
        headers=auth_headers_admin
    )
    assert response.status_code == 200
    assert "modules" in response.json()
```

**Resultado**: Teste falha (endpoint não existe)

#### Passo 2: 🟢 GREEN - Implementar Mínimo

```python
# forgeerp/core/api/routes/modules.py
@router.get("/modules")
async def list_modules():
    return {"modules": []}
```

**Resultado**: Teste passa (mas funcionalidade básica)

#### Passo 3: 🔵 REFACTOR - Melhorar

```python
# forgeerp/core/api/routes/modules.py
@router.get("/modules", response_model=ModuleListResponse)
async def list_modules(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Module).where(Module.is_active == True)
    modules = session.exec(statement).all()
    return ModuleListResponse(modules=modules, total=len(modules))
```

**Resultado**: Código melhorado, testes ainda passam

## 🎯 Quando Usar TDD

### ✅ Ideal para TDD:

1. **Nova Funcionalidade**
   - Criar novo endpoint
   - Adicionar novo modelo
   - Implementar novo serviço

2. **Correção de Bug**
   - Escrever teste que reproduz o bug
   - Corrigir o bug
   - Teste deve passar

3. **Refatoração**
   - Testes garantem que nada quebrou
   - Refatorar com confiança

### ⚠️ Menos Ideal:

1. **Protótipos Rápidos**
   - Explorar ideias
   - Validar conceitos

2. **Código Existente**
   - Adicionar testes depois (regression tests)
   - Não é TDD, mas é útil

## 📝 Exemplo Prático: Criar Sistema de Módulos

### 1. 🔴 RED - Testes

```python
# tests/test_modules.py
def test_create_module(client, auth_headers_admin):
    """Testa criação de módulo"""
    response = client.post(
        "/api/v1/modules",
        json={
            "name": "hetzner",
            "display_name": "Hetzner",
            "description": "Hetzner provider"
        },
        headers=auth_headers_admin
    )
    assert response.status_code == 201
    assert response.json()["name"] == "hetzner"

def test_list_modules(client, auth_headers_admin):
    """Testa listagem de módulos"""
    # ... criar módulo primeiro
    response = client.get(
        "/api/v1/modules",
        headers=auth_headers_admin
    )
    assert response.status_code == 200
    assert len(response.json()["modules"]) > 0
```

### 2. 🟢 GREEN - Implementar

```python
# forgeerp/core/api/routes/modules.py
@router.post("/modules", response_model=ModuleResponse)
async def create_module(
    module_data: ModuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    module = Module(**module_data.model_dump())
    session.add(module)
    session.commit()
    return module

@router.get("/modules", response_model=ModuleListResponse)
async def list_modules(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    modules = session.exec(select(Module)).all()
    return ModuleListResponse(modules=modules, total=len(modules))
```

### 3. 🔵 REFACTOR - Melhorar

- Adicionar validações
- Adicionar tratamento de erros
- Melhorar organização
- Adicionar mais testes

## 🚀 Como Trabalhar com TDD no ForgeERP

### Quando você pedir uma nova funcionalidade:

1. **Posso começar pelos testes**:
   - "Escreva testes para criar módulo"
   - "Implemente testes para workflow de disaster-recovery"

2. **Depois implementar**:
   - "Agora implemente a funcionalidade para os testes passarem"

3. **Ou tudo junto**:
   - "Implemente sistema de módulos usando TDD"

### Fluxo Recomendado:

```
1. Você pede: "Implemente sistema de módulos"
2. Eu pergunto: "Quer que eu use TDD?"
3. Se sim:
   - Escrevo testes primeiro (RED)
   - Implemento funcionalidade (GREEN)
   - Refatoro se necessário (REFACTOR)
4. Testes sempre passam ✅
```

## 📊 Benefícios do TDD

1. **Cobertura de Testes**: 100% do código novo testado
2. **Confiança**: Refatorar sem medo
3. **Design**: Testes forçam design melhor
4. **Documentação**: Testes documentam comportamento
5. **Debugging**: Mais fácil encontrar bugs

## 🎯 Próximos Passos com TDD

Podemos usar TDD para:

1. ✅ **Sistema de Módulos** - CRUD completo
2. ✅ **Motor de Geração de .github/** - Templates e workflows
3. ✅ **Sistema de Permissões Avançado** - Integração com GitHub PRs
4. ✅ **Módulos de Infraestrutura** - Hetzner, PostgreSQL, Kubernetes
5. ✅ **Workflows GitHub Actions** - Setup, deploy, disaster-recovery

## 💡 Dica

Sempre que você pedir uma nova funcionalidade, posso:
1. **Começar pelos testes** (TDD)
2. **Implementar e depois testar** (testes de regressão)
3. **Você escolhe** - prefere TDD ou implementação direta?

