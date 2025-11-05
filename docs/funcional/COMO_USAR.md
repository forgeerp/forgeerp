# 📖 Como Usar o ForgeERP

Guia completo de uso do ForgeERP, desde a instalação até o uso diário.

## 🚀 Início Rápido

### 1. Fazer Fork do Repositório

Primeiro, faça um fork do repositório para sua organização ou conta pessoal:

[➡️ Criar um fork deste repositório](https://github.com/forgeerp/forgeerp/fork)

### 2. Instalar Dependências

```bash
# Ubuntu/Debian
chmod +x scripts/install-ubuntu.sh && ./scripts/install-ubuntu.sh

# Fedora/RHEL
chmod +x scripts/install-fedora.sh && ./scripts/install-fedora.sh

# macOS
chmod +x scripts/install-macos.sh && ./scripts/install-macos.sh
```

**Ou instale manualmente**: Docker, Git, GitHub CLI, Python 3.11+, Node.js 18+.  
Veja [INSTALACAO.md](INSTALACAO.md) para instruções detalhadas.

### 3. Configurar Ambiente

```bash
git clone https://github.com/SEU_USUARIO/forgeerp.git
cd forgeerp
cp .env.example .env
# Edite o .env com suas configurações
```

### 4. Instalar CLI

```bash
cd cli
pip install -e .
```

### 5. Subir a Aplicação

```bash
forge up
```

### 6. Criar Usuário Admin

```bash
forge user
```

### 7. Acessar

Abra http://localhost:3000 e faça login com:
- **Username**: `admin`
- **Password**: `admin`

⚠️ **Altere a senha padrão após o primeiro login!**

## 📸 Guias Visuais

### Guia Visual Completo

Veja [GUIA_VISUAL.md](GUIA_VISUAL.md) para documentação visual com screenshots de todas as funcionalidades.

### Guia Passo a Passo

See [STEP_BY_STEP_GUIDE.md](../operacional/STEP_BY_STEP_GUIDE.md) for detailed step-by-step instructions on how to use each feature.

## 💻 Uso do CLI

O ForgeERP CLI é a ferramenta principal para uso diário:

```bash
# Ver todos os comandos
forge --help

# Subir/parar aplicação
forge up
forge down

# Ver status
forge status

# Ver logs
forge logs
forge logs --follow

# Gerenciar usuários
forge user --username admin --password senha123

# Executar testes
forge test
forge test --unit
forge test --coverage

# Atualizar aplicação
forge update
```

Veja [DAILY_USAGE.md](DAILY_USAGE.md) para mais comandos.

## 🔧 Funcionalidades Principais

### 1. Login e Autenticação

1. Acesse http://localhost:3000
2. Digite seu usuário e senha
3. Clique em "Entrar"
4. Você será redirecionado para o dashboard

### 2. Dashboard

- Visualize estatísticas gerais
- Veja lista de clientes
- Acesse diferentes seções do sistema

### 3. Configurações

- Crie novas configurações (chaves/valores)
- Edite configurações existentes
- Delete configurações
- Configure tipos (string, json, integer, boolean)

### 4. Gerenciamento de Clientes

- Crie novos clientes
- Edite informações de clientes
- Gerencie múltiplos clientes

### 5. Geração de Workflows

- Os workflows do GitHub Actions são gerados automaticamente
- Baseados nos módulos instalados
- Salvos em `.github/workflows/` no seu fork

## 📚 Documentação Adicional

- [README.md](../README.md) - Documentação principal
- [INSTALACAO.md](INSTALACAO.md) - Instalação detalhada
- [DAILY_USAGE.md](DAILY_USAGE.md) - Uso diário
- [GUIA_VISUAL.md](GUIA_VISUAL.md) - Guia visual
- [STEP_BY_STEP_GUIDE.md](../operacional/STEP_BY_STEP_GUIDE.md) - Step-by-step guide

## 🔗 Links Úteis

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📞 Suporte

- **Issues**: https://github.com/forgeerp/forgeerp/issues
- **Documentação**: [README.md](README.md)

