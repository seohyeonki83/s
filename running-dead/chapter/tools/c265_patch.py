# c265: 모든 도트 피해에 숫자 — 산성 자폭(사람·보스) · 산성 폭발(사람·보스). 숫자는 실제 피해 (산성 강도 포함)
C265_R = [
 ("""      if (c.mesh.visible) {                   // 아주 작은 -1 이 떠올랐다 사라진다
        const f = puff(c.foot.x + 0.6, 1.3, c.foot.z, 0xffffff, 0.5, 0.5, 0.75, 0, 0.9, 0, 1);   // v294: 커진 만큼 옆으로
        f.s.material.map = minusTex; f.s.scale.set(1.0, 0.5, 1); f.fixedScale = true; f.peak = true; f.s.renderOrder = UI - 1;   // v294: 2배 (0.5×0.25 → 1×0.5)
      }""",
  """      if (c.mesh.visible) chDotPop(c.foot.x + 0.6, c.foot.z, 2 + chAcidB());   // c265: 실제 피해 숫자"""),
 ("  function gooTick(dt) {",
  """  const chDotTexC = new Map();
  function chDotTex(n) {                       // c265: '-n' 글자 (숫자마다 한 번만 만든다)
    let t = chDotTexC.get(n); if (t) return t;
    const cv = document.createElement('canvas'); cv.width = 128; cv.height = 64; const g = cv.getContext('2d'); g.font = '800 52px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineWidth = 10; g.strokeStyle = 'rgba(0,0,0,0.75)'; g.strokeText('-' + n, 64, 34); g.fillStyle = '#ff4a3d'; g.fillText('-' + n, 64, 34);
    t = new THREE.CanvasTexture(cv); chDotTexC.set(n, t); return t;
  }
  function chDotPop(x, z, n, y = 1.3) {        // c265: 도트 숫자가 떠올랐다 사라진다
    const f = puff(x, y, z, 0xffffff, 0.5, 0.5, 0.75, 0, 0.9, 0, 1);
    f.s.material.map = chDotTex(n); f.s.scale.set(1.0, 0.5, 1); f.fixedScale = true; f.peak = true; f.s.renderOrder = UI - 1;
  }
  function gooTick(dt) {"""),
 ("      if (car) { const o = e.obj; if (o && o.hp > d) o.hp -= d; continue; }", "      if (car) { const o = e.obj; if (o && o.hp > d) { o.hp -= d; chDotPop(e.x + 0.9, e.z, d, 2.2); } continue; }   // c265"),
 ("      e.hp = Math.max(0, e.hp - d);\n      if (e.hp <= 0 && !e.police && e.state !== 'held') enterPanic(e, null, true);", "      e.hp = Math.max(0, e.hp - d); if (e.mesh.visible) chDotPop(e.foot.x + 0.6, e.foot.z, d);   // c265\n      if (e.hp <= 0 && !e.police && e.state !== 'held') enterPanic(e, null, true);"),
 ("const gd = 2 + chAcidB(); if (o && o.hp > gd) o.hp -= gd; }   // c259", "const gd = 2 + chAcidB(); if (o && o.hp > gd) { o.hp -= gd; chDotPop(car.x + 0.9, car.z, gd, 2.2); } }   // c259 · c265"),
]
