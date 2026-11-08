---
description: Produce el anuncio de la voz al máster (voz rápida → Kling sobre la voz → montaje → mezcla → QA → entrega)
argument-hint: <nombre-del-anuncio>
---
Usa la skill `anuncios-ia` para `proyectos/$ARGUMENTS` (pasos 3-7 de `docs/METODOLOGIA.md`), comprobando cada control antes de seguir:
1. Voz: `tools/voz.py $ARGUMENTS` → `pace.py` en verde y texto exacto.
2. Persona: `tools/kling_refs.py $ARGUMENTS`, prompts de `docs/PROMPTS.md`; dime planos, segundos y créditos y **espera mi «sí»**; lanza Kling;
   `tools/kling_qa.sh` + hoja de fotogramas; `tools/kling_sync.py`.
3. Imágenes / B-roll que pida `escenas.json` (con coste y mi «sí»).
4. Montaje: `tools/build.py`, render, hoja de fotogramas revisada y corregida.
5. Sonido y mezcla: `tools/sonido.py`, `tools/make_mix.py`, `tools/mix.py`; QA del máster (Scribe + `pace.py`).
6. Entrega: `tools/export_edit.py --overlay`, sala de revisión si la uso, `LEEME.md`. Dame un resumen corto y dónde está el vídeo.
