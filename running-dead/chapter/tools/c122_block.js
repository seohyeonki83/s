  // ── c122: 특공대는 시간으로 온다 (감염 수와 상관없이) + 다섯 번째는 보스 (군부대 — 장갑차) ──
  //   시계는 난리남이 뜨는 순간 돈다. 수상함이 뜨고 3분이 지나도 난리남이 안 뜨면 그때 강제로 돈다.
  //   2분마다 한 번: 1~4번째 = 특공대 (갈수록 세다), 5번째(10분) = 군부대 (장갑차 + 저격수 5 + 군인 15).
  //   장갑차가 살아 있는 동안은 40초마다 4번째 특공대(군인차 한 대)가 계속 온다. 장갑차 · 같이 온 호위 · 그 뒤에 온 군인을 다 잡으면 승리.
  //   장갑차: 군인차의 2배 크기 · 사람이 안 내린다 · 체력 = 경찰차의 10배 · 미는 힘 = 보통 차의 4배 · 속도 = 보통 차의 4분의 1.
  //           기관포 = 군인처럼 4발 연사, 사거리는 저격수, 한 발이 군인의 2배 + 둘레 스플래시 + 넉백 2배. 20초마다 좀비가 가장 많은 쪽으로 0.3초 돌진.
  //           건물·사물을 피해 다니지 않는다 — 사물은 깔아뭉개고, 벽은 비비다가 부순다 (벽 조각 단위, 체력 표시 없음). 산·강만 못 넘는다.
  const CH_SF_GAP = 120, CH_SF_FORCE = 180, CH_SF_WAVE = 40, CH_TK_K = MIL_K * 2, CH_TK_ESC = 2.6, CH_TK_DASH_EVERY = 20, CH_TK_DASH_T = 0.3, CH_TK_SPLASH = 1.2, CH_TK_WALL_T = 2.4, CH_TK_HOLE = 2.3;
  const chSf = { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0, shown: '' };
  const chBanner = [], chCuts = [], chTkBuf = [], chTkBuf2 = [];
  let chTank = null;
  const chSfEl = document.createElement('div');
  chSfEl.id = 'sfcd';
  chSfEl.style.cssText = 'position:absolute;left:0;right:0;top:calc(66px + env(safe-area-inset-top, 0px));z-index:4;pointer-events:none;text-align:center;font:800 13px/1 system-ui,sans-serif;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,0.9);display:none';
  stage.appendChild(chSfEl);
  function chSfHud() {
    let s = '';
    if (chSf.on && !chSf.boss) {
      const left = Math.max(0, Math.ceil(CH_SF_GAP * (chSf.n + 1) - chSf.T));
      s = chSf.n < 4 ? '특공대 도착까지 ' + left + '초' : '<b style="color:#ff4a3a">보스</b> 군부대 도착까지 ' + left + '초';
    }
    if (s !== chSf.shown) { chSf.shown = s; chSfEl.innerHTML = s; chSfEl.style.display = s ? 'block' : 'none'; }
  }
  function chSfReset() {
    Object.assign(chSf, { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0 });
    chBanner.length = 0;
    if (chTank && chTank.tracer) scene.remove(chTank.tracer);
    chTank = null;
    chWallRestore();
    chSfHud();
  }
  function chSfTick(dt) {
    if (!chSf.on) {
      if (stars >= 2) chSf.on = true;                                             // 난리남
      else if (stars >= 1 && (chSf.susT += dt) >= CH_SF_FORCE) chSf.on = true;    // 수상함에서 3분 버팀 → 강제
    } else if (!chSf.boss) {
      chSf.T += dt;
      while (!chSf.boss && chSf.T >= CH_SF_GAP * (chSf.n + 1)) {
        chSf.n++;
        if (chSf.n <= 4) chQueueTeam(chSf.n - 1);
        else { chSf.boss = true; teamsSpawned++; chBanner.push('boss'); teamWait.push({ boss: true, t: 0, seg: teamSeg(), hold: true }); }
      }
    } else {
      const T = chTank;
      if (T && !T.wreck && (chSf.waveT += dt) >= CH_SF_WAVE) { chSf.waveT -= CH_SF_WAVE; teamWait.push({ car: [S_, G_, G_, G_, S_, G_, G_], t: 0, seg: teamSeg(), tk: true }); }
      if (T && T.wreck && !chSf.won && (chSf.chk -= dt) <= 0) {
        chSf.chk = 0.5;
        if (!teamWait.some((w) => w.tk || w.boss) && !cars.some((c) => c.tkWave && !c.wreck && c.state !== 'parked') && !bodies.some((b) => b.kind === 'citizen' && b.tkU)) chSf.won = true;
      }
    }
    chSfHud();
  }
  function chTankMaster(c) {                   // 군부대 호위: 군인 → 제 저격수 (죽으면 장갑차) · 저격수 → 장갑차 · 장갑차가 죽으면 아무도 호위 안 한다
    const T = chTank;
    if (!T || T.wreck) { c.master = null; return null; }
    const m = c.master;
    if (c.soldier && m && m.kind === 'citizen' && m.sniper && bodies.includes(m)) return m;
    if (m !== T) { c.master = T; c.slotA = Math.random() * Math.PI * 2; c.slotK = rand(0.85, 1); }
    return T;
  }
  function chBossSpawn(seg) {
    const p = teamSpot(seg), h = Math.atan2(me.foot.z - p.z, me.foot.x - p.x);
    addCar(p.x, p.z, h, null, 0, ['tank']);
    const car = cars[cars.length - 1], K = car.g.children;
    car.squad = null; car.tank = true; car.state = 'tank'; car.kl = car.kw = CH_TK_K; car.massK = 4; car.hpK = 10;
    car.g.scale.set(CH_TK_K, 1, CH_TK_K);
    K[0].material.color.setHex(0x3c4a2a); K[1].visible = K[2].visible = K[3].visible = false;
    const tur = new THREE.Mesh(new THREE.CircleGeometry(0.27, 20).rotateX(-Math.PI / 2), carMat(0x222b16)); tur.position.y = 0.002; tur.renderOrder = -0.44;
    const brl = new THREE.Mesh(new THREE.PlaneGeometry(0.72, 0.09).rotateX(-Math.PI / 2), carMat(0x161c0e)); brl.position.set(0.5, 0.003, 0); brl.renderOrder = -0.435;
    for (const sd of [-1, 1]) { const tr = new THREE.Mesh(new THREE.PlaneGeometry(CAR_L * 0.96, 0.13).rotateX(-Math.PI / 2), carMat(0x1a2010)); tr.position.set(0, 0.001, sd * (CAR_W / 2 - 0.065)); tr.renderOrder = -0.445; car.g.add(tr); }
    car.g.add(tur, brl);
    chCarObj(car, false); car.obj.oneBar = true;
    Object.assign(car, { tkV: 1, atkT: 1, burstN: 0, burstT: 0, burstZ: null, dashAt: CH_TK_DASH_EVERY, dashT: 0, tkSegs: [], scanT: 0, foe: null, shotT: -1, shotX: 0, shotZ: 0, rubBack: 0, rubCool: 0, crT: 0, goo: false, gooT: 0 });
    car.gun = { kind: 'tank', foot: car.foot };
    car.tracer = new THREE.Mesh(tracerGeo, new THREE.MeshBasicMaterial({ color: 0xffb84d, transparent: true, depthTest: false, depthWrite: false }));
    car.tracer.renderOrder = -0.5; car.tracer.visible = false; scene.add(car.tracer);
    chTank = car;
    const mk = (type, x, z) => { if (!freeSpot(x, z, null)) { x = p.x; z = p.z; } const c = addCitizen(x, z, square(x, z), type); c.met = true; c.tkU = c.tkE = true; c.tick = 0; return c; };
    for (let i = 0; i < 5; i++) {
      const a = h + i / 5 * Math.PI * 2, R = GUARD_NEAR * CH_TK_ESC, sx = p.x + Math.cos(a) * R, sz = p.z + Math.sin(a) * R;
      const sn = mk('sniper', sx, sz); sn.master = car; sn.slotA = a; sn.slotK = rand(0.85, 1);
      for (let k = 0; k < 3; k++) { const b = k / 3 * Math.PI * 2, g = mk('soldier', sx + Math.cos(b) * 1.3, sz + Math.sin(b) * 1.3); g.master = sn; g.slotA = Math.random() * Math.PI * 2; g.slotK = rand(0.5, 1); }
    }
    chSf.waveT = 0;
  }
  function chTankFoe(car) {                    // 사거리(저격수와 같다) 안에서 벽에 안 막힌 가장 가까운 좀비
    const R = SIGHT * 1.1; let best = null, bd = R;
    for (const z of nearIn(zCells, car.x, car.z, R, chTkBuf)) {
      if (!isZombie(z)) continue;
      const d = Math.hypot(z.foot.x - car.x, z.foot.z - car.z);
      if (d > bd || fireBlocked(car.x, car.z, z.foot.x, z.foot.z)) continue;
      bd = d; best = z;
    }
    return best;
  }
  function chTankDense(car) {                  // 9칸 안 좀비가 가장 많이 몰린 쪽 (60도 부채꼴)
    const L = [];
    for (const z of nearIn(zCells, car.x, car.z, 9, chTkBuf)) { if (!isZombie(z)) continue; const dx = z.foot.x - car.x, dz = z.foot.z - car.z, d = Math.hypot(dx, dz); if (d > 9 || d < 0.01) continue; L.push([dx / d, dz / d]); }
    let best = null, bn = 0;
    for (const a of L) { let n = 0; for (const b of L) if (a[0] * b[0] + a[1] * b[1] > 0.866) n++; if (n > bn) { bn = n; best = a; } }
    return best;
  }
  function chTankKnock(car, v) {               // 넉백 = 군인의 2배 (6)
    if (v.hp <= 0 || v.mut === 'armor' || v.mode === 'bite') return;
    const T = ARMOR_KT * 6 / 12, D = SNIPER_KD * 6 / 12, V = D * 4 / (1 - Math.exp(-4 * T));
    if (v === me && absorbAmt() >= D - 0.001) return;
    if (v.mode === 'pounce') stopPounce(v);
    giveKnock(v, v.foot.x - car.x, v.foot.z - car.z, V, T);
  }
  function chTankBullet(car) {
    car.burstN--; car.burstT += BURST_GAP;
    const z = car.burstZ;
    if (!(z && isZombie(z) && z.hp > 0 && bodies.includes(z))) { car.burstN = 0; return; }
    const first = car.burstN === 3, base = POLICE_DAMAGE * 1.2 / 4 * 0.9 * 0.9 * 2;   // 군인 한 발의 2배
    const dx = z.foot.x - car.x, dz = z.foot.z - car.z, d = Math.hypot(dx, dz) || 1, ux = dx / d, uz = dz / d;
    car.shotT = 0; car.shotX = z.foot.x; car.shotZ = z.foot.z;
    const f1 = puff(car.x + ux * 1.6, 0, car.z + uz * 1.6, 0xfff23a, 1.5, 1.5, 0.07, 0, 0, 0, 0.8);
    f1.s.material.map = flashTex; f1.s.position.addScaledVector(UP, RADIUS); f1.s.renderOrder = UI - 0.5; f1.peak = true; f1.blink = true;
    const f2 = puff(z.foot.x, 0.4, z.foot.z, 0xffa53a, 0.9, CH_TK_SPLASH * 2, 0.12, 0, 0, 0, 0.55);
    f2.s.material.map = flashTex; f2.s.renderOrder = UI - 0.5; f2.peak = true;
    const hit = [z];
    for (const o of nearIn(zCells, z.foot.x, z.foot.z, CH_TK_SPLASH, chTkBuf2)) if (o !== z && isZombie(o) && o.hp > 0 && o.space === z.space && Math.hypot(o.foot.x - z.foot.x, o.foot.z - z.foot.z) <= CH_TK_SPLASH) hit.push(o);
    for (const v of hit) { landHit(car.gun, v, v === me && hasVest ? base * vestK(lv('vest')) : base); if (first && isZombie(v)) chTankKnock(car, v); }
  }
  function chSegBox(sg, cx, cz, fx, fz, hu, hv) {   // 벽 토막이 장갑차 네모에 걸치나
    const ax = sg[0] - cx, az = sg[1] - cz, bx = sg[2] - cx, bz = sg[3] - cz;
    const u0 = ax * fx + az * fz, v0 = -ax * fz + az * fx, du = bx * fx + bz * fz - u0, dv = -bx * fz + bz * fx - v0;
    let t0 = 0, t1 = 1;
    for (const [p, q] of [[-du, u0 + hu], [du, hu - u0], [-dv, v0 + hv], [dv, hv - v0]]) {
      if (Math.abs(p) < 1e-9) { if (q < 0) return false; continue; }
      const r = q / p;
      if (p < 0) { if (r > t1) return false; if (r > t0) t0 = r; } else { if (r < t0) return false; if (r < t1) t1 = r; }
    }
    return true;
  }
  function chTankWalls(car, dt) {              // 닿은 벽은 데미지가 쌓인다 (닿은 뒤 1.2초까지는 계속 쌓인다 — 비비는 동안) → 다 쌓이면 그 자리가 뚫린다
    const fx = Math.cos(car.h), fz = Math.sin(car.h), hu = CAR_L * CH_TK_K / 2 * 0.92, hv = CAR_W * CH_TK_K / 2 * 0.92, R = hu + hv;
    let hit = false;
    for (const B of buildings) {
      if (B.type === 'hill' || car.x < B.x0 - R || car.x > B.x1 + R || car.z < B.z0 - R || car.z > B.z1 + R) continue;
      for (const sg of B.walls) {
        if (!chSegBox(sg, car.x, car.z, fx, fz, hu, hv)) continue;
        hit = true; sg.tkAt = clock; sg.tkB = B;
        if (!car.tkSegs.includes(sg)) car.tkSegs.push(sg);
      }
    }
    for (let i = car.tkSegs.length - 1; i >= 0; i--) {
      const sg = car.tkSegs[i];
      if (clock - sg.tkAt > 1.2 || clock < sg.tkAt) { car.tkSegs.splice(i, 1); continue; }
      if ((sg.tkT = (sg.tkT || 0) + dt) >= CH_TK_WALL_T) { car.tkSegs.splice(i, 1); chWallBreak(sg.tkB, sg, car); }
    }
    return hit;
  }
  function chWallBreak(B, sg, car) {           // 벽 토막에서 장갑차가 닿은 자리(폭 4.6칸)를 뚫는다 — 남는 양옆은 새 토막으로
    const o = objs.find((q) => q.type === 'door' && q.seg === sg && !q.dead);
    if (o) { breakObj(o); return; }             // 잠긴 문은 문으로 부서진다
    const i = walls.indexOf(sg), j = B.walls.indexOf(sg);
    if (i < 0 && j < 0) return;
    if (i >= 0) walls.splice(i, 1); if (j >= 0) B.walls.splice(j, 1);
    const [ax, az, bx, bz] = sg, hz = az === bz, lo = hz ? Math.min(ax, bx) : Math.min(az, bz), hi = hz ? Math.max(ax, bx) : Math.max(az, bz);
    const c = Math.max(lo, Math.min(hi, hz ? car.x : car.z)), h0 = Math.max(lo, c - CH_TK_HOLE), h1 = Math.min(hi, c + CH_TK_HOLE), pieces = [];
    if (h0 - lo > 0.7) pieces.push(hz ? [lo, az, h0, az] : [ax, lo, ax, h0]);
    if (hi - h1 > 0.7) pieces.push(hz ? [h1, az, hi, az] : [ax, h1, ax, hi]);
    const P = B.parent, edge = P && (hz ? (Math.abs(az - P.z0) < 1e-6 || Math.abs(az - P.z1) < 1e-6) : (Math.abs(ax - P.x0) < 1e-6 || Math.abs(ax - P.x1) < 1e-6));
    if (sg.m) sg.m.visible = false;
    if (P && B.inner) {                         // 방 안쪽 벽 그림 — 그 토막 위에 놓인 것들
      const x0 = Math.min(ax, bx) - 0.06, x1 = Math.max(ax, bx) + 0.06, z0 = Math.min(az, bz) - 0.06, z1 = Math.max(az, bz) + 0.06;
      sg.ms = B.inner.filter((m) => m.position.x > x0 && m.position.x < x1 && m.position.z > z0 && m.position.z < z1);
      B.inner = B.inner.filter((m) => !sg.ms.includes(m)); for (const m of sg.ms) m.visible = false;
    }
    for (const q of pieces) {
      const w = Math.abs(q[2] - q[0]), d = Math.abs(q[3] - q[1]), mx = (q[0] + q[2]) / 2, mz = (q[1] + q[3]) / 2;
      if (!P) q.m = flat(w + WALL, d + WALL, mx, mz, wallMat, -0.505);
      else if (!edge) { const m = B.type === 'jail' ? flat(hz ? w : 0.09, hz ? 0.09 : d, mx, mz, chBarMat, -0.505) : flat(w + WALL, d + WALL, mx, mz, wallMat, -0.505); m.visible = !!P.open; B.inner.push(m); q.pm = m; }
    }
    walls.push(...pieces); B.walls.push(...pieces);
    let L = null;
    if (!P) {
      const side = hz ? (Math.abs(az - B.z0) < Math.abs(az - B.z1) ? 'n' : 's') : (Math.abs(ax - B.x0) < Math.abs(ax - B.x1) ? 'w' : 'e');
      const nx = side === 'e' ? 1 : side === 'w' ? -1 : 0, nz = side === 's' ? 1 : side === 'n' ? -1 : 0;
      L = { side, cx: hz ? (h0 + h1) / 2 : ax, cz: hz ? az : (h0 + h1) / 2, nx, nz, tx: -nz, tz: nx, w: h1 - h0, hole: true };
      B.doors.push(L);
    }
    B.tkCut = true;
    chCuts.push({ B, sg, pieces, L });
    rebuildSight(B);
    B.navDirty = true; if (P) P.navDirty = true; if (B.rooms) for (const Q of B.rooms) Q.navDirty = true;
    visDirty = true;
    const hx = hz ? (h0 + h1) / 2 : ax, hzz = hz ? az : (h0 + h1) / 2;
    dust(hx, hzz, 26, 2.4); debris(hx, hzz, 30, [0x2b2b2b, 0x3a3a3a, 0x555555], 0.45, 7);
  }
  function chWallRestore() {                   // 새 판: 뚫린 벽을 되돌린다 (나중에 뚫린 것부터 거꾸로)
    const done = new Set();
    for (let k = chCuts.length - 1; k >= 0; k--) {
      const { B, sg, pieces, L } = chCuts[k];
      for (const q of pieces) {
        const i = walls.indexOf(q), j = B.walls.indexOf(q);
        if (i >= 0) walls.splice(i, 1); if (j >= 0) B.walls.splice(j, 1);
        if (q.m) scene.remove(q.m);
        if (q.pm) { scene.remove(q.pm); const n = B.inner.indexOf(q.pm); if (n >= 0) B.inner.splice(n, 1); }
      }
      if (!walls.includes(sg)) walls.push(sg); if (!B.walls.includes(sg)) B.walls.push(sg);
      sg.tkT = 0; if (sg.m) sg.m.visible = true;
      if (sg.ms) { B.inner.push(...sg.ms); sg.ms = null; }
      if (L) { const n = B.doors.indexOf(L); if (n >= 0) B.doors.splice(n, 1); }
      B.tkCut = false; done.add(B);
    }
    chCuts.length = 0;
    for (const B of done) { rebuildSight(B); B.navDirty = true; if (B.parent) B.parent.navDirty = true; }
    for (const B of buildings) for (const sg of B.walls) if (sg.tkT) sg.tkT = 0;
  }
  function chSightCut(B) {                     // 벽이 뚫린 건물의 시야 벽 = 남아 있는 벽 토막 그대로 (두께만큼 네모로)
    if (B.type === 'jail') return;
    const W = [], C = [], k = WALL / 2;
    for (const sg of B.walls) {
      const x0 = Math.min(sg[0], sg[2]) - k, x1 = Math.max(sg[0], sg[2]) + k, z0 = Math.min(sg[1], sg[3]) - k, z1 = Math.max(sg[1], sg[3]) + k;
      W.push([x0, z0, x1, z0], [x1, z0, x1, z1], [x0, z1, x1, z1], [x0, z0, x0, z1]);
      C.push([x0, z0], [x1, z0], [x1, z1], [x0, z1]);
    }
    B.sightW = W; B.sightC = C;
  }
  function chTankCrush(car, b, fx, fz, rx, rz) {   // 장갑차에 깔린 사물 — 밀리면서 계속 깎이다가 부서진다 (박힌 것은 그 자리에서 깎인다). 분수도 부서진다
    if (b.dead || car.wreck) return;
    const dx = b.foot.x - car.x, dz = b.foot.z - car.z, hl = CAR_L * CH_TK_K / 2 + b.r, hw = CAR_W * CH_TK_K / 2 + b.r, u = dx * fx + dz * fz, v = dx * rx + dz * rz;
    if (Math.abs(u) >= hl || Math.abs(v) >= hw) return;
    if (!(b.hp > 0) || !isFinite(b.hp) || b.inv) { b.tkHp = (b.tkHp === undefined ? 600 : b.tkHp) - 400 * chDt; if (b.tkHp <= 0) breakSafe(b); return; }   // 못 부수던 것(분수·동상 …)도 1.5초면 부서진다
    b.hp -= Math.max(300, (b.maxHp || 100) / 1.2) * chDt;
    if (b.hp <= 0) { breakSafe(b); return; }
    if (!b.fixed && u > -hl * 0.5) { const pen = Math.min(hl - u, 8 * chDt); b.foot.x += fx * pen; b.foot.z += fz * pen; }   // 앞으로 밀려간다
  }
  function chTankCar(o) {                      // 장갑차에 닿은 차 — 1.5초면 부서진다
    if (!o.obj || o.obj.dead || o.wreck) return;
    o.obj.hp -= MY_DAMAGE * 9.5 / 1.5 * chDt;
    if (o.obj.hp <= 0) { o.obj.hp = 0; breakObj(o.obj); }
  }
  function chTankGoo(car) {                    // 산성 — 이동·공격 20% 느리게 + 초당 2 데미지 (사람과 같다)
    if (car.goo) return;
    car.goo = true; car.gooT = 0;
    for (const [ox, oz, sc] of [[0.3, 0.1, 0.5], [-0.35, -0.12, 0.4], [0, 0.2, 0.34]]) { const s = new THREE.Sprite(gooMat); s.position.set(ox, 0.3, oz); s.scale.setScalar(sc); s.renderOrder = 1; car.g.add(s); }
  }
  function chTankDead(car) {
    if (car.tracer) car.tracer.visible = false;
    for (let i = 0; i < 3; i++) boom(car.x + rand(-1.6, 1.6), car.z + rand(-1, 1));
  }
  function chTankDrive(car, dt) {
    car.foot.set(car.x, 0, car.z);
    const o = car.obj; if (o) o.foot.set(car.x, 0, car.z);
    if (car.wreck) return;
    const spd = CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / 4 * (car.goo ? 0.8 : 1);   // 보통 차(승용차)의 4분의 1
    if (car.goo && (car.gooT += dt) >= 0.5) { car.gooT -= 0.5; if (o && o.hp > 1) o.hp -= 1; }
    // 벽
    if (chTankWalls(car, dt)) {
      if (car.tkPX !== undefined) { car.x = car.tkPX; car.z = car.tkPZ; car.h = car.tkPH; car.foot.set(car.x, 0, car.z); if (o) o.foot.set(car.x, 0, car.z); }
      car.dashT = 0;
      if (car.rubBack <= 0 && car.rubCool <= 0) { car.rubBack = 0.3; dust(car.x + Math.cos(car.h) * CAR_L * CH_TK_K / 2, car.z + Math.sin(car.h) * CAR_L * CH_TK_K / 2, 8, 1.2); }
    } else { car.tkPX = car.x; car.tkPZ = car.z; car.tkPH = car.h; }
    // 건물 안 네모 사물 (책상 …)
    if ((car.crT -= dt) <= 0) {
      car.crT = 0.1;
      const fx = Math.cos(car.h), fz = Math.sin(car.h), hl = CAR_L * CH_TK_K / 2 + 0.5, hw = CAR_W * CH_TK_K / 2 + 0.5, L = [];
      for (const q of objs) if (q.type === 'table' && !q.dead && q.t) { const dx = q.t.x - car.x, dz = q.t.z - car.z; if (Math.abs(dx * fx + dz * fz) < hl && Math.abs(-dx * fz + dz * fx) < hw) L.push(q); }
      for (const q of L) breakObj(q);
    }
    // 기관포
    car.atkT -= dt * (car.goo ? 0.56 : 1);
    if ((car.scanT -= dt) <= 0) { car.scanT = 0.2; car.foe = chTankFoe(car); }
    if (car.burstN > 0) { if ((car.burstT -= dt) <= 0) chTankBullet(car); }
    else if (car.atkT <= 0 && car.foe && isZombie(car.foe)) { car.burstN = 4; car.burstT = 0; car.burstZ = car.foe; car.atkT = HIT_EVERY; }
    // 돌진
    car.dashAt -= dt;
    if (car.dashT > 0) { car.dashT -= dt; car.tkV = CAR_SPEED * 1.6; return; }
    if (car.dashAt <= 0 && car.rubBack <= 0) {
      const d = chTankDense(car);
      if (d) { const V = CAR_SPEED * 1.6; car.dashAt = CH_TK_DASH_EVERY; car.dashT = CH_TK_DASH_T; car.rev = false; car.vx = d[0] * V; car.vz = d[1] * V; car.h = Math.atan2(d[1], d[0]); car.tkV = V; return; }
    }
    car.tkV = spd;
    // 벽에 걸렸다 → 물러났다가 다시 민다
    if (car.rubBack > 0) {
      car.rubBack -= dt; car.rev = true;
      carSteer(car, -Math.cos(car.h) * spd * 2, -Math.sin(car.h) * spd * 2, CAR_ACCEL * dt);
      if (car.rubBack <= 0) car.rubCool = 0.6;
      return;
    }
    car.rev = false; if (car.rubCool > 0) car.rubCool -= dt;
    let wx = 0, wz = 0;
    const t = isZombie(me) ? me : bodies.find(isZombie);
    if (t && !(car.foe && isZombie(car.foe))) {   // 쏠 좀비가 없으면 나한테 곧장 온다 (건물을 돌아가지 않는다 — 구역을 건널 때만 다리·산길로)
      const r = chRoute({ foot: { x: car.x, z: car.z }, laneK: 0 }, t.foot.x, t.foot.z), dx = r[0] - car.x, dz = r[1] - car.z, l = Math.hypot(dx, dz);
      if (l > 1.5) { const v = spd * (car.loadK ?? 1); wx = dx / l * v; wz = dz / l * v; }
    }
    const sp = Math.hypot(car.vx, car.vz);
    carSteer(car, wx, wz, (sp > spd * 1.5 ? 40 : CAR_ACCEL) * dt);
  }
  function chTankDraw(dt) {                    // 기관포 총알 선
    const car = chTank; if (!car || !car.tracer) return;
    const tr = car.tracer;
    if (car.shotT < 0 || car.wreck) { tr.visible = false; return; }
    const dx = car.shotX - car.x, dz = car.shotZ - car.z, L = Math.hypot(dx, dz) || 1e-3;
    tr.visible = true;
    tr.position.set(car.x + dx / 2, 0, car.z + dz / 2).addScaledVector(UP, RADIUS);
    tr.rotation.y = -Math.atan2(dz, dx);
    tr.scale.set(L, 1, 1.8);
    tr.material.opacity = 1 - car.shotT / SHOT_FLASH;
    if ((car.shotT += dt) >= SHOT_FLASH) car.shotT = -1;
  }
  window.__sf = { get s() { return chSf; }, get tank() { return chTank; }, cuts: chCuts, queue: (i) => chQueueTeam(i), kill: () => { if (chTank && chTank.obj && !chTank.obj.dead) breakObj(chTank.obj); }, teams: teamWait };
