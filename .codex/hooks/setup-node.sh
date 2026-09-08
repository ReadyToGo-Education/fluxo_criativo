#!/bin/bash
# setup-node.sh — SessionStart hook: verifica Node.js e instala se ausente.
# Deve ser o primeiro hook de SessionStart para garantir que os demais (que usam node) funcionem.

if command -v node &>/dev/null; then
  exit 0  # Node ja instalado, sai sem ruido
fi

echo ""
echo "## Node.js nao encontrado"
echo ""
echo "Os hooks deste projeto precisam do Node.js. Tentando instalar agora..."
echo ""

OS="$(uname -s 2>/dev/null)"
INSTALLED=false

case "$OS" in
  Darwin)
    if command -v brew &>/dev/null; then
      echo "-> macOS detectado. Instalando via Homebrew..."
      brew install node --quiet && INSTALLED=true
    else
      echo "-> Homebrew nao encontrado. Instalando Homebrew + Node.js..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
        && brew install node --quiet && INSTALLED=true
    fi
    ;;
  Linux)
    if command -v apt-get &>/dev/null; then
      echo "-> Linux (Debian/Ubuntu) detectado. Instalando via NodeSource LTS..."
      curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - \
        && sudo apt-get install -y nodejs && INSTALLED=true
    else
      echo "-> Linux detectado (distro nao-Debian). Instalando via nvm..."
      curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
        && export NVM_DIR="$HOME/.nvm" \
        && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" \
        && nvm install --lts && INSTALLED=true
    fi
    ;;
  *)
    # Windows (Git Bash)
    echo "-> Windows detectado. Instalando via winget..."
    powershell.exe -Command \
      "winget install --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements --silent" \
      && INSTALLED=true
    ;;
esac

echo ""
if $INSTALLED; then
  echo "Node.js instalado com sucesso."
  echo "IMPORTANTE: reinicie o VS Code para que o PATH seja atualizado e os hooks funcionem."
else
  echo "Nao foi possivel instalar automaticamente."
  echo "Instale o Node.js manualmente em: https://nodejs.org"
  echo "Depois reinicie o VS Code."
fi
echo ""

exit 0
