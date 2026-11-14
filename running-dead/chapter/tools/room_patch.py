# c53: 건물 안 방 (마트 창고 방 · 병원 방 둘 · 군부대 작은 방 · 경찰서 철창) · 수감자 · 랜덤 시작 자리
ROOM_FN = r"""  // ── c53: 건물 안 방 ──
  //   방 = 건물 안의 작은 건물. 자기 벽·문·지붕이 있고, 안은 따로 떨어진 공간이다 (문이 닫혀 있으면 서로 못 보고 못 때린다).
  //   방문(안쪽 문, L.out = 복도)은 복도로, 쪽문(바깥 문, L.ext)은 건물 밖으로 이어진다. 철창은 벽 너머가 보인다 (시야 벽이 없다)
  function chCutWall(P, L) {                 // 부모 건물 바깥벽에서 방 쪽문 자리를 비운다
    const h = L.w / 2;
    for (let i = P.walls.length - 1; i >= 0; i--) {
      const w = P.walls[i], [ax, az, bx, bz] = w, hz = az === bz;
      if (hz !== !!L.nz) continue;
      if (hz ? Math.abs(az - L.cz) > 1e-6 : Math.abs(ax - L.cx) > 1e-6) continue;
      const lo = hz ? Math.min(ax, bx) : Math.min(az, bz), hi = hz ? Math.max(ax, bx) : Math.max(az, bz), c = hz ? L.cx : L.cz;
      if (c - h < lo - 1e-6 || c + h > hi + 1e-6) continue;
      const a = hz ? [lo, az, c - h, az] : [ax, lo, ax, c - h], b = hz ? [c + h, az, hi, az] : [ax, c + h, ax, hi];
      P.walls.splice(i, 1, a, b);
      const j = walls.indexOf(w); if (j >= 0) walls.splice(j, 1, a, b);
      return true;
    }
    return false;
  }
  // 길 찾기: 밖 — 복도 — 방 (방문) · 밖 — 방 (쪽문). 지금 공간에서 목적지 공간까지 열린 문만 거쳐 가장 짧은 길의 첫 문
  const chFam = (S) => S && (S.parent || S);
  function chDoorsFrom(cur, F) {              // 그 공간에서 지날 수 있는 열린 문 [문, 건너편 공간, 문 주인]
    const out = [];
    if (cur) {
      for (const D of cur.doors) out.push([D, D.out || null, cur]);
      if (cur.rooms) for (const R of cur.rooms) for (const D of R.doors) if (D.out === cur) out.push([D, R, R]);
    } else {
      for (const D of F.doors) out.push([D, F, F]);
      if (F.rooms) for (const R of F.rooms) for (const D of R.doors) if (!D.out) out.push([D, R, R]);
    }
    return out;
  }
  function chNextDoor(S, goal, F, px, pz, tx, tz) {
    let best = null, bl = Infinity;
    const go = (cur, x, z, len, first, used) => {
      if (cur === goal) { const l = len + Math.hypot(tx - x, tz - z); if (l < bl) { bl = l; best = first; } return; }
      if (used.length >= 4 || len >= bl) return;
      for (const e of chDoorsFrom(cur, F)) {
        if (used.includes(e[0])) continue;
        go(e[1], e[0].cx, e[0].cz, len + Math.hypot(e[0].cx - x, e[0].cz - z), first || e, used.concat([e[0]]));
      }
    };
    go(S, px, pz, 0, null, []);
    return best;
  }
  function via0(b, tx, tz) {
    if (b.doorway) {                          // c58: 문틈에 서 있는데 (몸은 아직 그 건물·방 안) 갈 곳이 그 밖이면 먼저 문 밖으로 똑바로 나간다
      const D = b.doorway, B0 = spaceOf(b.foot.x, b.foot.z), to0 = spaceOf(tx, tz);   //   (전엔 문틈에서 '밖'으로 쳐서 벽 너머 목적지로 곧장 가려다 도로 안으로 들어가, 문간에서 왔다 갔다 했다)
      if (B0 && (to0 === (D.out || null) || (!B0.parent && !D.out && to0 !== B0 && !(to0 && to0.parent === B0)))) {   /* 문 너머가 바로 갈 곳이거나, 건물 바깥문에 서 있고 갈 곳이 이 건물 밖 (방의 문은 문 너머가 갈 곳일 때만 — 방 안을 거쳐 가는 길을 되돌리지 않게) */ const rx = b.foot.x - D.cx, rz = b.foot.z - D.cz, m = Math.max(0, (D.w || DOOR) / 2 - BODY - 0.1), al = Math.max(-m, Math.min(m, rx * D.tx + rz * D.tz)); return wp.set(D.cx + D.tx * al + D.nx * LANE, D.cz + D.tz * al + D.nz * LANE); }
    }
    const from = b.space, to = spaceOf(tx, tz), ff = chFam(from), tf = chFam(to);
    if (!((ff && ff.rooms) || (tf && tf.rooms))) return via0_(b, tx, tz);   // 방 없는 건물은 원래대로
    if (from === to) return from ? chInside(b, from, tx, tz) : via0_(b, tx, tz);
    const F = ff || tf, e = chNextDoor(from, tf === F ? to : null, F, b.foot.x, b.foot.z, tx, tz);
    if (!e) return wp.set(b.foot.x, b.foot.z);                               // 갈 길이 없다 (문이 다 닫혀 있다) → 제자리
    const D = e[0], s = from === e[2] ? 1 : -1;                              // 문 주인 쪽에서 나가면 +, 들어가면 −
    const rx = b.foot.x - D.cx, rz = b.foot.z - D.cz, along = rx * D.tx + rz * D.tz;
    const DH = (D.w || DOOR) / 2, lim = Math.max(0, DH - (b.r || BODY) - 0.1), a = Math.max(-lim, Math.min(lim, along));
    const lx = D.cx + D.tx * a, lz = D.cz + D.tz * a;
    if (Math.abs(along) < DH - BODY / 2 && Math.abs(rx * D.nx + rz * D.nz) < LANE) return wp.set(lx + D.nx * LANE * s, lz + D.nz * LANE * s);   // 문을 지나는 중 → 똑바로 건너편으로
    const fx = lx - D.nx * s, fz = lz - D.nz * s;                            // 문 앞 (내 쪽)
    return from ? chInside(b, from, fx, fz) : via0_(b, fx, fz);
  }
  function chInside(b, S, tx, tz) {            // 한 공간 안에서 가기 — 방문 틈에선 먼저 똑바로 나오고, 복도에선 방 모서리를 돌아서
    if (S.rooms) {
      for (const R of S.rooms) for (const D of R.doors) if (D.out === S) {
        const rx = b.foot.x - D.cx, rz = b.foot.z - D.cz, al = rx * D.tx + rz * D.tz, no = rx * D.nx + rz * D.nz, DH = (D.w || DOOR) / 2;
        if (Math.abs(al) < DH && no > -0.7 && no < 0.25) { const lim = Math.max(0, DH - (b.r || BODY) - 0.1), a = Math.max(-lim, Math.min(lim, al)); return wp.set(D.cx + D.tx * a + D.nx * LANE, D.cz + D.tz * a + D.nz * LANE); }
      }
      const c = chCorner(b, S, tx, tz);
      if (c) return insideVia(b, S, c[0], c[1]);
    }
    return insideVia(b, S, tx, tz);
  }
  function chCorner(b, H, tx, tz) {            // 복도에서 가는 길이 방을 가로지르면 그 방 모서리(복도 쪽)를 거쳐서
    const px = b.foot.x, pz = b.foot.z, pad = GAP + 0.05, m = (b.r || BODY) + 0.35;
    let R = null, bt = Infinity;
    for (const Q of H.rooms) {
      if (px > Q.x0 - pad && px < Q.x1 + pad && pz > Q.z0 - pad && pz < Q.z1 + pad) continue;   // 그 방 벽에 붙어 있으면 건너뛴다
      const t = segRect(px, pz, tx, tz, Q, pad);
      if (t < bt) { bt = t; R = Q; }
    }
    if (!R) return null;
    let best = null, bl = Infinity;
    for (const [cx, cz, sx, sz] of [[R.x0, R.z0, -1, -1], [R.x1, R.z0, 1, -1], [R.x1, R.z1, 1, 1], [R.x0, R.z1, -1, 1]]) {
      const x = cx + sx * m, z = cz + sz * m;
      if (!(x > H.x0 + 0.3 && x < H.x1 - 0.3 && z > H.z0 + 0.3 && z < H.z1 - 0.3)) continue;                    // 바깥벽에 붙은 모서리는 못 돈다
      if (H.rooms.some((Q) => x > Q.x0 - 0.2 && x < Q.x1 + 0.2 && z > Q.z0 - 0.2 && z < Q.z1 + 0.2)) continue;   // 옆방 안
      if (Math.hypot(x - px, z - pz) < 0.5) continue;                                                            // 이미 닿은 모서리
      if (segRect(px, pz, x, z, R, pad) < Infinity) continue;                                                    // 그 모서리까지도 방에 막힌다
      const l = Math.hypot(x - px, z - pz) + Math.hypot(tx - x, tz - z);
      if (l < bl) { bl = l; best = [x, z]; }
    }
    return best;
  }
  function chSight(B) {                        // 시야 벽 — 자기 문 + (건물이면) 방 쪽문 자리를 뺀다. 한 벽에 문이 여럿이어도 된다
    const gaps = { n: [], e: [], s: [], w: [] }, all = [];
    for (const D of B.doors) { gaps[D.side].push(D); all.push(D); }
    if (B.rooms) for (const R of B.rooms) for (const D of R.doors) if (!D.out) { gaps[D.side].push(D); all.push(D); }
    const W = [], C = [];
    for (const k of [WALL / 2, -WALL / 2]) {
      const x0 = B.x0 - k, x1 = B.x1 + k, z0 = B.z0 - k, z1 = B.z1 + k;
      C.push([x0, z0], [x1, z0], [x1, z1], [x0, z1]);
      for (const [side, [ax, az, bx, bz]] of Object.entries({ n: [x0, z0, x1, z0], e: [x1, z0, x1, z1], s: [x0, z1, x1, z1], w: [x0, z0, x0, z1] })) {
        const hz = az === bz, G = gaps[side].map((D) => { const h = (D.w || DOOR) / 2, c = hz ? D.cx : D.cz; return [c - h, c + h]; }).sort((p, q) => p[0] - q[0]);
        let cur = hz ? ax : az;
        for (const [g0, g1] of G) { if (hz) { W.push([cur, az, g0, az]); C.push([g0, az], [g1, az]); } else { W.push([ax, cur, ax, g0]); C.push([ax, g0], [ax, g1]); } cur = g1; }
        if (hz) W.push([cur, az, bx, az]); else W.push([ax, cur, ax, bz]);
      }
    }
    for (const D of all) { const h = (D.w || DOOR) / 2; for (const sg of [-1, 1]) { const px = D.cx + D.tx * h * sg, pz = D.cz + D.tz * h * sg; W.push([px - D.nx * WALL / 2, pz - D.nz * WALL / 2, px + D.nx * WALL / 2, pz + D.nz * WALL / 2]); } }
    B.sightW = W; B.sightC = C;
  }
  function rebuildSight(B) {
    if (!(B.parent || B.rooms)) { rebuildSight0(B); return; }
    if (B.type === 'jail') { B.sightW = []; B.sightC = []; return; }   // 철창 = 시야가 뚫린다
    chSight(B);
    if (B.parent) chSight(B.parent);           // 방 쪽문이 열리면 건물 바깥벽 시야도 뚫린다
  }
  function chRoomDraw() {                      // 방 안쪽 벽·방문은 건물 지붕이 열렸을 때만 보인다 · 방이 (쪽문으로) 열리면 건물 지붕도 연다
    for (const R of chRooms) {
      const P = R.parent;
      if (R.open && !P.open) { P.open = true; P.roof.visible = false; if (P.sign) P.sign.visible = false; }
      for (const m of R.inner) m.visible = P.open;
      for (const L of R.locks) if (L.out) { const o = L.obj; o.mesh.visible = P.open && !o.dead; o.gap.visible = P.open && o.dead; }
    }
  }
  function chRoomPush(x, y, mine) {            // 동료 자리가 (내가 없는) 방 안에 걸리면 방 밖 복도로
    const m = 0.7;
    for (const R of chRooms) {
      const P = R.parent;
      if (R === mine || !(x > P.x0 && x < P.x1 && y > P.z0 && y < P.z1)) continue;
      if (x <= R.x0 - m || x >= R.x1 + m || y <= R.z0 - m || y >= R.z1 + m) continue;
      const c = [];
      if (R.x0 - P.x0 > 0.5) c.push([x - (R.x0 - m), R.x0 - m, y]);
      if (P.x1 - R.x1 > 0.5) c.push([R.x1 + m - x, R.x1 + m, y]);
      if (R.z0 - P.z0 > 0.5) c.push([y - (R.z0 - m), x, R.z0 - m]);
      if (P.z1 - R.z1 > 0.5) c.push([R.z1 + m - y, x, R.z1 + m]);
      const ok = c.filter((q) => !chRooms.some((Q) => Q !== R && Q.parent === P && q[1] > Q.x0 - 0.3 && q[1] < Q.x1 + 0.3 && q[2] > Q.z0 - 0.3 && q[2] < Q.z1 + 0.3));
      if (!ok.length) continue;
      const b = ok.reduce((p, q) => (q[0] < p[0] ? q : p));
      x = b[1]; y = b[2];
    }
    return [x, y];
  }
  function chOpenDoor(o) {                     // 부수는 것과 같되 조각·먼지 없이 — 처음부터 뚫려 있는 방문 (문짝이 없다)
    const B = o.B, i = walls.indexOf(o.seg), j = B.walls.indexOf(o.seg);
    o.dead = true; if (o.hpBar) o.hpBar.visible = false;
    if (i >= 0) walls.splice(i, 1);
    if (j >= 0) B.walls.splice(j, 1);
    if (!B.doors.includes(o.L)) B.doors.push(o.L);
    rebuildSight(B); o.mesh.visible = false; o.gap.visible = true;
  }
  function chRoomDoors() { for (const R of chRooms) if (R.type === 'room') for (const L of R.locks) if (L.out && Math.random() < 0.5) chOpenDoor(L.obj); }   // 건물 안 방문은 판마다 반은 뚫려 있다
  function chSafeGap(B, x, z, r) {             // 금고 자리가 방·방문 앞에서 얼마나 떨어졌나 (0보다 작으면 걸친다)
    let g = Infinity;
    for (const R of B.rooms) {
      g = Math.min(g, Math.max(R.x0 - x, x - R.x1, R.z0 - z, z - R.z1) - (r + 0.5));
      for (const L of R.locks) if (L.out) g = Math.min(g, Math.hypot(x - (L.cx + L.nx * 1.2), z - (L.cz + L.nz * 1.2)) - (r + 1.0));
    }
    return g;
  }
  function chSafeSpot(B, s) {                  // 금고는 방과 방문 앞을 피해서 — 무작위로 찾고, 안 되면 격자로 훑어 가장 떨어진 곳
    if (chSafeGap(B, s.foot.x, s.foot.z, s.r) >= 0) return;
    const m = 1.6;
    for (let t = 0; t < 120; t++) { const x = rand(B.x0 + m, B.x1 - m), z = rand(B.z0 + m, B.z1 - m); if (chSafeGap(B, x, z, s.r) >= 0) { s.foot.x = x; s.foot.z = z; return; } }
    let best = null, bg = -Infinity;
    for (let x = B.x0 + m; x <= B.x1 - m + 1e-6; x += 0.4) for (let z = B.z0 + m; z <= B.z1 - m + 1e-6; z += 0.4) { const g = chSafeGap(B, x, z, s.r); if (g > bg) { bg = g; best = [x, z]; } }
    if (best) { s.foot.x = best[0]; s.foot.z = best[1]; }
  }
  function chStart() {                         // 시작 자리 = 아무 구역(네 구역 같은 확률)의 바깥 라인 아무 데 — 문이 내 인지거리 밖이고 건물·강·산에 붙지 않은 곳. 경찰서 둘레(배회 경찰 자리)는 피한다
    const far = (x, z) => objs.every((o) => { if (o.type !== 'door' || o.off || o.dead) return true; const p = nearestOn(o.seg, x, z); return Math.hypot(x - p.x, z - p.y) > SIGHT + 0.8; });
    const cop = (x, z) => buildings.some((B) => B.type === 'police' && Math.max(B.x0 - x, x - B.x1, B.z0 - z, z - B.z1, 0) < 20);
    const order = CH_MAP.zones.map((Z, i) => i); for (let i = order.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }   // 고르게 섞는다
    for (const zi of order) for (let t = 0; t < 800; t++) {
      const [x0, z0, x1, z1] = CH_MAP.zones[zi], W = x1 - x0 - 5, H = z1 - z0 - 5, q = Math.random() * 2 * (W + H), j = rand(0, 3.5);
      const [x, z] = q < W ? [x0 + 2.5 + q, z0 + 2.5 + j] : q < W + H ? [x1 - 2.5 - j, z0 + 2.5 + (q - W)] : q < 2 * W + H ? [x1 - 2.5 - (q - W - H), z1 - 2.5 - j] : [x0 + 2.5 + j, z1 - 2.5 - (q - 2 * W - H)];
      if (chNearRiver(x, z, 2) || buildings.some((B) => x > B.x0 - 1.5 && x < B.x1 + 1.5 && z > B.z0 - 1.5 && z < B.z1 + 1.5) || cop(x, z) || !far(x, z)) continue;
      if (buildings.some((B) => B.doors.some((D) => !D.out) && Math.max(B.x0 - x, x - B.x1, B.z0 - z, z - B.z1, 0) < SIGHT * 1.1 + 1.5)) continue;   // 뚫린 문(차고) 건물은 건물째로 시야 밖에 둔다 — c58부터 문이 뚫린 건물은 안팎이 한 공간이라 벽 너머 사람도 나를 알아챈다
      return [x, z];
    }
    return CH_MAP.start;
  }
  const CH_PINK = 0xff5fa8;
  function chBoss(B, type, x, z) {             // 변이 좀비가 되는 사람 — 덩치 좀비만 한 몸, 무기 없이 주황처럼 때린다 (넉백 없음). 덩치형: 체력 4배·공격력 2배 / 히드라형: 체력 2배·공격력 4배 (자경단 기준). 머리 위 변이 주사 색 다이아몬드
    const c = chPut(x, z, B, 'attacker', B);
    c.boss = type; c.mesh.material.color.setHex(CH_PINK);   // c55: 변이 좀비가 될 사람은 분홍
    if (type === 'armor') { c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5); }   // c55: 덩치가 될 사람만 크다 — 히드라가 될 사람은 보통 크기 (다이아몬드로 알아본다)
    c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2); c.hpDisp = c.hp; c.dmgK = type === 'armor' ? 2 : 4;
    const g = new THREE.Group();
    const mk = (sz, col, zz) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(sz, sz), new THREE.MeshBasicMaterial({ color: col, transparent: true, depthTest: false, depthWrite: false })); m.rotation.z = Math.PI / 4; m.position.z = zz; m.renderOrder = 1; return m; };
    g.add(mk(0.38, 0x1c1c1e, 0), mk(0.27, 0xb05cff, 0.002)); g.position.set(0, 0.5, 0.02);
    c.mesh.add(g); c.gem = g;
    return c;
  }
  function chPrisoner(J) { return chBoss(J, J.parent.type === 'army' ? 'hydra' : Math.random() < 0.5 ? 'armor' : 'hydra', (J.x0 + J.x1) / 2, (J.z0 + J.z1) / 2); }   // 철창 수감자 1명 — 경찰서: 덩치·히드라 반반 / 군부대: 히드라
  function chBossTurn(b) {                     // 감염됐다 → 영구 변이 (덩치는 덩치 크기, 히드라는 보통 크기) + 검은 테두리
    const t = b.boss; b.boss = null; b.dmgK = 0;
    if (b.gem) { b.mesh.remove(b.gem); b.gem = null; }
    b.r = BODY; delete b.halfH; b.mesh.scale.setScalar(1);
    mutate(b, t);   // c56: 검은 테두리는 뺐다 (테두리는 변이한 나만)
  }
  function chSafeInRoom(s, R) {                // c54: 금고를 방 안에 — 방문에서 가장 먼 자리. 작은 방이면 그 방 사람은 복도로 옮긴다
    const D = R.locks.find((L) => L.out) || R.locks[0], m = s.r + 0.3;
    let best = [(R.x0 + R.x1) / 2, (R.z0 + R.z1) / 2], bd = -1;
    for (let x = R.x0 + m; x <= R.x1 - m + 1e-6; x += 0.25) for (let z = R.z0 + m; z <= R.z1 - m + 1e-6; z += 0.25) { const d = Math.hypot(x - D.cx, z - D.cz); if (d > bd) { bd = d; best = [x, z]; } }
    s.foot.x = best[0]; s.foot.z = best[1]; s.room = R; R.safe = s;
    if ((R.x1 - R.x0) * (R.z1 - R.z0) < 12) for (const c of bodies) if (c.kind === 'citizen' && c.space === R) { const P = R.parent, g = pickGoal(P); c.foot.x = g.x; c.foot.z = g.y; c.space = P; c.home = P; c.area = P; if (c.post) c.post = P; c.goal = null; }
  }
"""
LINK = r"""  const chRooms = buildings.filter((B) => B.rspec);   // c53: 방 (건물 안의 작은 건물) — 목록에서는 부모 건물 뒤에 온다
  for (const R of chRooms) {
    const P = R.parent = buildings[R.pidx]; (P.rooms = P.rooms || []).push(R);
    for (const k of ['x0', 'z0', 'x1', 'z1']) if (Math.abs(R[k] - P[k]) < 0.02) R[k] = P[k];   // 바깥벽에 붙은 변은 부모 벽과 똑같은 값으로
    for (const L of R.locks) {
      L.cx = L.nx > 0 ? R.x1 : L.nx < 0 ? R.x0 : (R.x0 + R.x1) / 2; L.cz = L.nz > 0 ? R.z1 : L.nz < 0 ? R.z0 : (R.z0 + R.z1) / 2;
      if (!L.ext) L.out = P;
    }
  }
"""
INNER = r"""  const chBarMat = flatMat(0x2a2e35);          // c53: 방 안쪽 벽 · 철창 창살 — 건물 지붕이 열렸을 때만 보인다 (chRoomDraw)
  for (const R of chRooms) {
    R.inner = [];
    for (const [ax, az, bx, bz] of R.walls) {
      const P = R.parent, hz = az === bz;
      if (hz ? (Math.abs(az - P.z0) < 1e-6 || Math.abs(az - P.z1) < 1e-6) : (Math.abs(ax - P.x0) < 1e-6 || Math.abs(ax - P.x1) < 1e-6)) continue;   // 바깥벽 쪽은 건물 벽이 이미 그린다
      if (R.type !== 'jail') { R.inner.push(flat(Math.abs(bx - ax) + WALL, Math.abs(bz - az) + WALL, (ax + bx) / 2, (az + bz) / 2, wallMat, -0.505)); continue; }
      const len = Math.hypot(bx - ax, bz - az), n = Math.max(1, Math.round(len / 0.45));   // 철창 = 가는 가로대 + 굵은 창살 (벽과 달리 사이가 비어 보인다)
      R.inner.push(flat(hz ? len : 0.09, hz ? 0.09 : len, (ax + bx) / 2, (az + bz) / 2, chBarMat, -0.505));
      for (let i = 0; i <= n; i++) R.inner.push(flat(0.24, 0.24, ax + (bx - ax) * i / n, az + (bz - az) * i / n, chBarMat, -0.5045));
    }
  }
"""
POP_OLD = "      if (T) { for (const [type, lo, hi] of T) { let k = R2(lo, hi); if (B.type !== 'store' && (type === '' || type === 'guard')) k = Math.round(k * 2 / 3);   /* c49: 랜드마크 하양·노랑 3분의 1 줄임 */ for (let i = 0; i < k; i++) inPut(B, type); } continue; }"
POP_NEW = r"""      if (T) {
        const list = [];
        for (const [type, lo, hi] of T) { let k = R2(lo, hi); if (B.type !== 'store' && (type === '' || type === 'guard')) k = Math.round(k * 2 / 3);   /* c49: 랜드마크 하양·노랑 3분의 1 줄임 */ for (let i = 0; i < k; i++) list.push(type); }
        for (const R of B.rooms || []) {        // c53: 방 안 — 그 건물 사람 중 몇 명 (없을 수도 있다). 경찰·저격수는 방에 안 들어간다. 철창엔 수감자 1명
          if (R.type === 'jail') { chPrisoner(R); continue; }
          const cap = Math.max(1, Math.floor((R.x1 - R.x0) * (R.z1 - R.z0) / 4.5)), pool = list.map((t, i) => i).filter((i) => list[i] !== null && list[i] !== 'police' && list[i] !== 'sniper');
          for (let n = R2(0, cap); n > 0 && pool.length; n--) { const i = pool.splice(Math.floor(Math.random() * pool.length), 1)[0]; inPut(R, list[i]); list[i] = null; }
        }
        for (const type of list) if (type !== null) inPut(B, type);
        if (B.type === 'gym') { let g = pickGoal(B); for (let t = 0; t < 30 && bodies.some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.4); t++) g = pickGoal(B); chBoss(B, 'armor', g.x, g.y); }   // c54: 헬스장 관장 — 갇혀 있지 않다. 감염시키면 영구 덩치
        continue;
      }"""
ROOM_R = [
  ("type: s.t || '', zone: s.zone, sideK: s.sideK, garage: !!s.garage };", "type: s.t || '', zone: s.zone, sideK: s.sideK, garage: !!s.garage, rspec: s.room || null, pidx: s.parent };"),
  ("    B.front = B.doors.find((o) => o.side === 's') || B.locks.find((o) => o.side === 's');", "    if (s.room) for (const L of B.locks) { const q = s.room.doors.find((d) => d.s === L.side); L.w = q.w; L.ext = !!q.ext; }   // c53: 방문 폭 · 바깥 쪽문\n    B.front = B.doors.find((o) => o.side === 's') || B.locks.find((o) => o.side === 's');"),
  ("  const walls = [];                           // [ax, az, bx, bz]", LINK + "  const walls = [];                           // [ax, az, bx, bz]"),
  ("    B.walls = walls.slice(n0);                // 이 건물 벽만 — 부딪힘 볼 때 먼 건물은 건너뛰게 (v121)\n  }\n", "    B.walls = walls.slice(n0);                // 이 건물 벽만 — 부딪힘 볼 때 먼 건물은 건너뛰게 (v121)\n  }\n  for (const R of chRooms) for (const L of R.locks) if (L.ext) chCutWall(R.parent, L);   // c53: 방 쪽문 자리는 건물 바깥벽도 비운다\n"),
  ("  for (const [ax, az, bx, bz] of buildings.flatMap((B) => (B.type === 'hill' ? [] : B.walls))) flat(", INNER + "  for (const [ax, az, bx, bz] of buildings.flatMap((B) => (B.type === 'hill' || B.parent ? [] : B.walls))) flat("),
  ("  const spaceOf = (x, z) => buildings.find((B) => x > B.x0 && x < B.x1 && z > B.z0 && z < B.z1) || null;", "  const chIn = (B, x, z) => x > B.x0 && x < B.x1 && z > B.z0 && z < B.z1;\n  const spaceOf = (x, z) => chRooms.find((B) => chIn(B, x, z)) || buildings.find((B) => chIn(B, x, z)) || null;   /* c53: 방이 먼저 */"),
  ("      if (along < (D.w || DOOR) / 2 && depth < 0.6) { b.doorway = D; return null; }", "      if (along < (D.w || DOOR) / 2 && depth < 0.6) { b.doorway = D; return D.out || null; }   /* c53: 방문 틈 = 복도 */"),
  ("    if (space) return x > space.x0 + 0.6 && x < space.x1 - 0.6 && z > space.z0 + 0.6 && z < space.z1 - 0.6;", "    if (space) return x > space.x0 + 0.6 && x < space.x1 - 0.6 && z > space.z0 + 0.6 && z < space.z1 - 0.6 && !(space.rooms && space.rooms.some((R) => x > R.x0 - 0.6 && x < R.x1 + 0.6 && z > R.z0 - 0.6 && z < R.z1 + 0.6));   /* c53: 복도 = 방을 뺀 곳 */"),
  ("  function via0(b, tx, tz) {", "  function via0_(b, tx, tz) {"),
  ("      const t = segRect(px, pz, tx, tz, B, pad);", "      if (B.parent) continue;   // c53: 방은 건물 안이라 밖 길 찾기에서 뺀다\n      const t = segRect(px, pz, tx, tz, B, pad);"),
  ("      if (a.doors || freeSpot(g.x, g.y, null)) break;", "      if (a.doors ? !(a.rooms && a.rooms.some((R) => g.x > R.x0 - 0.6 && g.x < R.x1 + 0.6 && g.y > R.z0 - 0.6 && g.y < R.z1 + 0.6)) : freeSpot(g.x, g.y, null)) break;   // c53: 복도 자리는 방을 피해서"),
  ("  const linked = (a, b) => a === b || (!a ? b.doors.length > 0 : !b ? a.doors.length > 0 : false);", "  const linked = (a, b) => a === b || (a && b ? (a.parent === b ? a.doors.some((D) => D.out === b) : b.parent === a ? b.doors.some((D) => D.out === a) : false) : (a || b).parent ? (a || b).doors.some((D) => !D.out) : (a || b).doors.length > 0);   /* c53: 복도 ↔ 방(방문), 밖 ↔ 방(쪽문)도 */"),
  ("    return !!B && Math.min(c.foot.x - B.x0, B.x1 - c.foot.x) < CORNER && Math.min(c.foot.z - B.z0, B.z1 - c.foot.z) < CORNER;", "    return !!B && !B.rooms && Math.min(c.foot.x - B.x0, B.x1 - c.foot.x) < CORNER && Math.min(c.foot.z - B.z0, B.z1 - c.foot.z) < CORNER;   /* c53: 방이 있는 복도는 벽 타고 돌지 않는다 */"),
  ("    if (!B) { enterPanic(c, null, true); c.tick = 0; return; }   // 문 밖으로 나왔다", "    if (!B || !B.doors.includes(c.door)) { enterPanic(c, null, true); c.tick = 0; return; }   // 문 밖으로 나왔다 (c53: 방에서 복도로 나온 것도)"),
  ("      B.open = eyes.some((z) => z.space === B) || B.doors.some((D) => { const ox = D.cx + D.nx * 0.4, oz = D.cz + D.nz * 0.4; return eyes.some((z) => !z.space && Math.hypot(z.foot.x - ox, z.foot.z - oz) <= z.sense && !blocked(z.foot.x, z.foot.z, ox, oz)); });",
   "      B.open = eyes.some((z) => z.space === B || (B.rooms && z.space && z.space.parent === B)) || B.doors.some((D) => { const ox = D.cx + D.nx * 0.4, oz = D.cz + D.nz * 0.4; return eyes.some((z) => (D.out ? z.space === D.out : !z.space) && Math.hypot(z.foot.x - ox, z.foot.z - oz) <= z.sense && !blocked(z.foot.x, z.foot.z, ox, oz)); }); if (B.type === 'jail') B.open = B.parent.open;   /* c53: 방 안에 있어도 건물 지붕은 열린다 · 방문은 복도에서 본다 · 철창은 건물과 같이 열린다 */"),
  ("      B.roof.visible = !B.open;", "      B.roof.visible = !B.open && B.type !== 'jail';"),
  ("        D.see.visible = eyes.some((z) => !z.space && Math.hypot(", "        D.see.visible = eyes.some((z) => (D.out ? z.space === D.out : !z.space) && Math.hypot("),
  ("    updateViewRect();\n    drawVision(eyes);", "    if (CHAPTER) chRoomDraw();   // c53\n    updateViewRect();\n    drawVision(eyes);"),
  ("  function rebuildSight(B) {                  // v357", "  function rebuildSight0(B) {                  // v357"),
  ("    const h = DOOR / 2, seg = L.nz ? [L.cx - h, L.cz, L.cx + h, L.cz] : [L.cx, L.cz - h, L.cx, L.cz + h];\n    const along = L.nz ? [DOOR, WALL * 2.2] : [WALL * 2.2, DOOR];",
   "    const LW = L.w || DOOR, h = LW / 2, seg = L.nz ? [L.cx - h, L.cz, L.cx + h, L.cz] : [L.cx, L.cz - h, L.cx, L.cz + h];   /* c53: 문마다 폭 */\n    const along = L.nz ? [LW, WALL * 2.2] : [WALL * 2.2, LW];"),
  ("    const bar = new THREE.Mesh(new THREE.PlaneGeometry(L.nz ? DOOR * 0.8 : WALL * 0.8, L.nz ? WALL * 0.8 : DOOR * 0.8).rotateX(-Math.PI / 2), lockBarMat);", "    const bar = new THREE.Mesh(new THREE.PlaneGeometry(L.nz ? LW * 0.8 : WALL * 0.8, L.nz ? WALL * 0.8 : LW * 0.8).rotateX(-Math.PI / 2), lockBarMat);"),
  ("      if (o.type === 'car' ? z.space : (z.space && z.space !== o.B)) continue;", "      if (o.type === 'car' ? z.space : (z.space ? z.space !== o.B && z.space !== o.L.out : !!o.L.out)) continue;   /* c53: 방문은 복도·방 안에서, 쪽문은 밖·방 안에서 */"),
  ("      if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5;   // c46: 랜드마크 문 체력 1.5배", "      if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5;   // c46: 랜드마크 문 체력 1.5배\n      if (CHAPTER && B.parent) o.hp = o.maxHp = MY_DAMAGE * 3.5 * (o.L.ext || B.type === 'jail' ? 1.5 : 1);   // c53: 방문 = 집 문 · 바깥 쪽문·철창 문 = 랜드마크 문"),
  ("      o.hpBar.visible = !o.dead && o.hp < o.maxHp;", "      o.hpBar.visible = !o.dead && o.hp < o.maxHp && !(o.L && o.L.out && !o.L.out.open);   // c53: 방문 체력바는 건물 지붕이 열렸을 때만"),
  ("      const D = DS.reduce((a, o) => Math.hypot(o.cx - car.x, o.cz - car.z) < Math.hypot(a.cx - car.x, a.cz - car.z) ? o : a);", "      const D = (DS.length ? DS : B.locks).reduce((a, o) => Math.hypot(o.cx - car.x, o.cz - car.z) < Math.hypot(a.cx - car.x, a.cz - car.z) ? o : a);   /* c53: 쓸 문이 하나도 없어도 멈추지 않게 */"),
  ("    const B = spaceOf(tx, tz);\n    if (B) {\n      const DS = B.doors.length ? B.doors :", "    let B = spaceOf(tx, tz); if (B && B.parent) B = B.parent;   // c53: 방 안이면 그 건물 문 앞으로\n    if (B) {\n      const DS = B.doors.length ? B.doors :"),
  ("    if (B && B.safe && !B.safe.dead) {        // v295: 건물 안 자리가 금고 위에 걸리면 금고 밖으로", "    if (CHAPTER && chRooms.length) { const f = chRoomPush(x, y, B); x = f[0]; y = f[1]; }   // c53: 방 안에 걸린 자리는 복도로\n    if (B && B.safe && !B.safe.dead) {        // v295: 건물 안 자리가 금고 위에 걸리면 금고 밖으로"),
  ("DAMAGE * (CHAPTER && b.attacker ? (b.vig ? 2 : 1.5) : 1))", "DAMAGE * (CHAPTER && b.attacker ? (b.vig || b.boss ? 2 : 1.5) : 1) * (b.dmgK || 1))"),
  ("  function mutate(z) {\n", "  function mutate(z, force) {   /* c53: force = 정해진 변이를 영구로 (철창 수감자) */\n"),
  ("    const type = TEST_ARMOR || CAR_TEST ? 'armor' : Math.random() < 0.5 ? 'armor' : 'hydra';\n    z.mut = type; z.mutT = MUT_T();", "    const type = force || (TEST_ARMOR || CAR_TEST ? 'armor' : Math.random() < 0.5 ? 'armor' : 'hydra');\n    z.mut = type; z.mutT = force ? Infinity : MUT_T(); z.mutPerm = !!force;"),
  ("    const al = nearAllies();\n    if (!al.length) return false;", "    const al = nearAllies().filter((z) => !z.mutPerm);   // c53: 영구 변이는 건드리지 않는다\n    if (!al.length) return false;"),
  ("    b.foe = null;\n    assignSlots();\n  }", "    b.foe = null;\n    if (CHAPTER && b.boss) chBossTurn(b);   // c53: 수감자 → 영구 변이\n    assignSlots();\n  }"),
  ("me.foot.set(CH_MAP.start[0], 0, CH_MAP.start[1]); me.space = null;", "chRoomDoors(); { const st = chStart(); me.foot.set(st[0], 0, st[1]); } me.space = null;   /* c53: 방문 반은 열어 두고, 시작 자리는 아무 구역 바깥 라인 */"),
  (POP_OLD, POP_NEW),
  ("      if (B.type === 'hill' || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;\n      addSafe(B);\n      const s = B.safe; s.B = B; s.loot = chLoot(B.type); s.dud = !s.loot;",
   "      if (B.type === 'hill' || B.parent || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;\n      addSafe(B);\n      const s = B.safe; s.B = B; s.loot = chLoot(B.type); s.dud = !s.loot;\n      s.room = null;\n      if (B.rooms) { const rs = B.rooms.filter((R) => R.type === 'room'); if (rs.length && Math.random() < 0.5) chSafeInRoom(s, rs[Math.floor(Math.random() * rs.length)]); else chSafeSpot(B, s); }   // c53: 금고는 방과 방문 앞을 피해서 · c54: 방이 있는 건물은 반반 확률로 방 안"),
  ("        if (c.kind !== 'citizen' || c.space !== B) continue;\n        const dx = c.foot.x - s.foot.x, dz = c.foot.z - s.foot.z, d = Math.hypot(dx, dz), R = s.r + BODY + 0.1;", "        if (c.kind !== 'citizen' || c.space !== (s.room || B)) continue;   /* c54: 금고가 방 안이면 그 방 사람 */\n        const dx = c.foot.x - s.foot.x, dz = c.foot.z - s.foot.z, d = Math.hypot(dx, dz), R = s.r + BODY + 0.1;"),
  ("        c.foot.x = Math.max(B.x0 + 0.6, Math.min(B.x1 - 0.6, s.foot.x + ux * R)); c.foot.z = Math.max(B.z0 + 0.6, Math.min(B.z1 - 0.6, s.foot.z + uz * R));", "        { const Q = s.room || B; c.foot.x = Math.max(Q.x0 + 0.6, Math.min(Q.x1 - 0.6, s.foot.x + ux * R)); c.foot.z = Math.max(Q.z0 + 0.6, Math.min(Q.z1 - 0.6, s.foot.z + uz * R)); }"),
  ("          c.foot.x = rand(B.x0 + 0.6, B.x1 - 0.6); c.foot.z = rand(B.z0 + 0.6, B.z1 - 0.6);", "          { const g = pickGoal(s.room || B); c.foot.x = g.x; c.foot.z = g.y; }   /* c53: 방을 피해서 · c54: 금고가 방 안이면 그 방 안에서 */"),
  ("      if (B.type === 'house' || B.type === 'hill') continue;             // 집과 산은 표시 없음", "      if (B.type === 'house' || B.type === 'hill' || B.parent) continue;             // 집과 산은 표시 없음 (c53: 방도)"),
  ("      B.roof.material = flatMat(B.type === 'house' ? CH_HOUSE_ROOF[i % CH_HOUSE_ROOF.length] : CH_DEF[B.type].roof);\n      if (B.type === 'house') return;", "      B.roof.material = flatMat(B.type === 'house' ? CH_HOUSE_ROOF[i % CH_HOUSE_ROOF.length] : CH_DEF[(B.parent || B).type].roof);   /* c53: 방 지붕 = 그 건물 지붕 색 */\n      if (B.type === 'house' || B.parent) return;"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, rooms: chRooms, spaceOf, linked, chStart, mutate, openDoor: chOpenDoor,"),
  ("  function showDud() {", ROOM_FN + "  function showDud() {"),   # 맨 끝에 — 위의 이름 바꾸기(via0 · rebuildSight)가 먼저 돼야 한다
]
