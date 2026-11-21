# c272: 산성 자폭 — 누르면 고른 동료 머리 위에 산성 아이콘 → 가장 가까운 인간에게 덮치기 속도로 돌진 → 닿으면 터진다
#   (4초 안에 못 닿거나 갈 인간이 없으면 그 자리에서 · 가다가 죽으면 그 자리에서 터진다)
C272_R = [
 ("    explode(best, R);\n    return true;", "    if (CHAPTER) chBombCharge(best, R); else explode(best, R);   // c272: 돌진한 뒤 터진다\n    return true;"),
 ("  function explode(z, R) {",
  """  const chBombTex = (() => { const cv = document.createElement('canvas'); cv.width = cv.height = 96; const g = cv.getContext('2d');
    g.beginPath(); g.arc(48, 48, 44, 0, Math.PI * 2); g.fillStyle = 'rgba(16,24,10,0.85)'; g.fill(); g.lineWidth = 5; g.strokeStyle = '#7ed321'; g.stroke();
    g.beginPath(); g.moveTo(48, 16); g.bezierCurveTo(62, 36, 70, 46, 70, 58); g.arc(48, 58, 22, 0, Math.PI); g.bezierCurveTo(26, 46, 34, 36, 48, 16); g.fillStyle = '#7ed321'; g.fill();
    g.beginPath(); g.arc(40, 60, 6, 0, Math.PI * 2); g.fillStyle = '#d8ff9a'; g.fill(); return new THREE.CanvasTexture(cv); })();
  const chBombBuf = [];
  function chBombCharge(z, R) {                // c272: 자폭할 동료 — 산성 아이콘을 달고 돌진 시작
    if (z.bombing) return;
    if (z.mode === 'pounce') stopPounce(z); if (z.mode === 'bite') endBite(z, false);
    z.bombing = { R, t: 0, tg: null };
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: chBombTex, transparent: true, depthTest: false, depthWrite: false })); s.scale.set(1.1, 1.1, 1); s.renderOrder = UI + 3; scene.add(s); z.bombS = s;
    chBombIcon(z);
  }
  function chBombIcon(z) { if (z.bombS) z.bombS.position.copy(z.foot).addScaledVector(UP, (z.halfH || RADIUS) * 2 + 0.85); }
  function chBombStep(z, dt) {                 // c272: 가장 가까운 인간에게 덮치기 속도로 — 닿으면 터진다
    const B = z.bombing; B.t += dt; chBombIcon(z);
    let t = B.tg;
    if (!t || t.kind !== 'citizen' || t.space !== z.space || !bodies.includes(t)) {
      t = null; let bd = 14;
      for (const c of nearIn(cCells, z.foot.x, z.foot.z, 14, chBombBuf)) { if (c.kind !== 'citizen' || c.space !== z.space) continue; const d = Math.hypot(c.foot.x - z.foot.x, c.foot.z - z.foot.z); if (d < bd) { bd = d; t = c; } }
      B.tg = t;
    }
    if (!t || B.t > 4) { chBombBoom(z); return; }
    const dx = t.foot.x - z.foot.x, dz = t.foot.z - z.foot.z, d = Math.hypot(dx, dz) || 1e-6, v = z.speed * POUNCE;
    if (d - (z.r || BODY) - (t.r || BODY) <= 0.15 + v * dt) { chBombBoom(z); return; }
    z.vel.set(dx / d * v, dz / d * v);
  }
  function chBombBoom(z) {                     // c272: 터진다 (아이콘을 치우고 원래 폭발)
    if (z.bombS) { scene.remove(z.bombS); z.bombS = null; }
    const B = z.bombing; z.bombing = null; if (B) explode(z, B.R);
  }
  function explode(z, R) {"""),
 ("  function updateZombie(z, dt) {\n    if (z.knockT > 0) { knockStep(z, dt); return; }", "  function updateZombie(z, dt) {\n    if (z.knockT > 0) { if (z.bombing) chBombIcon(z); knockStep(z, dt); return; }\n    if (CHAPTER && z.bombing) { chBombStep(z, dt); return; }   // c272: 자폭 돌진 중"),
 ("    if (z.dead) return;\n    z.dead = true;\n", "    if (z.dead) return;\n    if (CHAPTER && z.bombing) { chBombBoom(z); return; }   // c272: 돌진하다 죽으면 그 자리에서 터진다 (터지면서 다시 여기로 온다)\n    z.dead = true;\n"),
]
