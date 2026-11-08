---
description: Sube la versión a la sala de revisión o lee y aplica las notas del cliente
argument-hint: <nombre-del-anuncio> [leer]
---
Sigue `docs/METODOLOGIA.md` §7-8.
- **Sin `leer`:** si no tengo sala, publica `tools/review/sala.html` como artifact con las capacidades `db`, `user` y `assets` y apunta su URL en
  `marca/marca.json` (`sala_revision`). Después `python3 tools/review.py proyectos/$ARGUMENTS --version vN`, sube `review/<id>.mp4` como asset
  de la sala y escribe `review/<id>.json` (con su `asset`) en la colección `videos`. Borra de la sala la versión anterior (ficha, asset y notas
  resueltas): solo se queda la última. Dame el enlace `…#<id>`.
- **Con `leer`:** lee las notas abiertas (`notes` con `done == false` de este anuncio), resúmelas por tiempo, aplícalas (nada de pago sin mi «sí»),
  saca la versión siguiente, márcalas como resueltas y añade a `docs/REGLAS.md` las que valgan para todos los anuncios.
