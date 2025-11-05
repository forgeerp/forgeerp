#!/bin/bash
# Script to install recommended Cursor/VS Code extensions

echo "🔌 Installing recommended Cursor extensions..."

# Check if cursor command exists
if ! command -v cursor &> /dev/null; then
    echo "⚠️  Cursor command not found. Installing via VS Code..."
    CMD="code"
else
    CMD="cursor"
fi

# Extensions to install
EXTENSIONS=(
    "dbaeumer.vscode-eslint"
    "esbenp.prettier-vscode"
    "bradlc.vscode-tailwindcss"
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-vscode.vscode-typescript-next"
)

for ext in "${EXTENSIONS[@]}"; do
    echo "Installing $ext..."
    $CMD --install-extension $ext || echo "⚠️  Failed to install $ext"
done

echo "✅ Done! Reload Cursor window (Ctrl+Shift+P → 'Developer: Reload Window')"
