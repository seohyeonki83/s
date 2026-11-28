import pathlib
s = pathlib.Path('c604.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
L = s.split('\n')
r_old = [l for l in L if l.startswith('    rifle: [[')][0]; s_old = [l for l in L if l.startswith('    sniper: [[')][0]
rep(r_old, "    rifle: [[0.0, 0.18, 0.17], [0.18, 0.47, 0.15], [0.47, 0.62, 0.13], [0.62, 0.71, 0.085], [0.69, 0.75, 0.12]],   // c605: 소총 — 짧고 굵고 뭉툭 (개머리 · 몸통 · 손잡이 · 짧은 총열 · 뭉툭한 끝)")
rep(s_old, "    sniper: [[0.0, 0.24, 0.12], [0.24, 0.52, 0.075], [0.22, 0.52, 0.17, 0.0], [0.5, 0.54, 0.2], [0.34, 0.38, 0.05, 0.11], [0.52, 1.13, 0.034], [1.1, 1.21, 0.095]],   // c605: 저격총 — 10% 더 길게 · 굵은 조준경 + 앞 렌즈 고리 · 옆 노리쇠 손잡이 · 아주 가는 긴 총열 · 머즐 브레이크")
pathlib.Path('c605_patch.py').write_text('C605_R = ' + repr(R) + '\n')
print(len(R))
