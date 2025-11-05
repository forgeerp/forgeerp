# 📖 Documentação Visual - ForgeERP

## 🎯 Sobre

A documentação visual do ForgeERP é gerada automaticamente e mantida atualizada pela equipe de desenvolvimento.

## 📋 Geração Automática

A documentação visual é gerada automaticamente via GitHub Actions quando há mudanças no código.

O workflow `.github/workflows/generate-docs.yml` executa automaticamente:
- Quando há push para `main`
- Quando há mudanças no frontend ou backend
- Manualmente via `workflow_dispatch`

**Nota**: Esta documentação é mantida automaticamente pela equipe de desenvolvimento. Os usuários não precisam gerar documentação - ela está sempre atualizada no repositório.

## 📸 Documentação Gerada

A documentação visual inclui:
- `docs/GUIA_VISUAL.md` - Markdown com screenshots
- `docs/GUIA_VISUAL.html` - HTML visual
- `docs/operacional/STEP_BY_STEP_GUIDE.md` - Detailed step-by-step guide
- `docs/screenshots/*.png` - Screenshots individuais

## 🔧 Scripts de Geração (Uso Interno)

Os scripts de geração estão disponíveis em `backend/scripts/`:
- `generate_docs.py` - Geração de documentação visual simples
- `generate_docs_step_by_step.py` - Geração de guia passo a passo

**Nota**: Estes scripts são para uso interno da equipe de desenvolvimento.

## 📚 Documentação

A documentação visual gerada é commitada automaticamente no repositório e está sempre atualizada.

## 🔗 Referências

- [README.md](../README.md) - Documentação principal
- [docs/README.md](README.md) - Índice da documentação
- [scripts/README.md](../scripts/README.md) - Documentação dos scripts
