import pathlib
s = pathlib.Path('c509.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    obst(LX - 1.1, R1 - 4.6); obst(LX + 1.4, R1 - 4.6); obst(LX - 1.1, R1 - 9.8); obst(LX + 1.4, R1 - 9.8);",
    "    obst(LX - 1.5, R1 - 4.6); obst(LX + 1.8, R1 - 4.6); obst(LX - 1.5, R1 - 9.8); obst(LX + 1.8, R1 - 9.8);   /* c510: 바리케이트 사이를 조금 더 벌림 (2.5 → 3.3) */")
rep("      ['sniper', -1.9, R1 - 13.9], ['soldier', 1.6, R1 - 13.2]]) post(", "      ]) post(   /* c510: 철문 앞 저격수 1 · 군인 1 뺌 */")
pathlib.Path('c510_patch.py').write_text('C510_R = ' + repr(R) + '\n')
print(len(R))
