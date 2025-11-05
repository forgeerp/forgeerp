# Testes de GitHub Actions

## 📋 Visão Geral

Estes testes validam a geração e execução de GitHub Actions workflows usando `act` (Action runner for testing).

## 🚀 Pré-requisitos

### Instalar act

```bash
# macOS
brew install act

# Linux (via script)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (via Chocolatey)
choco install act-cli
```

### Verificar instalação

```bash
act --version
```

## 🧪 Executar Testes

### Todos os testes de GitHub Actions

```bash
pytest tests/github_actions/
```

### Testes com act (requer act instalado)

```bash
pytest tests/github_actions/ -m act
```

### Testes sem act (apenas validação YAML)

```bash
pytest tests/github_actions/ -m "not act"
```

## 📝 Tipos de Testes

### 1. Testes de Geração de Workflows
- ✅ Validação de sintaxe YAML
- ✅ Estrutura de workflows
- ✅ Geração de workflows específicos (setup-client, deploy-client)

### 2. Testes de Execução com act
- ✅ Execução de workflows
- ✅ Validação de steps
- ✅ Uso de secrets e variáveis de ambiente

### 3. Testes de Actions Reutilizáveis
- ✅ Geração de actions
- ✅ Validação de action.yml
- ✅ Actions com Docker

## 🔧 Fixtures Disponíveis

### `github_repo_dir`
Diretório temporário de repositório Git para testes.

### `github_workflows_dir`
Diretório `.github/workflows` do repositório de teste.

### `github_actions_dir`
Diretório `.github/actions` do repositório de teste.

### `act_available`
Verifica se `act` está disponível no sistema.

### `act_runner`
Helper para executar workflows com `act`.

## 📊 Cobertura

- ✅ Geração de workflows
- ✅ Validação de sintaxe YAML
- ✅ Execução de workflows com act
- ✅ Geração de actions reutilizáveis

## ⚠️ Notas

- Testes com `act` são marcados como `@pytest.mark.act`
- Testes sem `act` ainda validam sintaxe YAML
- Workflows podem não executar completamente sem configuração adequada

## 🔄 Próximos Testes

- ⏳ Testes de workflows específicos (disaster-recovery, diagnose-services)
- ⏳ Testes de integração com módulos
- ⏳ Testes de modificação de workflows (xpath-like)

