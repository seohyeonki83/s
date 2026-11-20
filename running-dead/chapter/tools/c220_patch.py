# c220: 처음 발견하는 빨강 5명 · 경찰 2명 (나나 동료 시야에 처음 들어온 순간) — 한 명마다 30% 노랑 · 30% 하양 · 40% 그대로
C220_R = [
 ("  function chSfTick(dt) {",
  """  let chDiscR = 0, chDiscP = 0, chDiscT = 0;
  function chDemote(c, to) {                   // c220: 그 자리에서 노랑('guard') 또는 하양('')으로
    if (c.police) { c.police = false; c.military = false; if (c.tracer) { scene.remove(c.tracer); c.tracer = null; } c.calls = []; c.heading = null; c.onDuty = false; }
    c.attacker = false; c.vig = false; c.guard = to === 'guard';
    if (c.stick) { c.mesh.remove(c.stick); c.stick = null; }
    c.mesh.material.color.setHex(COLOR[to === 'guard' ? 'guard' : 'citizen']);
    if (!c.soft) { c.soft = true; c.sight *= CH_SOFT_SIGHT; }
    if (to === 'guard') { c.hp = c.maxHp = GUARD_HP * 0.95 * 0.9 * 0.95; if (!c.hpBar) addHpBar(c, hpFoeMat); }
    else { c.hp = c.maxHp = 0; if (c.hpBar) { scene.remove(c.hpBar); c.hpBar = null; } }
    c.hpDisp = c.hp; enterNormal(c);
  }
  function chDiscTick(dt) {                    // c220: 처음 발견 — 나·동료 시야에 처음 들어온 빨강 5명 · 경찰 2명까지
    if (chDiscR >= 5 && chDiscP >= 2) return;
    if ((chDiscT -= dt) > 0) return; chDiscT = 0.1;
    for (const c of bodies) {
      if (c.kind !== 'citizen' || c.disc || c.boss || !(c.hp > 0)) continue;
      const red = c.attacker && c.vig, cop = c.police && !c.military;
      if (!(red && chDiscR < 5) && !(cop && chDiscP < 2)) continue;
      if (!(iSee(c) || zSeen(c))) continue;
      c.disc = true; if (red) chDiscR++; else chDiscP++;
      const r = Math.random(); if (r < 0.3) chDemote(c, 'guard'); else if (r < 0.6) chDemote(c, '');
      if (chDiscR >= 5 && chDiscP >= 2) return;
    }
  }
  function chSfTick(dt) {
    chDiscTick(dt);   // c220"""),
 ("    chBanner.length = 0;", "    chBanner.length = 0; chDiscR = chDiscP = 0; chDiscT = 0;   // c220"),
]
