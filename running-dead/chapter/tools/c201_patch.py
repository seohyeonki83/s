# c201: 보스 공격 = 난사 — 한 발 = 군인 한 발의 10분의 1 · 연사 = 군인의 10배 (초당 약 52발)
#   · 15초 주기: 난사 7초 · 쉬기 8초를 각각 두 번으로 (초 단위 랜덤) — 난사 → 쉼 → 난사 → 쉼
#   · 난사 시작마다 노릴 곳 = 사거리 안 좀비가 가장 많이 모인 곳 + 랜덤으로 살짝 옆 (반지름 2.5칸 안)
#   · 그쪽을 가운데로 부채꼴을 좌우로 왔다갔다 (폭 · 왕복 빠르기 랜덤) — 총알은 그 선에 처음 닿은 좀비가 맞는다
#   · 넉백 = 군인과 같다 (한 좀비당 0.77초에 한 번까지) · 돌진 중엔 안 쏜다
C201_R = [
 ("    if (car.tkPh === 'dash') car.burstN = 0;   // c173: 돌진 중엔 안 쏜다\n    else if (car.burstN > 0) { if ((car.burstT -= dt) <= 0) chTankBullet(car); }\n    else if (car.atkT <= 0 && car.foe && isZombie(car.foe)) { car.burstN = 4; car.burstT = 0; car.burstZ = car.foe; car.atkT = HIT_EVERY; }\n",
  "    car.burstN = 0; chTankSpray(car, dt);   // c201: 난사\n"),
 ("  function chTankBullet(car) {",
  """  const CH_SP_RATE = 10 * 4 / HIT_EVERY, CH_SP_DMG = POLICE_DAMAGE * 1.2 / 4 * 0.9 * 0.9 / 10, chSpBuf = [];
  function chTankSprayAim(car) {               // c201: 사거리 안 좀비가 가장 많이 모인 곳 → 반지름 2.5칸 안 아무 데
    const rim = CAR_L * CH_TK_KL / 2, R = SIGHT + rim, L = [];
    for (const z of nearIn(zCells, car.x, car.z, R, chSpBuf)) if (isZombie(z) && z.hp > 0 && Math.hypot(z.foot.x - car.x, z.foot.z - car.z) <= R && !fireBlocked(car.x, car.z, z.foot.x, z.foot.z)) L.push(z);
    if (!L.length) return null;
    let best = null, bn = -1;
    for (const a of L) { let n = 0; for (const b of L) if (Math.abs(a.foot.x - b.foot.x) < 2 && Math.abs(a.foot.z - b.foot.z) < 2 && Math.hypot(a.foot.x - b.foot.x, a.foot.z - b.foot.z) < 2) n++; if (n > bn) { bn = n; best = a; } }
    let cx = 0, cz = 0, k = 0; for (const b of L) if (Math.hypot(best.foot.x - b.foot.x, best.foot.z - b.foot.z) < 2) { cx += b.foot.x; cz += b.foot.z; k++; }
    const r = 2.5 * Math.sqrt(Math.random()), a = Math.random() * Math.PI * 2;
    return { x: cx / k + Math.cos(a) * r, z: cz / k + Math.sin(a) * r };
  }
  function chTankSpray(car, dt) {
    if (!car.spQ || !car.spQ.length) { const f = 1 + Math.floor(Math.random() * 6), r = 1 + Math.floor(Math.random() * 7); car.spQ = [['fire', f], ['rest', r], ['fire', 7 - f], ['rest', 8 - r]]; car.spT = 0; car.spAim = null; }
    const ph = car.spQ[0];
    if ((car.spT += dt) >= ph[1]) { car.spQ.shift(); car.spT = 0; car.spAim = null; car.spOn = false; return; }
    car.spOn = false;
    if (ph[0] !== 'fire' || car.tkPh === 'dash') return;   // 쉬는 중 · 돌진 중
    if (!car.spAim) { if ((car.spScan = (car.spScan || 0) - dt) > 0) return; car.spScan = 0.2; car.spAim = chTankSprayAim(car); if (!car.spAim) return; car.spS = rand(-1, 1); car.spDir = Math.random() < 0.5 ? -1 : 1; car.spP = rand(0.45, 1.2); car.spW = rand(0.35, 0.7); car.spAcc = 0; }
    // 부채꼴 왕복 (끝에 닿으면 반대로 — 왕복 빠르기는 매번 랜덤)
    car.spS += car.spDir * dt * 2 / car.spP;
    if (car.spS > 1 || car.spS < -1) { car.spS = Math.max(-1, Math.min(1, car.spS)); car.spDir = -car.spDir; car.spP = rand(0.45, 1.2); }
    car.spAng = Math.atan2(car.spAim.z - car.z, car.spAim.x - car.x) + car.spS * car.spW;
    car.spOn = true;
    const ta = car.h - car.tkAim; let dd = ta - car.spAng; dd = Math.atan2(Math.sin(dd), Math.cos(dd));
    if (Math.abs(dd) > 0.2) return;           // 포탑이 아직 그쪽을 안 봤다
    car.spAcc += dt * CH_SP_RATE * (car.goo ? 0.56 : 1);
    if (car.spAcc < 1) return;
    const rim = CAR_L * CH_TK_KL / 2, R = SIGHT + rim, tip = 0.63 * CH_TK_K, mx = car.x + Math.cos(ta) * tip, mz = car.z + Math.sin(ta) * tip;
    car.tipX = mx; car.tipZ = mz;
    const C = []; for (const z of nearIn(zCells, car.x, car.z, R + 1, chSpBuf)) if (isZombie(z) && z.hp > 0) C.push(z);
    let ex = 0, ez = 0;
    while (car.spAcc >= 1) {
      car.spAcc -= 1;
      const a = ta + rand(-0.04, 0.04), ux = Math.cos(a), uz = Math.sin(a);
      let hit = null, ht = R - tip;
      for (const z of C) { const dx = z.foot.x - mx, dz = z.foot.z - mz, t = dx * ux + dz * uz; if (t <= 0 || t >= ht) continue; if (Math.abs(-dx * uz + dz * ux) > (z.r || BODY) + 0.12) continue; if (fireBlocked(mx, mz, z.foot.x, z.foot.z)) continue; ht = t; hit = z; }
      ex = mx + ux * ht; ez = mz + uz * ht;
      if (!hit) { const da = Math.hypot(car.spAim.x - mx, car.spAim.z - mz) + 1.5; if (da < ht) { ex = mx + ux * da; ez = mz + uz * da; } continue; }
      landHit(car.gun, hit, hit === me && hasVest ? CH_SP_DMG * vestK(lv('vest')) : CH_SP_DMG);
      if (isZombie(hit) && hit.hp > 0 && hit.mut !== 'armor' && hit.mode !== 'bite' && !(clock - (hit.tkKn ?? -9) < HIT_EVERY)) {   // 군인 넉백 (3)
        hit.tkKn = clock;
        const T = ARMOR_KT * 3 / 12, D = SNIPER_KD * 3 / 12, V = D * 4 / (1 - Math.exp(-4 * T));
        if (!(hit === me && absorbAmt() >= D - 0.001)) { if (hit.mode === 'pounce') stopPounce(hit); giveKnock(hit, hit.foot.x - car.x, hit.foot.z - car.z, V, T); }
      }
      if (Math.random() < 0.35) { const f2 = puff(ex, 0.4, ez, 0xffa53a, 0.35, 0.6, 0.08, 0, 0, 0, 0.5); f2.s.material.map = flashTex; f2.s.renderOrder = UI - 0.5; f2.peak = true; }
    }
    car.shotT = 0; car.shotX = ex; car.shotZ = ez;
    const f1 = puff(mx, 0, mz, Math.random() < 0.5 ? 0xffe14d : 0xfff7c0, 0.6, rand(0.7, 0.9), 0.04, 0, 0, 0, 0.9);
    f1.s.material.map = flashTex; f1.s.renderOrder = UI - 0.5; f1.peak = true; f1.blink = true;
    if (Math.random() < 0.5) { const b = ta + rand(-0.45, 0.45), sp = rand(5, 9), s = puff(mx, 0.1, mz, 0xffc23a, 0.12, 0.08, rand(0.08, 0.12), Math.cos(b) * sp, 0, Math.sin(b) * sp, 0.95); s.s.material.map = flashTex; s.s.renderOrder = UI - 0.5; s.peak = true; }
  }
  function chTankBullet(car) {"""),
 ("      const z = car.burstN > 0 && car.burstZ && isZombie(car.burstZ) ? car.burstZ : car.foe && isZombie(car.foe) ? car.foe : null;\n      const want = z ? -(Math.atan2(z.foot.z - car.z, z.foot.x - car.x) - car.h) : 0;",
  "      const z = car.burstN > 0 && car.burstZ && isZombie(car.burstZ) ? car.burstZ : car.foe && isZombie(car.foe) ? car.foe : null;\n      const want = car.spOn ? -(car.spAng - car.h) : car.spAim ? -(Math.atan2(car.spAim.z - car.z, car.spAim.x - car.x) - car.h) : z ? -(Math.atan2(z.foot.z - car.z, z.foot.x - car.x) - car.h) : 0;   // c201: 난사 중엔 부채꼴 따라"),
]
