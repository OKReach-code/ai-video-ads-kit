# Metodología · de la idea al anuncio entregado

Cada paso dice **qué pedirle a Claude**, **qué hace por debajo**, **qué comprobar** y **cuánto cuesta**. Las reglas de calidad están en
[`REGLAS.md`](REGLAS.md); el montaje, en [`ESCENAS.md`](ESCENAS.md); los prompts, en [`PROMPTS.md`](PROMPTS.md).

## La cadena
```
guion por bloques ─► voz rápida (ElevenLabs v4) ─► persona hablando sobre ESA voz (Kling 4.0 1080p)
        │                                                   │
        └─► capturas de producto, imágenes, B-roll (Higgsfield: Nano Banana Pro / Veo)
                                                            ▼
     escenas.json ─► montaje (HyperFrames) ─► mezcla −14 LUFS ─► QA ─► revisión con notas ─► versión siguiente
```
**La idea clave:** en el vídeo final suena siempre la voz de ElevenLabs. Kling genera a la persona moviendo los labios sobre ese audio
y su vídeo entra mudo. Así el ritmo es el de la voz (rápido, de anuncio) y la pronunciación es la que tú controlas.

---

## Paso 0 · Tu marca (una vez)
**Pídele:** `/marca`. Claude te pregunta nombre, colores, fuentes, logo, la pregunta final (CTA) y la voz de ElevenLabs, y rellena
`marca/marca.json`. Si quieres un presentador fijo, te ofrece 3-4 fotos (look + plató) para elegir y guarda look y cara en `marca/`.

## Paso 1 · Proyecto nuevo y brief
**Pídele:** `/nuevo-anuncio lanzamiento-curso` (o «quiero un anuncio de 40 s para …»).
- Crea `proyectos/lanzamiento-curso/` desde `plantilla/`.
- Te pregunta en un solo bloque: producto, público, formato, duración, la pregunta final y **el guion**. Si no tienes guion, te propone
  2-3 (gancho → problema → solución → pregunta) y eliges o editas.

## Paso 2 · Plan (sin gastar nada)
- `audio/guion.json`: un bloque por frase o plano.
- `kling/shots.json`: qué bloques dice la persona en cámara (y cuántos segundos dura cada plano, enteros).
- `escenas.json`: qué se ve en cada momento (ver `ESCENAS.md`).
- Claude te enseña el plan plano a plano y **el coste**. No se gasta nada sin tu «sí».

## Paso 3 · Voz rápida
`tools/voz.py <proyecto>`: 3 tomas por bloque con Eleven v4 + etiqueta de ritmo, transcripción de cada toma (Scribe), elige la exacta más rápida.
**Control:** ≥ 6,4 sílabas/s, ninguna pausa > 0,6 s, ≤ 9 % de silencio, texto exacto. Si falla: más tomas. Nunca acelerar después.

## Paso 4 · La persona (Kling 4.0)
1. `tools/kling_refs.py <proyecto>` → las frases de cada plano con ruido de sala (`kling/refs/ref_<S>_rt.wav`) y el coste.
2. Prompts desde `PROMPTS.md`: identidad exacta, clip de pódcast, **mira al presentador, nunca a cámara**, gancho serio, imagen limpia.
3. Claude sube look, cara y referencias con el MCP de Kling (`file_upload`) y lanza `omni_ref_video` (Kling 4.0, 1080p, 9:16).
4. Cuando acaban (2-4 min): `tools/kling_qa.sh <proyecto> S1 <url> …` → texto, **r ≥ 0,9**, **deriva ≤ 0,1 s** y hoja de fotogramas.
   Desfase fijo → `kling/offsets.json`. Texto cambiado, mira a cámara, sonríe en el gancho → se regenera ese plano.
5. `tools/kling_sync.py <proyecto>` → cómo encaja cada plano con la voz.

## Paso 5 · Imágenes, capturas y B-roll
- **Capturas de tu producto:** graba la pantalla (vertical u horizontal) y deja los MP4 en `film/assets/video/`. Se muestran en tarjetas 3D.
- **Metáforas e imágenes:** Nano Banana Pro (Higgsfield), foto realista; si el objeto debe «salir» del marco, se le quita el fondo (Higgsfield).
- **B-roll:** Veo (Higgsfield) desde texto, en el formato de su ventana.

## Paso 6 · Montaje
`cd proyectos/<p> && python3 tools/build.py` y render:
```bash
cd film && npx -y hyperframes@0.8.162 render -f 24 -q high -w 4 -o ../render/video_noaudio_premium.mp4
```
**Control (Claude saca una hoja de fotogramas y la revisa):** ninguna cara tapada, cabezas enteras, textos en 270-1250 px, titulares sin
pisar tarjetas, contadores que acaban antes del corte.

## Paso 7 · Sonido, mezcla, QA y entrega
1. `tools/sonido.py <p> music sfx --dur=<segundos>` (música y efectos con ElevenLabs, una vez por anuncio).
2. `python3 tools/make_mix.py` → `python3 ../../tools/mix.py mix_premium.json` → `final_premium.mp4` (−14,5 LUFS, música ≈ 19-20 dB bajo la voz).
3. QA del máster: transcripción exacta (`tools/scribe.py`) y `tools/pace.py`.
4. **Paquete editable:** `python3 tools/export_edit.py proyectos/<p> --overlay --edition premium` → `edit_premium/` (XML para DaVinci Resolve /
   Premiere con los planos cortados, gráficos con transparencia, voz / música / efectos en pistas separadas y SRT).
5. **Sala de revisión** (opcional, recomendada): una página de Claude (Artifact) donde tu cliente ve los vídeos y deja notas en el fotograma exacto.
   La primera vez pídele a Claude: *«publica `tools/review/sala.html` como artifact con las capacidades db, user y assets»*. Después, en cada
   versión: `python3 tools/review.py proyectos/<p> --version vN`, sube el MP4 como asset de la sala y escribe su ficha en la colección `videos`.
   Para leer las notas: *«lee las notas abiertas de la sala para <p> y aplícalas»*. Solo se queda la última versión de cada anuncio.

## Paso 8 · Iterar
Claude aplica las notas, saca la vN+1 y marca las notas como resueltas. Lo que valga para todos los anuncios va a `REGLAS.md`.

---

## Costes orientativos
| Pieza | Coste |
|---|---|
| Kling 4.0 1080p | ≈ 15 créditos/s (3 planos de persona en un anuncio de 40 s: 300-450 créditos) |
| Nano Banana Pro (imagen) | ≈ 2 créditos por imagen |
| Recorte de fondo (imagen o vídeo) | pocos créditos |
| Veo (B-roll) | ≈ 70 créditos por plano |
| ElevenLabs | según tu plan (voz con 3 tomas por bloque, música y efectos) |

## Problemas frecuentes
| Síntoma | Solución |
|---|---|
| Kling rechaza la referencia de audio | tiene > 3 s de silencio digital: `kling_refs.py` ya añade ruido de sala |
| La persona sale ensanchada en una ventana cuadrada | genera ese plano con una referencia cuadrada |
| Voz lenta | quita etiquetas de tono y «…» del bloque y genera más tomas |
| Un efecto tapa una palabra | `make_mix.py` solo pone whoosh en huecos; revisa efectos añadidos a mano |
| Un objeto debe ir «detrás» de la persona | recorte de vídeo de la persona (Higgsfield) → vídeo con transparencia encima del objeto |
| `build.py`: «no encuentro la palabra» | escríbela como la transcribe Scribe (mira `audio/vo_words.json`) |
| Avisos de *timeout* al renderizar | HyperFrames reintenta solo; comprueba que el MP4 tiene todos los fotogramas |
