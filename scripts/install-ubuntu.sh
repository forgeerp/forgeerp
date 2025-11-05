#!/bin/bash
# Instalação automática para Ubuntu/Debian

set -e

echo "📦 Instalando dependências para Ubuntu/Debian..."
echo ""

# Atualizar pacotes
echo "📝 Atualizando pacotes..."
sudo apt-get update

# Instalar Docker
echo ""
echo "🐳 Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
sudo usermod -aG docker $USER

# Instalar Git
echo ""
echo "📥 Instalando Git..."
sudo apt-get install -y git

# Instalar GitHub CLI
echo ""
echo "🔧 Instalando GitHub CLI..."
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update
sudo apt-get install -y gh

# Instalar Python 3.11
echo ""
echo "🐍 Instalando Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Instalar Node.js 18 via nvm
echo ""
echo "📦 Instalando Node.js 18 via nvm..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 18
nvm use 18
nvm alias default 18

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Faça logout e login novamente para aplicar mudanças do grupo docker"
echo "   2. Configure Git: git config --global user.name 'Seu Nome'"
echo "   3. Configure GitHub CLI: gh auth login"
echo "   4. Clone o repositório: git clone https://github.com/forgeerp/forgeerp.git"
echo "   5. Siga as instruções em README.md"

