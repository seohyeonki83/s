# c304: 덮치기 — 덮칠 대상까지 직선 위에 자동차·바리케이트·금고(수조)가 있으면 덮치지 않는다 (일반 사물은 그대로 비비고 덮친다) · 나·동료 같음
C304_R = [
  ("  const dashOk = (z, t) => !(z.skip === t && z.skipT > 0);", """  const dashOk = (z, t) => !(z.skip === t && z.skipT > 0) && !(CHAPTER && chPounceBlocked(z.foot.x, z.foot.z, t.foot.x, t.foot.z));   // c304: 큰 물건에 가로막힌 사람은 덮치지 않는다
  function chPounceBlocked(ax, az, bx, bz) {   // c304: 두 점 사이 직선을 자동차(바리케이트·잔해 포함)나 금고(수조)가 가로막나 — 일반 사물은 안 본다
    const box = (car) => { const hu = CAR_L * ckl(car) / 2, hv = CAR_W * ck(car) / 2 * (car.barr ? CH_BARR_W : 1), m = hu + hv;
      if (Math.max(ax, bx) < car.x - m || Math.min(ax, bx) > car.x + m || Math.max(az, bz) < car.z - m || Math.min(az, bz) > car.z + m) return false;
      return chSegBox([ax, az, bx, bz], car.x, car.z, Math.cos(car.h), Math.sin(car.h), hu, hv); };
    for (const car of cars) { if (car.obj && car.obj.dead && !car.wreck) continue; if (box(car)) return true; }
    for (const o of chDecoObjs) if (!o.dead && o.car && box(o.car)) return true;
    const circ = (s) => { const r = s.r || 1, dx = bx - ax, dz = bz - az, L2 = dx * dx + dz * dz || 1e-9, t = Math.max(0, Math.min(1, ((s.foot.x - ax) * dx + (s.foot.z - az) * dz) / L2)); return Math.hypot(ax + dx * t - s.foot.x, az + dz * t - s.foot.z) < r; };
    for (const B of buildings) { const s = B.safe; if (s && !s.dead && circ(s)) return true; }
    if (CH_TUT) for (const p of chProps) if (!p.dead && (p.prop === 'zvat' || p.prop === 'hvat' || p.prop === 'avat') && circ(p)) return true;
    return false;
  }"""),
  ("      if (touching) stopPounce(z);              // 손가락을 대면 그만", "      if (CHAPTER && chPounceBlocked(z.foot.x, z.foot.z, t.foot.x, t.foot.z)) stopPounce(z);   // c304: 덮치는 도중 큰 물건이 끼면 그만\n      else if (touching) stopPounce(z);              // 손가락을 대면 그만"),
  ("  const huntable = (z, b) => b && b.kind === 'citizen' && !b.marked && (", "  const huntable = (z, b) => b && b.kind === 'citizen' && !b.marked && !(CHAPTER && b.hp <= 0 && chPounceBlocked(z.foot.x, z.foot.z, b.foot.x, b.foot.z)) && (   /* c304: 큰 물건 너머 쓰러진 사람은 쫓지 않는다 (그 물건을 친다) */"),
]
