import pathlib
s = pathlib.Path('c515.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 첫 방(좀비 수조) — 수조 앞 경찰 1 뺌
rep("    { const q = man(L2, 'police', L2.x0 + 6.55, L2.z0 + 5.7, 0.4); q.post = q.area; enterNormal(q); }", "    /* c516: 수조 앞 경찰 뺌 */")
# 주차장 첫 줄 진지 — 경찰 9 → 7 · 군인 4 → 3 (13 → 10, 약 20%)
rep("if (k === 3) return; put2('police', x + J(0.6), z - 1.7 - Math.random() * 0.6, 0.5); if (k % 2 || k === 6) return;",
    "if (k === 3) return; if (k !== 5) put2('police', x + J(0.6), z - 1.7 - Math.random() * 0.6, 0.5); if (k % 2 || k === 6 || k === 2) return;   /* c516: 병력 20% 줄임 — 경찰 9 → 7 */")
rep("      for (let k = 0; k < 4; k++) put2('soldier',", "      for (let k = 0; k < 3; k++) put2('soldier',   /* c516: 군인 4 → 3 */")
pathlib.Path('c516_patch.py').write_text('C516_R = ' + repr(R) + '\n')
print(len(R))
