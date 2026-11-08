---
description: Crea un anuncio nuevo: brief, guion por bloques y plan con el coste (sin gastar nada)
argument-hint: <nombre-del-anuncio>
---
Usa la skill `anuncios-ia` (pasos 1-2 de `docs/METODOLOGIA.md`).
1. `tools/new_project.sh $ARGUMENTS`.
2. Pídeme el brief en una sola pregunta: producto/oferta, público, formato (clip de pódcast / voz en off con demos / mixto), duración (35-60 s),
   la pregunta final y el guion literal (si no lo tengo, propón 2-3 guiones: gancho → problema con un dato → solución → pregunta).
3. Escribe `audio/guion.json` (un bloque por frase/plano), `kling/shots.json` y `escenas.json`, y enséñame el plan plano a plano con el coste
   estimado (Kling 1080p ≈ 15 créditos/s, imágenes ≈ 2 créditos). **No lances nada de pago hasta que diga «sí».**
Siguiente paso: `/producir $ARGUMENTS`.
