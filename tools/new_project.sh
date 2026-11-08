#!/bin/zsh
# new_project.sh <nombre>  ->  proyectos/<nombre>/ listo: guion por bloques, planos de Kling, escenas, montaje HyperFrames y efectos de sonido.
set -e
[ -z "$1" ] && { echo "uso: tools/new_project.sh <nombre-del-anuncio>"; exit 1; }
R=${0:A:h:h}; D=$R/proyectos/$1
[ -e $D ] && { echo "ya existe $D"; exit 1; }
cp -R $R/plantilla $D
mkdir -p $D/audio/sfx $D/kling/refs $D/render $D/film/assets/{fonts,video,img}
cp $R/marca/fuentes/* $D/film/assets/fonts/ 2>/dev/null || true
echo "ok -> $D"
echo "Siguiente: rellena audio/guion.json con el guion por bloques y ejecuta  .venv/bin/python3 tools/voz.py $1"
