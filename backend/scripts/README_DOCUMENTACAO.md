# 📖 Gerar Documentação Visual com Playwright

## 🎯 O que é?

Playwright pode gerar documentação visual automaticamente:
- ✅ Screenshots de cada passo
- ✅ Guias passo a passo
- ✅ Documentação HTML
- ✅ Markdown com imagens

## 🚀 Como Usar

### 1. Gerar Documentação Visual Simples

```bash
cd backend
python scripts/generate_docs.py
```

**Gera:**
- `docs/GUIA_VISUAL.md` - Markdown com screenshots
- `docs/GUIA_VISUAL.html` - HTML visual
- `docs/screenshots/*.png` - Screenshots individuais

### 2. Gerar Guia Passo a Passo Detalhado

```bash
cd backend
python scripts/generate_docs_step_by_step.py
```

**Gera:**
- `docs/GUIA_PASSO_A_PASSO.md` - Guia completo com instruções
- `docs/screenshots/*.png` - Screenshots de cada passo

## 📋 Requisitos

### 1. Aplicação Rodando

```bash
# Subir aplicação
docker-compose up -d

# Criar usuário admin
docker-compose exec backend python scripts/create_admin_user.py
```

### 2. Variáveis de Ambiente (opcional)

```bash
export FRONTEND_URL=http://localhost:3000
export API_URL=http://localhost:8000
```

## 📸 Exemplo de Documentação Gerada

### Markdown

```markdown
## 1. Acessar a aplicação

![login_01_initial_page](screenshots/login_01_initial_page.png)

### O que fazer:

1. Abra o navegador e acesse: http://localhost:3000
2. A página de login será exibida automaticamente
3. Você verá o formulário de login com campos para usuário e senha
```

### HTML

Gera um HTML visual completo com todas as imagens e instruções.

## 🎨 Personalizar Documentação

### Adicionar Mais Passos

Edite `generate_docs_step_by_step.py` e adicione novos passos:

```python
await self.add_step(
    page,
    15,
    "Título do passo",
    [
        "Instrução 1",
        "Instrução 2",
        "Instrução 3"
    ],
    "screenshot_name"
)
```

### Modificar Screenshots

```python
# Screenshot full page
await page.screenshot(path="path.png", full_page=True)

# Screenshot de elemento específico
await page.locator("selector").screenshot(path="path.png")

# Screenshot com delay
await asyncio.sleep(2)  # Espera 2 segundos
await page.screenshot(path="path.png")
```

## 🔧 Configurações

### Modo Headed (Ver Navegador)

```python
# Em generate_docs.py, mude:
browser = await p.chromium.launch(headless=False)  # Ver navegador
```

### Resolução Customizada

```python
context = await browser.new_context(
    viewport={"width": 1920, "height": 1080}  # Full HD
)
```

### Delay Entre Passos

```python
await asyncio.sleep(1)  # Espera 1 segundo entre passos
```

## 📊 Vantagens

### ✅ Documentação Automática
- Não precisa tirar screenshots manualmente
- Sempre atualizada com a UI atual
- Fácil de regenerar

### ✅ Guias Visuais
- Screenshots de cada passo
- Instruções detalhadas
- Fácil de seguir

### ✅ Múltiplos Formatos
- Markdown (para GitHub/README)
- HTML (para web)
- Imagens PNG (para documentos)

## 🎯 Casos de Uso

### 1. Documentação de Usuário
- Guias passo a passo
- Como usar cada funcionalidade
- Screenshots atualizados

### 2. Onboarding
- Guias para novos usuários
- Tutorial visual
- Documentação de configuração

### 3. Testes de Regressão Visual
- Screenshots de cada versão
- Comparar mudanças visuais
- Documentar evolução da UI

## 📚 Exemplos

### Exemplo 1: Documentação de Login

```bash
python scripts/generate_docs_step_by_step.py
```

Gera guia completo de como fazer login.

### Exemplo 2: Documentação de Configurações

Incluído no guia passo a passo.

### Exemplo 3: Documentação Personalizada

Crie seu próprio script baseado nos exemplos:

```python
async def generate_my_guide(self, page: Page):
    await self.add_step(
        page,
        1,
        "Meu passo",
        ["Instrução 1", "Instrução 2"],
        "my_screenshot"
    )
```

## 🐛 Troubleshooting

### Aplicação não está rodando

```bash
# Verificar se está rodando
docker-compose ps

# Subir se não estiver
docker-compose up -d
```

### Erro de autenticação

```bash
# Criar usuário admin
docker-compose exec backend python scripts/create_admin_user.py
```

### Screenshots não aparecem

```bash
# Verificar se diretório existe
mkdir -p docs/screenshots

# Verificar permissões
chmod 755 docs/screenshots
```

## 📝 Notas

- Screenshots são salvos em `docs/screenshots/`
- Markdown é gerado em `docs/GUIA_*.md`
- HTML é gerado em `docs/GUIA_*.html`
- Documentação é gerada automaticamente
- Sempre atualizada com a UI atual

## 🎉 Conclusão

Playwright é perfeito para gerar documentação visual:
- ✅ Automático
- ✅ Atualizado
- ✅ Visual
- ✅ Fácil de usar

