# Prompts que funcionan

## 1. Look del presentador (Nano Banana Pro, Higgsfield) — una vez por marca
Genera 3-4 opciones y elige una. Guarda la elegida como `marca/persona_look.png` y un primer plano de la cara como `marca/persona_cara.png`.
```
Photorealistic vertical 9:16 frame from a premium two-person video podcast. A <edad> <rasgos: pelo, barba, ojos> <hombre/mujer> with
<aspecto: p. ej. southern European>, wearing <ropa>, seated at <mesa> with a glass of water, a black broadcast microphone on a boom arm at
frame right. Medium shot, three-quarter toward frame right, looking at an off-camera host at frame right (NOT at the camera), relaxed and
confident. Set: <plató: p. ej. minimalist glass-and-wood pavilion in a forest / warm studio with shelves and plants>, soft natural light,
shallow depth of field, 35mm lens. Real skin texture, no beauty filter, no film grain, no text, no watermark.
```
Para una ventana cuadrada, pide la misma imagen recompuesta a 1:1 (si no, Kling ensancha a la persona).

## 2. Persona hablando (Kling 4.0 `omni_ref_video`, 1080p)
Entradas: `image_1` = look, `image_2` = cara, `audio_1` = `kling/refs/ref_<S>_rt.wav`. Duración = la de `kling/shots.json`.
La plantilla completa está en `plantilla/kling/prompts.json`. Lo imprescindible:
- **Identidad exacta** («keep their identity exactly…», rasgos, ropa, plató de 图片1).
- **Clip de pódcast que NO presenta a cámara:** «they look at the off-camera host at frame right for the WHOLE shot, never at the lens».
- **Su voz es 音频1:** «use its timbre, words, pacing and exact timing; lips perfectly synchronised to 音频1, with no extra pauses».
- **El diálogo literal** entre comillas y «they say exactly these words and nothing else».
- **Actuación:** en el gancho «serious and composed, does NOT smile or laugh, shows no teeth»; en el resto, la emoción de la frase.
- **Imagen limpia:** «clean hyperrealistic digital cinema image (no film grain, no noise, no painterly smoothing)».
- Pronunciación de siglas o marcas si hace falta («"IA" is said "Í-A"»).

## 3. Metáforas visuales (Nano Banana Pro)
Foto realista, el objeto grande y centrado, texto grabado o impreso **exacto** entre comillas y en orden de líneas:
```
Photorealistic close-up of <objeto> in <entorno>, <detalles de materiales y luz>. <Texto>, in this exact text and line order:
"LÍNEA 1" "LÍNEA 2". Spelling exactly as written. The whole <objeto> is fully visible, centred, occupying the middle 60% of the frame.
Cinematic natural light, sharp detail, shallow depth of field, real photograph, no people, no other text, no watermark.
```
Si debe «salir» de la tarjeta: quita el fondo a la imagen (Higgsfield `remove_background`) y usa el recorte encima del original.

## 4. B-roll (Veo, Higgsfield)
Texto a vídeo, en el formato de la ventana donde va (9:16 a pantalla completa, 1:1 en pantalla partida), describiendo acción concreta,
plano, luz y aspecto de las personas; sin texto en pantalla. Revisa la hoja de fotogramas antes de montarlo.

## 5. Voz (ElevenLabs Eleven v4)
`tools/tts.py` antepone `[very fast-paced social media ad, quick and direct, no long pauses]`. El parámetro `speed` no funciona en v4:
el ritmo sale de la etiqueta, de la voz elegida y de un guion sin «…». Prueba 3-4 voces de la biblioteca con el mismo bloque y quédate con
la que pase `pace.py` con mejor sonido.
