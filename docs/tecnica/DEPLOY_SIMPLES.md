# 🚀 Deploy Simples - ForgeERP

## Deploy Estilo Portainer (Um Comando)

```bash
docker run -d \
  --name forgeerp \
  -p 8000:8000 \
  -v forgeerp_data:/app/data \
  -e DATABASE_URL=sqlite:///app/data/forgeerp.db \
  -e SECRET_KEY=seu-secret-key-aqui \
  ghcr.io/forgeerp/forgeerp:latest
```

## Acessar

- **Frontend/API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Criar Usuário Admin

```bash
docker exec forgeerp python backend/scripts/create_admin_user.py \
  --username admin \
  --password admin \
  --email admin@forgeerp.ai
```

## Usar CLI (Pacote Pip)

O CLI é um pacote pip separado que se integra com o ForgeERP:

```bash
# Instalar CLI
pip install forgeerp-cli

# Ou do repositório
pip install git+https://github.com/forgeerp/forgeerp.git#subdirectory=cli

# Configurar conexão (se necessário)
export FORGEERP_URL=http://localhost:8000

# Usar CLI
forge status
forge logs
```

## Variáveis de Ambiente

```bash
docker run -d \
  --name forgeerp \
  -p 8000:8000 \
  -v forgeerp_data:/app/data \
  -e DATABASE_URL=sqlite:///app/data/forgeerp.db \
  -e SECRET_KEY=seu-secret-key-aqui \
  -e GITHUB_TOKEN=seu-token-github \
  -e GITHUB_OWNER=sua-org \
  -e GITHUB_REPO=seu-repo \
  ghcr.io/forgeerp/forgeerp:latest
```

## Docker Compose (Desenvolvimento)

```bash
# Usar docker-compose.yml
forge up --build

# Ou manualmente
docker compose --profile dev up --build
```

## Atualizar

```bash
# Parar container
docker stop forgeerp

# Remover container (mantém volume)
docker rm forgeerp

# Puxar nova imagem
docker pull ghcr.io/forgeerp/forgeerp:latest

# Subir novamente
docker run -d \
  --name forgeerp \
  -p 8000:8000 \
  -v forgeerp_data:/app/data \
  ghcr.io/forgeerp/forgeerp:latest
```

## Persistência de Dados

Os dados são salvos no volume Docker `forgeerp_data`:

```bash
# Ver volume
docker volume inspect forgeerp_data

# Backup
docker run --rm \
  -v forgeerp_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/forgeerp_backup.tar.gz /data

# Restore
docker run --rm \
  -v forgeerp_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/forgeerp_backup.tar.gz -C /
```

## Troubleshooting

```bash
# Ver logs
docker logs forgeerp

# Entrar no container
docker exec -it forgeerp bash

# Verificar saúde
curl http://localhost:8000/health
```

