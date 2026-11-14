# c59: 군인팀(특수부대) 출동 · 건널목 바리케이트와 수비대(사수지역) · 건물 사람은 목표를 잃으면 건물로 돌아간다 · 군인 첫 발 넉백
C59_FN = r"""  // ── c59: 군인팀 (특수부대) — 테스트 맵과 같은 방식. 경보 3단계(감염 75명)에 처음, 그 뒤로 감염 60명마다 (사람·경찰·군인·저격수 다 합쳐서).
  //    처음 두 번은 걸어서 오는 분대 셋 (저격수 1 + 군인 2씩), 그 뒤로는 군인차 두 대 (한 대에 저격수 2 + 군인 6). 나오는 곳 = 내가 있는 구역 바깥 라인 (경찰 출동과 같다). 목표 = 나 ──
  const CH_TEAM_GAP = 60;
  const CH_TEAM_EVENTS = Array.from({ length: 200 }, (_, i) => ({ at: STAR_AT[2] + CH_TEAM_GAP * i, tier: i < 2 ? 1 : 2 }));
  function chTeamSpot(seg) {                   // 그 자리(seg) 둘레 6칸 안, 같은 구역, 내 화면과 좀비 시야 밖 — 분대·군인차가 같은 곳 둘레에서 나온다
    for (let k = 0; k < 90; k++) {
      const a = Math.random() * Math.PI * 2, r = rand(0, 6), x = seg.x + Math.cos(a) * r, z = seg.z + Math.sin(a) * r;
      if (x < MM.x0 + 2 || x > MM.x1 - 2 || z < MM.z0 + 2 || z > MM.z1 - 2 || spaceOf(x, z) || chNearRiver(x, z, 1.5) || !freeSpot(x, z, null) || chZoneOf(x, z) !== seg.zi) continue;
      if (k < 60 && (onView(x, z, 3) || zombies.some((zb) => Math.hypot(zb.foot.x - x, zb.foot.z - z) < zb.sense + 2))) continue;
      return { x, z };
    }
    return { x: seg.x, z: seg.z };
  }
  // ── c59: 건널목 바리케이트와 수비대 ──
  //   바리케이트 = 서 있는 경찰차와 같은 물건 (밀리고, 부서지고, 가로막으면 좀비가 때린다). 무게 3배 · 체력 3배.
  //   경찰차와 같은 방식으로 밀린다 (무게만 3배): 좀비가 겹친 만큼을 힘 : 무게로 나눠 밀린다 — 나와 보통 좀비는 거의 못 밀고(겹친 만큼의 5%쯤) 덩치도 힘들게 민다(26%쯤). 사람은 못 민다.
  //   경보 1단계(수상함)가 되는 순간 모든 건널목(다리 3 · 산 길목 2)의 양 끝에 바리케이트와 경찰차가 놓이고, 내가 있는 구역 쪽 바리케이트 뒤에 수비대가 선다.
  //   단계가 오를 때마다 바리케이트와 수비대가 는다 (수와 놓이는 모양은 건널목마다 조금씩 다르다). 줄이 꽉 차면 안쪽에 한 겹 더 — 앞줄의 가장 큰 틈 뒤부터 막는다.
  //   수비대는 자리(사수지역)에 묶여 있다: 자리 둘레(근접 거리)에 서 있고, 지배 거리 밖으로 벗어나면 싸우다가도 돌아온다. 앞에서부터 경찰 → 군인 → 저격수.
  //   수비대는 먼저 다가가서 쏘지 않는다 (자리를 지킨다). 저격수는 맨 앞 바리케이트를 때리는 좀비가 보이는 거리에 선다. 내가 다른 구역으로 넘어가면 수비대는 그쪽 바리케이트 뒤로 옮겨 서고 순서도 뒤집힌다.
  const CH_BARR_K = 3, CH_BARR_HP = 4, CH_BARR_W = 1 / 3;   // c60: 무게 = 경찰차의 3배 · 체력 = 경찰차의 4배 · 모양 = 경찰차 길이의 막대 (폭은 경찰차의 3분의 1)
  const CH_HOLD_NEAR = 1.7, CH_HOLD_DOM = 3.2;
  const CH_BAR_ROW0 = 5.55, CH_BAR_ROWD = 0.8, CH_BAR_ROWS = 3, CH_BAR_HALF = 4;   // 첫 줄 = 건널목 한가운데에서 5.55칸 (건널목 끝에서 한 칸쯤 안쪽) · 줄 간격 · 건널목 반폭
  const chBarrTex = (() => { const c = document.createElement('canvas'); c.width = 448; c.height = 80; const g = c.getContext('2d');   // c60: 막대 — 노랑·검정 빗금, 양 끝에 받침
    g.fillStyle = '#141416'; g.fillRect(0, 0, 448, 80); g.fillStyle = '#e8b21c'; g.fillRect(6, 6, 436, 68);
    g.save(); g.beginPath(); g.rect(6, 6, 436, 68); g.clip(); g.fillStyle = '#1c1c1e';
    for (let x = -80; x < 500; x += 64) { g.beginPath(); g.moveTo(x, 74); g.lineTo(x + 32, 74); g.lineTo(x + 100, 6); g.lineTo(x + 68, 6); g.closePath(); g.fill(); }
    g.restore(); g.fillStyle = '#8f8f8a'; g.fillRect(6, 6, 26, 68); g.fillRect(416, 6, 26, 68); g.strokeStyle = 'rgba(0, 0, 0, 0.6)'; g.lineWidth = 3; g.strokeRect(32, 6, 384, 68);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const chBarrGeo = new THREE.PlaneGeometry(CAR_L, CAR_W * CH_BARR_W).rotateX(-Math.PI / 2);
  function chParked(x, z, h, barr) {           // 처음부터 서 있는 것 — 바리케이트(barr) 또는 빈 경찰차
    if (barr) {
      const g = new THREE.Group(), body = new THREE.Mesh(chBarrGeo, new THREE.MeshBasicMaterial({ map: chBarrTex, transparent: true, depthTest: false, depthWrite: false })), pad = new THREE.Mesh(lampGeo, carMat(0x000000)), dm = carMat(0x000000);
      body.renderOrder = -0.45; pad.visible = false; g.add(body, pad); scene.add(g);
      cars.push({ g, red: dm, blue: dm, x, z, vx: 0, vz: 0, h, calls: [], n: 0, squad: null, mil: false, state: 'parked', flashT: 0, sight: 0, foot: new THREE.Vector3(x, 0, z), barr: true });
    } else { addCar(x, z, h, null, 0); const c = cars[cars.length - 1]; c.state = 'parked'; c.red.color.setHex(0x4a3a3a); c.blue.color.setHex(0x3a3f4a); }
    const car = cars[cars.length - 1], hp = MY_DAMAGE * 9.5 * (barr ? CH_BARR_HP : 1);
    car.wall = true;                          // 건널목을 막는 물건 — 달리는 경찰차·군인차는 그냥 지나간다 (자기편 길은 열어 준다)
    car.obj = { kind: 'obj', type: 'car', car, foot: new THREE.Vector3(x, 0, z), hp, maxHp: hp, dead: false };
    addHpBar(car.obj, hpFoeMat); objs.push(car.obj);
    car.g.position.set(x, 0.05, z); car.g.rotation.y = -h; car.g.visible = false;
    return car;
  }
  let chBar = null;
  const chNB = [], chNB2 = [], chNB3 = [];
  function chNearBodies(car) {                 // 그 차 둘레 칸의 몸들 (좀비 + 사람)
    nearIn(zCells, car.x, car.z, 2.6, chNB); const n = chNB.length; nearIn(cCells, car.x, car.z, 2.6, chNB2);
    for (let i = 0; i < chNB2.length; i++) chNB[n + i] = chNB2[i];
    return chNB;
  }
  const chBarTmp = { zone: 0, corr: -1, land: true };
  const chZD = (() => { const n = CH_MAP.zones.length, D = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => i === j ? 0 : 99));   // 구역 사이 거리 (건널목 몇 개를 건너야 하나)
    for (const P of CH_MAP.passes2) { D[P.za][P.zb] = 1; D[P.zb][P.za] = 1; }
    for (let k = 0; k < n; k++) for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if (D[i][k] + D[k][j] < D[i][j]) D[i][j] = D[i][k] + D[k][j];
    return D; })();
  function chBarReset() {
    chBar = { stage: 0, zone: -1, t: 0, X: CH_MAP.passes2.map((P, i) => { const v = P.axis === 'v', ux = Math.sign(P.bx - P.ax), uz = Math.sign(P.bz - P.az);
      return { P, i, cx: v ? 0 : P.c, cz: v ? P.c : CH_MAP.zrMid, ux, uz, wx: -uz, wz: ux, side: 0, rows: [[], []], units: [] }; }) };   // u = a끝 → b끝 방향, w = 가로(폭) 방향, side = 수비대가 선 끝 (0 = a, 1 = b)
  }
  const chBarXZ = (X, s, l) => [X.cx + X.ux * s + X.wx * l, X.cz + X.uz * s + X.wz * l];   // 한가운데에서 건너는 방향으로 s, 폭 방향으로 l
  const chBarLive = (p) => !p.car.wreck && cars.includes(p.car);
  function chBarPut(X, e, r, l, barr) {
    const sg = e ? 1 : -1, [x, z] = chBarXZ(X, sg * (CH_BAR_ROW0 - r * CH_BAR_ROWD) + rand(-0.12, 0.12), l);
    const car = chParked(x, z, Math.atan2(X.wz, X.wx) + rand(-0.13, 0.13) + (Math.random() < 0.5 ? Math.PI : 0), barr);   // 폭 방향으로 눕혀 놓는다 — 조금씩 비뚤게
    (X.rows[e][r] = X.rows[e][r] || []).push({ l, car });
  }
  function chBarFree(row) {                    // 그 줄에서 비어 있는 폭 구간들
    const Lp = CAR_L + 0.05, iv = (row || []).filter(chBarLive).map((p) => [p.l - Lp / 2, p.l + Lp / 2]).sort((a, b) => a[0] - b[0]), out = [];
    let at = -CH_BAR_HALF; for (const [a, b] of iv) { if (a > at) out.push([at, a]); at = Math.max(at, b); } if (CH_BAR_HALF > at) out.push([at, CH_BAR_HALF]);
    return out;
  }
  function chBarAdd(X, e, barr) {              // 조각 하나 더 — 바깥 줄부터 들어갈 자리를 찾고, 없으면 안쪽 줄에 (앞줄의 가장 큰 틈 뒤부터)
    const Lp = CAR_L + 0.05, R = X.rows[e];
    for (let r = 0; r < CH_BAR_ROWS; r++) {   // 다리가 13칸뿐이라 한쪽에 세 겹까지만 — 더는 놓을 데가 없으면 안 는다
      const fit = chBarFree(R[r]).filter(([a, b]) => b - a >= Lp);
      if (!fit.length) continue;
      let l = null;
      if (r > 0) for (const [ga, gb] of chBarFree(R[r - 1]).sort((p, q) => (q[1] - q[0]) - (p[1] - p[0]))) {
        const m = (ga + gb) / 2, f = fit.find(([a, b]) => m >= a + Lp / 2 - 0.7 && m <= b - Lp / 2 + 0.7);
        if (f) { l = Math.max(f[0] + Lp / 2, Math.min(f[1] - Lp / 2, m + rand(-0.2, 0.2))); break; }
      }
      if (l === null) { const f = fit[Math.floor(Math.random() * fit.length)]; l = rand(f[0] + Lp / 2, f[1] - Lp / 2); }
      chBarPut(X, e, r, l, barr); return true;
    }
    return false;
  }
  function chBarRow0(X, e, kinds) {            // 첫 줄 — 조각을 한 줄로 늘어놓고 남는 폭을 틈으로 아무렇게나 나눈다 (틈이 보일 때도, 거의 막힐 때도 있다)
    const Lp = CAR_L + 0.05, n = Math.min(kinds.length, Math.floor(2 * CH_BAR_HALF / Lp)), slack = 2 * CH_BAR_HALF - n * Lp;
    const w = Array.from({ length: n + 1 }, () => -Math.log(1 - Math.random())), ws = w.reduce((a, b) => a + b, 0);
    let at = -CH_BAR_HALF; for (let i = 0; i < n; i++) { at += slack * w[i] / ws; chBarPut(X, e, 0, at + Lp / 2, kinds[i]); at += Lp; }
    for (let i = n; i < kinds.length; i++) chBarAdd(X, e, kinds[i]);
  }
  function chBarInner(X, e) {                  // 그 끝에서 가장 안쪽 줄의 안쪽 가장자리 (한가운데에서 잰 거리) — 그 줄에 경찰차가 있으면 차 두께만큼
    let r = 0, hd = CAR_W * CH_BARR_W / 2;
    X.rows[e].forEach((row, i) => { const L = (row || []).filter(chBarLive); if (L.length) { r = i; hd = L.some((p) => !p.car.barr) ? CAR_W / 2 : CAR_W * CH_BARR_W / 2; } });
    return CH_BAR_ROW0 - r * CH_BAR_ROWD - hd;
  }
  function chBarSeat(X, c, tele) {             // 그 사람의 자리(사수지역) — 수비대가 선 쪽 바리케이트 뒤. 경찰이 맨 앞, 군인은 그 뒤에 흩어져 서고, 저격수는 맨 앞 바리케이트가 보이는 데까지만 물러선다
    const sg = X.side ? 1 : -1, inner = chBarInner(X, X.side), back = 1 - chBarInner(X, 1 - X.side);
    for (let t = 0; t < 30; t++) {
      let l = rand(-3.3, 3.3), d;
      if (c.sniper) {                         // c60: 저격수 — 맨 앞 줄 바리케이트를 때리는 좀비(줄 어디에 붙든)가 시야 안에 들어와야 한다. 가운데쯤에 서고, 그게 보이는 거리보다 뒤로는 안 간다
        l = rand(-1.8, 1.8);
        const R = c.sight * 0.92, zf = CH_BAR_ROW0 + CAR_W * CH_BARR_W / 2 + 0.45, need = zf - Math.sqrt(Math.max(0, R * R - (CH_BAR_HALF + Math.abs(l)) ** 2));
        d = Math.min(inner - 0.9, Math.max(need, inner - rand(3.3, 4.0)));
      } else d = inner - (c.soldier ? rand(2.0, 3.2) : rand(1.0, 1.8));
      const [x, z] = chBarXZ(X, sg * Math.max(back, d), l);
      if (t < 29 && X.units.some((o) => o !== c && o.kind === 'citizen' && o.hold && Math.hypot(o.hold.x - x, o.hold.z - z) < 0.95)) continue;
      c.hold = { x, z }; break;
    }
    c.post = c.area = { x0: c.hold.x - 0.7, z0: c.hold.z - 0.7, x1: c.hold.x + 0.7, z1: c.hold.z + 0.7 };   // 근접 거리 — 평소엔 이 안에서만 서성인다
    c.recall = false; c.outT = 0; c.master = null;
    if (tele) { c.foot.x = c.hold.x; c.foot.z = c.hold.z; c.vel.set(0, 0); c.goal = null; }
    else if (c.state === 'normal') { c.goal = pickGoal(c.area); c.back = true; }
  }
  function chBarForm(X) {                      // 수비대를 지금 쪽 자리로 — 새로 온 사람과 보는 좀비가 없는(24칸 밖) 사람은 바로 그 자리에, 나머지는 걸어서
    X.units = X.units.filter((c) => c.kind === 'citizen' && bodies.includes(c));
    const far = (c) => !zombies.some((z) => Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z) < 24);
    for (const c of X.units) chBarSeat(X, c, !!c.fresh || !!c.sleep || far(c));   // c60: 군인도 저격수를 따라다니지 않고 자기 자리를 지킨다 (경찰 뒤에 흩어져 선다)
    for (const c of X.units) c.fresh = false;
  }
  function chBarGrow(s) {                      // 경보 s단계가 됐다 — 건널목마다 바리케이트와 수비대를 늘린다 (말한 수에서 조금씩 다르게)
    const N = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
    for (const X of chBar.X) {
      for (const e of [0, 1]) {
        if (s === 1) { const q = Math.random(), kinds = q < 0.7 ? [true, true, false] : q < 0.85 ? [true, true, false, false] : [true, true, true, false];   // 바리케이트 2 + 경찰차 1 (가끔 하나 더)
          kinds.sort(() => Math.random() - 0.5); chBarRow0(X, e, kinds); }
        else { const q = Math.random(), k = s === 4 ? (q < 0.25 ? 1 : 0) : q < 0.2 ? 0 : q < 0.8 ? 1 : 2;   // 단계마다 양쪽에 하나씩 (4단계는 그대로) — 가끔 안 늘거나 둘이 는다
          for (let i = 0; i < k; i++) chBarAdd(X, e, true); if (Math.random() < 0.2) chBarAdd(X, e, false); }   // 가끔 경찰차도 한 대
      }
      const r2 = Math.random();                // 수비대: 말한 수에서 한두 명씩 다르게 — 1단계 경찰 3 · 2단계 경찰 +2 · 3단계 군인 +3 저격수 +1 · 4단계 군인 +2 저격수 +1 · 그 뒤로 군인 +3씩
      const add = s === 1 ? { police: N(2, 4) } : s === 2 ? { police: N(1, 3) } : s === 3 ? { soldier: N(2, 4), sniper: r2 < 0.75 ? 1 : 2 } : s === 4 ? { soldier: N(1, 3), sniper: r2 < 0.2 ? 0 : r2 < 0.8 ? 1 : 2 } : { soldier: N(2, 4) };
      for (const type of ['police', 'soldier', 'sniper']) for (let i = 0; i < (add[type] || 0); i++) { const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), type); c.gar = X; c.fresh = true; X.units.push(c); }
      chBarForm(X);
    }
    updateCarObs();
  }
  function chBarTick(dt) {
    if (!chBar || !isZombie(me)) return;
    if ((chBar.t -= dt) > 0 && stars <= chBar.stage) return;
    chBar.t = 0.3;
    const o = chClass(me.foot.x, me.foot.z, chBarTmp);
    if (chBar.zone < 0 || (o.corr < 0 && o.land && o.zone !== chBar.zone)) {   // 내가 있는 구역이 바뀌었다 (다리·길목 위에 있는 동안은 그대로) → 건널목마다 내 쪽 끝으로
      chBar.zone = o.zone;
      for (const X of chBar.X) { const side = chZD[o.zone][X.P.za] <= chZD[o.zone][X.P.zb] ? 0 : 1; if (side !== X.side) { X.side = side; if (chBar.stage) chBarForm(X); } }
    }
    if (stars > chBar.stage) { for (let s = chBar.stage + 1; s <= stars; s++) chBarGrow(s); chBar.stage = stars; }
  }
  function chHoldLeash(c, dt) {                // 사수지역 지배 거리 — 자리에서 이만큼 벗어나면 싸우다가도 돌아온다 (군인이 저격수를 따르는 규칙과 같다)
    const H = c.hold;
    if (!H || Math.hypot(c.foot.x - H.x, c.foot.z - H.z) <= CH_HOLD_DOM) { c.outT = 0; return false; }
    if (!c.outT) c.outLimit = rand(0, 1);
    if ((c.outT = (c.outT || 0) + dt) < c.outLimit) return false;
    c.outT = 0; c.recall = true; c.foe = null; c.inRange = false; enterNormal(c);
    return true;
  }
"""
C59_R = [
  # ── 건물 사람은 목표를 잃으면 건물로 돌아간다 (전엔 건물 밖으로 한 번 나오면 그 자리 둘레를 새 영역으로 삼았다) ──
  ("      if (b.home && sp0 !== b.home) b.freed = true;", "      if (!CHAPTER && b.home && sp0 !== b.home) b.freed = true;   // c59: 챕터 — 건물 사람은 밖으로 나왔다가도 일반 상태가 되면 자기 건물로 돌아간다"),
  # ── 군인팀: 나오는 곳 = 내가 있는 구역 바깥 라인 (경찰 출동과 같다). 나온 군인은 깨어 있다 ──
  ("  function teamSeg() {", "  function teamSeg() {\n    if (CHAPTER) { const zi = chZoneOf(me.foot.x, me.foot.z), p = chEdgeSpot(zi); return { x: p.x, z: p.z, zi }; }   // c59"),
  ("  function teamSpot(seg) {", "  function teamSpot(seg) {\n    if (CHAPTER) return chTeamSpot(seg);   // c59"),
  ("      if (type === 'sniper') sns.push(c); else sol.push(c);", "      if (CHAPTER) c.met = true;   // c59: 출동한 군인은 멀리 있어도 서 있지 않는다\n      if (type === 'sniper') sns.push(c); else sol.push(c);"),
  # 군인 넉백: 한 번 쏘는 네 발 중 첫 발만, 넉백 3 (경찰 권총과 같은 세기 · 저격수는 12)
  ("    if (Math.random() < 0.5) return;           // 한 발마다 넉백 확률 50%",
   "    if (CHAPTER) {                            // c59: 첫 발만 밀린다 — 넉백 3\n"
   "      if (c.burstN !== 3) return;\n"
   "      const T = ARMOR_KT * 3 / 12, D = SNIPER_KD * 3 / 12, V = D * 4 / (1 - Math.exp(-4 * T));\n"
   "      if (z === me && absorbAmt() >= D - 0.001) return;\n"
   "      if (z.mode === 'pounce') stopPounce(z);\n"
   "      giveKnock(z, z.foot.x - c.foot.x, z.foot.z - c.foot.z, V, T);\n"
   "      return;\n"
   "    }\n"
   "    if (Math.random() < 0.5) return;           // 한 발마다 넉백 확률 50%"),
  # ── 바리케이트: 부딪힘 크기는 그림 그대로, 좀비만 밀고(무게 3배), 여럿이 밀어도 가장 센 하나만큼만 ──
  ("        const k = car.state === 'parked' ? PARKED_K * (car.wreck ? 0.16 : 1) : MOVING_K;   // 잔해는 1/5 (v239)",
   "        const k = car.barr ? (car.wreck ? 0.16 : 1) : car.state === 'parked' ? PARKED_K * (car.wreck ? 0.16 : 1) : MOVING_K;   // 잔해는 1/5 (v239)"),
  ("        if (car.state === 'parked') {         // v464: 서 있는 차는 누구에게나 밀린다",
   "        if (car.barr) {                       // c59 · c60: 바리케이트 — 경찰차와 같은 방식으로 밀린다 (무게 3배). 좀비만 민다 (사람은 못 민다)\n"
   "          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) && !car.wreck ? f / (f + CAR_MASS * 2 / 3 * CH_BARR_K) : 0, ex = nx - b.foot.x, ez = nz - b.foot.z;\n"
   "          b.foot.x += ex * (1 - sh); b.foot.z += ez * (1 - sh);\n"
   "          if (sh) { car.x -= ex * sh; car.z -= ez * sh;\n"
   "            const px = b.foot.x - car.x, pz = b.foot.z - car.z, mx = -ex * sh, mz = -ez * sh, Wb = CAR_W * CH_BARR_W;\n"
   "            car.h += (px * mz - pz * mx) / ((CAR_L * CAR_L + Wb * Wb) / 12 + px * px + pz * pz);   // 미는 자리에 따라 돈다\n"
   "            carClampB(car); car.obj.foot.set(car.x, 0, car.z); }\n"
   "          continue;\n"
   "        }\n"
   "        if (car.state === 'parked') {         // v464: 서 있는 차는 누구에게나 밀린다"),
  # 길 찾기: 건널목 바리케이트는 '돌아갈 장애물'로 안 본다 (줄 전체가 큰 덩어리로 묶여 다리를 통째로 막은 것처럼 보였다) — 막히는 쪽은 몸으로 부딪혀서 막힌다
  ("    const cs = cars.filter((c) => c.state === 'parked' && !CAR_TEST)", "    const cs = cars.filter((c) => c.state === 'parked' && !CAR_TEST && !c.wall)"),
  # 출동한 경찰·군인(자리 없이 나를 쫓는 쪽)은 자기편 바리케이트를 지나간다. 수비대·사수 경찰·시민은 막힌다
  ("        if (b.fixed || b.knockT > 0) continue;\n        const k = car.barr ? ",
   "        if (b.fixed || b.knockT > 0) continue;\n        if (car.wall && b.kind === 'citizen' && b.police && !b.post) continue;   // c59\n        const k = car.barr ? "),
  ("const kA = A.state === 'parked' ? PARKED_K * (A.wreck ? 0.16 : 1) : MOVING_K,", "const kA = A.barr ? (A.wreck ? 0.16 : 1) : A.state === 'parked' ? PARKED_K * (A.wreck ? 0.16 : 1) : MOVING_K,"),
  ("kB = B.state === 'parked' ? PARKED_K * (B.wreck ? 0.16 : 1) : MOVING_K;", "kB = B.barr ? (B.wreck ? 0.16 : 1) : B.state === 'parked' ? PARKED_K * (B.wreck ? 0.16 : 1) : MOVING_K;"),
  ("      if (Math.hypot(A.x - B.x, A.z - B.z) > CAR_L * 1.6 * Math.max(ck(A), ck(B))) continue;",
   "      if (Math.hypot(A.x - B.x, A.z - B.z) > CAR_L * 1.6 * Math.max(ck(A), ck(B))) continue;\n"
   "      if ((A.wall && B.state !== 'parked') || (B.wall && A.state !== 'parked')) continue;   // c59: 달리는 경찰차·군인차는 건널목 바리케이트를 그냥 지나간다"),
  # 부서질 때: 바리케이트는 폭발 없이 먼지만, 잔해는 금방 사라진다
  ("      boom(c.x, c.z); dust(c.x, c.z, 14, 2);", "      if (c.barr) { dust(c.x, c.z, 18, 1.8); c.wreckT = 9; } else { boom(c.x, c.z); dust(c.x, c.z, 14, 2); }   // c59"),
  ("      if ((c.smokeT = (c.smokeT || 0) - dt) <= 0) { c.smokeT = 0.18; puff(", "      if (!c.barr && (c.smokeT = (c.smokeT || 0) - dt) <= 0) { c.smokeT = 0.18; puff("),
  # ── 수비대 (사수지역) ──
  ("hv = CAR_W * ck(car) / 2 * k + b.r;", "hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) + b.r;   /* c60: 바리케이트는 폭이 3분의 1 */"),
  ("const ha = [CAR_L / 2 * kA * ck(A), CAR_W / 2 * kA * ck(A)], hb = [CAR_L / 2 * kB * ck(B), CAR_W / 2 * kB * ck(B)];",
   "const ha = [CAR_L / 2 * kA * ck(A), CAR_W / 2 * kA * ck(A) * (A.barr ? CH_BARR_W : 1)], hb = [CAR_L / 2 * kB * ck(B), CAR_W / 2 * kB * ck(B) * (B.barr ? CH_BARR_W : 1)];"),
  ("v = Math.abs(-dx * fz + dz * fx) - CAR_W * ck(c) / 2;", "v = Math.abs(-dx * fz + dz * fx) - CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1);"),
  # 수비대는 먼저 다가가서 쏘지 않는다 — 사거리 밖이어도 자리를 지킨다
  ("steer(c.vel, toward(c, z.foot.x, z.foot.z, copSpeed(c)), accelOf(c) * dt); moveShoot(c, dt); return; }",
   "steer(c.vel, CHAPTER && c.gar ? wantV.set(0, 0) : toward(c, z.foot.x, z.foot.z, copSpeed(c)), accelOf(c) * dt); moveShoot(c, dt); return; }   /* c60: 수비대는 안 다가간다 */"),
  ("    if (c.soldier && soldierLeash(c, dt)) { moveShoot(c, dt); return; }",
   "    if (c.soldier && soldierLeash(c, dt)) { moveShoot(c, dt); return; }\n"
   "    if (CHAPTER && c.gar && !(c.soldier && c.master) && chHoldLeash(c, dt)) { moveShoot(c, dt); return; }   // c59: 사수지역 — 자리에서 지배 거리 밖이면 돌아온다"),
  ("  function masterOf(c) {",
   "  function masterOf(c) {\n"
   "    if (CHAPTER && c.gar) { c.master = null; return null; }   // c59 · c60: 수비대 군인은 저격수를 따라다니지 않는다 — 자기 자리(사수지역)를 지킨다"),
  ("  function sniperEvade(c, dt) {",
   "  function sniperEvade(c, dt) {\n"
   "    if (CHAPTER && c.hold && Math.hypot(c.foot.x - c.hold.x, c.foot.z - c.hold.z) > CH_HOLD_DOM + 1.5) { c.isolated = true; enterFight(c, null, true); return; }   // c59: 사수지역 저격수 — 자리에서 너무 멀리는 안 물러난다 (그 자리에서 쏜다)"),
  ("    if ((c.tick -= dt) <= 0) { c.tick += TICK; if (!c.recall) sense(c); }   // v410: 복귀 중인 군인은 적을 무시",
   "    if (CHAPTER && c.recall && c.hold && !(c.soldier && c.master) && Math.hypot(c.foot.x - c.hold.x, c.foot.z - c.hold.z) <= CH_HOLD_NEAR) c.recall = false;   // c59: 자리(사수지역)로 돌아왔다\n"
   "    if ((c.tick -= dt) <= 0) { c.tick += TICK; if (!c.recall) sense(c); }   // v410: 복귀 중인 군인은 적을 무시"),
  # 빠르게: 서 있는 차·바리케이트는 둘레 칸의 몸하고만 부딪힘을 본다 (전엔 차마다 모든 몸을 훑었다 — 바리케이트 70여 개 × 몸 500여 명)
  ("      const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx;\n      for (const b of bodies) {\n        if (b.fixed || b.knockT > 0) continue;",
   "      const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx;\n      for (const b of (CHAPTER && car.state === 'parked' ? chNearBodies(car) : bodies)) {\n        if (b.fixed || b.knockT > 0) continue;"),
  ("      let vis = false;\n      for (const z of eyes) {", "      let vis = false;\n      for (const z of (CHAPTER && isZombie(me) ? nearIn(zCells, car.x, car.z, eyeMaxR + 2, chNB3) : eyes)) {   // c59: 둘레 칸의 좀비만"),
  # 빠르게: 사물을 훑을 때 먼 차·바리케이트는 거리 계산(삼각함수) 전에 거른다 — 바리케이트가 수십 개 놓여도 느려지지 않게
  ("if (o.type === 'car' && !o.dead) { const g = objGap(o, z);", "if (o.type === 'car' && !o.dead && Math.abs(o.car.x - z.foot.x) < 4 && Math.abs(o.car.z - z.foot.z) < 4) { const g = objGap(o, z);"),
  ("      const g = objGap(o, z);\n      if (g > (z === me || hotObj(o) ? z.sense : OBJ_SEE)",
   "      if (o.type === 'car' && (Math.abs(o.car.x - z.foot.x) > z.sense + 2 || Math.abs(o.car.z - z.foot.z) > z.sense + 2)) continue;   // c59\n      const g = objGap(o, z);\n      if (g > (z === me || hotObj(o) ? z.sense : OBJ_SEE)"),
  ("    if (CHAPTER) chRespawnTick(dt);   // c56", "    if (CHAPTER) chBarTick(dt);   // c59: 건널목 바리케이트와 수비대\n    if (CHAPTER) chRespawnTick(dt);   // c56"),
  ("chSafes(); chDispReset(); return; }", "chSafes(); chDispReset(); chBarReset(); return; }"),
  ("o.car.g.children[0].material.color.setHex(on ? TARGET_RED : 0x24305a);", "o.car.g.children[0].material.color.setHex(on ? TARGET_RED : o.car.barr ? 0xffffff : 0x24305a);   /* c59: 바리케이트는 원래 색(그림)으로 */"),
  ("zombify: makeZombie, slotOf, pop: () => chPop, awaken: awakenMe,", "zombify: makeZombie, slotOf, pop: () => chPop, awaken: awakenMe, bar: () => chBar, teams: () => teamWait, park: chParked, kills: (n) => { if (n !== undefined) deaths = n; return deaths; }, teamEv: () => CH_TEAM_EVENTS, incident: (x, z) => callPolice({ x, z }),"),
  ("  function showDud() {", C59_FN + "  function showDud() {"),
]
