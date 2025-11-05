#!/bin/bash
# Script para fazer primeiro push do ForgeERP para o GitHub

set -e

ORG="forgeerp"
REPO="forgeerp"

echo "🚀 Fazendo primeiro push do ForgeERP para GitHub"
echo ""

# Verificar se gh CLI está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) não está instalado"
    echo "   Instale com: brew install gh ou apt install gh"
    exit 1
fi

# Verificar se está logado
if ! gh auth status &> /dev/null; then
    echo "❌ Não está logado no GitHub CLI"
    echo "   Faça login com: gh auth login"
    exit 1
fi

# Verificar se repositório existe
if ! gh repo view "$ORG/$REPO" &> /dev/null; then
    echo "📦 Criando repositório $ORG/$REPO..."
    gh repo create "$ORG/$REPO" --public --description "ForgeERP - Sistema de infraestrutura para parceiros Odoo" || {
        echo "❌ Erro ao criar repositório"
        exit 1
    }
    echo "✅ Repositório criado"
else
    echo "✅ Repositório já existe"
fi

# Configurar git
echo ""
echo "🔧 Configurando git..."
git config user.name "$(gh api user --jq .login)" || git config user.name "ForgeERP"
git config user.email "$(gh api user --jq .email)" || git config user.email "forgeerp@users.noreply.github.com"

# Verificar se já tem remote
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin já configurado"
else
    echo "📝 Configurando remote origin..."
    git remote add origin "https://github.com/$ORG/$REPO.git" || {
        git remote set-url origin "https://github.com/$ORG/$REPO.git"
    }
    echo "✅ Remote origin configurado"
fi

# Adicionar arquivos
echo ""
echo "📝 Adicionando arquivos..."
git add .

# Commit inicial
echo ""
echo "💾 Fazendo commit inicial..."
git commit -m "🚀 MVP inicial do ForgeERP

- Backend FastAPI com SQLite
- Frontend React + Vite
- CLI Typer
- Docker Compose
- Testes E2E com Playwright
- GitHub Actions com runners self-hosted
- Sistema de módulos
- Geração de workflows GitHub Actions
- Integração com GitHub PRs" || {
    echo "⚠️  Nenhuma mudança para commitar"
}

# Renomear branch para main se necessário
if git branch --show-current | grep -q "master"; then
    echo "🔄 Renomeando branch para main..."
    git branch -M main
fi

# Push
echo ""
echo "📤 Fazendo push para GitHub..."
git push -u origin main || {
    echo "⚠️  Tentando push forçado (primeira vez)..."
    git push -u origin main --force
}

echo ""
echo "✅ Push realizado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Configure secrets: ./scripts/setup_github_secrets.sh"
echo "   2. Configure runners: ./scripts/setup_runners.sh"
echo "   3. Acesse: https://github.com/$ORG/$REPO"

