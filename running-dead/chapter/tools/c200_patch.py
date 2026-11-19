# c200: 집·랜드마크 벽을 부술 수 있다 · 보스 사거리(어그로)는 몸 둘레(원)부터 · 보스가 죽으면 군인 5 + 특공대 3팀
C200_R = [
 # ① 벽 토막 나누기 — 평균 집 = 문 빼고 8토막 (토막 길이는 같고, 큰 건물일수록 토막이 많다)
 ("  for (const sg of buildings.flatMap((B) => (B.type === 'hill' || B.parent ? [] : B.walls)))",
  """  const CH_WALL_T = { house: 3, bank: 6, fire: 6, mart: 6, hospital: 6, library: 6, conv: 6, gym: 6, police: 9, army: 12 };   // c200: 벽 체력 = 집 문의 몇 배
  const chWallBs = [], chWallObjs = [];
  { const hs = buildings.filter((B) => B.type === 'house' && !B.parent), sl = (w) => Math.hypot(w[2] - w[0], w[3] - w[1]);
    const LP = hs.length ? hs.reduce((s, B) => s + B.walls.reduce((t, w) => t + sl(w), 0), 0) / hs.length / 8 : 4, old = new Set(), add = [];
    for (const B of buildings) {
      if (B.parent || !CH_WALL_T[B.type]) continue;
      const out = [];
      for (const w of B.walls) { old.add(w); const [ax, az, bx, bz] = w, n = Math.max(1, Math.round(sl(w) / LP)); for (let i = 0; i < n; i++) out.push([ax + (bx - ax) * i / n, az + (bz - az) * i / n, ax + (bx - ax) * (i + 1) / n, az + (bz - az) * (i + 1) / n]); }
      B.walls = out; B.wos = []; B.wHit = new Map(); B.wN = 0; B.wNF = -1; add.push(...out); chWallBs.push(B);
      for (const q of out) { const o = { kind: 'obj', type: 'wall', B, seg: q, foot: new THREE.Vector3((q[0] + q[2]) / 2, 0, (q[1] + q[3]) / 2), hp: 1, maxHp: 1, dead: false, off: false, k: CH_WALL_T[B.type] }; q.wo = o; B.wos.push(o); chWallObjs.push(o); }
    }
    const keep = walls.filter((w) => !old.has(w)); walls.length = 0; walls.push(...keep, ...add);
    window.__walls = { bs: chWallBs, objs: chWallObjs, LP, brk: (o) => breakObj(o) };
  }
  for (const sg of buildings.flatMap((B) => (B.type === 'hill' || B.parent ? [] : B.walls)))"""),
 # ② 벽 = 사물 순위 · 사물보다 30% 짧게 알아챈다 · 때리는 좀비 한 마리당 그 건물 벽 전부 10%씩 멀리서
 ("  function chObjLim(z, o) { return ",
  "  function chWallN(B) { if (B.wNF !== objFrame) { B.wNF = objFrame; let n = 0; for (const [z, t] of B.wHit) { if (clock - t > 1.5 || clock < t) B.wHit.delete(z); else n++; } B.wN = n; } return B.wN; }   // c200: 이 건물 벽을 지금 때리는 좀비 수\n"
  "  function chObjLim(z, o) { if (o.type === 'wall') return chReach(z) * 0.7 * (1 + 0.1 * chWallN(o.B)); return "),
 ("    if (v.kind === 'obj') { if (!v.dead) {",
  "    if (v.kind === 'obj' && v.type === 'wall' && !v.dead) { if (a) v.B.wHit.set(a, clock); if (!v.hpBar) { addHpBar(v, hpFoeMat); v.hpDisp = v.hp; } }   // c200\n"
  "    if (v.kind === 'obj') { if (!v.dead) {"),
 ("    if (CHAPTER && z !== me) { z.noV = best; z.noT",
  """    if (CHAPTER) for (const B of chWallBs) {   // c200: 집·랜드마크 벽 (밖에서, 또는 그 건물 안에서)
      if (z.space && z.space !== B) continue;
      const lim = chReach(z) * 0.7 * (1 + 0.1 * chWallN(B)), m = lim + 0.5;
      if (z.foot.x < B.x0 - m || z.foot.x > B.x1 + m || z.foot.z < B.z0 - m || z.foot.z > B.z1 + m) continue;
      for (const o of B.wos) {
        if (o.dead) continue; const g = objGap(o, z); if (g > lim || (g >= bd && g >= ad)) continue;
        const [px, pz] = objPoint(o, z); if (blocked(z.foot.x, z.foot.z, px, pz)) continue;
        if (g < ad) { ad = g; any = o; } if (g < bd) { bd = g; best = o; }
      }
    }
    if (CHAPTER && z !== me) { z.noV = best; z.noT"""),
 ("    if (o.type === 'table') return [o.t.x, o.t.z];   // c70\n",
  "    if (o.type === 'table') return [o.t.x, o.t.z];   // c70\n"
  "    if (o.type === 'wall') { const p = nearestOn(o.seg, z.foot.x, z.foot.z), dx = z.foot.x - p.x, dz = z.foot.z - p.y, d = Math.hypot(dx, dz) || 1; return [p.x + dx / d * 0.6, p.y + dz / d * 0.6]; }   // c200: 벽 — 그 좀비 쪽 가장 가까운 자리\n"),
 # ③ 벽이 부서지면 그 토막이 통째로 뚫린다 (장갑차가 뚫은 자리와 같은 구멍) · 뒤에 방 벽이 붙어 있으면 같이
 ("    if (o.type === 'door') {                  // 문: 먼지만",
  "    if (o.type === 'wall') { chWallObjBreak(o); return; }   // c200\n    if (o.type === 'door') {                  // 문: 먼지만"),
 ("  function chWallBreak(B, sg, car) {",
  """  function chWallObjBreak(o) {                // c200: 벽 토막 하나가 통째로 뚫린다
    const B = o.B, q = o.seg, hz = q[1] === q[3], c = { x: (q[0] + q[2]) / 2, z: (q[1] + q[3]) / 2, hw: Math.hypot(q[2] - q[0], q[3] - q[1]) / 2 + 0.01 };
    chWallBreak(B, q, c);
    // 구멍이 좁으면(몸이 못 지나가면) 양옆 토막 끝을 조금씩 깎아 1.8칸까지 넓힌다
    const A = hz ? 0 : 1, ln = (s) => Math.abs(s[2 + A] - s[A]), L = B.doors[B.doors.length - 1];
    let lo = Math.min(q[A], q[2 + A]), hi = Math.max(q[A], q[2 + A]);
    const need = Math.max(0, (1.8 - (hi - lo)) / 2);
    if (need > 0) for (const [end, dir] of [[lo, -1], [hi, 1]]) {
      const n = B.wos.find((w) => !w.dead && (w.seg[1] === w.seg[3]) === hz && Math.abs(w.seg[1 - A] - q[1 - A]) < 1e-6 && (Math.abs(w.seg[A] - end) < 1e-6 || Math.abs(w.seg[2 + A] - end) < 1e-6));
      if (!n) continue;
      const s = n.seg, cut = Math.min(need, ln(s) - 0.3); if (cut <= 0) continue;
      if (!s.orig) s.orig = s.slice();
      if (Math.abs(s[A] - end) < 1e-6) s[A] += dir * cut; else s[2 + A] += dir * cut;
      chWallRedraw(n);
      if (dir < 0) lo -= cut; else hi += cut;
    }
    if (L && L.hole) { L.w = hi - lo; if (hz) L.cx = (lo + hi) / 2; else L.cz = (lo + hi) / 2; }
    if (hz) c.x = (lo + hi) / 2; else c.z = (lo + hi) / 2; c.hw = (hi - lo) / 2;
    rebuildSight(B); B.navDirty = true; visDirty = true;
    if (B.rooms) for (const R of B.rooms) for (const rs of R.walls.slice()) {
      if ((rs[1] === rs[3]) !== hz) continue;
      if (hz ? Math.abs(rs[1] - q[1]) > 1e-6 : Math.abs(rs[0] - q[0]) > 1e-6) continue;
      const lo = hz ? Math.min(rs[0], rs[2]) : Math.min(rs[1], rs[3]), hi = hz ? Math.max(rs[0], rs[2]) : Math.max(rs[1], rs[3]), m = hz ? c.x : c.z;
      if (hi <= m - c.hw + 0.05 || lo >= m + c.hw - 0.05) continue;
      chWallBreak(R, rs, c);
    }
  }
  function chWallRedraw(o) {                   // c200: 깎인 벽 토막 그림을 다시
    const s = o.seg; if (s.m) scene.remove(s.m);
    s.m = flat(Math.abs(s[2] - s[0]) + WALL, Math.abs(s[3] - s[1]) + WALL, (s[0] + s[2]) / 2, (s[1] + s[3]) / 2, wallMat, -0.505);
    o.foot.set((s[0] + s[2]) / 2, 0, (s[1] + s[3]) / 2);
  }
  function chWallObjReset() {                  // c200: 새 판 — 벽 체력 = 집 문 체력 × (집 3 · 랜드마크 6 · 경찰서 9 · 군부대 12)
    if (!chObjLists2.includes(chWallObjs)) chObjLists2.push(chWallObjs);
    const hd = objs.find((o) => o.type === 'door' && o.B.type === 'house'), u = hd ? hd.maxHp : MY_DAMAGE * 3.5;
    for (const o of chWallObjs) if (o.seg.orig) { for (let i = 0; i < 4; i++) o.seg[i] = o.seg.orig[i]; o.seg.orig = null; chWallRedraw(o); }
    for (const o of chWallObjs) { o.dead = false; o.hp = o.maxHp = u * o.k; o.hpDisp = o.hp; o.hotF = undefined; if (o.hpBar) o.hpBar.visible = false; }
    for (const B of chWallBs) { B.wHit.clear(); B.wN = 0; }
  }
  function chWallBreak(B, sg, car) {
    if (sg.wo && !sg.wo.dead) { breakObj(sg.wo); if (car && car.tkPh === 'dash') car.tkM -= 0.15; return; }   // c200: 벽 토막이면 통째로"""),
 ("c - CH_TK_HOLE), h1 = Math.min(hi, c + CH_TK_HOLE)", "c - (car.hw || CH_TK_HOLE)), h1 = Math.min(hi, c + (car.hw || CH_TK_HOLE))"),
 ("    for (const f of fx) scene.remove(f.s);\n    fx.length = 0;\n  }\n  function drawObjBars",
  "    if (CHAPTER) chWallObjReset();   // c200\n    for (const f of fx) scene.remove(f.s);\n    fx.length = 0;\n  }\n  function drawObjBars"),
 # ④ 보스: 좀비가 알아채는 거리(인지거리)를 몸 둘레(원)부터 잰다
 ("      const g = objGap(o, z);\n      if (g > (CHAPTER ? chObjLim(z, o) :",
  "      const tk = CHAPTER && o.type === 'car' && o.car.tank, g = tk ? Math.max(0, Math.hypot(o.car.x - z.foot.x, o.car.z - z.foot.z) - CAR_L * CH_TK_KL / 2) : objGap(o, z);   // c200: 보스는 몸 둘레(원)부터 인지거리\n"
  "      if (g > (tk ? z.sense : CHAPTER ? chObjLim(z, o) :"),
 # ⑤ 보스가 죽으면: 타고 있던 군인 5 (장갑차 자리에서) + 특공대 3팀 (군인 2씩) 동시 출동 — 다 잡아야 클리어
 ("    for (let i = 0; i < 3; i++) boom(car.x + rand(-1.6, 1.6), car.z + rand(-1, 1));\n  }",
  """    for (let i = 0; i < 3; i++) boom(car.x + rand(-1.6, 1.6), car.z + rand(-1, 1));
    if (!CHAPTER || car !== chTank) return;
    for (let i = 0; i < 5; i++) {               // c200: 타고 있던 군인 5
      const a = i / 5 * Math.PI * 2, r = rand(0.4, 1.2); let x = car.x + Math.cos(a) * r, z = car.z + Math.sin(a) * r;
      if (!freeSpot(x, z, null)) { x = car.x; z = car.z; }
      const c = addCitizen(x, z, square(x, z), G_); c.met = true; c.tkU = true; c.noMaster = true; c.tick = 0;
    }
    for (let i = 0; i < 3; i++) teamWait.push({ comp: [G_, G_], t: 0, first: false, seg: teamSeg(), tk: true });   // c200: 특공대 3팀 동시
    chSf.chk = 1;
  }"""),
]
