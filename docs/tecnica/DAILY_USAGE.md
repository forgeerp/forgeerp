# 📖 Uso no Dia a Dia - ForgeERP

Guia prático para uso diário do ForgeERP usando o CLI.

## 🚀 Comandos Básicos

### Subir/Parar Aplicação

```bash
# Subir (puxa imagens pré-compiladas se existirem)
forge up

# Subir com rebuild
forge up --build

# Parar
forge down
```

### Ver Status e Logs

```bash
# Status dos serviços
forge status

# Ver logs
forge logs

# Ver logs de um serviço específico
forge logs backend
forge logs frontend

# Seguir logs em tempo real
forge logs --follow

# Últimas 50 linhas
forge logs --tail 50
```

### Reiniciar Serviços

```bash
# Reiniciar tudo
forge restart

# Reiniciar apenas backend
forge restart backend

# Reiniciar apenas frontend
forge restart frontend
```

## 👤 Gerenciar Usuários

### Criar Usuário Admin Padrão

```bash
forge user
```

### Criar Usuário Customizado

```bash
forge user --username seu_usuario --password sua_senha --email seu_email@exemplo.com
```

## 🧪 Executar Testes

### Todos os Testes

```bash
forge test
```

### Testes Específicos

```bash
# Testes unitários
forge test --unit

# Testes de integração
forge test --integration

# Testes E2E
forge test --e2e

# Com cobertura
forge test --coverage

# Todos os testes
forge test --all
```

## 🔄 Atualizar Aplicação

### Atualizar Código e Rebuild

```bash
forge update
```

Isso irá:
1. Fazer `git pull` do código
2. Reconstruir as imagens Docker
3. Reiniciar os serviços

## 🛠️ Manutenção

### Limpar Cache

```bash
forge clean
```

Remove containers parados e limpa o cache do Docker.

### Resetar Banco de Dados

⚠️ **CUIDADO**: Isso apaga todos os dados!

```bash
forge reset
```

Isso irá:
1. Parar os serviços
2. Remover o banco de dados
3. Reiniciar os serviços

**Depois execute**: `forge user` para criar um novo usuário admin.

## 📊 Verificar Status da API

```bash
forge status
```

Mostra:
- Status dos containers Docker
- Status da API (online/offline)

## 🔧 Configuração GitHub (Avançado)

### Configurar Secrets

```bash
./scripts/setup_github_secrets.sh
```

### Configurar Runners

```bash
./scripts/setup_runners.sh
```

### Verificar Runners

```bash
gh runner list --repo forgeerp/forgeerp
```

## 📚 Ajuda

### Ver Todos os Comandos

```bash
forge --help
```

### Ajuda de um Comando Específico

```bash
forge up --help
forge test --help
forge user --help
```

## 🎯 Comandos Mais Usados

| Comando | Descrição |
|---------|-----------|
| `forge up` | Subir aplicação |
| `forge down` | Parar aplicação |
| `forge status` | Ver status |
| `forge logs --follow` | Ver logs em tempo real |
| `forge test` | Executar testes |
| `forge update` | Atualizar aplicação |
| `forge user` | Criar usuário admin |

## 📝 Notas

- O CLI sempre executa `docker compose` automaticamente
- Não precisa executar `docker compose` manualmente após a instalação
- Todos os comandos são executados na raiz do projeto
- O CLI verifica se o Docker está instalado antes de executar

## 🔗 Mais Informações

- [README.md](../README.md) - Documentação principal
- [Instalação](INSTALACAO.md) - Instruções detalhadas
- [Testes](TESTES.md) - Guia de testes
