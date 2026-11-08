"""How faithfully a generated clip kept our VO: envelope correlation + best offset.
usage: audiomatch.py clip.mp4 seg.mp3"""
import subprocess, numpy as np, sys
def ld(f):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(p, np.int16).astype(float) / 32768
def env(x): k = 80; m = len(x) // k; return np.sqrt((x[:m * k].reshape(m, k) ** 2).mean(1))
a, b = env(ld(sys.argv[1])), env(ld(sys.argv[2])); L = len(b) - 100; best = (-2, 0)
for lag in range(0, 200):
    if lag + L > len(a): break
    best = max(best, (np.corrcoef(a[lag:lag + L], b[:L])[0, 1], lag))
print(f'{sys.argv[1].split("/")[-1]}: audio r={best[0]:.3f} offset={best[1]*0.005:+.3f}s')
