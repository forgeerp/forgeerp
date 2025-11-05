# 🔐 GitHub Secrets - Configuração

## 📋 Secrets Necessários

Configure os secrets no GitHub: **Settings → Secrets and variables → Actions → New repository secret**

### 🔑 Secrets Obrigatórios

| Secret Name | Descrição | Exemplo |
|-------------|-----------|---------|
| `GHCR_TOKEN` | Personal Access Token do GitHub (para GHCR) | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `GITHUB_TOKEN` | Token do GitHub (gerado automaticamente, mas pode precisar) | `ghs_xxxxxxxxxxxxxxxxxxxx` |
| `SECRET_KEY` | Chave secreta para JWT | `change-this-secret-key-in-production` |
| `DATABASE_URL` | URL do banco de dados | `sqlite:///./data/forgeerp.db` |

### 🔑 Secrets para Self-Hosted Runners (Contabo)

| Secret Name | Descrição | Exemplo |
|-------------|-----------|---------|
| `SSH_KEY` | Chave SSH privada (base64) | `base64 da chave ~/.ssh/id_ed25519` |
| `SSH_KEY_NAME` | Nome da chave SSH | `forgeerp-key` |
| `RUNNER_DEV_HML_IP` | IP do servidor DEV/HML | `123.45.67.89` |
| `RUNNER_PROD_IP` | IP do servidor PROD | `123.45.67.90` |

### 🔑 Secrets Opcionais (Infraestrutura)

| Secret Name | Descrição | Exemplo |
|-------------|-----------|---------|
| `HETZNER_API_TOKEN` | Token da API Hetzner Cloud | `xxxxxxxxxxxxxxxxxxxx` |
| `GODADDY_API_KEY` | API Key da GoDaddy | `xxxxxxxxxxxxxxxxxxxx` |
| `GODADDY_API_SECRET` | API Secret da GoDaddy | `xxxxxxxxxxxxxxxxxxxx` |
| `B2_ACCOUNT_ID` | Backblaze B2 Account ID | `xxxxxxxxxxxxxxxxxxxx` |
| `B2_APPLICATION_KEY` | Backblaze B2 Application Key | `xxxxxxxxxxxxxxxxxxxx` |
| `POSTGRES_PASSWORD` | Senha PostgreSQL | `xxxxxxxxxxxxxxxxxxxx` |

## 🚀 Configurar Runners Self-Hosted

### 1. Obter Token do Runner

```bash
# Via GitHub CLI
gh runner create-token --repo forgeerp/forgeerp

# Ou via API
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/forgeerp/forgeerp/actions/runners/registration-token
```

### 2. Configurar Runner no Servidor Contabo

```bash
# No servidor Contabo
ssh root@<IP_SERVIDOR>

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar GitHub Actions Runner
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configurar runner
./config.sh --url https://github.com/forgeerp/forgeerp \
  --token <RUNNER_TOKEN> \
  --name contabo-dev-hml \
  --labels contabo,self-hosted,linux,x64,dev-hml \
  --work _work \
  --replace

# Instalar como serviço
sudo ./svc.sh install
sudo ./svc.sh start

# Verificar status
sudo ./svc.sh status
```

### 3. Usar Workflow de Setup Automático

Use o workflow `.github/workflows/setup-runners.yml`:

```bash
# Via GitHub CLI
gh workflow run setup-runners.yml \
  -f server_ip=<IP_SERVIDOR> \
  -f server_type=dev-hml \
  -f runner_name=contabo-dev-hml
```

## 📝 Notas

- **Runners Self-Hosted**: Configure máquinas da Contabo como runners self-hosted
- **Labels**: Use labels `contabo,self-hosted,linux,x64` para identificar runners
- **Segurança**: Nunca commite secrets no código
- **Tokens**: Use PAT (Personal Access Token) com permissões mínimas necessárias

