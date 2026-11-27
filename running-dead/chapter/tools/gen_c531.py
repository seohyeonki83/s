import pathlib
s = pathlib.Path('c530.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    for (const m of me.hpBar.children) m.renderOrder += UI_ME + 50 - UI;", "    for (const m of me.hpBar.children) m.renderOrder += UI_ME + 50 - UI;\n    if (CHAPTER) me.hpBar.children[0].geometry = new THREE.PlaneGeometry(GAUGE_W + GAUGE_PAD, GAUGE_H + GAUGE_PAD);   // c531: 내 체력바 검은 테두리만 1.5배 두껍게 (안쪽 초록 막대는 그대로)")
pathlib.Path('c531_patch.py').write_text('C531_R = ' + repr(R) + '\n')
print(len(R))
