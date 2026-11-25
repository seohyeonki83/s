# c448: 괴물 좀비 — 머리에 뿔 두 개 · 괴물 히드라 토사물에 빨간 덩어리가 섞여 날아간다 (흡수는 그대로)
src = open('c447.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    if (want === null) { if (z.brHalo) { z.mesh.remove(z.brHalo); z.brHalo.material.dispose(); z.brHalo = null; } return; }", """    const horn = !!B && B.id === 'monster';   // c448: 괴물 = 뿔
    if (horn && !z.brHorn) { const g = new THREE.Group(); for (const sd of [-1, 1]) { const sh = new THREE.Shape(); sh.moveTo(sd * 0.12, 0.36); sh.lineTo(sd * 0.32, 0.38); sh.lineTo(sd * 0.36, 0.78); sh.lineTo(sd * 0.27, 0.6); sh.closePath(); const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), chHornMat); m.renderOrder = 1; g.add(m); } g.position.z = 0.015; z.mesh.add(g); z.brHorn = g; }
    else if (!horn && z.brHorn) { z.mesh.remove(z.brHorn); z.brHorn = null; }
    if (want === null) { if (z.brHalo) { z.mesh.remove(z.brHalo); z.brHalo.material.dispose(); z.brHalo = null; } return; }""")
rep("  function chMutLook(z) {", "  const chHornMat = new THREE.MeshBasicMaterial({ color: 0xb3121b, transparent: true, depthTest: false, depthWrite: false, side: THREE.DoubleSide });   // c448: 괴물 뿔\n  function chMutLook(z) {")
rep("    scene.add(s);\n    spits.push({ s, z, t, dmg: z === me ? zDamage(z) : zDamage(z) * 4, dT: 0 });", "    scene.add(s);\n    let rs = null; if (CHAPTER && chMonster(z)) { rs = new THREE.Sprite(new THREE.SpriteMaterial({ map: flashTex, color: 0xff2a2a, transparent: true, depthTest: false, depthWrite: false })); rs.scale.setScalar(0.62); rs.renderOrder = UI_ME - 0.9; rs.position.copy(s.position); scene.add(rs); }   // c448: 괴물 히드라 — 빨간 덩어리가 섞인다\n    spits.push({ s, z, t, dmg: z === me ? zDamage(z) : zDamage(z) * 4, dT: 0, rs });")
rep("        scene.remove(p.s); p.s.material.dispose(); spits.splice(i, 1);", "        if (p.rs) { if (live) for (let k = 0; k < 6; k++) { const a = Math.random() * 6.28, sp = rand(1.4, 3); puff(p.s.position.x, 0.5, p.s.position.z, k % 2 ? 0xff3a3a : 0xb3121b, rand(0.12, 0.2), rand(0.05, 0.1), rand(0.25, 0.4), Math.cos(a) * sp, rand(0.5, 1.2), Math.sin(a) * sp, 0.9); } scene.remove(p.rs); p.rs.material.dispose(); }   // c448\n        scene.remove(p.s); p.s.material.dispose(); spits.splice(i, 1);")
rep("      p.s.position.addScaledVector(sV2, step / d);", "      p.s.position.addScaledVector(sV2, step / d); if (p.rs) p.rs.position.copy(p.s.position);   // c448")
rep("puff(p.s.position.x, p.s.position.y, p.s.position.z, 0x8fe84a,", "puff(p.s.position.x, p.s.position.y, p.s.position.z, p.rs && Math.random() < 0.5 ? 0xff3a3a : 0x8fe84a,")
open('c448_patch.py', 'w').write("# c448: 괴물 뿔 · 괴물 히드라 빨간 토사물\nC448_R = " + repr(R) + "\n")
