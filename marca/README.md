# Tu marca

Todo lo que es «de tu marca» vive aquí y lo leen la plantilla de montaje (`plantilla/tools/build.py`) y Claude. La forma fácil: `/marca`.

| Campo de `marca.json` | Qué es |
|---|---|
| `nombre`, `web` | nombre de la marca y su web |
| `colores.primario` | color principal (borde de las tarjetas, detalles) |
| `colores.acento` | titulares grandes y palabras en la fuente de titulares |
| `colores.resaltado` | palabras resaltadas, contadores, palabras clave de la pregunta final |
| `colores.alerta`, `colores.fondo` | rojo de aviso y color de fondo (oscuro) |
| `fuentes.texto`, `fuentes.titulares` | archivos `.ttf`/`.otf` dentro de `marca/fuentes/` (por defecto Montserrat, OFL) |
| `fuentes.titulares_mayusculas` | `none`, `uppercase` o `lowercase` |
| `logo` | `marca/logo.png`: logo en **blanco sobre transparente** (va sobre fondo oscuro en la pantalla final) |
| `cta` | la pregunta final por defecto (p. ej. «¿Quieres probarlo gratis?») |
| `voz` | `elevenlabs_voice_id`, `idioma` (`es`, `en`…), `stability`, `style` |
| `persona` | presentador fijo: `persona_look.png` (look + plató) y `persona_cara.png` (primer plano) |
| `asistente_ia` | imagen de tu mascota o asistente de IA, si tienes (nunca un robot genérico) |
| `sala_revision` | URL de tu sala de revisión (la añade `/revision`) |

El `logo.png` incluido es un ejemplo («MI MARCA»): cámbialo por el tuyo.
