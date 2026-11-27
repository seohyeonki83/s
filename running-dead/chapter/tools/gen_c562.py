import pathlib
s = pathlib.Path('c561.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("c.mesh.geometry = chSqGeo; c.mesh.material.color.setHex(0x6f7a86);", "c.mesh.geometry = chSqGeo; c.mesh.material.color.setHex(0x2f5a1a);   /* c562: 회색 → 진한 녹색 (군인 0x556b2f보다 진하게) */")
rep("debris(c.foot.x, c.foot.z, 12, [0x6f7a86, 0x2a2f35, 0x151515]", "debris(c.foot.x, c.foot.z, 12, [0x2f5a1a, 0x2a2f35, 0x151515]")
pathlib.Path('c562_patch.py').write_text('C562_R = ' + repr(R) + '\n')
print(len(R))
