# 🧰 Documentação Operacional (Automática)

Documentação gerada automaticamente (Playwright) e mantida no repositório.

## Como Funciona

- Workflow: `.github/workflows/generate-docs.yml`
- Scripts: `backend/scripts/generate_docs.py` e `backend/scripts/generate_docs_step_by_step.py`
- Saída: arquivos em `docs/` (GUIA_VISUAL.md, GUIA_PASSO_A_PASSO.md) e `docs/screenshots/`

## Arquivos

- [Documentação Visual](DOCUMENTACAO_VISUAL.md)
- [Resumo da Documentação](RESUMO_DOCUMENTACAO.md)
- [GUIA_VISUAL.md](GUIA_VISUAL.md) (gerado automaticamente)
- [GUIA_PASSO_A_PASSO.md](GUIA_PASSO_A_PASSO.md) (gerado automaticamente)
- [screenshots/](screenshots/) (screenshots gerados)

## Notas

- A geração é automática em pushes para `main` (conforme workflow) e pode ser disparada manualmente.
- Usuários não precisam gerar documentação; mantemos atualizada via CI.

