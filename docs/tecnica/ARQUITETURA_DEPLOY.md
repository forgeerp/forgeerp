# 🏗️ Arquitetura de Deploy - ForgeERP

## 📊 Análise de Padrões do Mercado

### Portainer (Referência: Simplicidade)
- **Deploy**: `docker run -d -p 9000:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce`
- **Arquitetura**: **Imagem única** que contém tudo
- **Vantagens**: 
  - Deploy extremamente simples
  - Um único comando para começar
  - Sem necessidade de docker-compose
  - Fácil de entender e manter

### Odoo (Referência: ERP Modular)
- **Deploy**: Imagem única `odoo/odoo` que serve:
  - Backend Python (servidor Odoo)
  - Frontend estático (servido pelo próprio servidor)
  - CLI integrado (comandos `odoo-bin`
- **Arquitetura**: **Imagem única** com multi-stage build
- **Vantagens**:
  - Tudo em um lugar
  - Frontend buildado servido como estático
  - CLI embutido na imagem

### Rancher (Referência: Complexidade)
- **Deploy**: Kubernetes ou Docker Compose com múltiplos serviços
- **Arquitetura**: **Múltiplos containers** (server, agentes, etc)
- **Uso**: Para sistemas complexos que precisam de escalabilidade

### Doodba (Referência: Odoo + Docker)
- **Deploy**: `docker compose up` com imagem única do Odoo
- **Arquitetura**: Imagem única do Odoo + serviços auxiliares (Postgres, etc)
- **Padrão**: Odoo serve tudo (frontend + backend)

## 🎯 Proposta para ForgeERP

### Arquitetura Recomendada: **Imagem Única** (estilo Portainer/Odoo)

#### Estrutura da Imagem

```
forgeerp:latest
├── Backend FastAPI (Python)
│   └── Serve API em /api/*
│   └── Serve frontend estático em /*
├── Frontend React (build estático)
│   └── Buildado via multi-stage
│   └── Copiado para /app/static/
└── CLI (Typer)
    └── Comando `forge` disponível
    └── Pode ser usado dentro do container
```

#### Dockerfile Multi-Stage

```dockerfile
# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install CLI
COPY cli/pyproject.toml ./cli/
RUN pip install --no-cache-dir -e ./cli

# Copy backend
COPY backend/ ./backend/

# Copy frontend build from stage 1
COPY --from=frontend-builder /app/frontend/dist ./static/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI (servindo frontend estático + API)
CMD ["uvicorn", "forgeerp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deploy Simples

```bash
# Opção 1: Docker run direto (estilo Portainer)
docker run -d \
  --name forgeerp \
  -p 8000:8000 \
  -v forgeerp_data:/app/data \
  -e DATABASE_URL=sqlite:///app/data/forgeerp.db \
  ghcr.io/forgeerp/forgeerp:latest

# Opção 2: Docker Compose (para desenvolvimento)
docker compose up -d
```

#### Vantagens

1. **Simplicidade**: Um único comando para deploy
2. **Portabilidade**: Funciona em qualquer lugar (Docker, K8s, etc)
3. **Manutenção**: Mais fácil de manter uma imagem única
4. **Performance**: Sem overhead de rede entre containers
5. **Alinhado com padrões**: Segue Portainer/Odoo/Doodba

#### Desvantagens (e como mitigar)

1. **Tamanho da imagem**: 
   - Mitigação: Multi-stage build remove dependências de build
   - Resultado: ~200-300MB (similar ao Portainer)

2. **Escalabilidade do frontend**:
   - Mitigação: Frontend é estático, pode usar CDN se necessário
   - FastAPI serve estáticos eficientemente

3. **Escalabilidade do backend**:
   - Mitigação: Pode fazer deploy múltiplo da mesma imagem
   - Load balancer na frente se necessário

## 🔄 Comparação: Imagem Única vs Múltiplos Containers

| Aspecto | Imagem Única | Múltiplos Containers |
|---------|--------------|---------------------|
| Simplicidade | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Deploy | `docker run` | `docker compose up` |
| Manutenção | Mais fácil | Mais complexo |
| Escalabilidade | Horizontal igual | Vertical melhor |
| Overhead | Menor | Maior (rede) |
| Padrão | Portainer/Odoo | Rancher/K8s |

## 📝 Próximos Passos

1. ✅ Criar Dockerfile multi-stage
2. ✅ Atualizar FastAPI para servir frontend estático
3. ✅ Integrar CLI na imagem
4. ✅ Atualizar docker-compose para desenvolvimento
5. ✅ Atualizar workflow de build para imagem única
6. ✅ Documentar deploy simples

## 🔗 Referências

- Portainer: https://docs.portainer.io/
- Odoo Docker: https://hub.docker.com/_/odoo
- Doodba: https://github.com/Tecnativa/doodba

