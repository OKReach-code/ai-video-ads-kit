#!/bin/bash
# Instalación en un comando:
#   curl -fsSL https://raw.githubusercontent.com/OKReach-code/ai-video-ads-kit/main/install.sh | bash
# Descarga el kit en ~/ai-video-ads-kit, instala Claude Code si falta y abre Claude con /instalar,
# que te guía paso a paso (programas, cuentas, claves y comprobación final).
set -e
REPO="https://github.com/OKReach-code/ai-video-ads-kit"
DEST="${AI_ADS_KIT_DIR:-$HOME/ai-video-ads-kit}"

echo "▶ AI Video Ads Kit"

# 1. El kit
if [ -d "$DEST/.git" ]; then
  echo "· Ya está en $DEST; actualizando…"
  git -C "$DEST" pull --ff-only -q || echo "  (no se pudo actualizar; sigo con la versión que tienes)"
elif [ -d "$DEST" ]; then
  echo "· Ya existe $DEST; lo uso tal cual."
elif command -v git >/dev/null 2>&1 && git --version >/dev/null 2>&1; then
  git clone -q "$REPO.git" "$DEST"
else
  mkdir -p "$DEST"
  curl -fsSL "$REPO/archive/refs/heads/main.tar.gz" | tar xz -C "$DEST" --strip-components 1
fi
echo "✓ Kit en $DEST"

# 2. Claude Code
if ! command -v claude >/dev/null 2>&1; then
  echo "· Instalando Claude Code…"
  curl -fsSL https://claude.ai/install.sh | bash
  export PATH="$HOME/.local/bin:$PATH"
fi
command -v claude >/dev/null 2>&1 || { echo "✗ No encuentro 'claude'. Abre una Terminal nueva y vuelve a lanzar el comando."; exit 1; }
echo "✓ Claude Code"

# 3. Claude toma el relevo
echo "▶ Abriendo Claude. Te guiará en el resto (inicia sesión con tu cuenta de Claude si te lo pide)."
cd "$DEST"
exec claude "/instalar" < /dev/tty
