#!/bin/bash
# Script para configurar runners self-hosted nas máquinas Contabo

set -e

ORG="forgeerp"
REPO="forgeerp"

echo "🚀 Configurando runners self-hosted para $ORG/$REPO"
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

# Obter token do runner
echo "📝 Obtendo token do runner..."
RUNNER_TOKEN=$(gh runner create-token --repo "$ORG/$REPO" 2>/dev/null || gh api repos/$ORG/$REPO/actions/runners/registration-token --jq .token)

if [ -z "$RUNNER_TOKEN" ]; then
    echo "❌ Erro ao obter token do runner"
    exit 1
fi

echo "✅ Token obtido"
echo ""

# Perguntar IPs dos servidores
read -p "IP do servidor DEV/HML (ou deixe vazio para pular): " DEV_HML_IP
read -p "IP do servidor PROD (ou deixe vazio para pular): " PROD_IP

# Configurar runner DEV/HML
if [ -n "$DEV_HML_IP" ]; then
    echo ""
    echo "🔧 Configurando runner DEV/HML em $DEV_HML_IP..."
    
    ssh -o StrictHostKeyChecking=no root@"$DEV_HML_IP" << EOF
        # Instalar Docker
        if ! command -v docker &> /dev/null; then
            echo "📦 Instalando Docker..."
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
        fi
        
        # Instalar GitHub Actions Runner
        mkdir -p ~/actions-runner && cd ~/actions-runner
        
        if [ ! -f "./run.sh" ]; then
            echo "📦 Instalando GitHub Actions Runner..."
            curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
            tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
        fi
        
        # Configurar runner
        echo "🔧 Configurando runner..."
        ./config.sh --url https://github.com/$ORG/$REPO \\
          --token $RUNNER_TOKEN \\
          --name contabo-dev-hml \\
          --labels contabo,self-hosted,linux,x64,dev-hml \\
          --work _work \\
          --replace
        
        # Instalar como serviço
        echo "📦 Instalando como serviço..."
        sudo ./svc.sh install
        sudo ./svc.sh start
        
        # Verificar status
        echo "✅ Verificando status..."
        sudo ./svc.sh status
EOF
    
    echo "✅ Runner DEV/HML configurado"
fi

# Configurar runner PROD
if [ -n "$PROD_IP" ]; then
    echo ""
    echo "🔧 Configurando runner PROD em $PROD_IP..."
    
    ssh -o StrictHostKeyChecking=no root@"$PROD_IP" << EOF
        # Instalar Docker
        if ! command -v docker &> /dev/null; then
            echo "📦 Instalando Docker..."
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
        fi
        
        # Instalar GitHub Actions Runner
        mkdir -p ~/actions-runner && cd ~/actions-runner
        
        if [ ! -f "./run.sh" ]; then
            echo "📦 Instalando GitHub Actions Runner..."
            curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
            tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
        fi
        
        # Configurar runner
        echo "🔧 Configurando runner..."
        ./config.sh --url https://github.com/$ORG/$REPO \\
          --token $RUNNER_TOKEN \\
          --name contabo-prod \\
          --labels contabo,self-hosted,linux,x64,prod \\
          --work _work \\
          --replace
        
        # Instalar como serviço
        echo "📦 Instalando como serviço..."
        sudo ./svc.sh install
        sudo ./svc.sh start
        
        # Verificar status
        echo "✅ Verificando status..."
        sudo ./svc.sh status
EOF
    
    echo "✅ Runner PROD configurado"
fi

echo ""
echo "✅ Runners configurados com sucesso!"
echo ""
echo "📝 Verificar runners:"
echo "   gh runner list --repo $ORG/$REPO"

