# 🚀 Scripts - ForgeERP

Este diretório contém scripts utilitários para instalação, configuração e gerenciamento do ForgeERP.

## 📋 Índice

- [Scripts de Instalação](#scripts-de-instalação)
- [Scripts de Configuração](#scripts-de-configuração)
- [Scripts Utilitários](#scripts-utilitários)

## 📦 Scripts de Instalação

Scripts de instalação automática para diferentes distribuições:

### Ubuntu/Debian

```bash
chmod +x scripts/install-ubuntu.sh
./scripts/install-ubuntu.sh
```

**Instala:**
- Docker e Docker Compose
- Git
- GitHub CLI
- Python 3.11
- Node.js 18 (via nvm)

### Fedora/RHEL

```bash
chmod +x scripts/install-fedora.sh
./scripts/install-fedora.sh
```

**Instala:**
- Docker e Docker Compose
- Git
- GitHub CLI
- Python 3.11
- Node.js 18 (via nvm)

### macOS

```bash
chmod +x scripts/install-macos.sh
./scripts/install-macos.sh
```

**Instala:**
- Docker Desktop (via Homebrew)
- Git
- GitHub CLI
- Python 3.11
- Node.js 18 (via nvm)

### Windows

Windows não possui scripts de instalação automática. Instale manualmente:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git for Windows](https://git-scm.com/download/win)
- [GitHub CLI](https://cli.github.com/)

## ⚙️ Scripts de Configuração

### GitHub Secrets

```bash
chmod +x scripts/setup_github_secrets.sh
./scripts/setup_github_secrets.sh
```

**Configura:**
- Secrets do GitHub automaticamente
- Lê arquivo `.secrets` local
- Configura todos os secrets necessários

### Runners Self-Hosted

```bash
chmod +x scripts/setup_runners.sh
./scripts/setup_runners.sh
```

**Configura:**
- Runners self-hosted nas máquinas Contabo
- Instala Docker e GitHub Actions Runner
- Configura runners com labels apropriados

### Primeiro Push

```bash
chmod +x scripts/first_push.sh
./scripts/first_push.sh
```

**Faz:**
- Cria repositório no GitHub (se não existir)
- Configura remote origin
- Faz commit inicial
- Faz push para GitHub

## 📝 Notas

- Todos os scripts são executáveis (`chmod +x`)
- Scripts de instalação requerem `sudo` em Linux
- Scripts de configuração requerem `gh` CLI instalado e logado

## 🔗 Referências

- [README.md](../README.md) - Documentação principal
- [docs/INSTALACAO.md](../docs/INSTALACAO.md) - Instruções detalhadas de instalação
- [.github/SECRETS.md](../.github/SECRETS.md) - Documentação de secrets

