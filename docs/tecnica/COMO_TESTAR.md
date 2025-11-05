# 🧪 Como Testar o ForgeERP MVP

## 🚀 Quick Start

### 1. Subir a Aplicação

```bash
cd /home/gabriel/softhill/forgeerp

# Criar arquivo .env (se não existir)
cp .env.example .env

# Subir com Docker Compose
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### 2. Criar Usuário Admin

```bash
# Criar usuário admin no banco
docker-compose exec backend python scripts/create_admin_user.py

# Ou com parâmetros customizados
docker-compose exec backend python scripts/create_admin_user.py \
  --username admin \
  --password admin \
  --email admin@forgeerp.ai
```

### 3. Acessar a Aplicação

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Login

- **Usuário**: `admin`
- **Senha**: `admin`

## 📋 Testar Funcionalidades

### 1. Tela de Login

1. Acesse http://localhost:3000
2. Faça login com `admin` / `admin`
3. Deve redirecionar para o Dashboard

### 2. Tela de Configurações

1. Após login, clique na aba **"Configurações"**
2. Clique em **"Nova Configuração"**
3. Preencha:
   - **Chave**: `test_config`
   - **Valor**: `test_value`
   - **Tipo**: `string`
   - **Descrição**: `Teste de configuração`
4. Clique em **"Criar"**
5. Verifique se a configuração aparece na lista

### 3. Editar Configuração

1. Na lista de configurações, clique em **"Editar"**
2. Modifique o valor
3. Clique em **"Atualizar"**
4. Verifique se a mudança foi salva

### 4. Deletar Configuração

1. Na lista de configurações, clique em **"Deletar"**
2. Confirme a exclusão
3. Verifique se a configuração foi removida

### 5. Dashboard

1. Na aba **"Dashboard"**, veja:
   - Estatísticas (Clientes, Usuário, Status)
   - Lista de clientes (se houver)

## 🔧 Testar API Diretamente

### Via API Docs (Swagger UI)

1. Acesse http://localhost:8000/docs
2. Clique em **"Authorize"** (ícone de cadeado)
3. Faça login para obter token
4. Teste os endpoints diretamente

### Via cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Obter token (copie do response)
TOKEN="seu_token_aqui"

# Listar configurações
curl -X GET "http://localhost:8000/api/v1/configurations" \
  -H "Authorization: Bearer $TOKEN"

# Criar configuração
curl -X POST "http://localhost:8000/api/v1/configurations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "test_config",
    "value": "test_value",
    "value_type": "string",
    "description": "Teste"
  }'
```

## 🐛 Troubleshooting

### Frontend não conecta com API

1. Verifique se o backend está rodando:
   ```bash
   docker-compose ps
   ```

2. Verifique se a URL da API está correta:
   - Frontend usa `VITE_API_URL` do `.env`
   - Padrão: `http://localhost:8000`

3. Verifique CORS:
   - Backend deve permitir `http://localhost:3000`

### Erro de autenticação

1. Verifique se o usuário admin foi criado:
   ```bash
   docker-compose exec backend python scripts/create_admin_user.py
   ```

2. Verifique se o token está sendo salvo:
   - Abra DevTools → Application → Local Storage
   - Deve ter `token` salvo

### Banco de dados vazio

1. O banco é criado automaticamente na primeira execução
2. Crie o usuário admin:
   ```bash
   docker-compose exec backend python scripts/create_admin_user.py
   ```

## 📊 Logs

```bash
# Ver logs do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend

# Ver todos os logs
docker-compose logs -f
```

## 🔄 Reiniciar

```bash
# Parar tudo
docker-compose down

# Limpar volumes (apaga banco de dados)
docker-compose down -v

# Subir novamente
docker-compose up -d
```

## ✅ Checklist de Teste

- [ ] Backend está rodando (porta 8000)
- [ ] Frontend está rodando (porta 3000)
- [ ] Usuário admin criado
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Tela de configurações funciona
- [ ] Criar configuração funciona
- [ ] Editar configuração funciona
- [ ] Deletar configuração funciona

