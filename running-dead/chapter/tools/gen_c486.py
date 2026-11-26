import pathlib
s = pathlib.Path('c485.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("    const want = !B ? null : B.id === 'monster' ? 0xff2a2a : chAbsK === 'taser' ? 0xffe14a : chAbsK === 'bomb' ? bc : 0xdfe6f0;", "    const want = null; void bc;   // c486: 괴물은 뿔만 — 발광 테두리 없음")
rep("g.position.z = 0.015; z.mesh.add(g); z.brHorn = g; }", "g.position.z = 0.015; g.scale.set(1.5, 1.5, 1); g.position.y = -0.37 * 0.5;   /* c486: 뿔 1.5배 (뿌리 자리는 그대로) */ z.mesh.add(g); z.brHorn = g; }")
rep("  const CH_MY_FORCE = 5;", "  const CH_MY_FORCE = 6;   /* c486: 5 → 6 */")
pathlib.Path('c486_patch.py').write_text('C486_R = ' + repr(R) + '\n')
