#!/bin/bash
# Script para configurar secrets do GitHub baseado no .secrets do k8s-deploy-softhill

set -e

ORG="forgeerp"
REPO="forgeerp"
SECRETS_FILE="../k8s-deploy-softhill/.secrets"

echo "🔐 Configurando GitHub Secrets para $ORG/$REPO"
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

# Verificar se arquivo .secrets existe
if [ ! -f "$SECRETS_FILE" ]; then
    echo "⚠️  Arquivo .secrets não encontrado em $SECRETS_FILE"
    echo "   Criando a partir do .secrets.example..."
    echo ""
    echo "   Por favor, copie o .secrets do k8s-deploy-softhill para continuar"
    exit 1
fi

# Carregar secrets do arquivo
source "$SECRETS_FILE"

# Função para configurar secret
set_secret() {
    local secret_name=$1
    local secret_value=$2
    
    if [ -z "$secret_value" ]; then
        echo "⚠️  $secret_name está vazio - pulando"
        return
    fi
    
    echo "📝 Configurando $secret_name..."
    gh secret set "$secret_name" --repo "$ORG/$REPO" --body "$secret_value" || {
        echo "❌ Erro ao configurar $secret_name"
        return 1
    }
    echo "✅ $secret_name configurado"
}

# Secrets obrigatórios
echo "📋 Configurando secrets obrigatórios..."
echo ""

# SSH e Infraestrutura
set_secret "SSH_KEY" "$SSH_KEY"
set_secret "SSH_KEY_NAME" "${SSH_KEY_NAME:-forgeerp-key}"
set_secret "RUNNER_DEV_HML_IP" "$SECRET_DEV_HML_SERVER_IP"
set_secret "RUNNER_PROD_IP" "$SECRET_PROD_SERVER_IP"

# GitHub
set_secret "GHCR_TOKEN" "$GHCR_TOKEN"
set_secret "GITHUB_TOKEN" "$GITHUB_TOKEN"

# APIs
set_secret "GODADDY_API_KEY" "$GODADDY_API_KEY"
set_secret "GODADDY_API_SECRET" "$GODADDY_API_SECRET"

# Backblaze B2
set_secret "B2_ACCOUNT_ID" "$B2_ACCOUNT_ID"
set_secret "B2_APPLICATION_KEY" "$B2_APPLICATION_KEY"

# PostgreSQL
set_secret "POSTGRES_PASSWORD" "$POSTGRES_PASSWORD"

# Hetzner (opcional)
set_secret "HETZNER_API_TOKEN" "$HETZNER_API_TOKEN"

# Secrets do ForgeERP
set_secret "SECRET_KEY" "${SECRET_KEY:-$(openssl rand -hex 32)}"
set_secret "DATABASE_URL" "${DATABASE_URL:-sqlite:///./data/forgeerp.db}"

echo ""
echo "✅ Secrets configurados com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Configure os runners self-hosted nas máquinas Contabo"
echo "   2. Execute: ./scripts/setup_runners.sh"

