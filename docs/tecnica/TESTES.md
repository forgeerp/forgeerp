# 🧪 Guia Rápido de Testes - ForgeERP

## Executar Testes

\`\`\`bash
cd backend

# Todos os testes
pytest

# Com cobertura
pytest --cov=forgeerp --cov-report=html

# Usando Makefile
make test
make test-coverage
\`\`\`

## Estrutura

- \`tests/\` - Testes principais
- \`tests/unit/\` - Testes unitários
- \`tests/integration/\` - Testes de integração

## Documentação Completa

Veja [ARQUITETURA_TESTES.md](./ARQUITETURA_TESTES.md) para detalhes completos.
