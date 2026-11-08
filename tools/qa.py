"""QA of one Kling take against its audio_1 reference. usage: qa.py kling_K.mp4 ref_K.wav
Prints: Scribe text (exact?), gaps, waveform r + offset (did Kling keep OUR voice?), first-word offset and per-word drift; writes a frame sheet.
Pass: text exact · no gap > 0.25 s that is not in our VO · drift < 0.1 s. r >= 0.9 = it kept our voice (use the image as is)."""
import json, re, subprocess, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
clip, ref = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
aud = clip.with_name(clip.stem + '_audio.wav'); cw = clip.with_name(clip.stem + '_words.json'); rw = ref.with_name(ref.stem + '_words.json')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vn','-ac','1','-ar','48000',str(aud)], check=True)
py = lambda *a: subprocess.run([sys.executable, str(HERE/a[0]), *map(str, a[1:])], check=True)
py('scribe.py', aud, cw)
if not rw.exists(): subprocess.run([sys.executable, str(HERE/'scribe.py'), str(ref), str(rw)], check=True, capture_output=True)
py('audiomatch.py', aud, ref)
a, b = json.load(open(rw)), json.load(open(cw))
n = lambda t: re.sub(r'[^\wáéíóúñü]', '', t.lower())
if [n(x[2]) for x in a] != [n(x[2]) for x in b]:
    print('TEXT MISMATCH -> regenerate'); print(' ref:', ' '.join(x[2] for x in a)); print(' kl :', ' '.join(x[2] for x in b))
else:
    d = [round(y[0]-x[0]-(b[0][0]-a[0][0]), 2) for x, y in zip(a, b)]
    print(f'first-word offset {b[0][0]-a[0][0]:+.2f}s  drift max {max(map(abs, d)):.2f}s ->', ' '.join(f'{x[2]}{v:+.2f}' for x, v in zip(a, d) if abs(v) >= 0.08))
sheet = clip.with_name('sheet_' + clip.stem + '.png')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vf','fps=2,scale=180:-1,tile=10x2','-frames:v','1',str(sheet)], check=True)
print('sheet', sheet)
