#!/bin/zsh
# Instala y comprueba lo necesario para AI Video Ads Kit (macOS; en Linux/WSL instala ffmpeg, node y python3 con tu gestor de paquetes).
R=${0:A:h}; ok=1
need(){ command -v $1 >/dev/null && echo "✓ $1" || { echo "✗ falta $1 → $2"; ok=0; } }
need ffmpeg "brew install ffmpeg"
need node   "brew install node"
need python3 "brew install python"
command -v claude >/dev/null && echo "✓ claude (terminal)" || echo "· CLI claude no instalada (vale la app de escritorio de Claude › Code)"
[ -x $R/.venv/bin/python3 ] || python3 -m venv $R/.venv
$R/.venv/bin/python3 -m pip install -q --upgrade pip >/dev/null 2>&1
$R/.venv/bin/python3 -m pip install -q -r $R/requirements.txt && echo "✓ .venv con numpy + opencv-python" || { echo "✗ falló pip install -r requirements.txt"; ok=0; }
[ -f $R/.env ] || { cp $R/.env.example $R/.env; echo "→ creado .env: pon tu ELEVENLABS_API_KEY"; }
grep -q '^ELEVENLABS_API_KEY=.\+' $R/.env && echo "✓ ELEVENLABS_API_KEY" || { echo "✗ falta ELEVENLABS_API_KEY en .env"; ok=0; }
chmod +x $R/tools/*.sh
echo "→ preparando HyperFrames 0.8.162…"; (cd /tmp && HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes@0.8.162 --version >/dev/null 2>&1) && echo "✓ hyperframes" || { echo "✗ HyperFrames no arranca (¿Node ≥ 18?)"; ok=0; }
echo
echo "Siguiente: abre esta carpeta en Claude Code, acepta el servidor MCP 'kling' (.mcp.json) e inicia sesión;"
echo "en claude.ai › Conectores añade Higgsfield. Luego escribe /marca. Guía: docs/INSTALACION.md"
[ $ok = 1 ] && echo "Todo listo." || echo "Hay cosas pendientes (✗)."
