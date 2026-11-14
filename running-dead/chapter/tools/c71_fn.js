  // ── c71: 돌아다니는 민간 차 ──
  //   구역마다 3~4대가 그 구역 도로(가장자리 순환도로 + 큰길)만 계속 돈다 — 다른 구역으로는 안 넘어간다. 우측통행.
  //   시야 = 앞쪽 좁은 부채꼴 (반각 14° + 차 폭만큼의 앞길), 거리는 경찰차와 같다. 좀비가 보이면 선다, 안 보이면 다시 간다.
  //   서 있는 동안: 반은 옆으로 피해 가 본다 (도로 가장자리에서 1.5칸까지만). 3~5초 막혀 있으면 탄 사람(1~3명)이 내린다.
  //   서 있는(느린) 차는 좀비가 때릴 수 있다. 맞으면 얼어붙고, 체력이 10~30% 깎이면 내린다. 내린 차는 그 자리에 남는다 (주차된 차와 같은 물건).
  //   못 본 좀비(옆에서 뛰어든)는 그대로 친다 — 경찰차와 같은 넉백·데미지. 사람은 안 친다 (밀어내기만 한다)
  const CH_TR_SPD = { compact: 0.62, sedan: 0.62, sports: 0.74, van: 0.55, truck: 0.48 };   // 경찰차 속도의 몇 배로 다니나
  const CH_TR_FAN = Math.tan(14 * Math.PI / 180), CH_TR_ROAM = 1.5, CH_TR_KEEP = 10, CH_TR_ACC = 7;
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
      car.state = 'civ'; car.sight = SIGHT * 0.7 * rand(0.8, 1.2); car.vx = g.d1x * spd; car.vz = g.d1z * spd;
      chCarObj(car, false); car.obj.off = true;
      car.tr = Object.assign(T, { g, mode: 'go', off: 0, spd, who, hp: car.obj.hp, hitT: 0, exitDmg: rand(0.1, 0.3), exitAt: rand(3, 5), zT: 0, jamT: 0, stopT: 0, clearT: 0, dodge: false, avoidZ: false, pickT: 0, scanT: Math.random() * 0.07, dFree: Infinity, blk: null, stuckT: 0, uT: 0, born: clock });
      chTr.cars.push(car); return car;
    }
    return null;
  }
  function chTrReset() {                       // 새 판 — 구역마다 3~4대를 바로 채운다
    if (!chRoadG) chRoadG = chRoadGraphs();
    chTr = { cars: [], Z: CH_MAP.zones.map(() => ({ n: 0, want: 3 + (Math.random() < 0.5 ? 1 : 0), t: 0 })), gone: CH_MAP.zones.map(() => []) };
    chTr.Z.forEach((Z, zi) => { for (let k = 0; k < Z.want; k++) if (chTrSpawn(zi, true)) Z.n++; Z.t = rand(8, 16); });
  }
  function chTrBox(car, g, s, off, zomb) {     // 그 차선(옆으로 off)으로 앞 7칸이 비었나 — 건물·강·서 있는 차(·좀비)
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
    if (zomb) for (const z of nearIn(zCells, (x0 + x1) / 2, (z0 + z1) / 2, 5, chTrL2)) if (!z.space && isZombie(z) && z.foot.x > x0 - 0.7 && z.foot.x < x1 + 0.7 && z.foot.z > z0 - 0.7 && z.foot.z < z1 + 0.7) return false;
    return true;
  }
  function chTrPick(car, T, g, s, zomb) {      // 피해 갈 옆자리 — 가까운 쪽부터. 도로 가장자리에서 CH_TR_ROAM칸까지만 벗어난다
    for (const k of [-1, 1, -2, 2, -3, 3]) { const off = k * 1.3; if (Math.abs(g.o1 + off) > g.hw1 + CH_TR_ROAM) continue; if (chTrBox(car, g, s, off, zomb)) return off; }
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
    const Q = chTr.gone[T.zone]; Q.push(car);
    for (let k = 0; Q.length > CH_TR_KEEP && k < Q.length; k++) {   // 빈 차가 너무 쌓이면 안 보이는 가장 오래된 것부터 치운다
      const c = Q[k]; if (!cars.includes(c)) { Q.splice(k--, 1); continue; }
      if (c.wreck || chTrSeen(c.x, c.z, 6)) continue;
      chTrGone(c); Q.splice(k--, 1);
    }
    updateCarObs();
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
      g = T.g = chTrGeom(G, T); s = (car.x - g.ax) * g.d1x + (car.z - g.az) * g.d1z; sc = g.len + (g.turn ? (g.o2 + T.off) * g.k : 0);
    }
    const look = 2 + sp * 0.3, sa = s + look, lat = g.o1 + T.off;
    let tx, tz;                                // 향할 자리 — 차선 위 조금 앞 (교차로에서는 다음 차선으로 이어서)
    if (!g.turn || sa <= sc) { tx = g.ax + g.r1x * lat + g.d1x * sa; tz = g.az + g.r1z * lat + g.d1z * sa; }
    else { const rem = sa - sc, l2 = g.o2 + T.off; tx = g.bx + g.r1x * lat + g.r2x * l2 + g.d2x * rem; tz = g.bz + g.r1z * lat + g.r2z * l2 + g.d2z * rem; }
    let ux = tx - car.x, uz = tz - car.z; const ul = Math.hypot(ux, uz) || 1; ux /= ul; uz /= ul;
    const fx = Math.cos(car.h), fz = Math.sin(car.h);
    let seeZ = false;                          // 좀비 — 앞쪽 좁은 부채꼴 + 차 폭만큼의 앞길 (건물 안 좀비·벽 너머는 못 본다)
    for (const z of nearIn(zCells, car.x, car.z, car.sight + L, chTrL)) {
      if (z.space || !isZombie(z)) continue;
      const dx = z.foot.x - car.x, dz = z.foot.z - car.z, al = dx * fx + dz * fz; if (al <= 0 || al > car.sight + L / 2) continue;
      const lt = Math.abs(-dx * fz + dz * fx); if (lt > W / 2 + 0.5 && lt > al * CH_TR_FAN) continue;
      if (blocked(car.x, car.z, z.foot.x, z.foot.z)) continue;
      seeZ = true; break;
    }
    if ((T.scanT -= dt) <= 0) {                // 가려는 쪽 앞길을 막는 것 — 다른 차 · 깨어 있는 사람 · (피해 가는 중엔) 좀비
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
      if (T.mode === 'avoid') for (const z of nearIn(zCells, car.x, car.z, range + L, chTrL2)) {
        if (z.space || !isZombie(z)) continue;
        const px = z.foot.x - car.x, pz = z.foot.z - car.z, al = px * ux + pz * uz - L / 2 - z.r;
        if (al > -0.3 && al < range + 1 && Math.abs(-px * uz + pz * ux) < hw + z.r + 0.2 && al < dF) { dF = Math.max(0, al); blk = z; }
      }
      T.dFree = dF; T.blk = blk;
    }
    const blk = T.blk, zBlk = blk && blk.kind && isZombie(blk);
    let want = T.spd;                          // 내고 싶은 속도
    if (g.turn && sc - s < 3.5) want *= 0.55;                                    // 꺾기 전에 줄인다
    if (sp > 0.5 && (car.vx * ux + car.vz * uz) / sp < 0.85) want *= 0.6;         // 아직 도는 중
    if (T.mode === 'avoid') want *= 0.55;
    if (T.dFree < Infinity) {
      let lim = Math.sqrt(2 * CAR_BRAKE * Math.max(0, T.dFree - 0.7));
      if (blk && !blk.kind && blk.state !== 'parked') { const v2 = Math.hypot(blk.vx, blk.vz); if (v2 > 0.5 && blk.vx * ux + blk.vz * uz > 0 && T.dFree > 0.9) lim = Math.max(lim, v2 * 0.9); }   // 앞차를 따라간다
      want = Math.min(want, lim);
    }
    // 좀비
    if (T.mode === 'go' && seeZ) { T.mode = 'stop'; T.stopT = 0; T.clearT = 0; T.dodge = Math.random() < 0.5; }
    else if (T.mode !== 'stop' && T.hitT > 0) { T.mode = 'stop'; T.stopT = 0; T.clearT = 0; T.dodge = false; T.off = 0; T.avoidZ = false; }   // 못 본 좀비에게 맞았다 → 그 자리에 선다
    if (T.mode === 'stop') {
      want = 0; T.stopT += dt;
      if (seeZ) T.clearT = 0; else if ((T.clearT += dt) > 0.5 && T.hitT <= 0) { T.mode = 'go'; T.zT = 0; }   // 시야에 좀비가 없다 → 다시 출발
      if (T.mode === 'stop' && T.dodge && T.stopT > 0.7 && T.hitT <= 0 && (T.pickT -= dt) <= 0) {            // 옆으로 피해 가 본다
        T.pickT = 0.5; const off = chTrPick(car, T, g, s, true);
        if (off !== null) { T.mode = 'avoid'; T.off = off; T.avoidZ = true; T.backT = 1.2; }
      }
    } else if (T.mode === 'avoid') {
      if ((T.backT -= dt) <= 0) { T.backT = 0.4;   // 제 차선이 비었으면 돌아간다 · 지금 가는 옆자리가 막혔으면 다른 자리
        if (chTrBox(car, g, s, 0, T.avoidZ)) { T.off = 0; T.mode = 'go'; T.avoidZ = false; T.jamT = 0; }
        else if (want < 0.3 && sp < 0.3) { const off = chTrPick(car, T, g, s, T.avoidZ); if (off !== null) T.off = off; }
      }
    } else {                                   // 가는 중 — 서 있는 것에 막혔으면 피해 간다
      const stat = blk && !zBlk && (blk.kind ? T.jamT > 2.5 : (blk.state === 'parked' || Math.hypot(blk.vx, blk.vz) < 0.25));
      if (want < 0.4 && blk) T.jamT += dt; else T.jamT = Math.max(0, T.jamT - dt * 2);
      if (stat && T.jamT > 1 && (T.pickT -= dt) <= 0) { T.pickT = 0.5; const off = chTrPick(car, T, g, s, false); if (off !== null) { T.mode = 'avoid'; T.off = off; T.avoidZ = false; T.backT = 1.2; } }
    }
    if (T.hitT > 0) want = 0;                  // 맞는 중엔 못 간다
    // 좀비에 막혀 서 있는 시간 → 3~5초면 내린다
    if (sp < 0.6 && (seeZ || zBlk || T.hitT > 0) && T.mode !== 'go') { if ((T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }
    else if (T.mode === 'go') T.zT = Math.max(0, T.zT - dt);
    // 오래 못 가면 (좀비 때문이 아닌데) 돌아서 간다 · 그래도 안 되고 아무도 안 보면 조용히 치운다
    if (sp < 0.3 && !seeZ && !zBlk && T.hitT <= 0) T.stuckT += dt; else T.stuckT = Math.max(0, T.stuckT - dt * 3);
    if (T.stuckT > 7) {
      T.stuckT = 0; T.jamT = 0;
      if (clock - T.uT < 40 && !chTrSeen(car.x, car.z, 6)) { chTrGone(car); T.mode = 'gone'; return; }
      T.uT = clock; const a = T.ai, b = T.aj; T.ci = a; T.cj = b; T.ai = T.bi; T.aj = T.bj; T.bi = a; T.bj = b;   // 유턴: 가던 길을 되돌아간다
      const n = chTrNext(G, T.ai, T.aj, T.bi, T.bj); T.ci = n[0]; T.cj = n[1]; T.g = chTrGeom(G, T); T.off = 0; T.mode = 'go'; T.avoidZ = false;
      return;
    }
    if (want <= 0.05) carSteer(car, 0, 0, CAR_BRAKE * dt);
    else if (want < sp - 0.3) { const k = Math.max(0, sp - CAR_BRAKE * dt) / (sp || 1); car.vx *= k; car.vz *= k; carSteer(car, ux * want, uz * want, CH_TR_ACC * 0.5 * dt); }   // 줄이면서 방향만 조금씩
    else carSteer(car, ux * want, uz * want, CH_TR_ACC * dt);
  }
