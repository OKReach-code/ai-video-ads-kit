"""Final mix + master: OUR ElevenLabs VO (never the video model's audio) + ducked music + SFX -> -14 LUFS (2 passes) -> mux.
usage: mix.py mix.json
mix.json = {"video": "render/video_noaudio.mp4", "out": "final.mp4", "dur": 44.0,
            "vo": "audio/vo.wav", "vo_delay": 0.15,
            "music": "audio/music.mp3", "music_gain": 0.5, "music_start": 0.0,
            "music_af": "acompressor=...",                                  # optional: ffmpeg filters on the music only (e.g. tame a very dynamic track)
            "sfx": [["audio/sfx/whoosh.mp3", 4.6, 0.35], ...]}      # [file, film second, gain]  · no SFX on top of a syllable
Also writes <out>_stems/{vo,music,sfx}.wav (same master gain, already ducked/placed, full film length) so a human editor
can rebalance the mix in Premiere/DaVinci (see tools/export_edit.py)."""
import json, re, subprocess, sys, pathlib
c = json.load(open(sys.argv[1])); DUR = c['dur']
inp = ['-i', c['vo'], '-ss', str(c.get('music_start', 0)), '-i', c['music']]
for f, _, _ in c['sfx']: inp += ['-i', f]
fc = [f"[0:a]aresample=48000,adelay={int(c.get('vo_delay',0)*1000)}:all=1,highpass=f=80,equalizer=f=3500:t=q:w=1:g=2,"
      f"acompressor=threshold=-20dB:ratio=3:attack=5:release=80,apad=whole_dur={DUR},atrim=0:{DUR},asplit=3[vo][key][vost]",
      f"[1:a]aresample=48000,atrim=0:{DUR},{c['music_af'] + ',' if c.get('music_af') else ''}volume={c.get('music_gain',0.5)},afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-1.2}:d=1.2[mus0]",
      f"[mus0][key]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350:makeup=1,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[mus][musst]"]
names = []
for i, (f, t, g) in enumerate(c['sfx']):
    fc.append(f"[{i+2}:a]aresample=48000,adelay={int(t*1000)}:all=1,volume={g}[s{i}]"); names.append(f"[s{i}]")
if names: fc.append(''.join(names) + f"amix=inputs={len(names)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[sfx][sfxst]")
else: fc.append(f"anullsrc=r=48000:cl=mono,atrim=0:{DUR},asplit=2[sfx][sfxst]")
fc.append(f"[vo][mus][sfx]amix=inputs=3:normalize=0:duration=longest,apad=whole_dur={DUR},atrim=0:{DUR},alimiter=limit=0.89:attack=3:release=60[out]")
base = c['out'].rsplit('.', 1)[0]
wav, tmp = base + '_mix.wav', base + '_mixn.wav'
stems = pathlib.Path(base + '_stems'); stems.mkdir(parents=True, exist_ok=True)
raw = {k: str(stems/f'_{k}_raw.wav') for k in ('vo', 'music', 'sfx')}
subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[out]','-ac','2',wav,
                '-map','[vost]','-ac','2',raw['vo'],'-map','[musst]','-ac','2',raw['music'],'-map','[sfxst]','-ac','2',raw['sfx']], check=True)
lufs = lambda f: float(re.findall(r'I:\s+(-?[\d.]+) LUFS', subprocess.run(['ffmpeg','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr)[-1])
I = lufs(wav); g = -14.3 - I
subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-af',f'volume={g:.2f}dB,alimiter=limit=0.79:attack=2:release=50:level=disabled',tmp], check=True)
print(f'pass1 {I} LUFS, gain {g:+.2f} dB -> final {lufs(tmp)} LUFS')
for k, f in raw.items():   # same master gain as the mix (no limiter): vo + music + sfx ~= master
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-af',f'volume={g:.2f}dB',str(stems/f'{k}.wav')], check=True); pathlib.Path(f).unlink()
subprocess.run(['ffmpeg','-v','error','-y','-i',c['video'],'-i',tmp,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k',
                '-shortest','-movflags','+faststart',c['out']], check=True)
print('ok', c['out'], '· stems in', stems)
# Regla (docs/REGLAS.md): la música va ≈ 19 dB por debajo de la voz; aviso si queda a menos de 17 dB
dv, dm = lufs(str(stems/'vo.wav')), lufs(str(stems/'music.wav'))
print(f'voz {dv} LUFS · música {dm} LUFS · música {dv - dm:.1f} dB bajo la voz' +
      ('' if dv - dm >= 17 else '  ->  AVISO: MÚSICA DEMASIADO ALTA (objetivo ≈ 19 dB bajo la voz): baja music_gain'))
