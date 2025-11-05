#!/bin/bash
# Instalação automática para Fedora/RHEL

set -e

echo "📦 Instalando dependências para Fedora/RHEL..."
echo ""

# Instalar Docker
echo "🐳 Instalando Docker..."
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Instalar Git
echo ""
echo "📥 Instalando Git..."
sudo dnf install -y git

# Instalar GitHub CLI
echo ""
echo "🔧 Instalando GitHub CLI..."
sudo dnf install -y 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install -y gh

# Instalar Python 3.11
echo ""
echo "🐍 Instalando Python 3.11..."
sudo dnf install -y python3.11 python3.11-pip

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

