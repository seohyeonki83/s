import pathlib
s = pathlib.Path('c546.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
L = s.split('\n'); i = next(k for k, l in enumerate(L) if l.startswith('  function chDiscTick(dt) {'))
old = '\n'.join(L[i:i + 14]); assert old.rstrip().endswith('}') and '그대로 남은 수' in old, old[-60:]
rep(old, """  function chDiscTick(dt) {                    // c547: 처음 발견 보정 — 빨강 · 거리 경찰을 처음 볼 때 70% 확률로 바꾼다 (35% 노랑 · 35% 하양). 바뀐 빨강 2명 · 바뀐 경찰 2명이 되면 각각 끝. 주황 · 노랑은 안 바꾼다
    if (chDiscR >= CH_DISC_N && chDiscP >= CH_DISC_N) return;
    if ((chDiscT -= dt) > 0) return; chDiscT = 0.1;
    for (const c of bodies) {
      if (c.kind !== 'citizen' || c.disc || c.boss || !(c.hp > 0)) continue;
      const red = c.attacker && c.vig && chDiscR < CH_DISC_N, cop = c.police && !c.military && c.street && chDiscP < CH_DISC_N;
      if (!red && !cop) continue;
      if (!(iSee(c) || zSeen(c))) continue;
      c.disc = true;
      const r = Math.random(); if (r < 0.7) { chDemote(c, r < 0.35 ? 'guard' : ''); if (red) chDiscR++; else chDiscP++; }
    }""")
rep("  const CH_DISC_N = 4, CH_DISC_O = 2, CH_DISC_Y = 2;", "  const CH_DISC_N = 2;   /* c547: 바뀐 빨강 2 · 바뀐 경찰 2 (각각) */")
pathlib.Path('c547_patch.py').write_text('C547_R = ' + repr(R) + '\n')
print(len(R))
