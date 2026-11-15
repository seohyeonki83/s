  // ── c71: 돌아다니는 민간 차 (c73: 시야와 좀비 대응을 다시 잡았다) ──
  //   구역마다 3~4대가 그 구역 도로(가장자리 순환도로 + 큰길)만 계속 돈다 — 다른 구역으로는 안 넘어간다. 우측통행.
  //   시야 = 앞으로 곧게 뻗은 좁은 띠: 길이는 경찰차 시야의 40%, 폭은 자기 차 폭의 80%. 그 밖의 좀비는 못 본다 (옆으로 스치거나 그냥 지나친다).
  //   띠를 가로로 셋으로 나눠 — 가운데에 좀비: 선다 (안 보이면 다시 간다) · 오른쪽에 좀비: 속도 그대로 왼쪽으로 튼다 · 왼쪽에 좀비: 오른쪽으로 튼다.
  //   못 피하면 그대로 치고 지나간다 (경찰차와 같은 넉백·데미지, 방금 친 좀비는 다시 안 본다). 도로를 많이 벗어나면 좀비가 있든 없든 차선으로 돌아온다.
  //   가운데 좀비에 막혀 3~5초 서 있으면 탄 사람(1~3명)이 내린다. 서 있는(느린) 차는 좀비가 때릴 수 있다 — 맞으면 얼어붙고, 체력이 10~30% 깎이면 내린다.
  //   내린 차는 그 자리에 남는다 (주차된 차와 같은 물건). 구역마다 15대까지 — 넘으면 내 시야 밖의 빈 차 하나가 사라진다. 사람은 안 친다 (밀어내기만 한다)
  const CH_TR_SPD = { compact: 0.62, sedan: 0.62, sports: 0.74, van: 0.55, truck: 0.48 };   // 경찰차 속도의 몇 배로 다니나
  const CH_TR_SEE = 0.4, CH_TR_SEE_W = 0.8;   // c73: 시야 길이 = 경찰차의 40% · 시야 폭 = 자기 차 폭의 80%
  const CH_TR_SW = 200 * Math.PI / 180, CH_TR_SW_D = 1.2, CH_TR_SW_LOOK = 1.2, CH_TR_SW_HOLD = 0.25, CH_TR_OUT = 0.3;   // 피할 때: 옆으로 1.2칸 비켜난 자리를 1.2칸 앞에 두고 초당 200°까지 꺾는다 (속도는 그대로) · 안 보이게 된 뒤 0.25초 더 · 차 옆구리는 도로 밖으로 0.3칸까지만
  const CH_TR_ROAM = 1.5, CH_TR_KEEP = 15, CH_TR_ACC = 7;
  const CH_TR_WHO = [['', 35], ['guard', 30], ['attacker', 20], ['vig', 15]];   // 탄 사람 — 하양 · 노랑 · 주황 · 자경단
  let chTr = null, chRoadG = null;
  const chTrL = [], chTrL2 = [];
  function chRoadGraphs() {                    // 구역마다: 세로줄 V · 가로줄 H (도로 한가운데 선 c · 도로 반폭 hw · 차선 벌림 lane). 줄이 만나는 곳마다 교차로
    const r = CH_MAP.ring / 2;
    return CH_MAP.zones.map(([x0, z0, x1, z1]) => {
      const V = [{ c: x0 + r, hw: r }, { c: x1 - r, hw: r }], H = [{ c: z0 + r, hw: r }, { c: z1 - r, hw: r }];
      for (const [a, b, c, d] of CH_MAP.roads) {   // 구역을 끝에서 끝까지 가로지르는 큰길
        if (b <= z0 + 0.01 && d >= z1 - 0.01 && a > x0 + 6 && c < x1 - 6) V.push({ c: (a + c) / 2, hw: (c - a) / 2 });
        if (a <= x0 + 0.01 && c >= x1 - 0.01 && b > z0 + 6 && d < z1 - 6) H.push({ c: (b + d) / 2, hw: (d - b) / 2 });
      }
      for (const L of [V, H]) { L.sort((p, q) => p.c - q.c); for (const l of L) l.lane = Math.min(1.3, l.hw / 2); }
      return { V, H };
    });
  }
  function chTrNext(G, ai, aj, bi, bj) {       // b에서 다음 갈 교차로 — 온 길로는 안 돌아간다. 곧장 가는 쪽이 두 배 흔하다
    const opt = [];
    for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const i = bi + di, j = bj + dj; if (i < 0 || j < 0 || i >= G.V.length || j >= G.H.length || (i === ai && j === aj)) continue;
      opt.push([i, j]); if (di === bi - ai && dj === bj - aj) opt.push([i, j]);
    }
    return opt[Math.floor(Math.random() * opt.length)];
  }
  function chTrGeom(G, T) {                    // 지금 길(a→b)과 다음 길(b→c)의 차선
    const ax = G.V[T.ai].c, az = G.H[T.aj].c, bx = G.V[T.bi].c, bz = G.H[T.bj].c, cx = G.V[T.ci].c, cz = G.H[T.cj].c;
    const len = Math.abs(bx - ax) + Math.abs(bz - az), d1x = Math.sign(bx - ax), d1z = Math.sign(bz - az), d2x = Math.sign(cx - bx), d2z = Math.sign(cz - bz);
    const R1 = d1x ? G.H[T.aj] : G.V[T.ai], R2 = d2x ? G.H[T.bj] : G.V[T.bi], r1x = -d1z, r1z = d1x, r2x = -d2z, r2z = d2x;
    return { ax, az, bx, bz, len, d1x, d1z, d2x, d2z, o1: R1.lane, o2: R2.lane, hw1: R1.hw, r1x, r1z, r2x, r2z, turn: d1x !== d2x || d1z !== d2z, k: r2x * d1x + r2z * d1z };   // k: 우회전 −1 (가운데 못 미쳐 꺾는다) · 좌회전 +1 (지나서 꺾는다)
  }
  function chTrSeen(x, z, pad, all) {          // 그 자리가 좀비(나·동료) 시야 안인가
    if (me && isZombie(me) && Math.hypot(me.foot.x - x, me.foot.z - z) < (me.sense || SIGHT) + pad) return true;   // 나는 늘 따로 본다 (좀비 목록은 걸음마다 새로 만든다)
    for (const b of (all ? bodies : zombies)) if (isZombie(b) && Math.hypot(b.foot.x - x, b.foot.z - z) < (b.sense || SIGHT) + pad) return true;
    return false;
  }
  function chTrSpawn(zi, all) {                // 그 구역 도로 위 안 보이는 자리에 한 대 — 다 보이면 아무 데나
    const G = chRoadG[zi];
    for (let t = 0; t < 40; t++) {
      const vert = Math.random() < 0.5, i = Math.floor(Math.random() * (vert ? G.V.length : G.V.length - 1)), j = Math.floor(Math.random() * (vert ? G.H.length - 1 : G.H.length));
      const T = { zone: zi, ai: i, aj: j, bi: vert ? i : i + 1, bj: vert ? j + 1 : j };
      if (Math.random() < 0.5) { const a = T.ai, b = T.aj; T.ai = T.bi; T.aj = T.bj; T.bi = a; T.bj = b; }
      const n = chTrNext(G, T.ai, T.aj, T.bi, T.bj); T.ci = n[0]; T.cj = n[1];
      const g = chTrGeom(G, T); if (g.len < 9) continue;
      const s = rand(4, g.len - 4), x = g.ax + g.r1x * g.o1 + g.d1x * s, z = g.az + g.r1z * g.o1 + g.d1z * s;
      if (t < 30 && chTrSeen(x, z, 5, all)) continue;
      if (cars.some((c) => Math.abs(c.x - x) < 4.5 && Math.abs(c.z - z) < 4.5)) continue;
      const type = chCarPick(), car = chCivCar(type, x, z, Math.atan2(g.d1z, g.d1x)), spd = CAR_SPEED * CH_TR_SPD[type], who = [];
      for (let k = 1 + Math.floor(Math.random() * 3); k > 0; k--) { let r = Math.random() * 100, w = ''; for (const [q, p] of CH_TR_WHO) if ((r -= p) < 0) { w = q; break; } who.push(w); }
      car.state = 'civ'; car.sight = SIGHT * 0.7 * rand(0.8, 1.2) * CH_TR_SEE; car.vx = g.d1x * spd; car.vz = g.d1z * spd;
      chCarObj(car, false); car.obj.off = true;
      car.tr = Object.assign(T, { g, mode: 'go', off: 0, spd, who, hp: car.obj.hp, hitT: 0, exitDmg: rand(0.1, 0.3), exitAt: rand(3, 5), zT: 0, jamT: 0, clearT: 0, resume: 'go', swT: 0, swDir: 0, swLat: null, back: false, pickT: 0, scanT: Math.random() * 0.07, dFree: Infinity, blk: null, stuckT: 0, uT: 0, born: clock });
      chTr.cars.push(car); return car;
    }
    return null;
  }
  function chTrReset() {                       // 새 판 — 구역마다 3~4대를 바로 채운다
    if (!chRoadG) chRoadG = chRoadGraphs();
    chTr = { cars: [], Z: CH_MAP.zones.map(() => ({ n: 0, want: 3 + (Math.random() < 0.5 ? 1 : 0), t: 0 })), gone: CH_MAP.zones.map(() => []) };
    chTr.Z.forEach((Z, zi) => { for (let k = 0; k < Z.want; k++) if (chTrSpawn(zi, true)) Z.n++; Z.t = rand(8, 16); });
  }
  function chTrBox(car, g, s, off) {           // 그 차선(옆으로 off)으로 앞 7칸이 비었나 — 건물·강·서 있는 차
    const W = CAR_W * ck(car), L = CAR_L * ckl(car), hw = W / 2 + 0.35, s0 = s - 0.4, s1 = Math.min(s + 7, g.len + 3);
    const px = g.ax + g.r1x * (g.o1 + off), pz = g.az + g.r1z * (g.o1 + off);
    const xa = px + g.d1x * s0, xb = px + g.d1x * s1, za = pz + g.d1z * s0, zb = pz + g.d1z * s1;
    const x0 = Math.min(xa, xb) - (g.d1x ? 0 : hw), x1 = Math.max(xa, xb) + (g.d1x ? 0 : hw), z0 = Math.min(za, zb) - (g.d1z ? 0 : hw), z1 = Math.max(za, zb) + (g.d1z ? 0 : hw);
    if (x0 < MM.x0 + 0.5 || x1 > MM.x1 - 0.5 || z0 < MM.z0 + 0.5 || z1 > MM.z1 - 0.5) return false;
    for (const B of buildings) if (!B.parent && x1 > B.x0 - 0.2 && x0 < B.x1 + 0.2 && z1 > B.z0 - 0.2 && z0 < B.z1 + 0.2) return false;
    for (const [a, b, c, d] of CH_MAP.rivers) if (x1 > a && x0 < c && z1 > b && z0 < d) return false;
    for (const c of cars) {
      if (c === car || c.wreck || Math.abs(c.x - car.x) > 14 || Math.abs(c.z - car.z) > 14) continue;
      const cs = Math.abs(Math.cos(c.h)), sn = Math.abs(Math.sin(c.h)), l2 = CAR_L * ckl(c) / 2, w2 = CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1), hx = l2 * cs + w2 * sn, hz = l2 * sn + w2 * cs;
      const moving = c.state !== 'parked' && Math.hypot(c.vx, c.vz) > 0.6, same = moving && c.vx * g.d1x + c.vz * g.d1z > 0;
      if (same) continue;                      // 같은 쪽으로 가는 차는 곧 비킨다
      const far = moving ? 6 : 0;              // 마주 오는 차는 멀리서부터 막힌 걸로
      if (x1 + (g.d1x > 0 ? far : 0) > c.x - hx && x0 - (g.d1x < 0 ? far : 0) < c.x + hx && z1 + (g.d1z > 0 ? far : 0) > c.z - hz && z0 - (g.d1z < 0 ? far : 0) < c.z + hz) return false;
    }
    return true;
  }
  function chTrPick(car, T, g, s) {            // 서 있는 차를 피해 갈 옆자리 — 가까운 쪽부터. 도로 가장자리에서 CH_TR_ROAM칸까지만 벗어난다
    for (const k of [-1, 1, -2, 2, -3, 3]) { const off = k * 1.3; if (Math.abs(g.o1 + off) > g.hw1 + CH_TR_ROAM) continue; if (chTrBox(car, g, s, off)) return off; }
    return null;
  }
  function chTrExit(car) {                     // 탄 사람이 내린다 — 차는 그 자리에 빈 차로 남는다
    const T = car.tr; if (!T || T.mode === 'left') return;
    T.mode = 'left'; car.vx = car.vz = 0; car.state = 'parked'; car.deco = true; car.left = clock;
    const j = objs.indexOf(car.obj); if (j >= 0) objs.splice(j, 1); car.obj.off = false; if (!car.obj.dead) chDecoObjs.push(car.obj);
    const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx, off = CAR_W * ck(car) / 2 + BODY + 0.25, row = BODY * 2 + 0.3, s0 = Math.random() < 0.5 ? 1 : -1;
    T.who.forEach((w, i) => {
      let x = car.x, z = car.z, ok = false;
      for (const [sd, bk] of [[i % 2 ? -s0 : s0, Math.floor(i / 2)], [i % 2 ? s0 : -s0, Math.floor(i / 2) + 1], [s0, -1], [-s0, -1], [s0, 2], [-s0, 2]]) {
        x = car.x + rx * off * sd - fx * bk * row; z = car.z + rz * off * sd - fz * bk * row;
        if (freeSpot(x, z, null) && !spaceOf(x, z) && !chOnCar(x, z) && !chNearRiver(x, z, 0.6)) { ok = true; break; }
      }
      if (!ok) { x = car.x; z = car.z; }       // 내릴 자리가 다 막혔으면 차 자리에서 (차가 옆으로 밀어낸다) — 벽 속에 서지 않게
      const c = chPut(x, z, square(x, z), w, null); c.sleep = false; c.met = true; c.tick = 0; c.fromCar = true;
    });
    chTr.gone[T.zone].push(car);
    chTrTrim(T.zone);
    updateCarObs();
  }
  function chTrTrim(zi) {                      // c73: 그 구역 도로에 버려진 빈 차는 15대까지 — 넘으면 내(좀비) 시야 밖의 것 중 아무거나 하나씩 사라진다 (다 보이면 안 보이게 될 때까지 둔다)
    const Q = chTr.gone[zi]; let cut = false;
    for (let k = Q.length - 1; k >= 0; k--) if (!cars.includes(Q[k]) || Q[k].wreck) Q.splice(k, 1);   // 부서진 차는 세지 않는다 (곧 사라진다)
    while (Q.length > CH_TR_KEEP) {
      const cand = Q.filter((c) => !chTrSeen(c.x, c.z, 3)); if (!cand.length) break;
      const c = cand[Math.floor(Math.random() * cand.length)]; chTrGone(c); Q.splice(Q.indexOf(c), 1); cut = true;
    }
    return cut;
  }
  function chTrGone(car) {                     // 차 하나를 조용히 치운다
    scene.remove(car.g); const i = cars.indexOf(car); if (i >= 0) cars.splice(i, 1);
    for (const L of [objs, chDecoObjs]) { const j = L.indexOf(car.obj); if (j >= 0) L.splice(j, 1); }
    if (car.obj && car.obj.hpBar) scene.remove(car.obj.hpBar);
    if (car.obj) car.obj.dead = true;
  }
  function chTrafficTick(dt) {
    if (!chTr) return;
    chTr.Z.forEach((Z, zi) => { if (Z.n < Z.want && (Z.t -= dt) <= 0) { if (chTrSpawn(zi)) Z.n++; Z.t = rand(8, 16); } });
    if ((chTr.trimT = (chTr.trimT || 0) - dt) <= 0) { chTr.trimT = 2; let cut = false; chTr.gone.forEach((Q, zi) => { if (Q.length > CH_TR_KEEP && chTrTrim(zi)) cut = true; }); if (cut) updateCarObs(); }   // 다 보여서 못 치운 빈 차는 2초마다 다시 본다
    for (let k = chTr.cars.length - 1; k >= 0; k--) {
      const car = chTr.cars[k], T = car.tr;
      if (car.wreck || T.mode === 'left' || T.mode === 'gone') { chTr.cars.splice(k, 1); const Z = chTr.Z[T.zone]; Z.n--; Z.want = 3 + (Math.random() < 0.5 ? 1 : 0); Z.t = rand(8, 16); continue; }
      chTrDrive(car, T, dt);
    }
  }
  function chTrDrive(car, T, dt) {
    const G = chRoadG[T.zone], o = car.obj, L = CAR_L * ckl(car), W = CAR_W * ck(car), sp = Math.hypot(car.vx, car.vz);
    o.foot.set(car.x, 0, car.z); o.off = sp > 1.2;   // 달리는 차는 때릴 대상이 아니다
    if (o.hp < T.hp) { T.hp = o.hp; T.hitT = 2; }     // 맞았다 → 얼어붙는다
    if (o.hp <= o.maxHp * (1 - T.exitDmg)) { chTrExit(car); return; }   // 10~30% 깎였다 → 내린다
    if (T.hitT > 0) T.hitT -= dt;
    let g = T.g, s = (car.x - g.ax) * g.d1x + (car.z - g.az) * g.d1z, sc = g.len + (g.turn ? (g.o2 + T.off) * g.k : 0);
    if (s >= sc - (g.turn ? 0.4 : 0)) {        // 교차로를 지났다 → 다음 길
      T.ai = T.bi; T.aj = T.bj; T.bi = T.ci; T.bj = T.cj; const n = chTrNext(G, T.ai, T.aj, T.bi, T.bj); T.ci = n[0]; T.cj = n[1];
      g = T.g = chTrGeom(G, T); s = (car.x - g.ax) * g.d1x + (car.z - g.az) * g.d1z; sc = g.len + (g.turn ? (g.o2 + T.off) * g.k : 0); T.swT = 0; T.swLat = null;
    }
    const look = 2 + sp * 0.3, sa = s + look, lat = g.o1 + T.off;
    let tx, tz;                                // 향할 자리 — 차선 위 조금 앞 (교차로에서는 다음 차선으로 이어서)
    if (!g.turn || sa <= sc) { tx = g.ax + g.r1x * lat + g.d1x * sa; tz = g.az + g.r1z * lat + g.d1z * sa; }
    else { const rem = sa - sc, l2 = g.o2 + T.off; tx = g.bx + g.r1x * lat + g.r2x * l2 + g.d2x * rem; tz = g.bz + g.r1z * lat + g.r2z * l2 + g.d2z * rem; }
    let ux = tx - car.x, uz = tz - car.z; const ul = Math.hypot(ux, uz) || 1; ux /= ul; uz /= ul;
    const fx = Math.cos(car.h), fz = Math.sin(car.h);
    let zMid = false, zL = false, zR = false;  // 좀비 — 앞으로 곧게 뻗은 좁은 띠 (길이 car.sight · 폭 = 차 폭의 80%)를 가로로 셋으로. 띠 밖·건물 안·벽 너머는 못 보고, 이 차가 방금 친 좀비는 3초 동안 없는 셈 친다 (받고 지나간다)
    const sw = W * CH_TR_SEE_W / 2;
    for (const z of nearIn(zCells, car.x, car.z, car.sight + L, chTrL)) {
      if (z.space || !isZombie(z) || (z.trHit === car && z.trHitT > clock)) continue;
      const dx = z.foot.x - car.x, dz = z.foot.z - car.z, al = dx * fx + dz * fz - L / 2; if (al <= 0 || al > car.sight) continue;   // 앞 범퍼에서부터
      const lt = -dx * fz + dz * fx; if (Math.abs(lt) > sw) continue;   // + = 오른쪽
      if (blocked(car.x, car.z, z.foot.x, z.foot.z)) continue;
      if (Math.abs(lt) <= sw / 3) { zMid = true; break; }
      if (lt > 0) zR = true; else zL = true;
    }
    if ((T.scanT -= dt) <= 0) {                // 가려는 쪽 앞길을 막는 것 — 다른 차 · 깨어 있는 사람 (좀비는 위의 띠로만 본다)
      T.scanT = 0.07;
      const range = Math.max(2.4, sp * sp / (2 * CAR_BRAKE) + 1.8), hw = W / 2 + 0.3; let dF = Infinity, blk = null;
      for (const c of cars) {
        if (c === car || c.wreck || Math.abs(c.x - car.x) > range + 6 || Math.abs(c.z - car.z) > range + 6) continue;
        const cfx = Math.cos(c.h), cfz = Math.sin(c.h), l2 = CAR_L * ckl(c) / 2, w2 = CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1);
        for (let q = 0; q < 9; q++) { const a = (q % 3 - 1) * l2, b = (Math.floor(q / 3) - 1) * w2, px = c.x + cfx * a - cfz * b - car.x, pz = c.z + cfz * a + cfx * b - car.z, al = px * ux + pz * uz - L / 2;
          if (al > -0.4 && al < range && Math.abs(-px * uz + pz * ux) < hw + 0.05 && al < dF) { dF = Math.max(0, al); blk = c; } }
      }
      for (const b of nearIn(cCells, car.x, car.z, range + L, chTrL2)) {
        if (b.sleep || b.space) continue;
        const px = b.foot.x - car.x, pz = b.foot.z - car.z, al = px * ux + pz * uz - L / 2 - b.r;
        if (al > -0.3 && al < range && Math.abs(-px * uz + pz * ux) < hw + b.r && al < dF) { dF = Math.max(0, al); blk = b; }
      }
      T.dFree = dF; T.blk = blk;
    }
    const blk = T.blk;
    // 옆 3분의 1에 좀비 → 속도는 그대로 두고 반대쪽으로 비켜난다 (도로 가장자리까지만). 도로를 많이 벗어났으면 좀비가 있든 없든 차선으로 돌아온다
    const latNow = (car.x - g.ax) * g.r1x + (car.z - g.az) * g.r1z - g.o1;   // 제 차선 한가운데에서 오른쪽으로 얼마나
    const limR = Math.max(g.hw1 - g.o1 - W / 2 + CH_TR_OUT, T.off), limL = Math.min(-(g.hw1 + g.o1 - W / 2 + CH_TR_OUT), T.off);   // 차 옆구리가 도로 밖으로 CH_TR_OUT칸까지
    if ((latNow > limR + 0.3 || latNow < limL - 0.3) && s > 2.5 && (!g.turn || sc - s > 3.5)) { T.back = true; T.swT = 0; T.swLat = null; }   // 교차로에서 도는 중엔 안 따진다
    else if (T.back && Math.abs(latNow - T.off) < 0.35) T.back = false;
    const halt = zMid || T.hitT > 0;           // 가운데 좀비 · 맞는 중 → 선다
    if (!halt && !T.back && zL !== zR) {       // 오른쪽에 있으면 왼쪽으로, 왼쪽에 있으면 오른쪽으로
      const dir = zR ? -1 : 1; T.swT = CH_TR_SW_HOLD;
      if (T.swLat === null || T.swDir !== dir) { T.swDir = dir; T.swLat = Math.max(limL, Math.min(limR, latNow + dir * CH_TR_SW_D)); }
    } else if (T.swT > 0 && (T.swT -= dt) <= 0) T.swLat = null;
    const swerve = !halt && (T.back || T.swLat !== null), swTo = T.back ? T.off : T.swLat;   // 도로를 벗어났으면 같은 빠르기로 제 차선(swTo)으로 돌아온다
    let want = T.spd;                          // 내고 싶은 속도
    if (g.turn && sc - s < 3.5) want *= 0.55;                                               // 꺾기 전에 줄인다
    if (!swerve && (s < 2.5 || (g.turn && sc - s < 3.5)) && sp > 0.5 && (car.vx * ux + car.vz * uz) / sp < 0.85) want *= 0.6;   // 교차로에서 아직 도는 중 (좀비를 피하거나 차선으로 돌아오는 중엔 안 줄인다)
    if (T.mode === 'avoid' || (T.mode === 'stop' && T.resume === 'avoid')) want *= 0.55;
    if (T.dFree < Infinity) {
      let lim = Math.sqrt(2 * CAR_BRAKE * Math.max(0, T.dFree - 0.7));
      if (blk && !blk.kind && blk.state !== 'parked') { const v2 = Math.hypot(blk.vx, blk.vz); if (v2 > 0.5 && blk.vx * ux + blk.vz * uz > 0 && T.dFree > 0.9) lim = Math.max(lim, v2 * 0.9); }   // 앞차를 따라간다
      want = Math.min(want, lim);
    }
    if (halt && T.mode !== 'stop') { T.resume = T.mode; T.mode = 'stop'; T.clearT = 0; T.swT = 0; T.swLat = null; }
    if (T.mode === 'stop') {
      want = 0;
      if (halt) T.clearT = 0; else if ((T.clearT += dt) > 0.4) { T.mode = T.resume; T.zT = 0; }   // 가운데에 좀비가 없다 → 다시 출발
    } else if (T.mode === 'avoid') {
      if ((T.backT -= dt) <= 0) { T.backT = 0.4;   // 제 차선이 비었으면 돌아간다 · 지금 가는 옆자리가 막혔으면 다른 자리
        if (chTrBox(car, g, s, 0)) { T.off = 0; T.mode = 'go'; T.jamT = 0; }
        else if (want < 0.3 && sp < 0.3) { const off = chTrPick(car, T, g, s); if (off !== null) T.off = off; }
      }
    } else {                                   // 가는 중 — 서 있는 것(차·오래 선 사람)에 막혔으면 옆으로 피해 간다
      const stat = blk && (blk.kind ? T.jamT > 2.5 : (blk.state === 'parked' || Math.hypot(blk.vx, blk.vz) < 0.25));
      if (want < 0.4 && blk) T.jamT += dt; else T.jamT = Math.max(0, T.jamT - dt * 2);
      if (stat && T.jamT > 1 && (T.pickT -= dt) <= 0) { T.pickT = 0.5; const off = chTrPick(car, T, g, s); if (off !== null) { T.mode = 'avoid'; T.off = off; T.backT = 1.2; } }
    }
    // 좀비에 막혀(가운데 좀비 · 맞는 중) 서 있는 시간 → 3~5초면 내린다
    if (T.mode === 'stop') { if (sp < 0.6 && (T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }
    else T.zT = Math.max(0, T.zT - dt);
    // 오래 못 가면 (좀비 때문이 아닌데) 돌아서 간다 · 그래도 안 되고 아무도 안 보면 조용히 치운다
    if (sp < 0.3 && T.mode !== 'stop') T.stuckT += dt; else T.stuckT = Math.max(0, T.stuckT - dt * 3);
    if (T.stuckT > 7) {
      T.stuckT = 0; T.jamT = 0;
      if (clock - T.uT < 40 && !chTrSeen(car.x, car.z, 6)) { chTrGone(car); T.mode = 'gone'; return; }
      T.uT = clock; const a = T.ai, b = T.aj; T.ci = a; T.cj = b; T.ai = T.bi; T.aj = T.bj; T.bi = a; T.bj = b;   // 유턴: 가던 길을 되돌아간다
      const n = chTrNext(G, T.ai, T.aj, T.bi, T.bj); T.ci = n[0]; T.cj = n[1]; T.g = chTrGeom(G, T); T.off = 0; T.mode = 'go'; T.back = false;
      return;
    }
    if (want <= 0.05) carSteer(car, 0, 0, CAR_BRAKE * dt);
    else if (swerve) {                         // 피하는 중 — 비켜난 자리(조금 앞)를 향해 속도 벡터를 돌리기만 한다 (초당 CH_TR_SW까지 · 속도는 안 줄인다)
      const qx = g.ax + g.r1x * (g.o1 + swTo) + g.d1x * (s + CH_TR_SW_LOOK) - car.x, qz = g.az + g.r1z * (g.o1 + swTo) + g.d1z * (s + CH_TR_SW_LOOK) - car.z;
      const a0 = sp > 0.3 ? Math.atan2(car.vz, car.vx) : car.h; let da = Math.atan2(qz, qx) - a0; da = Math.atan2(Math.sin(da), Math.cos(da));
      const a1 = a0 + Math.max(-CH_TR_SW * dt, Math.min(CH_TR_SW * dt, da)), ns = sp < want ? Math.min(want, sp + CH_TR_ACC * dt) : want < sp - 0.3 ? Math.max(want, sp - CAR_BRAKE * dt) : sp;
      car.vx = Math.cos(a1) * ns; car.vz = Math.sin(a1) * ns;
    }
    else if (want < sp - 0.3) { const k = Math.max(0, sp - CAR_BRAKE * dt) / (sp || 1); car.vx *= k; car.vz *= k; carSteer(car, ux * want, uz * want, CH_TR_ACC * 0.5 * dt); }   // 줄이면서 방향만 조금씩
    else carSteer(car, ux * want, uz * want, CH_TR_ACC * dt);
  }
