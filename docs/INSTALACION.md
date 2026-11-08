# Instalación paso a paso

## La forma fácil (recomendada)
1. Descarga [ai-video-ads-kit.zip](https://github.com/OKReach-code/ai-video-ads-kit/releases/latest/download/ai-video-ads-kit.zip) y descomprímelo.
2. En la app de escritorio de Claude, pestaña *Code*, abre la carpeta `ai-video-ads-kit`.
3. Escribe «instálalo». Claude hace contigo todo lo de abajo: instala los programas, te lleva a crear cada cuenta, te abre
   `.env` para la clave y comprueba que todo funciona.

Desde la Terminal: `curl -fsSL https://raw.githubusercontent.com/OKReach-code/ai-video-ads-kit/main/install.sh | bash`

## A mano

Tiempo: unos 20 minutos la primera vez. Probado en macOS; en Windows usa WSL 2 (Ubuntu) y los mismos comandos con `apt` en lugar de `brew`.

## 1. Cuentas que necesitas
| Servicio | Para qué | Plan |
|---|---|---|
| **Claude** (Pro, Max, Team o Enterprise) | Claude Code: el director que lo hace todo | cualquiera con Claude Code |
| **ElevenLabs** | voz, transcripción (Scribe), música y efectos | Creator o superior (uso comercial) |
| **Kling AI** | la persona que habla (Kling 4.0) | con créditos (≈ 15 créditos/s a 1080p) |
| **Higgsfield** (recomendado) | imágenes (Nano Banana Pro), B-roll (Veo), recortes de fondo | con créditos |
| GitHub | descargar el repositorio | gratis |

## 2. Programas
1. **Homebrew** (si no lo tienes): https://brew.sh
2. En la Terminal:
   ```bash
   brew install ffmpeg node python git gh
   ```
3. **Claude Code**: instala la app de escritorio de Claude (pestaña *Code*) desde https://claude.ai/download, o la terminal:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

## 3. Descargar e instalar el kit
```bash
git clone https://github.com/OKReach-code/ai-video-ads-kit.git ~/ai-video-ads-kit
cd ~/ai-video-ads-kit && ./setup.sh
```
`setup.sh` comprueba ffmpeg, Node y Python, crea un entorno de Python propio (`.venv`), crea el archivo `.env` y prepara HyperFrames
(el motor de montaje). Al final te dice qué falta.

## 4. Tu clave de ElevenLabs
1. En ElevenLabs: *Developers › API Keys › Create key* (con permisos de Text to Speech, Speech to Text, Sound Effects y Music).
2. Abre `~/ai-video-ads-kit/.env` y pégala: `ELEVENLABS_API_KEY=sk_...`
3. **Nunca** la pegues en el chat ni la subas a GitHub (`.env` está en `.gitignore`).

## 5. Conectar Kling e Higgsfield a Claude
- **Kling:** viene configurado en `.mcp.json`. Al abrir la carpeta en Claude Code, acepta el servidor MCP del proyecto *kling* e inicia sesión
  con tu cuenta de Kling (en la terminal: `/mcp` › kling › Authenticate; en la app de escritorio, el aviso que aparece).
- **Higgsfield:** en claude.ai › *Configuración › Conectores* añade **Higgsfield** e inicia sesión (o su servidor MCP si tu plan no tiene
  conectores). Sin Higgsfield puedes usar tus propias imágenes y vídeos.

## 6. Abrir el kit en Claude Code
- App de escritorio: pestaña *Code* › abre la carpeta `ai-video-ads-kit`.
- Terminal: `cd ~/ai-video-ads-kit && claude`.

La **skill `anuncios-ia`** y los comandos (`/marca`, `/nuevo-anuncio`, `/producir`, `/revision`) vienen dentro del repositorio
(`.claude/`), así que están disponibles en cuanto abres la carpeta. Si quieres la skill en todos tus proyectos:
```bash
mkdir -p ~/.claude/skills && cp -R ~/ai-video-ads-kit/.claude/skills/anuncios-ia ~/.claude/skills/
```

## 7. Comprobación
Pídele a Claude:
> comprueba la instalación: ffmpeg, la clave de ElevenLabs (lista 3 voces en español), who_am_i de Kling y el saldo de Higgsfield

Si todo sale bien, empieza por tu marca: `/marca`.

## 8. Tu marca
`/marca` rellena `marca/marca.json` contigo: nombre, colores (primario, acento, resaltado), fuentes (pon los `.ttf`/`.otf` en `marca/fuentes/`),
logo en blanco sobre transparente (`marca/logo.png`), la pregunta final del anuncio y la voz. Si quieres un presentador fijo, Claude te enseña
3-4 fotos para elegir. Detalles en [`marca/README.md`](../marca/README.md).

## 9. Primer anuncio
```text
/nuevo-anuncio mi-primer-anuncio
/producir mi-primer-anuncio
```
Sigue el paso a paso de [`METODOLOGIA.md`](METODOLOGIA.md).
