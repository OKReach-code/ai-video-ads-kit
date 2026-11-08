# Reglas de calidad · se cumplen en TODOS los anuncios

Son las lecciones de muchos anuncios producidos e iterados con este método. Claude las repasa enteras antes de cada entrega.
Cuando tu cliente (o tú) corrija algo que valga para todos los anuncios, **añádelo aquí** para no repetirlo nunca.

## Voz y guion
1. **Ritmo de anuncio, conseguido al generar:** ≥ 6,4 sílabas/s, ninguna pausa > 0,6 s, ≤ 9 % de silencio. Nunca se acelera, estira ni se
   recortan silencios después (suena artificial). `tools/tts.py` añade una etiqueta de ritmo a Eleven v4; si una toma va lenta, se regenera.
   Lo comprueba `tools/pace.py`.
2. **Lo que frena el ritmo:** etiquetas de tono al principio de un bloque (`[con media sonrisa]`) y los «…». `tools/voz.py` los quita
   (los «…» pasan a coma) sin tocar las palabras.
3. **El guion es del cliente:** no se reescriben sus palabras; se proponen cambios y él decide.
4. **Siglas:** si el motor de voz lee mal una sigla (p. ej. «IA» en español), se envía escrita como se pronuncia (`tts.py` manda «ía»).
5. **La persona habla con NUESTRA voz:** Kling 4.0 `omni_ref_video` genera el vídeo moviendo los labios sobre el audio de ElevenLabs y ese vídeo
   entra mudo. Toma con r < 0,9 o deriva > 0,1 s → otra toma (o se corrige el desfase si es fijo).

## Puesta en escena
6. **Nunca se rompe la cuarta pared:** la persona mira al presentador fuera de cuadro todo el plano, también al final.
7. **Gancho serio:** en la primera frase la persona no sonríe ni se ríe, aunque el texto sea irónico (la ironía la pone la voz).
8. **CTA:** pantalla con el logo de la marca y la **pregunta apareciendo palabra a palabra** mientras se dice; sin la persona, sin botón
   (lo pone la plataforma) y sin cartela final. El anuncio termina ahí.
9. **Nunca tapar una cara** (tarjetas, rótulos, contadores) **ni un clip con texto**; personas siempre con la cabeza entera.
10. **Planos cuadrados sin deformar:** si una ventana es 1:1, se genera con una referencia también cuadrada (si no, la persona sale ensanchada).
11. **Metáforas visuales con fotos realistas** (Nano Banana Pro), no dibujos ni emojis. Recurso que funciona: foto en tarjeta y el objeto
    recortado «saliendo» del marco.
12. **Si hay un «asistente de IA» o mascota de la marca, sale siempre esa imagen**, nunca un robot genérico.
13. **Mostrar la interacción real:** en las capturas de producto se ve el clic y se salta al resultado, sin pantallas de carga.

## Estilo de edición
14. Fondo de líneas que fluyen en los tramos sin persona; la persona puede encogerse de pantalla completa a ventana; capturas en tarjetas 3D
    con borde de color; destello de luz al volver de un B-roll a la persona; caras reales en vez de iconos de personas.
15. **Subtítulos por frases cortas**, la frase entera de una vez; en el gancho, palabra a palabra.
16. **Titulares cinéticos:** una sola palabra grande por bloque, en la fuente de titulares, con halo suave del mismo color; nunca encima de una
    tarjeta. **Como mucho 1-2 inclinados por anuncio.**
17. **Números siempre en cifras** («50», «5.000», «40 %»), también en subtítulos (`captions.numerals`).
18. **Contadores:** terminan exactamente en la cifra final y se quedan quietos ≥ 0,3 s antes del corte.
19. Zona segura de Meta: textos entre 270 y 1250 px de alto; colores sólidos en las letras (nunca degradado); sin filtros (grano, viñeta).
20. No repetir en pantalla el mismo texto dos veces a la vez (subtítulo y rótulo).

## Sonido
21. **Música muy baja:** la pista de música ≈ 19-20 dB por debajo de la voz (`tools/mix.py` lo mide y avisa por debajo de 17 dB). Música épica
    o enérgica, sin melodías protagonistas.
22. **Golpe desde el primer fotograma**, impactos en los cambios de escena, «pop» al entrar tarjetas y **ningún efecto encima de una sílaba**
    (los *whoosh* solo en huecos sin voz). Se comprueba transcribiendo el máster (Scribe).

## Entrega y versiones
23. Cada versión: vídeo final + paquete editable (`tools/export_edit.py --overlay`) + revisión con notas por fotograma.
24. **Solo se conserva la última versión** de cada anuncio (en la sala y en la carpeta).
25. Antes de gastar créditos se dice qué, cuánto y cuánto cuesta, y se espera el «sí».
