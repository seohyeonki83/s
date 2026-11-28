import pathlib
s = pathlib.Path('c583.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 샷건 두께 1.5배 · 권총 밝게 · 로봇 기관포
rep("    shotgun: [[0.0, 0.2, 0.14], [0.2, 0.42, 0.13], [0.42, 0.74, 0.1], [0.46, 0.62, 0.15], [0.72, 0.76, 0.12]],  // 샷건 — 굵은 총열 · 펌프 손잡이",
    """    shotgun: [[0.0, 0.2, 0.21], [0.2, 0.42, 0.195], [0.42, 0.74, 0.15], [0.46, 0.62, 0.225], [0.72, 0.76, 0.18]],  // 샷건 — 굵은 총열 · 펌프 손잡이   /* c584: 두께 1.5배 */
    gatling: [[0.08, 0.34, 0.24], [0.34, 0.66, 0.04, -0.065], [0.34, 0.68, 0.04, 0], [0.34, 0.66, 0.04, 0.065], [0.42, 0.47, 0.2], [0.62, 0.67, 0.2]],   // c584: 사각 로봇 기관포 — 몸통 · 총신 3개 · 고리 2개""")
rep("  function chGunShape(c, k) {\n    if (c.aimGun) c.mesh.remove(c.aimGun);\n    const g = new THREE.Group(); let i = 0;\n    for (const [a, b, w] of CH_GUN_SHAPE[k]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(b - a, w).translate((a + b) / 2 + 0.02, 0, 0), chGunMat);",
    "  const chPistolMat = new THREE.MeshBasicMaterial({ color: 0x6b7480, transparent: true, depthTest: false, depthWrite: false }), chGatMat = new THREE.MeshBasicMaterial({ color: 0x2a2f35, transparent: true, depthTest: false, depthWrite: false });   /* c584: 권총은 밝은 회색 */\n  function chGunShape(c, k) {\n    if (c.aimGun) c.mesh.remove(c.aimGun);\n    const g = new THREE.Group(); let i = 0; const mat = k === 'pistol' ? chPistolMat : k === 'gatling' ? chGatMat : chGunMat;\n    for (const [a, b, w, y = 0] of CH_GUN_SHAPE[k]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(b - a, w).translate((a + b) / 2 + 0.02, y, 0), mat);")
# 사각 로봇: 모서리 둥글게 · 크기 10% 줄임 · 기관포
rep("chRobotAny = true; c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 1.6;   /* c554: 사각 로봇 체력 20% 줄임 (2 → 1.6배) */ c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5);",
    "chRobotAny = true; c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 1.6;   /* c554: 사각 로봇 체력 20% 줄임 (2 → 1.6배) */ c.r = BODY * 1.35; c.halfH = RADIUS * 1.35; c.mesh.scale.setScalar(1.35);   /* c584: 크기 10% 줄임 (1.5 → 1.35) */")
rep("    c.mesh.geometry = chSqGeo; c.mesh.material.color.setHex(0x2f5a1a); c.baseCol = 0x2f5a1a;", "    c.mesh.geometry = chRSqGeo; c.mesh.material.color.setHex(0x2f5a1a); c.baseCol = 0x2f5a1a;   /* c584: 모서리 살짝 뭉툭 */")
rep("chAddGun(c, 0.55, 0.17, 0x2a2f35);\n  }", "chGunShape(c, 'gatling');   /* c584: 기관포 */\n  }")
rep("  const chOctGeo = ", """  const chRSqGeo = (() => { const h = RADIUS * 0.9, r = 0.13, S = new THREE.Shape(); S.moveTo(-h + r, -h); S.lineTo(h - r, -h); S.quadraticCurveTo(h, -h, h, -h + r); S.lineTo(h, h - r); S.quadraticCurveTo(h, h, h - r, h); S.lineTo(-h + r, h); S.quadraticCurveTo(-h, h, -h, h - r); S.lineTo(-h, -h + r); S.quadraticCurveTo(-h, -h, -h + r, -h); return new THREE.ShapeGeometry(S, 6); })();   // c584: 둥근 모서리 사각
  const chOctGeo = """)
# 보스 로봇은 그대로 (각진 몸 · 쌍포)
rep("    c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5); c.mesh.material.color.setHex(0x7a1212); c.baseCol = 0x7a1212;",
    "    c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5); c.mesh.material.color.setHex(0x7a1212); c.baseCol = 0x7a1212; c.mesh.geometry = chSqGeo; if (c.aimGun) { c.mesh.remove(c.aimGun); c.aimGun = null; }   /* c584: 보스는 각진 몸 · 쌍포만 */")
pathlib.Path('c584_patch.py').write_text('C584_R = ' + repr(R) + '\n')
print(len(R))
