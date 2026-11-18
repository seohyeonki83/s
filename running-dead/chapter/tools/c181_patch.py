# c181: 장갑차 총구 불꽃 · 총알 선이 실제 기관총 끝에서 나온다 — 포탑이 보는 방향 기준, 화면 위로 띄우던 것(사람 몸 높이용)은 뺀다
C181_R = [
 ("    const tip = 0.74 * CH_TK_K, mx = car.x + ux * tip, mz = car.z + uz * tip;   // c178: 총구 끝",
  "    const ta = car.tkTur ? car.h - car.tkAim : Math.atan2(uz, ux), tip = 0.73 * CH_TK_K, mx = car.x + Math.cos(ta) * tip, mz = car.z + Math.sin(ta) * tip;   // c181: 기관총 끝 (포탑이 보는 쪽)\n    car.tipX = mx; car.tipZ = mz;"),
 ("const a = Math.atan2(uz, ux) + rand(-0.45, 0.45), sp = rand(5, 9); const s = puff(mx, 0.1, mz,", "const a = ta + rand(-0.45, 0.45), sp = rand(5, 9); const s = puff(mx, 0.1, mz,"),
 ("    f1.s.material.map = flashTex; f1.s.position.addScaledVector(UP, RADIUS); f1.s.renderOrder = UI - 0.5; f1.peak = true; f1.blink = true;\n    const f2 = puff(z.foot.x, 0.4, z.foot.z, 0xffa53a, 0.9, CH_TK_SPLASH * 2,",
  "    f1.s.material.map = flashTex; f1.s.renderOrder = UI - 0.5; f1.peak = true; f1.blink = true;   /* c181: 바닥 높이 그대로 (장갑차는 납작하다) */\n    const f2 = puff(z.foot.x, 0.4, z.foot.z, 0xffa53a, 0.9, CH_TK_SPLASH * 2,"),
 ("""    const dx = car.shotX - car.x, dz = car.shotZ - car.z, L = Math.hypot(dx, dz) || 1e-3;
    tr.visible = true;
    tr.position.set(car.x + dx / 2, 0, car.z + dz / 2).addScaledVector(UP, RADIUS);
    tr.rotation.y = -Math.atan2(dz, dx);
    tr.scale.set(L, 1, 1.8);""", """    const sx = car.tipX ?? car.x, sz = car.tipZ ?? car.z;   // c181: 기관총 끝 → 맞은 몸 가운데
    chTkS.set(sx, 0.02, sz); chTkE.set(car.shotX, 0, car.shotZ).addScaledVector(UP, RADIUS); chTkE.sub(chTkS); const L = chTkE.length() || 1e-3;
    tr.visible = true;
    tr.position.copy(chTkS).addScaledVector(chTkE, 0.5);
    tr.quaternion.setFromUnitVectors(chTkX, chTkE.normalize());
    tr.scale.set(L, 1, 1.8);"""),
 ("  function chTankDraw(dt) {", "  const chTkS = new THREE.Vector3(), chTkE = new THREE.Vector3(), chTkX = new THREE.Vector3(1, 0, 0);\n  function chTankDraw(dt) {"),
]
