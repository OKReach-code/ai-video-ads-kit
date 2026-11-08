#!/bin/zsh
# kling_qa.sh <proyecto> S1 URL [S2 URL ...] : descarga cada plano de Kling (urlWithoutWatermark de query_tasks) en kling/kling_<S>.mp4,
# lo deja mudo en film/assets/video/<S>.mp4 y le pasa tools/qa.py contra kling/refs/ref_<S>_rt.wav (texto exacto, r, desfase, deriva)
# y la hoja de fotogramas kling/sheet_kling_<S>.png (mirar: nadie mira a cámara, cara entera, sin sonrisa en el gancho).
# Criterio (docs/REGLAS.md): r ≥ 0,9 y deriva ≤ 0,1 s → vale. Desfase FIJO (todas las palabras igual) → apuntarlo en kling/offsets.json.
set -e
R=${0:A:h:h}; P=$1; shift
[ -d "$P" ] && D=${P:A} || D=$R/proyectos/$P
PY=$R/.venv/bin/python3; mkdir -p $D/film/assets/video
while [ $# -ge 2 ]; do
  K=$1; U=$2; shift 2
  curl -sL -o $D/kling/kling_$K.mp4 "$U"
  ffmpeg -v error -y -i $D/kling/kling_$K.mp4 -c:v copy -an $D/film/assets/video/$K.mp4
  echo "================ $K ($(ffprobe -v error -show_entries format=duration -of csv=p=0 $D/kling/kling_$K.mp4) s)"
  (cd $D && $PY $R/tools/qa.py kling/kling_$K.mp4 kling/refs/ref_${K}_rt.wav 2>&1 | grep -v "^$" | tail -6)
done
