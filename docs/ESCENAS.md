# escenas.json · cómo se describe el montaje

El montaje no se programa a mano: describes las escenas en `proyectos/<anuncio>/escenas.json` y `tools/build.py` calcula todos los tiempos
a partir de las palabras reales de la voz. Claude lo rellena por ti; esta página explica qué significa cada campo.

## Escenas (se suceden en el tiempo)
Cada escena empieza en un bloque del guion (`"desde": "B3"`) o en una palabra (`"desde_palabra": "precio"`) y dura hasta que empieza la siguiente.

| Tipo | Qué muestra | Campos |
|---|---|---|
| `persona` | La persona hablando a pantalla completa (plano de Kling) | `plano` (S1…), opcional `"modo": "ventana"` y `"ventana_y": "41%"` (encuadre dentro de la ventana) |
| `fondo` | Fondo de líneas que fluyen (voz en off) | — (encima van los insertos) |
| `broll` | Un vídeo a pantalla completa | `archivo` (en `film/assets/video/`), opcional `media_inicio` |
| `cta` | Logo + la pregunta palabra a palabra. **Siempre la última** | `desde_palabra` = la primera palabra de la pregunta |

Con `"modo": "ventana"` la persona se encoge a una ventana arriba (y = 90-850): debajo caben insertos con `"posicion": "abajo"`.

## Insertos (encima de las escenas)
Van de `desde_palabra` a `hasta_palabra` (o `duracion`). Si la palabra se repite, usa `"en": "B3"` (buscar desde ese bloque) o `"n": 2`.

| Tipo | Qué es | Campos |
|---|---|---|
| `clip` | Vídeo (captura de producto, demo) en tarjeta | `archivo`, `modo`: `tarjeta3d` · `tarjeta` · `completa`, `posicion`: `arriba` · `centro` · `abajo`, `ancho` (px) |
| `imagen` | Imagen o metáfora | `archivo` (en `film/assets/img/`), `modo`: `tarjeta3d` · `tarjeta` · `recorte` (PNG sin fondo, con sombra) |
| `contador` | Número que sube y se para antes del corte | `de`, `a`, `sufijo`, `etiqueta`, `posicion` |
| `titular` | Texto fijo grande (úsalo poco) | `texto`, `posicion` |

## Texto
- `resaltar`: palabras del subtítulo en el color de resaltado.
- `fuente_titulares`: palabras del subtítulo en la fuente de titulares (en vez de repetirlas en un rótulo).
- `titulares`: `{"palabra": "acento" | "resaltado" | "primario" | "alerta" | "texto"}` → esa palabra sale GRANDE (una por bloque, nunca
  encima de una tarjeta: si choca, se queda como subtítulo normal).
- `inclinados`: las 1-2 palabras de `titulares` que van inclinadas.
- `cta_resaltar`: palabras de la pregunta final en color (expresión regular, p. ej. `"gratis|demo"`).
- `encuadre_persona`: punto de la cara para los acercamientos (`"50% 30%"`).

## Ejemplo
```json
{
 "escenas": [
  {"tipo": "persona", "plano": "S1", "desde": "B1"},
  {"tipo": "persona", "plano": "S2", "desde": "B2", "modo": "ventana"},
  {"tipo": "broll", "archivo": "oficina.mp4", "desde": "B3"},
  {"tipo": "fondo", "desde_palabra": "plataforma"},
  {"tipo": "persona", "plano": "S5", "desde": "B5"},
  {"tipo": "cta", "desde_palabra": "¿Quieres"}
 ],
 "insertos": [
  {"tipo": "contador", "desde_palabra": "abandonan", "hasta_palabra": "curso.", "de": 0, "a": 70, "sufijo": " %", "posicion": "abajo"},
  {"tipo": "clip", "archivo": "demo.mp4", "desde_palabra": "plataforma", "hasta_palabra": "resultado.", "modo": "tarjeta3d", "posicion": "arriba"},
  {"tipo": "imagen", "archivo": "metafora_recorte.png", "desde_palabra": "antes", "hasta_palabra": "después", "modo": "recorte", "posicion": "centro"}
 ],
 "resaltar": ["gratis", "resultado"],
 "titulares": {"resultado": "acento", "nunca": "alerta"},
 "inclinados": ["nunca"],
 "cta_resaltar": "gratis"
}
```
`build.py` avisa si un plano de Kling se queda corto para su escena, si una palabra no existe en la voz o si hay más de 2 titulares inclinados.
