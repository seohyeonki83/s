import pathlib
s = pathlib.Path('c582.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("function chAddGun(c, L, W, col) { const g = ", "function chAddGun(c, L, W, col) { if (c.aimGun) c.mesh.remove(c.aimGun);   /* c583: 있던 총은 바꿔 낀다 */ const g = ")
rep("  function chMakeSg(c) {", """  const CH_GUN_SHAPE = {   // c583: 위에서 본 총 — [앞쪽 시작, 앞쪽 끝, 폭] 조각들 (몸 가운데 = 0, 몸 반지름 0.5)
    pistol: [[0.2, 0.46, 0.1], [0.44, 0.5, 0.06]],                                                     // 권총 — 아주 짧게
    rifle: [[0.0, 0.22, 0.13], [0.22, 0.56, 0.1], [0.3, 0.42, 0.14], [0.56, 0.8, 0.05], [0.78, 0.84, 0.08]],   // 소총 — 개머리 · 몸통 · 손잡이 · 총열 · 소염기
    sniper: [[0.0, 0.2, 0.13], [0.2, 0.52, 0.09], [0.24, 0.46, 0.15], [0.52, 1.02, 0.045], [0.98, 1.1, 0.1]],  // 저격총 — 길쭉 · 가운데 조준경 · 끝에 머즐 브레이크
    shotgun: [[0.0, 0.2, 0.14], [0.2, 0.42, 0.13], [0.42, 0.74, 0.1], [0.46, 0.62, 0.15], [0.72, 0.76, 0.12]],  // 샷건 — 굵은 총열 · 펌프 손잡이
  };
  function chGunShape(c, k) {
    if (c.aimGun) c.mesh.remove(c.aimGun);
    const g = new THREE.Group(); let i = 0;
    for (const [a, b, w] of CH_GUN_SHAPE[k]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(b - a, w).translate((a + b) / 2 + 0.02, 0, 0), chGunMat); m.renderOrder = 1 + 0.001 * i++; g.add(m); }
    g.position.z = 0.012; c.mesh.add(g); c.aimGun = g;
  }
  const chOctGeo = new THREE.CircleGeometry(RADIUS * 1.04, 8, Math.PI / 8);   // c583: 샷건 경찰 — 팔각형 몸
  function chMakeSg(c) {""")
rep("c.sg = true; c.hp = c.maxHp = c.maxHp * CH_SG_HPK; chAddGun(c, 0.62, 0.15);", "c.sg = true; c.hp = c.maxHp = c.maxHp * CH_SG_HPK; chGunShape(c, 'shotgun'); c.mesh.geometry = chOctGeo;   /* c583: 샷건 모양 · 팔각형 */")
rep("    if (robo) chMakeRobot(c); if (chSfTag) c.sfw = chSfTag;", "    if (CHAPTER && c.police && !c.aimGun) chGunShape(c, c.sniper ? 'sniper' : c.soldier ? 'rifle' : 'pistol');   /* c583: 경찰 권총 · 군인 소총 · 저격수 저격총 */\n    if (robo) chMakeRobot(c); if (chSfTag) c.sfw = chSfTag;")
rep("    c.attacker = false; c.vig = false; c.guard = to === 'guard';\n    if (c.stick) { c.mesh.remove(c.stick); c.stick = null; }", "    c.attacker = false; c.vig = false; c.guard = to === 'guard';\n    if (c.stick) { c.mesh.remove(c.stick); c.stick = null; }\n    if (c.aimGun) { c.mesh.remove(c.aimGun); c.aimGun = null; } if (c.sg) { c.sg = false; c.baseCol = undefined; c.mesh.geometry = circleGeo; }   /* c583: 하양 · 노랑으로 바뀌면 총도 내려놓는다 */")
pathlib.Path('c583_patch.py').write_text('C583_R = ' + repr(R) + '\n')
print(len(R))
