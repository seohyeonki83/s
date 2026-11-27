import pathlib
s = pathlib.Path('c555.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  function chPopulate() {\n",
    """  function chOrange10() {                      // c556: 맵 전체 주황(건물 안 포함) 10%를 하양으로
    const L = bodies.filter((b) => b.kind === 'citizen' && b.attacker && !b.vig && !b.police && !b.boss && !b.robot && !b.fixed && b !== me);
    for (let i = L.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [L[i], L[j]] = [L[j], L[i]]; }
    for (const b of L.slice(0, Math.round(L.length * 0.1))) chDemote(b, '');
  }
  function chPopulate() {
""")
rep("if (!CH_TUT) chCull15();", "if (!CH_TUT) { chCull15(); chOrange10(); }   /* c556 */")
pathlib.Path('c556_patch.py').write_text('C556_R = ' + repr(R) + '\n')
print(len(R))
