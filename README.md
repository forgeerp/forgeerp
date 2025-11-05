# ForgeERP

Sistema de infraestrutura para gestão de deploy e provisionamento de infraestrutura de forma simples e automatizada.

## 🎯 O que fazemos

**Automação completa de deploy e infraestrutura.**

Do clone ao ambiente pronto com um comando. Pipelines e infraestrutura são configurados automaticamente. Com GitHub Actions configurados automaticamente, infraestrutura como código, e automação total, você foca no que importa: seu produto.

### ✨ Principais Funcionalidades

- **🚀 Deploy em minutos** - Setup de semanas para minutos, sem trabalho manual
- **⚙️ Automação total** - GitHub Actions configurados automaticamente para cada cliente
- **🔒 Infraestrutura como código** - Tudo versionado, auditável e reproduzível
- **📊 Estimativas precisas** - Ferramentas que ajudam na decisão técnica
- **🔄 Backup automático** - Disaster recovery integrado
- **🔐 SSL automático** - Certificados renovados automaticamente
- **📈 Monitoramento** - Health checks e alertas configurados
- **🎯 Multi-provedor** - Hetzner, AWS, GCP, Azure e mais

## 🧠 Princípios de Engenharia

- **Simplicidade primeiro** — Arquitetura mínima para entregar valor com clareza
- **Automação por padrão** — Tudo o que pode ser automatizado, será
- **Observabilidade nativa** — Saúde e métricas disponíveis desde o dia 1
- **Configuração declarativa** — Reprodutível, auditável, versionada
- **Seguro por padrão** — SSL automático, segredos, permissões
- **Modularidade** — Habilite apenas o que precisa, quando precisa

## 🌟 Por que usar o ForgeERP?

### 🚀 Automação Completa

- **Deploy automatizado** — GitHub Actions prontos para uso
- **Infraestrutura como código** — Reprodutível e auditável
- **Backup automático** — Sem intervenção manual
- **SSL automático** — Renovação contínua
- **Monitoramento automático** — Health checks e alertas

### 💎 Qualidade Profissional

- **Enterprise-grade** — Boas práticas desde o primeiro commit
- **Multi-provedor** — Hetzner, AWS, GCP, Azure e mais
- **Escalável** — 1 a 100+ clientes
- **Seguro** — Boas práticas aplicadas automaticamente
- **Documentado** — Documentação sempre atualizada

### 🔒 Código Aberto

- **Fork público** — Transparência e colaboração
- **PRs automáticos** — Melhorias retornam ao ecossistema
- **Sem lock-in** — Você no controle
- **Self-hosting opcional** — Flexibilidade total

### 📊 Gestão Inteligente

- **Ferramentas de decisão** — Estimativas que guiam escolhas técnicas
- **Dashboard centralizado** — Gestão em um lugar
- **Relatórios automáticos** — Uso e performance
- **Alertas inteligentes** — Notificações proativas
- **Histórico completo** — Auditoria de mudanças

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
# Ubuntu/Debian
chmod +x scripts/install-ubuntu.sh && ./scripts/install-ubuntu.sh

# Fedora/RHEL
chmod +x scripts/install-fedora.sh && ./scripts/install-fedora.sh

# macOS
chmod +x scripts/install-macos.sh && ./scripts/install-macos.sh
```

**Ou instale manualmente**: Docker, Git, GitHub CLI, Python 3.11+, Node.js 18+.  
Veja [docs/INSTALACAO.md](docs/INSTALACAO.md) para instruções detalhadas.

### 2. Clonar e Configurar

```bash
git clone https://github.com/forgeerp/forgeerp.git
cd forgeerp
cp .env.example .env
# Edite o .env com suas configurações
```

### 3. Instalar CLI

```bash
cd cli
pip install -e .
```

### 4. Subir a Aplicação

```bash
forge up
```

### 5. Criar Usuário Admin

```bash
forge user
```

### 6. Acessar

Abra http://localhost:3000 e faça login com:
- **Username**: `admin`
- **Password**: `admin`

⚠️ **Altere a senha padrão após o primeiro login!**

## 💻 Uso do CLI

O ForgeERP CLI é a ferramenta principal para uso diário:

```bash
# Ver todos os comandos
forge --help

# Subir/parar aplicação
forge up
forge down

# Ver status
forge status

# Ver logs
forge logs
forge logs --follow

# Gerenciar usuários
forge user --username admin --password senha123

# Executar testes
forge test
forge test --unit
forge test --coverage

# Atualizar aplicação
forge update
```

Veja [docs/DAILY_USAGE.md](docs/DAILY_USAGE.md) para mais comandos.

## 📊 Comparação com Alternativas

| Característica | **ForgeERP** | **odoo.sh** | **DIY Manual** |
|---|---|---|---|
| **Automação** | ✅ Total | ✅ Alta | ❌ Manual |
| **Código Aberto** | ✅ Obrigatório | ❌ Proprietário | ✅ Sim |
| **Self-Hosting** | ✅ Opcional | ❌ Não | ✅ Sim |
| **Ferramentas de Decisão** | ✅ Precisas | ⚠️ Limitadas | ❌ Não |
| **Multi-provedor** | ✅ Sim | ❌ Não | ⚠️ Manual |

## 🎯 Pronto para engenharia

Sem política. Sem distração. Tecnologia clara, moderna e objetiva para quem quer construir bem e rápido.

## 📖 Documentação

- **Uso diário**: [docs/DAILY_USAGE.md](docs/DAILY_USAGE.md)
- **Documentação completa**: [docs/README.md](docs/README.md)
- **Instalação detalhada**: [docs/INSTALACAO.md](docs/INSTALACAO.md)
- **Scripts**: [scripts/README.md](scripts/README.md)

## 📞 Suporte

- **Issues**: https://github.com/forgeerp/forgeerp/issues
- **Documentação**: [docs/README.md](docs/README.md)

## 📄 Licença

MIT
