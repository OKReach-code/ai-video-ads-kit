"""Human-editable export of an ad: a timeline that opens in DaVinci Resolve / Premiere Pro with every piece on its own track.
usage: export_edit.py PROJECT_DIR [--caps caps.json] [--overlay] [--name NAME] [--edition cheap|premium]
  --edition E  premium (por defecto) o cheap: lee mix_E.json y render/video_noaudio_E.mp4 y escribe edit_E/.
               Ejecútalo justo después de construir esa edición (film/index.html y film/caps.json son de la última build).

Reads (all paths relative to PROJECT_DIR):
  film/index.html          the generated HyperFrames film: every <video class="clip" data-start data-duration data-media-start>
  mix.json                 the mix config used by tools/mix.py (out, dur, vo, sfx...) -> its <out>_stems/{vo,music,sfx}.wav
  caps.json                caption blocks from tools/captions.py (default: film/caps.json or audio/caps.json if present)
  render/video_noaudio.mp4 the HyperFrames render (reference track, muted, disabled)
Writes PROJECT_DIR/edit/:
  <NAME>.xml               FCP7 XML (xmeml v5), 24 fps, 1080x1920. File > Import > Timeline (Resolve) / File > Import (Premiere)
  <NAME>.srt               captions as editable subtitles (import into the timeline, restyle as you like)
  media/                   every file the timeline uses, copied so the folder can be zipped and handed over
  graphics_alpha.mov       (--overlay) ProRes 4444 with transparency: all HyperFrames UI cards / titles / CTA, WITHOUT the footage,
                           captions, vignette or grain -> sits on V2 above the clips
Tracks: V1-Vn footage clips (Kling persona + B-roll, already trimmed and placed), V(n+1) graphics_alpha.mov,
        V(top) full render for reference (disabled) · A1 VO · A2 music (ducked) · A3 SFX · A4 full master (disabled).
The source of truth is still template + build.py: this export is for human touch-ups on top of the AI cut."""
import argparse, html, json, os, pathlib, re, shutil, subprocess, sys
FPS, W, H = 24, 1080, 1920
ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--caps'); ap.add_argument('--overlay', action='store_true')
ap.add_argument('--name'); ap.add_argument('--edition'); a = ap.parse_args()
suf = f'_{a.edition}' if a.edition else ''
P = pathlib.Path(a.project).resolve(); E = P/f'edit{suf}'; M = E/'media'; M.mkdir(parents=True, exist_ok=True)
name = a.name or P.name + suf.replace('_', '-')
fr = lambda s: int(round(float(s) * FPS))

def probe_dur(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def media(src):  # copy into edit/media (flattened, keeps the name unique) and return the local path
    src = pathlib.Path(src); dst = M/src.name
    if dst.exists() and dst.stat().st_size != src.stat().st_size: dst = M/f'{src.parent.name}_{src.name}'
    if not dst.exists(): shutil.copy2(src, dst)
    return dst

# ---- footage clips from the generated film --------------------------------------------------------------------------------
film = (P/'film/index.html').read_text()
clips = []
for tag in re.findall(r'<video\b[^>]*>', film):
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
    if 'clip' not in at.get('class', '') or 'src' not in at: continue
    clips.append({'id': at.get('id', pathlib.Path(at['src']).stem), 'src': P/'film'/at['src'], 't': float(at.get('data-start', 0)),
                  'd': float(at['data-duration']), 'm': float(at.get('data-media-start', 0))})
clips.sort(key=lambda c: c['t'])
tracks = []   # greedy: a clip goes on the first video track where it does not overlap
for c in clips:
    for tr in tracks:
        if fr(tr[-1]['t'] + tr[-1]['d']) <= fr(c['t']): tr.append(c); break
    else: tracks.append([c])

mix = json.load(open(P/f'mix{suf}.json')) if (P/f'mix{suf}.json').exists() else {}
DUR = float(mix.get('dur') or max((c['t'] + c['d'] for c in clips), default=0))
stems = pathlib.Path(P/(mix['out'].rsplit('.', 1)[0] + '_stems')) if mix.get('out') else None
master = P/mix['out'] if mix.get('out') else None
render = P/f'render/video_noaudio{suf}.mp4'

# ---- graphics overlay with alpha ------------------------------------------------------------------------------------------
overlay = None
if a.overlay:
    css = ('<style id="__edit_overlay__">html,body,#root{background:transparent!important}'
           '#caps,#grain,#vignette,#flash{display:none!important}</style>')
    # the renderer composites <video> frames outside the DOM, so hiding them is not enough: swap each one for an empty div
    # with the same id/class/style, so the template's GSAP (punch-ins, windows) still finds its targets
    novid = re.sub(r'<video\b([^>]*)>\s*</video>', lambda m: '<div' + re.sub(r'\s(src|data-[\w-]+|muted|playsinline)(="[^"]*")?', '', m.group(1)) + '></div>', film)
    (P/'film/_overlay.html').write_text(novid.replace('</head>', css + '</head>', 1))
    out = E/'graphics_alpha.mov'
    env = dict(os.environ, HYPERFRAMES_SKIP_SKILLS='1')
    subprocess.run(['npx', '-y', 'hyperframes@0.8.162', 'render', '-c', '_overlay.html', '--format', 'mov', '-f', str(FPS), '-w', '4', '-o', str(out)],
                   cwd=P/'film', env=env, check=True)
    (P/'film/_overlay.html').unlink(missing_ok=True)
    overlay = out

# ---- FCP7 XML -------------------------------------------------------------------------------------------------------------
fid = 0; seen = {}
def file_el(path, kind):
    global fid
    path = pathlib.Path(path); key = str(path)
    if key in seen: return f'<file id="{seen[key]}"/>'
    fid += 1; seen[key] = f'file-{fid}'; d = fr(probe_dur(path))
    media_el = (f'<video><samplecharacteristics><width>{W}</width><height>{H}</height></samplecharacteristics></video>' if kind == 'v'
                else '<audio><channelcount>2</channelcount><samplecharacteristics><samplerate>48000</samplerate><depth>16</depth></samplecharacteristics></audio>')
    return (f'<file id="{seen[key]}"><name>{html.escape(path.name)}</name><pathurl>{path.resolve().as_uri()}</pathurl>'
            f'<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate><duration>{d}</duration><media>{media_el}</media></file>')

cid = 0
def clipitem(path, kind, start, dur, mstart=0.0, label=None, enabled=True):
    global cid; cid += 1
    s, e, i = fr(start), fr(start) + max(1, fr(dur)), fr(mstart)
    tag = 'clipitem'
    return (f'<{tag} id="clip-{cid}"><name>{html.escape(label or pathlib.Path(path).name)}</name><enabled>{"TRUE" if enabled else "FALSE"}</enabled>'
            f'<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate><start>{s}</start><end>{e}</end><in>{i}</in><out>{i + e - s}</out>'
            f'{file_el(path, kind)}</{tag}>')

vtracks = []
for tr in tracks:
    vtracks.append(''.join(clipitem(media(c['src']), 'v', c['t'], c['d'], c['m'], c['id']) for c in tr))
if overlay: vtracks.append(clipitem(overlay, 'v', 0, DUR, 0, 'GRAFICOS (HyperFrames, alpha)'))
if render.exists(): vtracks.append(clipitem(media(render), 'v', 0, DUR, 0, 'REFERENCIA render completo', enabled=False))
atracks = []
if stems and stems.exists():
    for k, lab in (('vo', 'VOZ ElevenLabs'), ('music', 'MUSICA (ducking)'), ('sfx', 'SFX')):
        f = stems/f'{k}.wav'
        if f.exists():
            atracks.append(clipitem(media(f), 'a', 0, DUR, 0, lab))
if master and master.exists(): atracks.append(clipitem(media(master), 'a', 0, DUR, 0, 'REFERENCIA master', enabled=False))

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="5"><sequence id="seq-1">'
       f'<name>{html.escape(name)}</name><duration>{fr(DUR)}</duration><rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>'
       '<media><video><format><samplecharacteristics>'
       f'<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate><width>{W}</width><height>{H}</height>'
       '<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format>'
       + ''.join(f'<track>{t}</track>' for t in vtracks) + '</video><audio>'
       + ''.join(f'<track>{t}</track>' for t in atracks) + '</audio></media></sequence></xmeml>\n')
(E/f'{name}.xml').write_text(xml)

# ---- captions -> SRT ------------------------------------------------------------------------------------------------------
cap_src = pathlib.Path(a.caps) if a.caps else next((p for p in (P/'film/caps.json', P/'audio/caps.json') if p.exists()), None)
n_caps = 0
if cap_src and cap_src.exists():
    ts = lambda s: f'{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
    caps = json.load(open(cap_src)); lines = []
    for i, c in enumerate(caps, 1):
        txt = ' '.join(w['t'] for w in c['w']); lines.append(f"{i}\n{ts(c['s'])} --> {ts(c.get('x', c['e']))}\n{txt}\n")
    (E/f'{name}.srt').write_text('\n'.join(lines)); n_caps = len(caps)

print(f'ok {E/(name + ".xml")} · {len(clips)} clips on {len(tracks)} video tracks · overlay={"yes" if overlay else "no"} '
      f'· audio tracks={len(atracks)} · captions={n_caps} · {DUR:.2f}s @ {FPS} fps')
