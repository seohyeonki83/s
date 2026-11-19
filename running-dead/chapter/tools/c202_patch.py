# c202: 보스 난사 — 총알이 떨어진 자리마다 세게 튀는 이펙트 (번쩍 + 불티 튐 + 바닥 먼지) · 한 걸음에 2곳까지
C202_R = [
 ("    let ex = 0, ez = 0;\n    while (car.spAcc >= 1) {", "    let ex = 0, ez = 0; const ends = [];\n    while (car.spAcc >= 1) {"),
 ("      if (!hit) { const da = Math.hypot(car.spAim.x - mx, car.spAim.z - mz) + 1.5; if (da < ht) { ex = mx + ux * da; ez = mz + uz * da; } continue; }",
  "      if (!hit) { const da = Math.hypot(car.spAim.x - mx, car.spAim.z - mz) + 1.5; if (da < ht) { ex = mx + ux * da; ez = mz + uz * da; } ends.push([ex, ez, false, ux, uz]); continue; }\n      ends.push([ex, ez, true, ux, uz]);"),
 ("      if (Math.random() < 0.35) { const f2 = puff(ex, 0.4, ez, 0xffa53a, 0.35, 0.6, 0.08, 0, 0, 0, 0.5); f2.s.material.map = flashTex; f2.s.renderOrder = UI - 0.5; f2.peak = true; }\n    }\n",
  "    }\n    if (ends.length) chSpImpact(...ends[ends.length - 1]); if (ends.length > 1) chSpImpact(...ends[0]);   // c202\n"),
 ("  function chTankSpray(car, dt) {",
  """  function chSpImpact(x, z, hit, ux, uz) {      // c202: 총알 튀는 자리 — 번쩍 · 불티가 사방으로 (주로 맞은 쪽 반대로) · 먼지
    const f = puff(x, 0.3, z, hit ? 0xfff2b0 : 0xffe08a, 0.55, rand(1.0, 1.35), 0.07, 0, 0, 0, 1); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; f.blink = true;
    for (let k = 0; k < 6; k++) {
      const back = Math.random() < 0.6, a = back ? Math.atan2(-uz, -ux) + rand(-1.1, 1.1) : Math.random() * Math.PI * 2, sp = rand(5, 11);
      const s = puff(x, 0.25, z, Math.random() < 0.5 ? 0xffc23a : 0xfff7c0, rand(0.12, 0.2), 0.05, rand(0.1, 0.2), Math.cos(a) * sp, rand(1, 3), Math.sin(a) * sp, 1);
      s.s.material.map = flashTex; s.s.renderOrder = UI - 0.5; s.peak = true;
    }
    if (Math.random() < (hit ? 0.4 : 0.8)) { const d = puff(x + rand(-0.15, 0.15), 0.1, z + rand(-0.15, 0.15), Math.random() < 0.5 ? 0x8a8a84 : 0x6a6a64, 0.3, rand(0.9, 1.3), rand(0.3, 0.45), rand(-0.6, 0.6), rand(0.4, 0.9), rand(-0.6, 0.6), 0.55); d.s.renderOrder = -0.4; }
  }
  function chTankSpray(car, dt) {"""),
]
