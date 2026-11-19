# c191: 보스 테스트에서 동료 수 칭호 알림 건너뜀 · 테이저건이 보스(장갑차)에도 듣는다 — 감전 시간은 3분의 1. 순위는 분홍 다음 (저격수보다 위). 감전 중엔 서고 · 안 쏘고 · 돌진 순서도 멈춘다 · 몸이 번쩍인다
C191_R = [
 ("      cand.sort((a, b) => b.k - a.k || a.d - b.d);\n      const hit = cand.slice(0, CH_WV('taserN', lv('taser')));",
  "      if (CHAPTER && chTank && !chTank.wreck && !(chTank.stunT > 0) && !me.space) { const T = chTank, d = Math.max(0, Math.hypot(T.x - me.foot.x, T.z - me.foot.z) - CAR_W * CH_TK_K / 2); if (d <= me.sense && !fireBlocked(me.foot.x, me.foot.z, T.x, T.z)) cand.push({ c: T, k: 98, d }); }   // c191: 보스도 감전\n"
  "      cand.sort((a, b) => b.k - a.k || a.d - b.d);\n      const hit = cand.slice(0, CH_WV('taserN', lv('taser')));"),
 ("      for (const { c } of hit) { c.stunT = CH_WV('taserT', lv('taser'));   /* c139 */ c.vel.set(0, 0); zaps.push({ to: c, t: 0.45 }); }",
  "      for (const { c } of hit) { if (c.tank) { c.stunT = CH_WV('taserT', lv('taser')) / 3; c.vx = c.vz = 0; zaps.push({ to: c, t: 0.45 }); continue; }   /* c191: 보스 = 3분의 1 */ c.stunT = CH_WV('taserT', lv('taser'));   /* c139 */ c.vel.set(0, 0); zaps.push({ to: c, t: 0.45 }); }"),
 ("    const spd = (car.tkSeen ?", """    if (car.stunT > 0) {                       // c191: 감전 — 서고 · 안 쏘고 · 돌진 순서도 멈춘다 · 몸이 번쩍인다
      car.stunT -= dt; car.vx = car.vz = 0; car.burstN = 0; const K0 = car.g.children[0];
      K0.material.color.setHex(car.stunT > 0 && Math.floor(clock * 14) % 2 ? 0xc8f0ff : 0x3c4a2a);
      return;
    }
    const spd = (car.tkSeen ?"""),
 ("      chSf.on = true; chSf.n = 4; chSf.T = chSfAt(5) - 0.05;   // 다음 걸음에 보스 출동", "      chSf.on = true; chSf.n = 4; chSf.T = chSfAt(5) - 0.05;   // 다음 걸음에 보스 출동\n      while (rankNext < RANKS.length && 70 >= RANKS[rankNext].n) rankNext++;   // c191: 보스 테스트 — 동료 수 칭호 알림은 건너뛴다 (보스 알림이 늦게 뜨던 것)"),
]
