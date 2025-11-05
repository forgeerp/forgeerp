# Frontend - ForgeERP

## 📦 Estrutura

```
frontend/
├── src/
│   ├── components/       # Componentes React
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   └── Configurations.tsx
│   ├── lib/             # Utilitários
│   │   ├── api.ts        # Cliente API
│   │   └── auth.ts      # Autenticação
│   ├── App.tsx          # Componente principal
│   ├── main.tsx         # Entry point
│   └── index.css        # Estilos globais
├── package.json
├── vite.config.ts
└── Dockerfile
```

## 🚀 Como Rodar

### Desenvolvimento

```bash
cd frontend
npm install
npm run dev
```

Acesse: http://localhost:3000

### Produção

```bash
cd frontend
npm run build
npm run preview
```

## 📋 Funcionalidades

### ✅ Implementado
- ✅ Tela de Login
- ✅ Dashboard básico
- ✅ Tela de Configurações (CRUD completo)
- ✅ Integração com API
- ✅ Autenticação JWT
- ✅ Gerenciamento de estado básico

### ⏳ Próximas
- ⏳ Tela de Clientes
- ⏳ Tela de Módulos
- ⏳ Tela de Ambientes
- ⏳ Geração de Workflows
- ⏳ Gerenciamento de PRs

## 🎨 Stack

- **React 19** - Framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Estilização
- **Fetch API** - HTTP client

## 🔧 Configuração

Variáveis de ambiente (`.env`):
- `VITE_API_URL` - URL da API (padrão: http://localhost:8000)
