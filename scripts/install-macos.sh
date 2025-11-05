#!/bin/bash
# Instalação automática para macOS

set -e

echo "📦 Instalando dependências para macOS..."
echo ""

# Verificar se Homebrew está instalado
if ! command -v brew &> /dev/null; then
    echo "🍺 Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Instalar Docker
echo ""
echo "🐳 Instalando Docker..."
brew install --cask docker

# Instalar Git
echo ""
echo "📥 Instalando Git..."
brew install git

# Instalar GitHub CLI
echo ""
echo "🔧 Instalando GitHub CLI..."
brew install gh

# Instalar Python 3.11
echo ""
echo "🐍 Instalando Python 3.11..."
brew install python@3.11

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
echo "   1. Abra Docker Desktop e aguarde iniciar"
echo "   2. Configure Git: git config --global user.name 'Seu Nome'"
echo "   3. Configure GitHub CLI: gh auth login"
echo "   4. Clone o repositório: git clone https://github.com/forgeerp/forgeerp.git"
echo "   5. Siga as instruções em README.md"

