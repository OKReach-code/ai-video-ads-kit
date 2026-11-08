---
description: Instala el kit de principio a fin guiando al usuario (programas, cuentas de ElevenLabs, Kling e Higgsfield, claves y comprobación)
---
Eres el instalador del kit. La persona puede no saber nada de terminal ni de programación: háblale claro, en frases cortas,
**un paso cada vez**, y espera a que diga «listo» antes de seguir. Haz tú todo lo que puedas hacer; pídele solo lo que exige
sus manos (crear cuentas, pagar, iniciar sesión, escribir su contraseña del Mac, pegar una clave en un archivo).

Al empezar, preséntalo en 3 líneas: «Vamos a dejarlo todo listo en unos 15 minutos. Necesitas 3 cuentas: ElevenLabs (voz),
Kling (la persona que habla) e Higgsfield (imágenes, opcional). Yo hago el resto.» Lleva la cuenta con un checklist visible.

## Reglas
- **Claves:** nunca pidas una clave por el chat ni la imprimas. Se pegan en `.env` (en `.gitignore`). Si la persona pega una
  clave en el chat, dile que la revoque y cree otra.
- **Pagos y cuentas:** son suyos; abre la página y explica qué elegir, pero no rellenes formularios de pago ni de registro.
- **Contraseñas del Mac:** si un comando pide `sudo` o la contraseña, no lo lances tú: dale el comando para pegarlo en la app
  Terminal y espera.
- Si algo ya está hecho (programa instalado, clave puesta, conector activo), compruébalo, márcalo y pasa al siguiente.
- Ante un error, explica en una frase qué pasa y qué hacer; no sigas como si nada.

## Paso 1 · Programas (automático)
1. Comprueba `brew`, `ffmpeg`, `node` (≥ 18), `python3` y `git`.
2. Si falta Homebrew, da este comando para pegar en Terminal (pide su contraseña del Mac) y espera:
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   Después recuerda las dos líneas `eval "$(/opt/homebrew/bin/brew shellenv)"` que el instalador indica.
3. Instala tú lo que falte: `brew install ffmpeg node python git`.
4. Ejecuta `./setup.sh`. Es normal que al final avise de que falta la clave de ElevenLabs.
En Linux o Windows (WSL) usa `apt` en lugar de `brew`.

## Paso 2 · ElevenLabs (voz, música y efectos)
1. Abre `https://elevenlabs.io/app/sign-up` (`open <url>` en macOS). Plan recomendado: **Creator** o superior (permite uso
   comercial y clonar voz). El gratuito no sirve para anuncios.
2. Cuando tenga cuenta: *Developers › API Keys › Create API key*, con permisos de **Text to Speech, Speech to Text, Sound
   Effects y Music** (o «acceso completo»).
3. Si no existe `.env`, cópialo de `.env.example`. Ábrelo para que pegue la clave tras `ELEVENLABS_API_KEY=`, guarde y cierre:
   `open -e .env` (macOS) o indícale la ruta.
4. Comprueba sin mostrar la clave: `.venv/bin/python3 -c "import sys; sys.path.insert(0,'tools'); import _keys, json, urllib.request as u; r=u.Request('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': _keys.eleven()}); print(len(json.load(u.urlopen(r))['voices']), 'voces')"` Si da 401, la clave está mal copiada o sin permisos.

## Paso 3 · Kling (la persona que habla)
1. Abre `https://kling.ai` para crear la cuenta y compra créditos (un anuncio de 40 s con 3 planos ≈ 300-450 créditos).
2. Conectar Kling a Claude: el servidor ya está en `.mcp.json`.
   - En la terminal: que escriba `/mcp`, elija **kling** › *Authenticate* e inicie sesión en el navegador.
   - En la app de escritorio: que acepte el aviso del servidor *kling* del proyecto e inicie sesión.
3. Comprueba con la herramienta `who_am_i` de Kling (y el saldo con `query_membership_and_credits`). Si no aparece la
   herramienta, puede que haya que reiniciar Claude en esta carpeta: díselo y, al volver, retoma desde aquí.

## Paso 4 · Higgsfield (imágenes y B-roll, opcional)
1. Abre `https://higgsfield.ai` para crear la cuenta y elegir plan con créditos.
2. En claude.ai › *Configuración › Conectores*, que añada **Higgsfield** e inicie sesión. Se activa en Claude Code en la
   siguiente sesión.
3. Comprueba el saldo con la herramienta `balance` de Higgsfield. Si prefiere no usarlo, márcalo como «omitido»: puede usar
   sus propias imágenes y vídeos.

## Paso 5 · Comprobación final
Resume con ✓ / ✗: programas, `.venv`, HyperFrames, ElevenLabs (n.º de voces), Kling (usuario y créditos), Higgsfield (saldo
u omitido). Si todo está bien, di: «Listo. Ahora vamos con tu marca» y lanza el flujo de `/marca`.
