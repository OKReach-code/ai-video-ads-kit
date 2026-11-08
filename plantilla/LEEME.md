# «<Nombre del anuncio>» · v1

| | |
|---|---|
| Máster | `final_premium.mp4` · __ s · −14,5 LUFS · música __ dB bajo la voz |
| Editable | `edit_premium/` (XML para DaVinci Resolve / Premiere, gráficos con alfa, pistas de audio, SRT) |
| Revisión | enlace de tu sala de revisión |

## Brief
- Producto / oferta:
- Público:
- Formato:
- Anuncio de referencia:

## Cadena
| Paso | Qué se usó |
|---|---|
| Guion | `audio/guion.json` |
| Voz | `tools/voz.py` · voz `<id>` · __ síl/s · __ % pausas |
| Persona | look + cara · Kling 4.0 `omni_ref_video` 1080p · planos y créditos |
| Imágenes / B-roll | |
| Montaje | `escenas.json` + `tools/build.py` |
| Mezcla | `tools/make_mix.py` + `tools/mix.py` |

## QA de Kling
| Plano | Texto | r | Desfase | Deriva | Uso |
|---|---|---|---|---|---|

## Checklist (docs/REGLAS.md)
- [ ] Voz ≥ 6,4 síl/s, sin pausas > 0,6 s, texto exacto
- [ ] Nadie mira a cámara · gancho serio · ninguna cara tapada
- [ ] Cifras · gancho palabra a palabra · 1-2 titulares inclinados como mucho
- [ ] Contadores que acaban antes del corte · ningún efecto encima de una palabra · música ≈ 19 dB bajo la voz
- [ ] CTA: pregunta palabra a palabra + logo, sin persona ni cartela
