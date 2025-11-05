# 📦 Instalar act - GitHub Actions Local Testing

## O que é act?

`act` é uma ferramenta que permite executar GitHub Actions localmente para testes.

## 🚀 Instalação

### macOS (Homebrew)

\`\`\`bash
brew install act
\`\`\`

### Linux

\`\`\`bash
# Via script de instalação
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Ou via Snap
snap install act

# Ou via AUR (Arch Linux)
yay -S act-bin
\`\`\`

### Windows

\`\`\`bash
# Via Chocolatey
choco install act-cli

# Via Scoop
scoop install act
\`\`\`

## ✅ Verificar Instalação

\`\`\`bash
act --version
\`\`\`

## 🧪 Executar Testes com act

\`\`\`bash
cd backend

# Testes sem act (apenas validação YAML)
pytest tests/github_actions/ -m "not act"

# Testes com act (requer act instalado)
pytest tests/github_actions/ -m act

# Ou usando Makefile
make test-github-actions      # Sem act
make test-github-actions-act # Com act
make check-act               # Verificar se act está instalado
\`\`\`

## 📚 Documentação

- [act GitHub](https://github.com/nektos/act)
- [act Documentation](https://github.com/nektos/act#readme)
