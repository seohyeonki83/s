import pathlib
s = pathlib.Path('c524.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("sf.loot = 'revive'; sf.dud = false; }   // c302: 첫 방 문을 막고 선 금고 — 늘 변이 줄기세포",
    "sf.loot = 'revive'; sf.dud = false; if (D.obj && !D.obj.dead) { const o = D.obj, B = o.B; o.dead = true; if (o.hpBar) o.hpBar.visible = false; const i = walls.indexOf(o.seg), j = B.walls.indexOf(o.seg); if (i >= 0) walls.splice(i, 1); if (j >= 0) B.walls.splice(j, 1); if (!B.doors.includes(o.L)) B.doors.push(o.L); rebuildSight(B); o.mesh.visible = false; o.gap.visible = true; } }   // c302: 첫 방 문을 막고 선 금고 — 늘 변이 줄기세포 · c525: 그 뒤 문은 처음부터 뚫려 있다")
pathlib.Path('c525_patch.py').write_text('C525_R = ' + repr(R) + '\n')
print(len(R))
