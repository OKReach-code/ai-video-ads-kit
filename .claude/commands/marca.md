---
description: Configura tu marca (colores, fuentes, logo, CTA, voz y presentador) en marca/marca.json
---
Ayúdame a rellenar `marca/marca.json` (ver `marca/README.md`), en una sola tanda de preguntas:
1. Nombre de la marca, web y a qué se dedica (una frase).
2. Colores: primario, acento y resaltado en hexadecimal (si no los sé, propón 3 paletas con buen contraste sobre fondo oscuro y elijo).
3. Fuentes: la de texto y la de titulares (archivos `.ttf`/`.otf` en `marca/fuentes/`; si no tengo, Montserrat para las dos) y si los titulares van en mayúsculas.
4. Logo: comprueba `marca/logo.png` (blanco sobre transparente, ~600 px de ancho); si lo tengo en otro color o con fondo, conviértelo.
5. La pregunta final del anuncio (CTA), p. ej. «¿Quieres probarlo gratis?».
6. Voz: lista 4-6 voces de ElevenLabs en mi idioma (con la API de `tools/_keys.py`), genera la misma frase de prueba con cada una
   (`tools/tts.py`) y mide el ritmo con `tools/pace.py`; me das los enlaces locales para escucharlas y elijo.
7. Presentador (opcional): si quiero uno fijo, genera 3-4 opciones de look y plató con Higgsfield Nano Banana Pro (`docs/PROMPTS.md` §1, ~2 créditos
   cada una, dímelo antes), guarda la elegida en `marca/persona_look.png` y un primer plano en `marca/persona_cara.png`.
Al terminar, enséñame el `marca.json` final.
