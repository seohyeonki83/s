import pathlib
s = pathlib.Path('c586.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("function chAddGun(c, L, W, col) { if (col === 0x1a1d21 && c.turret) { chGunShape(c, 'tgat'); return; }",
    "function chAddGun(c, L, W, col) { if (col === 0x1a1d21 && c.turret) { c.mesh.geometry = chTurGeo; if (!c.turDome) { const d = new THREE.Mesh(chTurDome, chTurDomeMat); d.position.z = 0.006; d.renderOrder = 0.5; c.mesh.add(d); c.turDome = d; } chGunShape(c, 'tgat'); return; }   /* c587: 터렛 = 동그란 몸 (사각과 같은 폭) + 가운데 포탑 + 기관포 */")
rep("  const chOctGeo = ", "  const chTurGeo = new THREE.CircleGeometry(RADIUS * 0.9, 40), chTurDome = new THREE.CircleGeometry(RADIUS * 0.52, 32), chTurDomeMat = new THREE.MeshBasicMaterial({ color: 0x5f6875, transparent: true, depthTest: false, depthWrite: false });   // c587\n  const chOctGeo = ")
pathlib.Path('c587_patch.py').write_text('C587_R = ' + repr(R) + '\n')
print(len(R))
