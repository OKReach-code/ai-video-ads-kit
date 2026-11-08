# AI Video Ads Kit · instrucciones para Claude Code

Este repositorio produce anuncios en vídeo verticales (1080×1920) con IA para la marca del usuario. Para cualquier petición de anuncio usa la
skill `anuncios-ia` y sigue `docs/METODOLOGIA.md`. Antes de entregar, repasa `docs/REGLAS.md` punto por punto.

## Antes de empezar
- **Instalación:** si falta `.venv`, `.env` o la clave de ElevenLabs, o no responden las herramientas de Kling, propón `/instalar`.
- **Marca:** `marca/marca.json`. Si tiene valores de ejemplo («Mi Marca», sin `elevenlabs_voice_id`), propón `/marca` antes de nada.
- **Python:** usa siempre `.venv/bin/python3` (si no existe, `./setup.sh`). **Montaje:** HyperFrames 0.8.162, render a 24 fps; nunca edites
  `film/index.html` a mano: se regenera con `tools/build.py` desde `src/template.html` + `escenas.json`.
- **Conectores:** Kling por `.mcp.json` (empieza por `who_am_i`); Higgsfield como conector de claude.ai (imágenes, Veo, recortes).

## Reglas que no se negocian
- **Gasto:** cada job de Kling o Higgsfield cuesta créditos. Antes de lanzar, di planos, segundos y créditos estimados y espera el «sí».
  Consulta los trabajos en serie (`query_tasks`), sin martillear la API. Apunta saldos y costes en el `LEEME.md` del proyecto.
- **Guion:** el guion es del usuario; no cambies sus palabras sin permiso. Si no tiene, propón opciones y que elija.
- **Voz rápida al generar** (≥ 6,4 síl/s, sin pausas > 0,6 s, ≤ 9 % de silencio) con `tools/voz.py`; nunca acelerar, estirar ni recortar
  silencios después. Comprueba siempre con `tools/pace.py`.
- **La persona habla con nuestra voz:** Kling 4.0 `omni_ref_video` 1080p con `audio_1` = la frase exacta; su vídeo entra mudo. Cada plano pasa
  `tools/kling_qa.sh` (r ≥ 0,9, deriva ≤ 0,1 s) y se mira la hoja de fotogramas. Si cambia el texto o mira a cámara, se regenera; no se parchea.
- **Nadie mira a cámara**, tampoco al final; **gancho serio**; **CTA** = pregunta palabra a palabra + logo, sin persona, sin botón y sin cartela.
- **Nunca tapar una cara** ni un clip con texto; textos en la banda 270-1250 px; colores sólidos en las letras; sin filtros.
- **Claves** solo en `.env` o variables de entorno; nunca en el repo ni en el chat.
- **Personas reales:** no clones la cara ni la voz de nadie sin su consentimiento explícito.

## Entregable de cada versión
1. `final_premium.mp4` (−14,5 LUFS, música ≈ 19-20 dB bajo la voz).
2. `edit_premium/` con `tools/export_edit.py proyectos/<p> --overlay --edition premium` (editable por un humano).
3. Sala de revisión (si el usuario la usa) con la versión nueva; solo se conserva la última versión de cada anuncio.
4. `LEEME.md` del proyecto actualizado (cadena, QA, costes, versiones).

## Aprender
Cada corrección que valga para todos los anuncios se añade a `docs/REGLAS.md` (y, si cambia el proceso, a `docs/METODOLOGIA.md`).
