  // ── c85: 길거리 사물 · 자리(공원·주유소·농구장·공사 현장) 사람 ──
  //   사물은 맵에 적힌 자리에 판마다 다시 선다. 부수는 규칙은 주차된 차와 같다 — 나는 손 닿는 것을 치고, 동료는 내가 치는 것만 같이 친다.
  //   달리는 차는 박혀 있는 사물을 들이받아 부수고 지나간다 (부술 수 없는 것은 그냥 지나친다). 안 박힌 사물은 차에 받히면 밀리고, 가벼우면 바로 부서진다
  const chOutProps = [], chOutGrid = new Map(), chBigOut = [];
  let chHotOut = null;
  function chOutPlace() {                      // 새 판 — 길거리 사물을 다시 세운다 (그 판의 문 앞에 걸리는 것은 뺀다)
    chOutProps.length = 0; chBigOut.length = 0; chOutGrid.clear(); chHotOut = null;
    const keep = [], door = (L) => { const hw = (L.w || DOOR) / 2 + 0.15, cx = L.cx + L.nx * 1.0, cz = L.cz + L.nz * 1.0, hx = Math.abs(L.tx) * hw + Math.abs(L.nx) * 1.0, hz = Math.abs(L.tz) * hw + Math.abs(L.nz) * 1.0; keep.push([cx - hx, cz - hz, cx + hx, cz + hz]); };
    for (const o of objs) if (o.type === 'door' && !o.off && !(o.B.parent && !o.L.ext)) door(o.L);
    for (const B of buildings) for (const D of B.doors || []) door(D);
    for (const [t, x, z, inv] of CH_MAP.props || []) {
      const P = CH_PROP[t]; if (!P) continue;
      if (!(P.inv || inv) && keep.some((k) => x > k[0] - P.r && x < k[2] + P.r && z > k[1] - P.r && z < k[3] + P.r)) continue;
      const b = chAddProp(t, x, z); b.out = true; b.space = null; b.fixed = !!P.fix; b.inv = !!(P.inv || inv);
      if (b.inv) b.hp = b.maxHp = 1e12;
      chOutProps.push(b); if (P.r > 0.6) chBigOut.push(b);
    }
  }
  function chOutGridAdd(p) { const k = Math.floor(p.foot.x / 4) * 4096 + Math.floor(p.foot.z / 4); let L = chOutGrid.get(k); if (!L) chOutGrid.set(k, L = []); L.push(p); if (!p.fixed) chOutMov.push(p); }
  const chOutMov = [];                         // 깨어 있는 안 박힌 길거리 사물 (0.3초마다 다시 모은다)
  function chOutCars() {                       // 이번 걸음에 밀린 길거리 사물이 차(서 있는 차 · 주차된 차 · 잔해 포함)와 겹치면 차 밖으로 — 쓰레기통이 차를 뚫고 지나가지 않게
    for (const p of chOutMov) { if (p.dead || p.sleep || (p.foot.x === p.px && p.foot.z === p.pz)) continue;
      for (const car of cars) { const dx = p.foot.x - car.x, dz = p.foot.z - car.z; if (dx > 4 || dx < -4 || dz > 4 || dz < -4) continue;
        const k = car.wreck ? 0.16 : car.wall ? 1 : car.state === 'parked' ? PARKED_K : 1;   // 몸이 차와 부딪힐 때와 같은 크기 (잔해는 5분의 1)
        const fx = Math.cos(car.h), fz = Math.sin(car.h), hu = CAR_L * ckl(car) / 2 * k + p.r, hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) + p.r; let u = dx * fx + dz * fz, v = -dx * fz + dz * fx;
        if (Math.abs(u) >= hu || Math.abs(v) >= hv) continue;
        if (hu - Math.abs(u) < hv - Math.abs(v)) u = (u < 0 ? -1 : 1) * hu; else v = (v < 0 ? -1 : 1) * hv;
        p.foot.x = car.x + u * fx - v * fz; p.foot.z = car.z + u * fz + v * fx; } }
  }
  function chNearOut(z) {                      // 밖에서 칠 사물 — 나: 손 닿는 것 (벽에 안 가린 가장 가까운 것) · 동료: 내가 지금 치고 있는 것만 (인지거리 안)
    if (z !== me) { const p = chHotOut; return p && !p.dead && p.hotF >= objFrame - 1 && Math.hypot(p.foot.x - z.foot.x, p.foot.z - z.foot.z) <= z.sense && !blocked(z.foot.x, z.foot.z, p.foot.x, p.foot.z) ? p : null; }
    let best = null, bd = MELEE; const cx = Math.floor(z.foot.x / 4), cz = Math.floor(z.foot.z / 4);
    for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) { const L = chOutGrid.get((cx + i) * 4096 + (cz + j)); if (!L) continue;
      for (const p of L) { if (p.dead) continue; const d = Math.hypot(p.foot.x - z.foot.x, p.foot.z - z.foot.z) - p.r; if (d < bd && !blocked(z.foot.x, z.foot.z, p.foot.x, p.foot.z)) { bd = d; best = p; } } }
    return best;
  }
  function chOutBlock(z, dt) {                 // 길을 막은 길거리 사물 — 동료가 가려고 하는데(속도는 내는데) 1.25초 동안 제자리이고 사물에 닿아 있으면 그것부터 부순다 (건물 안 사물과 같은 규칙. 벽과 박힌 사물 사이에 끼는 일이 없게)
    const P = z.outP;
    if (P) { if (!P.dead && clock < z.outUntil && Math.hypot(P.foot.x - z.foot.x, P.foot.z - z.foot.z) < P.r + z.r + 0.6) { fight(z, P, dt); return true; } z.outP = null; z.outAt = undefined; return false; }
    if (z.outAt === undefined || Math.hypot(z.foot.x - z.outAx, z.foot.z - z.outAz) > 0.3 || z.vel.lengthSq() < 0.8) { z.outAx = z.foot.x; z.outAz = z.foot.z; z.outAt = clock; return false; }
    if (clock - z.outAt < 1.25) return false;
    z.outAt = clock;
    let best = null, bd = 0.15; const cx = Math.floor(z.foot.x / 4), cz = Math.floor(z.foot.z / 4);
    for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) { const L = chOutGrid.get((cx + i) * 4096 + (cz + j)); if (!L) continue;
      for (const p of L) { if (p.dead) continue; const d = Math.hypot(p.foot.x - z.foot.x, p.foot.z - z.foot.z) - p.r - z.r; if (d < bd) { bd = d; best = p; } } }
    if (best) { z.outP = best; z.outUntil = clock + 8; }
    return false;
  }
  function chCarSmash(car, b, fx, fz, rx, rz) {   // 달리는 차와 박혀 있는 사물 — 부술 수 있는 것은 들이받으면 부서진다 (차는 조금 느려진다). 부술 수 없는 것(분수·동상·굴착기 …)은 벽처럼 차를 막는다. 서 있는 차는 아무 일 없다
    if (b.dead || b.sleep || car.state === 'parked' || car.wall || car.wreck) return;   // 자는 사물(좀비가 10칸 안에 없다)은 그대로 둔다
    const dx = b.foot.x - car.x, dz = b.foot.z - car.z; if (Math.abs(dx) > 5 || Math.abs(dz) > 5) return;
    const hl = CAR_L * ckl(car) / 2, hw = CAR_W * ck(car) / 2, u = dx * fx + dz * fz, v = dx * rx + dz * rz;
    if (Math.abs(u) >= hl + b.r || Math.abs(v) >= hw + b.r) return;
    if (b.inv) {                                // 차 네모에서 사물 중심에 가장 가까운 점까지가 반지름보다 짧으면 겹친 것 → 차를 그만큼 밖으로 밀고, 파고드는 속도를 없앤다
      const qu = Math.max(-hl, Math.min(hl, u)), qv = Math.max(-hw, Math.min(hw, v)), eu = u - qu, ev = v - qv, d = Math.hypot(eu, ev);
      if (d >= b.r) return;
      let nu, nv, pen;
      if (d > 1e-6) { nu = -eu / d; nv = -ev / d; pen = b.r - d; }
      else if (hl - Math.abs(u) < hw - Math.abs(v)) { nu = u < 0 ? 1 : -1; nv = 0; pen = hl - Math.abs(u) + b.r; }   // 사물 중심이 차 네모 안 — 가까운 변 쪽으로
      else { nu = 0; nv = v < 0 ? 1 : -1; pen = hw - Math.abs(v) + b.r; }
      const nx = nu * fx + nv * rx, nz = nu * fz + nv * rz;
      car.x += nx * pen; car.z += nz * pen;
      const vn = car.vx * nx + car.vz * nz; if (vn < 0) { car.vx -= vn * nx; car.vz -= vn * nz; }
      return;
    }
    const sp = Math.hypot(car.vx, car.vz); if (sp < 1.5) return;
    breakSafe(b); car.vx *= 0.8; car.vz *= 0.8;
  }
  function chCarProp(car, b, sp) {             // 달리는 차에 받힌 (안 박힌) 사물 — 가벼운 것은 바로 부서지고, 무거운 것은 깎이면서 밀려간다
    const same = b.carC === car && clock < b.carCT; b.carC = car; b.carCT = clock + 3;
    if (same || sp < 1.5 || b.inv || b.dead || b.sleep) return;
    b.hp -= CAR_HIT_DMG * 3 * sp / CAR_SPEED;
    if (b.hp <= 0 || CH_PROP[b.prop].hits <= 2) breakSafe(b); else { car.vx *= 0.85; car.vz *= 0.85; }
  }
  function chTrProps() {                       // 달리는 길거리 차와 길거리 사물 — 길거리 차는 둘레의 사람·좀비하고만 부딪힘을 재므로 사물은 여기서 따로 본다 (깨어 있는 것만)
    if (!chOutGrid.size) return;
    for (const car of chTr.cars) { const T = car.tr; if (!T || T.mode === 'left' || T.mode === 'gone' || car.wreck) continue; const sp = Math.hypot(car.vx, car.vz); if (sp < 1.5) continue;
      const fx = Math.cos(car.h), fz = Math.sin(car.h), hl = CAR_L * ckl(car) / 2, hw = CAR_W * ck(car) / 2, cx = Math.floor(car.x / 4), cz = Math.floor(car.z / 4);
      for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) { const L = chOutGrid.get((cx + i) * 4096 + (cz + j)); if (!L) continue;
        for (const b of L) { if (b.dead) continue; const dx = b.foot.x - car.x, dz = b.foot.z - car.z; let u = dx * fx + dz * fz, v = -dx * fz + dz * fx; const hu = hl + b.r, hv = hw + b.r; if (Math.abs(u) >= hu || Math.abs(v) >= hv) continue;
          if (b.fixed) { breakSafe(b); car.vx *= 0.8; car.vz *= 0.8; continue; }   // 박힌 것은 부서진다
          chCarProp(car, b, sp); if (b.dead) continue;
          if (hu - Math.abs(u) < hv - Math.abs(v)) u = (u < 0 ? -1 : 1) * hu; else v = (v < 0 ? -1 : 1) * hv;   // 안 부서진 것은 차 밖으로 밀려난다 (범퍼 앞이면 밀려간다)
          b.foot.x = car.x + u * fx - v * fz; b.foot.z = car.z + u * fz + v * fx; } } }
  }
  function chBigCollide() {                    // 큰 사물(분수·동상·굴착기 …)은 몸 부딪힘 계산의 범위(0.6칸) 밖이라 따로 본다 — 겹친 몸을 밖으로 민다
    for (const p of chBigOut) { if (p.sleep || p.dead) continue;
      for (const b of byX) { if (b === p || b.fixed || b.mode === 'pounce') continue; const dx = b.foot.x - p.foot.x; if (dx > p.r + 0.7 || dx < -p.r - 0.7) continue;
        const dz = b.foot.z - p.foot.z, d = Math.hypot(dx, dz), min = p.r + b.r; if (d >= min) continue;
        if (d > 1e-6) { const k = (min - d) / d; b.foot.x += dx * k; b.foot.z += dz * k; } else b.foot.x += min; } }
  }
  const CH_OUT_WAKE = 10;                      // 길거리 사물은 좀비가 이 거리 안에 있을 때만 깨어 있다 — 좀비 시야(7.2칸) 밖 사물은 어차피 안 보인다
  function chOutNearZ(p) { const x = p.foot.x, z = p.foot.z, R2 = CH_OUT_WAKE * CH_OUT_WAKE; for (const q of zombies) { const dx = q.foot.x - x, dz = q.foot.z - z; if (dx * dx + dz * dz < R2) return true; } return false; }
  let chDrawF = 0;
  function chOutHidden(b, eyes) {              // 길거리 사물이 안 보이나 — 시야 판정(벽에 가렸나)은 네 번 그릴 때 한 번만 다시 한다 (사물마다 엇갈리게)
    if (b.hidC === undefined || ((chDrawF + (b.drawK === undefined ? (b.drawK = Math.floor(Math.random() * 4)) : b.drawK)) & 3) === 0) b.hidC = !seen(b, eyes);
    return b.hidC;
  }
  function chCanopyDraw(eyes) {                // 주유소 지붕 — 좀비가 밑(이나 바로 옆 1.2칸)에 있으면 사라진다
    chDrawF++;
    for (const C of chCanopies) { C.open = eyes.some((z) => !z.space && z.foot.x > C.x0 - 1.2 && z.foot.x < C.x1 + 1.2 && z.foot.z > C.z0 - 1.2 && z.foot.z < C.z1 + 1.2); C.m.visible = !C.open; }
  }
  function chFuelCars() {                      // 주유소: 기름 넣는 빈 차 0~2대 (판마다 다르다)
    for (const F of CH_MAP.fuel || []) { const sl = F.slots.slice().sort(() => Math.random() - 0.5), n = Math.floor(Math.random() * 3);
      for (let i = 0; i < n; i++) { const [x, z, h0] = sl[i], t = ['sedan', 'compact', 'sedan', 'sports', 'van'][Math.floor(Math.random() * 5)], h = h0 + (Math.random() < 0.5 ? Math.PI : 0), box = chCarBox(x, z, h, t);
        if (!chDecoOk(box)) continue;
        chDecoCar(t, x + rand(-0.05, 0.05), z + rand(-0.2, 0.2), h + rand(-0.04, 0.04)).tag = 'gas'; chDeco.boxes.push(box); chDeco.n.gas = (chDeco.n.gas || 0) + 1; } }
  }
  function chSpotPeople() {                    // 자리마다 모여 있는 사람들 — 주유소 · 버스킹(기타 든 하양 + 둘러선 사람들) · 농구장 · 공사 현장(연장 든 일꾼). 다시 채우지 않는다
    const N = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
    const free = (x, z) => !spaceOf(x, z) && freeSpot(x, z, null) && !chOnRoad(x, z, 0.3) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < (o.r || BODY) + BODY + 0.22);
    for (const S of CH_MAP.spots || []) {
      const list = []; for (const [type, a, b] of S.mix) for (let k = N(a, b); k > 0; k--) list.push(type);
      for (const type of list) for (let t = 0; t < 60; t++) {
        let x, z;
        if (S.ring) { const [cx, cz, r0, r1, sg] = S.ring, a = rand(-1.25, 1.25), r = rand(r0, r1); x = cx + sg * Math.cos(a) * r; z = cz + Math.sin(a) * r; }
        else if (S.rad) { const a = Math.random() * 6.283, r = S.rad * Math.sqrt(Math.random()); x = S.at[0] + Math.cos(a) * r; z = S.at[1] + Math.sin(a) * r; }
        else { x = S.at[0] + (t ? rand(-0.5, 0.5) : 0); z = S.at[1] + (t ? rand(-0.5, 0.5) : 0); }
        if (!free(x, z)) continue;
        const area = { x0: x - 0.45, z0: z - 0.45, x1: x + 0.45, z1: z + 0.45 }, c = chPut(x, z, area, type); c.spotK = S.k;
        const tool = S.tool === 'work' ? ['pick', 'drill', 'hammer'][Math.floor(Math.random() * 3)] : S.tool; if (tool && type !== 'vig') chTool(c, tool);
        break;
      }
    }
  }
