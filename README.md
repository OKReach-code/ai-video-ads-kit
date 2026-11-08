# AI Video Ads Kit

**Crea anuncios en vídeo verticales para Meta, TikTok y Reels con IA, con tu marca, hablando con Claude Code.**

Le das a Claude la idea y el guion; él genera la voz, la persona que habla, el montaje con animaciones, la música, la mezcla, un paquete
editable para DaVinci Resolve o Premiere y una sala de revisión donde tu cliente deja notas en el fotograma exacto.

| | |
|---|---|
| **Director** | Claude Code (con la skill `anuncios-ia` incluida) |
| **Voz** | ElevenLabs Eleven v4, con ritmo de anuncio conseguido al generar (≥ 6,4 sílabas/s), sin acelerar después |
| **Persona que habla** | Kling 4.0 `omni_ref_video` 1080p, moviendo los labios sobre tu voz (suena siempre tu locución) |
| **Imágenes y B-roll** | Higgsfield: Nano Banana Pro, Veo, recorte de fondos |
| **Montaje** | HyperFrames: fondo de líneas que fluyen, persona que se encoge a ventana, capturas en 3D, titulares cinéticos, contadores, CTA final |
| **Salida** | MP4 1080×1920 a −14,5 LUFS + paquete editable (XML, gráficos con transparencia, pistas, SRT) |

## Empieza aquí
1. **Instalación paso a paso:** [`docs/INSTALACION.md`](docs/INSTALACION.md) (unos 20 min)
2. **Tu marca:** abre la carpeta en Claude Code y escribe `/marca`
3. **Tu primer anuncio:**
   ```text
   /nuevo-anuncio lanzamiento-curso     → brief, guion y plan con el coste (sin gastar nada)
   /producir lanzamiento-curso          → voz, persona, montaje, mezcla, QA y entrega (te pide el «sí» antes de gastar)
   /revision lanzamiento-curso          → aplica las notas y saca la versión siguiente
   ```
   O en lenguaje natural: *«Quiero un anuncio de 40 s para mi curso de fotografía, formato clip de pódcast»*.

## Cómo funciona
[`docs/METODOLOGIA.md`](docs/METODOLOGIA.md) explica cada paso, qué se comprueba y cuánto cuesta. Las reglas de calidad que hacen que un anuncio
funcione (y que Claude repasa en cada entrega) están en [`docs/REGLAS.md`](docs/REGLAS.md). El montaje se describe en un archivo sencillo
(`escenas.json`, ver [`docs/ESCENAS.md`](docs/ESCENAS.md)) y los prompts que funcionan están en [`docs/PROMPTS.md`](docs/PROMPTS.md).

## Estructura
```
CLAUDE.md                     reglas que Claude sigue siempre en este repositorio
.claude/skills/anuncios-ia/   la skill (flujo completo)
.claude/commands/             /marca, /nuevo-anuncio, /producir, /revision
.mcp.json                     servidor MCP de Kling
marca/                        tu marca: marca.json, logo, fuentes, presentador
plantilla/                    proyecto base (guion, planos, escenas, plantilla de montaje, build y mezcla)
tools/                        voz.py, kling_refs.py, kling_qa.sh, kling_sync.py, qa.py, pace.py, sonido.py, mix.py, export_edit.py, review.py…
docs/                         instalación, metodología, reglas, escenas, prompts
proyectos/                    un directorio por anuncio (los vídeos y audios no se suben a git)
```

## Costes
Tú pagas tus propias cuentas. Un anuncio de 40 s con 3 planos de persona suele costar 300-450 créditos de Kling, unas pocas imágenes en
Higgsfield y el uso de ElevenLabs de tu plan. Claude siempre te dice el coste antes de gastar.

## Uso responsable
No clones la cara ni la voz de una persona real sin su consentimiento explícito. Revisa las condiciones de uso comercial de cada servicio y
las políticas de publicidad de cada plataforma (anuncios con contenido generado por IA).

## Licencia
Código y documentación bajo licencia MIT ([`LICENSE`](LICENSE)). La fuente Montserrat incluida es de Google Fonts bajo SIL Open Font License 1.1.
HyperFrames, GSAP, ElevenLabs, Kling e Higgsfield son de sus respectivos dueños y se usan según sus propias condiciones.
