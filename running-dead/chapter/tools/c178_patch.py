# c178: 장갑차 총신 길이 반 · 기관총처럼 — 가는 총열 두 줄 + 냉각 덮개 + 끝에 소염기. 총구 불꽃은 작고 빠르게 번쩍이며 불티가 튄다 (총구 끝에서)
C178_R = [
 ("    const tg = new THREE.Group(); tg.add(tur, brl); car.g.add(tg); car.tkTur = tg; car.tkAim = 0;",
  "    brl.visible = false;   // c178: 긴 총신 대신 기관총\n"
  "    const mg = (w, h, x, z, col, o) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h).rotateX(-Math.PI / 2), carMat(col)); m.position.set(x, 0.004 + o * 0.0005, z); m.renderOrder = -0.435 + o * 0.001; return m; };\n"
  "    const mgs = [mg(0.2, 0.17, 0.33, 0, 0x2a3218, 0), mg(0.3, 0.035, 0.55, -0.035, 0x0b0d07, 1), mg(0.3, 0.035, 0.55, 0.035, 0x0b0d07, 1), mg(0.06, 0.13, 0.7, 0, 0x050604, 2)];   // 냉각 덮개 · 총열 둘 · 소염기\n"
  "    const tg = new THREE.Group(); tg.add(tur, brl, ...mgs); car.g.add(tg); car.tkTur = tg; car.tkAim = 0;"),
 ("    const f1 = puff(car.x + ux * 1.6, 0, car.z + uz * 1.6, 0xfff23a, 1.5, 1.5, 0.07, 0, 0, 0, 0.8);",
  "    const tip = 0.74 * CH_TK_K, mx = car.x + ux * tip, mz = car.z + uz * tip;   // c178: 총구 끝\n"
  "    const f1 = puff(mx, 0, mz, car.burstN % 2 ? 0xffe14d : 0xfff7c0, 0.75, rand(0.85, 1.05), 0.045, 0, 0, 0, 0.9);\n"
  "    for (let k = 0; k < 3; k++) { const a = Math.atan2(uz, ux) + rand(-0.45, 0.45), sp = rand(5, 9); const s = puff(mx, 0.1, mz, 0xffc23a, 0.14, 0.1, rand(0.08, 0.14), Math.cos(a) * sp, 0, Math.sin(a) * sp, 0.95); s.s.material.map = flashTex; s.s.renderOrder = UI - 0.5; s.peak = true; }   // 불티"),
]
