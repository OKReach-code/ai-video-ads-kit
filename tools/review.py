"""Sala de revisión: prepara un vídeo para la biblioteca de revisión (reproductor con notas por fotograma, tipo Frame.io).
usage: review.py proyectos/<marca>-<nombre> [--edition premium|cheap] [--version v2] [--label "..."] [--src final_<edición>.mp4] [--name "Mi anuncio"]
Ediciones (docs/METODOLOGIA.md): «premium» (la edición por defecto) o «cheap» (una variante más barata, si la generas).
Escribe en <proyecto>/review/:
  <id>.mp4   copia ligera (≤ 14 MB, 1080×1920) para subir como asset de la sala
  <id>.json  documento para la colección `videos` de la sala ({title, project, version, label, dur, fps, scenes, lufs, created, asset, src})
id = <proyecto>-<edición>[-<version>][-<label>] (también es el enlace directo: <url de la sala>#<id>). Sin --version = primera entrega.
La sala es UNA página fija (tools/review/sala.html) publicada una vez; los vídeos se añaden sin republicarla (ver docs/METODOLOGIA.md §7)."""
import argparse, json, pathlib, subprocess, re, time, unicodedata
ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument('project'); ap.add_argument('--edition', choices=['cheap', 'premium'], default='premium')
ap.add_argument('--version', default='', help='solo para iteraciones posteriores: v2, v3...')
ap.add_argument('--label', default='', help='variante, p. ej. "Clips nuevos" (planos nuevos)')
ap.add_argument('--src', default=None, help='máster a revisar (por defecto final_<edición>.mp4, o final.mp4)')
ap.add_argument('--brand', default=None); ap.add_argument('--name', default=None)
a = ap.parse_args()
P = pathlib.Path(a.project).resolve()
slug = P.name                                              # p. ej. mimarca-lanzamiento
brand = a.brand or slug.split('-')[0].capitalize()
name = a.name or ' '.join(slug.split('-')[1:]).capitalize()
src = P / (a.src or (f'final_{a.edition}.mp4' if a.edition else 'final.mp4'))
ed = f'{a.edition.capitalize()} version' if a.edition else ''
assert src.exists(), f'falta {src}: entrega primero el vídeo final'
norm = lambda s: re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()).strip('-')
vid = '-'.join(x for x in (slug, a.edition, a.version, norm(a.label)) if x)
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_entries',
                                   'format=duration:stream=width,height,r_frame_rate,codec_type', str(src)], capture_output=True, text=True).stdout)
vs = next(s for s in probe['streams'] if s['codec_type'] == 'video')
dur = round(float(probe['format']['duration']), 2)
num, den = map(int, vs['r_frame_rate'].split('/')); fps = round(num / den)
out = P / 'review'; out.mkdir(exist_ok=True)
# copia ligera (los assets de la sala admiten hasta 20 MiB): ~2,2 Mb/s mantiene 1080×1920 legible
kbps = max(800, min(2200, int(13.5 * 8000 / dur) - 160))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-c:v', 'libx264', '-b:v', f'{kbps}k', '-maxrate', f'{int(kbps*1.3)}k',
                '-bufsize', f'{kbps*2}k', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
                '-movflags', '+faststart', str(out / f'{vid}.mp4')], check=True)
size = (out / f'{vid}.mp4').stat().st_size
assert size < 15_000_000, f'{vid}.mp4 pesa {size/1e6:.1f} MB'
# escenas de la pista: film/timeline.json["scenes"] = [[inicio, fin, "nombre"], ...] (lo escribe build.py)
scenes, tj = [], P / 'film' / 'timeline.json'
if tj.exists(): scenes = json.load(open(tj)).get('scenes', [])
lufs = None
m = re.search(r'(−?-?\d+[,.]\d+) LUFS', (P / 'LEEME.md').read_text() if (P / 'LEEME.md').exists() else '')
if m: lufs = m.group(1)
doc = {'title': ' · '.join(x for x in (f'{brand} · {name}', ed, a.version, a.label) if x), 'project': f'{brand} · {name}',
       'edition': a.edition or '', 'version': a.version, 'label': ' · '.join(x for x in (ed, a.label) if x), 'dur': dur, 'fps': fps, 'scenes': scenes, 'lufs': lufs,
       'created': int(time.time() * 1000), 'asset': None, 'src': ''}
json.dump(doc, open(out / f'{vid}.json', 'w'), ensure_ascii=False, indent=1)
print(f'ok {vid} · {out/(vid + ".mp4")} ({size/1e6:.1f} MB) · {out/(vid + ".json")} · {len(scenes)} escenas')
