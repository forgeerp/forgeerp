# 📦 Instalação de Dependências - ForgeERP

Este documento contém instruções detalhadas para instalar todas as dependências necessárias para executar o ForgeERP.

## 📋 Índice

- [Docker e Docker Compose](#docker-e-docker-compose)
- [Git](#git)
- [GitHub CLI](#github-cli-opcional-mas-recomendado)
- [Python 3.11+](#python-311-backend-desenvolvimento)
- [Node.js 18+](#nodejs-18-frontend-desenvolvimento)
- [Scripts de Instalação Automática](#scripts-de-instalação-automática)

## 🐳 Docker e Docker Compose

**Docker** é necessário para executar a aplicação em containers. O Docker Compose (plugin) é incluído e permite gerenciar múltiplos containers.

### Instalação

#### Linux (Ubuntu/Debian)

```bash
# Atualizar pacotes
sudo apt-get update

# Instalar dependências
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Adicionar chave GPG oficial do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Adicionar repositório Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Adicionar usuário ao grupo docker (opcional, para não precisar de sudo)
sudo usermod -aG docker $USER

# Verificar instalação
docker --version
docker compose version
```

**Nota**: Após adicionar o usuário ao grupo docker, faça logout e login novamente para que as mudanças tenham efeito.

#### Linux (Fedora/RHEL)

```bash
# Instalar dependências
sudo dnf install -y dnf-plugins-core

# Adicionar repositório Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Instalar Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar usuário ao grupo docker (opcional)
sudo usermod -aG docker $USER

# Verificar instalação
docker --version
docker compose version
```

**Nota**: Após adicionar o usuário ao grupo docker, faça logout e login novamente.

#### macOS

```bash
# Instalar via Homebrew
brew install --cask docker

# Ou baixar Docker Desktop: https://www.docker.com/products/docker-desktop/
```

**Verificar instalação:**
```bash
docker --version
docker compose version
```

#### Windows

Baixe e instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/).

**Verificar instalação:**
```bash
docker --version
docker compose version
```

### Verificar Instalação

```bash
docker --version          # Deve mostrar Docker version 24.0 ou superior
docker compose version   # Deve mostrar Docker Compose version v2.20 ou superior
docker ps                 # Deve listar containers (pode estar vazio)
```

### Troubleshooting

**Erro: "Cannot connect to the Docker daemon"**
```bash
# Iniciar Docker (Linux)
sudo systemctl start docker
sudo systemctl enable docker

# Verificar se está rodando
sudo systemctl status docker
```

**Erro: "Permission denied"**
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Fazer logout e login novamente
```

## 📥 Git

**Git** é necessário para clonar o repositório e gerenciar versões.

### Instalação

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y git
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install -y git
```

#### macOS

```bash
# Git já vem instalado, ou atualizar via Homebrew
brew install git
```

#### Windows

Baixe e instale o [Git for Windows](https://git-scm.com/download/win).

### Verificar Instalação

```bash
git --version  # Deve mostrar git version 2.30 ou superior
```

### Configuração Inicial

```bash
# Configurar nome e email
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Verificar configuração
git config --global --list
```

## 🔧 GitHub CLI (Opcional, mas recomendado)

**GitHub CLI** facilita a configuração de secrets e runners, além de gerenciar repositórios.

### Instalação

#### Linux (Ubuntu/Debian)

```bash
# Adicionar repositório oficial
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Instalar
sudo apt-get update
sudo apt-get install -y gh

# Fazer login
gh auth login
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install -y 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install -y gh

# Fazer login
gh auth login
```

#### macOS

```bash
brew install gh

# Fazer login
gh auth login
```

#### Windows

Baixe e instale o [GitHub CLI](https://cli.github.com/).

### Verificar Instalação

```bash
gh --version  # Deve mostrar gh version 2.40 ou superior
gh auth status  # Verificar se está logado
```

## 🐍 Python 3.11+ (Backend - Desenvolvimento)

**Python 3.11+** é necessário apenas se você quiser desenvolver localmente sem Docker.

### Instalação

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Verificar instalação
python3.11 --version
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install -y python3.11 python3.11-pip

# Verificar instalação
python3.11 --version
```

#### macOS

```bash
brew install python@3.11

# Verificar instalação
python3.11 --version
```

#### Windows

Baixe e instale o [Python 3.11](https://www.python.org/downloads/).

### Verificar Instalação

```bash
python3 --version  # Deve mostrar Python 3.11 ou superior
pip3 --version      # Deve mostrar pip version 23.0 ou superior
```

### Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r backend/requirements.txt
```

## 📦 Node.js 18+ (Frontend - Desenvolvimento)

**Node.js 18+** é necessário apenas se você quiser desenvolver o frontend localmente sem Docker.

### Instalação

#### Linux (Ubuntu/Debian) - Via nvm (Recomendado)

```bash
# Instalar nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recarregar shell
source ~/.bashrc

# Instalar Node.js 18
nvm install 18
nvm use 18

# Tornar padrão
nvm alias default 18
```

#### Linux (Fedora/RHEL) - Via nvm (Recomendado)

```bash
# Instalar nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recarregar shell
source ~/.bashrc

# Instalar Node.js 18
nvm install 18
nvm use 18

# Tornar padrão
nvm alias default 18
```

#### macOS

```bash
# Via Homebrew
brew install node@18

# Ou via nvm (recomendado)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

#### Windows

Baixe e instale o [Node.js 18](https://nodejs.org/).

### Verificar Instalação

```bash
node --version  # Deve mostrar v18.0 ou superior
npm --version   # Deve mostrar 9.0 ou superior
```

### Instalar Dependências

```bash
cd frontend
npm install
```

## 🚀 Scripts de Instalação Automática

Scripts de instalação automática para cada distribuição:

### Ubuntu/Debian

```bash
#!/bin/bash
# Instalação automática para Ubuntu/Debian

set -e

echo "📦 Instalando dependências para Ubuntu/Debian..."

# Atualizar pacotes
sudo apt-get update

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Git
sudo apt-get install -y git

# Instalar GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update
sudo apt-get install -y gh

# Instalar Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Instalar Node.js 18 via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

echo "✅ Instalação concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Faça logout e login novamente para aplicar mudanças do grupo docker"
echo "   2. Configure Git: git config --global user.name 'Seu Nome'"
echo "   3. Configure GitHub CLI: gh auth login"
echo "   4. Clone o repositório: git clone https://github.com/forgeerp/forgeerp.git"
```

### Fedora/RHEL

```bash
#!/bin/bash
# Instalação automática para Fedora/RHEL

set -e

echo "📦 Instalando dependências para Fedora/RHEL..."

# Instalar Docker
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Instalar Git
sudo dnf install -y git

# Instalar GitHub CLI
sudo dnf install -y 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install -y gh

# Instalar Python 3.11
sudo dnf install -y python3.11 python3.11-pip

# Instalar Node.js 18 via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

echo "✅ Instalação concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Faça logout e login novamente para aplicar mudanças do grupo docker"
echo "   2. Configure Git: git config --global user.name 'Seu Nome'"
echo "   3. Configure GitHub CLI: gh auth login"
echo "   4. Clone o repositório: git clone https://github.com/forgeerp/forgeerp.git"
```

### macOS

```bash
#!/bin/bash
# Instalação automática para macOS

set -e

echo "📦 Instalando dependências para macOS..."

# Verificar se Homebrew está instalado
if ! command -v brew &> /dev/null; then
    echo "Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Instalar Docker
brew install --cask docker

# Instalar Git
brew install git

# Instalar GitHub CLI
brew install gh

# Instalar Python 3.11
brew install python@3.11

# Instalar Node.js 18 via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

echo "✅ Instalação concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Abra Docker Desktop e aguarde iniciar"
echo "   2. Configure Git: git config --global user.name 'Seu Nome'"
echo "   3. Configure GitHub CLI: gh auth login"
echo "   4. Clone o repositório: git clone https://github.com/forgeerp/forgeerp.git"
```

## 📝 Notas

- **Docker** é obrigatório para executar o ForgeERP
- **Git** é obrigatório para clonar o repositório
- **GitHub CLI** é opcional, mas recomendado para facilitar a configuração
- **Python** e **Node.js** são necessários apenas para desenvolvimento local sem Docker

## 🔗 Referências

- [README.md](../README.md) - Documentação principal
- [Docker Documentation](https://docs.docker.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI Documentation](https://cli.github.com/)

