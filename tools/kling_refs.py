"""Referencias audio_1 para Kling 4.0 omni_ref (la persona dice NUESTRA locución, docs/METODOLOGIA.md).
Corta cada frase de audio/vo.wav con tools/make_refs.py (0,25 s de entrada + la frase + silencio hasta segundos enteros) y le añade
ruido de sala (rosa, amplitud 0,002): el filtro de seguridad de Kling rechaza referencias con > 3 s de silencio digital.
  kling/shots.json = {"S1": ["PrimeraPalabra", "última.", 5, 0.0], ...}  (palabras tal como las escribe Scribe en audio/vo_words.json,
                     segundos del plano —enteros, 3-15— y segundo de la locución desde el que buscar)
uso: tools/kling_refs.py <proyecto>
sale: kling/refs/ref_<S>.wav, ref_<S>_rt.wav (la que se sube) y segs.json; imprime segundos y créditos (1080p ≈ 15 cr/s)."""
import json, subprocess, sys, pathlib
T = pathlib.Path(__file__).resolve().parent
if len(sys.argv) < 2: sys.exit(__doc__)
R = (T.parent/'proyectos'/sys.argv[1]) if not pathlib.Path(sys.argv[1]).exists() else pathlib.Path(sys.argv[1]).resolve()
out = R/'kling/refs'
subprocess.run([sys.executable, T/'make_refs.py', R/'audio/vo.wav', R/'audio/vo_words.json', R/'kling/shots.json', out], check=True)
segs = json.load(open(out/'segs.json'))
for k in segs:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out/f'ref_{k}.wav', '-f', 'lavfi', '-i', 'anoisesrc=color=pink:amplitude=0.002:sample_rate=48000',
                    '-filter_complex', '[0][1]amix=inputs=2:duration=first:normalize=0', '-ac', '1', out/f'ref_{k}_rt.wav'], check=True)
s = sum(v['duration'] for v in segs.values())
print(f'ok {len(segs)} referencias en {out} · {s} s de Kling ≈ {15 * s} créditos a 1080p (súbelas con file_upload: ref_<S>_rt.wav)')
