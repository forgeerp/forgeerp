# Testes E2E com Playwright

## 🎯 O que é Playwright?

**Playwright** é uma ferramenta moderna de testes E2E que substitui o Selenium com vantagens:

- ✅ **Mais rápido** - Execução muito mais rápida que Selenium
- ✅ **Mais confiável** - Melhor espera automática de elementos
- ✅ **Melhor API** - API mais limpa e intuitiva
- ✅ **Multi-browser** - Chrome, Firefox, Safari, Edge
- ✅ **Headless** - Roda sem interface gráfica (mas pode ver)
- ✅ **Screenshots/Videos** - Captura automática de screenshots e vídeos

## 🚀 Instalação

### 1. Instalar dependências Python

```bash
cd backend
pip install -r requirements.txt
```

### 2. Instalar navegadores do Playwright

```bash
# Instalar navegadores
playwright install

# Ou apenas Chrome
playwright install chromium
```

## 🧪 Executar Testes

### Todos os testes E2E

```bash
cd backend
pytest tests/e2e/ -v
```

### Testes específicos

```bash
# Apenas testes de login
pytest tests/e2e/test_login.py -v

# Apenas testes de configurações
pytest tests/e2e/test_configurations.py -v

# Apenas testes de dashboard
pytest tests/e2e/test_dashboard.py -v
```

### Com interface gráfica (ver o navegador)

```bash
# Modo headed (ver o navegador)
pytest tests/e2e/ --headed -v

# Modo headed e lento (ver ações)
pytest tests/e2e/ --headed --slowmo=500 -v
```

### Com screenshots

```bash
# Screenshots em falhas
pytest tests/e2e/ --screenshot=only-on-failure -v
```

### Com vídeo

```bash
# Vídeo dos testes
pytest tests/e2e/ --video=on -v
```

## 📋 Fixtures Disponíveis

### `page`
Página limpa do navegador (não autenticada).

### `authenticated_page`
Página com usuário autenticado (login feito).

### `clean_page`
Página limpa sem autenticação.

### `frontend_url`
URL do frontend (padrão: http://localhost:3000).

### `api_url`
URL da API (padrão: http://localhost:8000).

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# .env ou export
export FRONTEND_URL=http://localhost:3000
export API_URL=http://localhost:8000
```

### Pytest Configuration

Adicionar ao `pytest.ini`:

```ini
[pytest]
addopts = 
    --headed=false  # Headless por padrão
    --slowmo=0      # Sem delay
    --video=on      # Gravar vídeos
    --screenshot=only-on-failure
```

## 📊 Vantagens do Playwright vs Selenium

| Feature | Playwright | Selenium |
|---------|-----------|----------|
| Velocidade | ⚡ Muito rápido | 🐌 Lento |
| API | ✅ Moderna e limpa | ❌ Verbosa |
| Espera automática | ✅ Excelente | ⚠️ Manual |
| Screenshots | ✅ Automático | ⚠️ Manual |
| Vídeos | ✅ Automático | ❌ Não |
| Headless | ✅ Nativo | ⚠️ Complicado |
| Multi-browser | ✅ Fácil | ✅ Sim |
| Debug | ✅ Excelente | ⚠️ Difícil |

## 🎯 Exemplos de Testes

### Teste Simples

```python
def test_login(clean_page: Page):
    """Test login"""
    clean_page.fill('input[type="text"]', "admin")
    clean_page.fill('input[type="password"]', "admin")
    clean_page.click('button[type="submit"]')
    expect(clean_page.locator("text=Dashboard")).to_be_visible()
```

### Teste com Espera

```python
def test_async_loading(authenticated_page: Page):
    """Test async loading"""
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    expect(authenticated_page.locator("text=Configurações")).to_be_visible()
```

### Teste com Screenshot

```python
def test_with_screenshot(authenticated_page: Page):
    """Test with screenshot"""
    authenticated_page.screenshot(path="screenshot.png")
    # Test continues...
```

## 🔄 CI/CD

Playwright funciona perfeitamente em CI/CD:

```yaml
# .github/workflows/test.yml
- name: Install Playwright
  run: |
    pip install playwright
    playwright install --with-deps chromium

- name: Run E2E tests
  run: pytest tests/e2e/ -v
```

## 📚 Recursos

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest-Playwright](https://github.com/microsoft/playwright-python)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)

