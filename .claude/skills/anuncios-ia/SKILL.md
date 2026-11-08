---
name: anuncios-ia
description: Crea anuncios en vídeo verticales (9:16) para Meta/TikTok/Reels con IA de principio a fin, con la marca del usuario — guion por bloques, voz rápida con ElevenLabs, persona que habla con Kling 4.0 sobre esa voz, imágenes y B-roll con Higgsfield, montaje en HyperFrames, mezcla, QA, paquete editable y revisión. Úsala cuando el usuario quiera crear, producir, montar, revisar o iterar un anuncio en vídeo, un reel publicitario o un clip tipo pódcast para vender un producto.
---

# Anuncios en vídeo con IA

Sigues la metodología de este repositorio. Antes de hacer nada lee `CLAUDE.md`, `docs/METODOLOGIA.md` y `docs/REGLAS.md`; para el montaje,
`docs/ESCENAS.md`; para los prompts de vídeo e imagen, `docs/PROMPTS.md`. La marca del usuario está en `marca/marca.json` (si está sin rellenar,
empieza por `/marca`).

## Flujo (no te saltes ningún control)
1. **Proyecto y brief** — `tools/new_project.sh <nombre>`. Pide en una sola pregunta: producto/oferta, público, formato, duración (35-60 s),
   CTA (pregunta final) y **el guion literal** (si el usuario no lo tiene, propón 2-3 guiones cortos con gancho, problema, solución y pregunta
   final, y espera a que elija o lo edite; no inventes datos ni testimonios).
2. **Plan sin gasto** — divide el guion en bloques (`audio/guion.json`), decide qué bloques dice la persona en cámara (`kling/shots.json`) y qué
   va en escenas (`escenas.json`), y presenta el plan plano a plano con el **coste estimado** (Kling 1080p ≈ 15 créditos/s). Espera el «sí».
   Si el usuario no tiene presentador, genera 3-4 opciones de foto (look y plató) con Higgsfield Nano Banana Pro y que elija una.
3. **Voz** — `tools/voz.py <p>`. Control: ≥ 6,4 sílabas/s, ninguna pausa > 0,6 s, ≤ 9 % de silencio, texto exacto. Si falla, regenera
   (más tomas o quita etiquetas/«…»). **Nunca** aceleres ni estires el audio.
4. **Persona (Kling 4.0)** — `tools/kling_refs.py <p>`; prompts desde la plantilla de `docs/PROMPTS.md` (nunca mira a cámara; gancho serio);
   sube look, cara y `kling/refs/ref_<S>_rt.wav` con `file_upload` del MCP de Kling y lanza `omni_ref_video` (modelo Kling 4.0, 1080p, 9:16,
   `audio_1`, `image_1`, `image_2`). Consulta `query_tasks` en serie (sin martillear la API). Al terminar: `tools/kling_qa.sh <p> S1 <url>…`
   y mira la hoja de fotogramas. r ≥ 0,9 y deriva ≤ 0,1 s → vale; desfase fijo → `kling/offsets.json`; lo demás → regenera ese plano.
   Después `tools/kling_sync.py <p>`.
5. **Montaje** — rellena `escenas.json`, `cd proyectos/<p> && python3 tools/build.py`, render con
   `cd film && npx -y hyperframes@0.8.162 render -f 24 -q high -w 4 -o ../render/video_noaudio_premium.mp4`, saca una hoja de fotogramas
   (ffmpeg, 1 cada 2-3 s) y **mírala**: ninguna cara tapada, cabezas enteras, textos dentro de 270-1250 px, titulares sin pisar tarjetas,
   contadores que acaban antes del corte. Corrige y vuelve a renderizar.
6. **Sonido y mezcla** — `tools/sonido.py <p> music sfx --dur=<s>` (una vez), `python3 tools/make_mix.py`, `python3 ../../tools/mix.py mix_premium.json`.
   Control: −14,5 LUFS, música ≈ 19-20 dB bajo la voz, ningún efecto encima de una palabra; Scribe del máster exacto (`tools/scribe.py`) y `tools/pace.py`.
7. **Entrega** — `python3 tools/export_edit.py proyectos/<p> --overlay --edition premium` (paquete editable), `tools/review.py` + sala de
   revisión (ver METODOLOGIA §7), `LEEME.md` del proyecto rellenado, y un resumen corto con el enlace.
8. **Iterar** — aplica las notas, saca la vN+1, conserva solo la última versión. Cada nota que valga para todos los anuncios va a `docs/REGLAS.md`.

## Reglas que no se negocian (resumen; detalle en docs/REGLAS.md)
- Antes de gastar créditos, di planos, segundos y coste, y espera el «sí».
- Nadie mira a cámara, tampoco al final; en el gancho la persona no sonríe ni se ríe.
- CTA final = la pregunta palabra a palabra + logo de la marca, sin persona, sin botón y sin cartela.
- Nunca tapes una cara; números en cifras; una palabra grande por titular y 1-2 inclinados por anuncio; colores sólidos en las letras.
- Claves solo en `.env`; nunca en el repo ni en el chat. No clones la cara ni la voz de una persona real sin su consentimiento.
