# ForgeERP

Infrastructure management system for simple and automated deployment and infrastructure provisioning.

## 🎯 What We Do

**Complete deployment and infrastructure automation.**

From clone to production-ready environment with a single command. Pipelines and infrastructure are configured automatically. With GitHub Actions configured automatically, infrastructure as code, and total automation, you focus on what matters: your product.

### ✨ Key Features

- **🚀 Deploy in minutes** - Setup from weeks to minutes, without manual work
- **⚙️ Total automation** - GitHub Actions configured automatically for each client
- **🔒 Infrastructure as code** - Everything versioned, auditable, and reproducible
- **📊 Accurate estimates** - Tools that help with technical decisions
- **🔄 Automatic backup** - Integrated disaster recovery
- **🔐 Automatic SSL** - Certificates renewed automatically
- **📈 Monitoring** - Health checks and alerts configured
- **🎯 Multi-provider** - Hetzner, AWS, GCP, Azure and more

## 🧠 Engineering Principles

- **Simplicity first** — Minimal architecture to deliver value with clarity
- **Automation by default** — Everything that can be automated, will be
- **Native observability** — Health and metrics available from day 1
- **Declarative configuration** — Reproducible, auditable, versioned
- **Secure by default** — Automatic SSL, secrets, permissions
- **Modularity** — Enable only what you need, when you need it

## 🌟 Why Use ForgeERP?

### 🚀 Complete Automation

- **Automated deployment** — GitHub Actions ready to use
- **Infrastructure as code** — Reproducible and auditable
- **Automatic backup** — No manual intervention
- **Automatic SSL** — Continuous renewal
- **Automatic monitoring** — Health checks and alerts

### 💎 Professional Quality

- **Enterprise-grade** — Best practices from the first commit
- **Multi-provider** — Hetzner, AWS, GCP, Azure and more
- **Scalable** — 1 to 100+ clients
- **Secure** — Best practices applied automatically
- **Documented** — Documentation always up to date

### 🔒 Open Source

- **MIT License** — Use, modify, distribute freely
- **Community-driven** — Contributions welcome
- **Transparent** — All code is open and auditable

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- GitHub CLI (optional, for GitHub integration)

See [Installation Guide](docs/technical/INSTALLATION.md) for detailed instructions.

### Installation

```bash
# Clone the repository
git clone https://github.com/forgeerp/forgeerp.git
cd forgeerp

# Start the application
forge up
```

### First Access

1. Access `http://localhost:8000`
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin`
3. Create your first client
4. Install modules
5. Generate workflows

See [Documentation](docs/README.md) for more details.

## 📚 Documentation

- **[Technical Documentation](docs/technical/README.md)** - Technical guides, CLI, and API
- **[Functional Documentation](docs/functional/README.md)** - Daily GUI usage
- **[Operational Documentation](docs/operational/README.md)** - Auto-generated guides

## 🛠️ Tech Stack

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLModel + SQLite
- **CLI**: Typer + Rich
- **Testing**: Pytest + Playwright
- **Containerization**: Docker (unified image)

## 🧪 Testing

```bash
# Run all tests
forge test

# Run specific tests
forge test --unit
forge test --integration
forge test --e2e
```

## 📝 Development

```bash
# Start development environment
forge up --build

# Run tests
forge test

# View logs
forge logs --follow
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation**: [docs/README.md](docs/README.md)
- **Installation**: [docs/technical/INSTALLATION.md](docs/technical/INSTALLATION.md)
- **Daily Usage**: [docs/technical/DAILY_USAGE.md](docs/technical/DAILY_USAGE.md)

---

**ForgeERP** - Infrastructure management made simple. 🚀
