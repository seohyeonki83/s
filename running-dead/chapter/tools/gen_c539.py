import pathlib
s = pathlib.Path('c538.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))

# ═══ 0. 플래그 · 표 ═══
rep("  const CH_RUN = CH_PICK === 'm' && !window.__noRun;", "  const CH_RUN = CH_PICK === 'm' && !window.__noRun;\n  const CH_TYPEB = CH_RUN && CH_STG === 3;   // c539: 챕터 3 = Type B (세로로 긴 맵 · 북쪽 군사기지)")
rep("  const CH_MIS_T = { e: [[3, 6], 30], n: [[4, 7], 50], h: [[5, 8], 70] };", "  const CH_MIS_T = { e: [[3, 6], 30], n: [[4, 7], 50], h: [[5, 8], 70] };\n  const CH_MIS_B = { e: [4, 10], n: [3, 9], h: [2, 8] };   // c539: Type B 서브 미션 (임시) — [검문소 점령 분, 클리어 분]")
L = s.split('\n'); i0 = next(k for k, l in enumerate(L) if l.startswith('  const chClrText = (d) =>'))
rep(L[i0], "  const chClrText = (d, n = CH_STG) => n === 3 ? '메인 기지 점령하기' : d === 'e' ? '특공대 3번 물리치기' : d === 'n' ? '특공대 4번 물리치기' : '보스 물리치기';   // c539")
rep("  const chMisTxt = (d, i) => { const M = CH_MIS_T[d]; return i ? `동료 ${M[1]}마리 모으기` : `${M[0][1]}분 안에 경보 '${CH_LVN[M[0][0] - 1]}' 도달`; };",
    "  const chMisTxt = (d, i, n = CH_STG) => { if (n === 3) { const B = CH_MIS_B[d]; return i ? `${B[1]}분 안에 스테이지 클리어` : `${B[0]}분 안에 검문소 점령`; } const M = CH_MIS_T[d]; return i ? `동료 ${M[1]}마리 모으기` : `${M[0][1]}분 안에 경보 '${CH_LVN[M[0][0] - 1]}' 도달`; };   // c539")
rep("chMisTxt(d, i)", "chMisTxt(d, i, n)")
rep("chClrText(d)", "chClrText(d, n)")
i1 = next(k for k, l in enumerate(L) if l.startswith('  const CH_STG_INFO = {'))
old = '\n'.join(L[i1:i1 + 5]); assert old.rstrip().endswith('};'), old[-40:]
rep(old, """  const CH_STG_INFO = {   // c539: 챕터 3 = Type B (북부 군사기지) · 장갑차는 챕터 4로
    1: { nm: '외곽 도시', ds: '감염이 처음 번진 조용한 도시.', boss: ['군인차 부대', '드론을 싣고 오는 군인차 3대', 'convoy'] },
    2: { nm: '공단 지구', ds: '공장과 창고가 늘어선 지구.', boss: ['불도저 2대', '벽을 부수며 돌진하는 불도저', 'dozer'] },
    3: { nm: '북부 군사기지', ds: '검문소 너머 군대가 지키는 기지.', boss: ['기지 수호 로봇', '기지 안을 지키는 거대한 사각 로봇', 'bbot'] },
    4: { nm: '국경 요새', ds: '군대가 지키는 마지막 도시.', boss: ['장갑차', '기관총을 쏘며 밀고 오는 장갑차', 'tank'] },
  };""")
# 아웃게임: 스테이지 4까지
rep("${[1, 2, 3].map((n) => [n, NODES[n][0] * 24, NODES[n][1] * 10])", "${[1, 2, 3, 4].map((n) => [n, NODES[n][0] * 24, NODES[n][1] * 10])")
rep("        if (n > 3) {", "        if (n > 4) {")
rep("    let curN = 1; for (const n of [1, 2, 3]) if (okN(n)) curN = n;", "    let curN = 1; for (const n of [1, 2, 3, 4]) if (okN(n)) curN = n;")
rep("else if (anim && anim.n < 3 &&", "else if (anim && anim.n < 4 &&")
rep("+a <= 3 &&", "+a <= 4 &&")
rep("kind: CH_RUN && CH_STG === 3 ? 'tank' : 'dozer'", "kind: CH_RUN && CH_STG === 4 ? 'tank' : 'dozer'")
rep("(CH_TUT ? '탈출하기' : CH_RUN ? (CH_DIF === 'h' ?", "(CH_TUT ? '탈출하기' : CH_TYPEB ? '메인 기지 점령' : CH_RUN ? (CH_DIF === 'h' ?")

# ═══ 1. 맵 ═══
rep("CH_MAIN ? chWorldGen(CH_BIGMAP, CH_SEED)", "CH_MAIN ? (CH_TYPEB ? chWorldGenB(CH_BIGMAP, CH_SEED) : chWorldGen(CH_BIGMAP, CH_SEED))")
rep("    const srcOf = (x, z) => SRC.findIndex((S) => inZ(S, x, z));\n    zones.forEach((Z, zi) => {\n      const S = SRC[Z.si], k = Z.k, f = Z.f;",
    "    const srcOf = (x, z) => SRC.findIndex((S) => inZ(S, x, z));\n    zones.forEach((Z, zi) => {\n      if (Z.custom) { out.zones.push([Z.x0, Z.z0, Z.x1, Z.z1]); out.net.push({ nodes: [], edges: [] }); out.ave.push({ V: null, H: null }); return; }   // c539: 손으로 짓는 구역 (군사기지)\n      const S = SRC[Z.si], k = Z.k, f = Z.f;")
rep("const span = cross.map((c) => { const p = zones[c.pi], q = zones[c.qi]; return c.x ? [p.x1, c.u - PW, q.x0, c.u + PW] : [c.u - PW, p.z1, c.u + PW, q.z0]; });",
    "const span = cross.map((c) => { const p = zones[c.pi], q = zones[c.qi], PW = M.passW / 2 * (c.wk || 1); return c.x ? [p.x1, c.u - PW, q.x0, c.u + PW] : [c.u - PW, p.z1, c.u + PW, q.z0]; });")
rep("      const rect = c.x ? [p.x1 - RH, u - PW, q.x0 + RH, u + PW] : [u - PW, p.z1 - RH, u + PW, q.z0 + RH];",
    "      const PW = M.passW / 2 * (c.wk || 1), rect = c.x ? [p.x1 - RH, u - PW, q.x0 + RH, u + PW] : [u - PW, p.z1 - RH, u + PW, q.z0 + RH];")
rep("  function chWorldBuild(M, SRC, zones, cross, seed, rnd) {", r"""  function chWorldGenB(M, seed0) {              // c539: Type B — 남쪽 큰 단락 덩어리(큰 1 + 작은 1 = 작은 단락 3개, 둘레 순환도로 하나) · 북쪽 끝 정사각형 군사기지 · 사이 검문소 하나
    let st = seed0 >>> 0; const rnd = () => { st = (st + 0x6D2B79F5) >>> 0; let t = st; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const ri = (n) => Math.floor(rnd() * n), GAP = M.gap * 1.875;
    const SRC = M.zones.map(([x0, z0, x1, z1], zi) => ({ zi, x0, z0, w: x1 - x0, h: z1 - z0, big: z1 - z0 > 60 }));
    const mk = (si) => { const S = SRC[si], k = ri(2) * 2, f = ri(2); return { si, k, f, W: S.w, H: S.h, g: 0 }; };   // 세로로 길게 — 180°만 돌리고 뒤집기
    const big = mk(ri(2)), small = mk(2 + ri(2)), pair = ri(2) ? [big, small] : [small, big];   // [북쪽, 남쪽]
    const NS = Math.round(Math.sqrt(0.7 * SRC[2].w * SRC[2].h));   // 작은 단락 넓이의 70% · 정사각형
    const W = big.W, N = { custom: true, si: -1, W: NS, H: NS, g: 0 };
    N.x0 = (W - NS) * (0.2 + 0.6 * rnd()); N.z0 = 0; N.x1 = N.x0 + NS; N.z1 = NS;
    const A = pair[0], B = pair[1]; A.x0 = 0; A.z0 = N.z1 + GAP; A.x1 = W; A.z1 = A.z0 + A.H; B.x0 = 0; B.z0 = A.z1; B.x1 = W; B.z1 = B.z0 + B.H; B.g = 4;   // B(남쪽)에서 시작
    const zones = [N, A, B], cx = W / 2, cz = B.z1 / 2;
    for (const z of zones) { z.x0 -= cx; z.x1 -= cx; z.z0 -= cz; z.z1 -= cz; }
    const u = (N.x0 + N.x1) / 2 + (rnd() - 0.5) * 4;
    const out = chWorldBuild(Object.assign({}, M, { passW: M.passW }), SRC, zones, [{ pi: 0, qi: 1, x: 0, u, g: GAP, wk: 1.5 }], seed0, rnd);
    out.passW = M.passW * 1.5; out.startZ = [2];
    // 군사기지 (북쪽 구역) — 메인 기지(맨 북쪽 · 문 3개) · 마당 · 막사 2+2 · 검문소 초소
    const bx = (N.x0 + N.x1) / 2, B0 = { x: bx, z: N.z0 + 2 + 5.5, w: 13, d: 11, doors: ['s', 'e', 'w'], locks: [], kinds: {}, local: out.b.length, block: -1, t: 'mbase', zone: 0 }; out.b.push(B0);
    const bks = [];
    for (const [sx, row] of [[-1, 0], [1, 0], [-1, 1], [1, 1]]) { const w = 8, d = 5.5, x = sx < 0 ? N.x0 + 2 + w / 2 : N.x1 - 2 - w / 2, z = N.z0 + 25.4 + row * 7.2;
      const b = { x, z, w, d, doors: [sx < 0 ? 'e' : 'w'], locks: [], kinds: {}, local: out.b.length, block: -1, t: 'bks', zone: 0 }; out.b.push(b); bks.push(b.local); }
    const ck = { x: u + M.passW / 2 * 1.5 + 1.6, z: N.z1 - 1.6, w: 2.4, d: 2.2, doors: ['w'], locks: [], kinds: {}, local: out.b.length, block: -1, t: 'chk', zone: 0 }; out.b.push(ck);
    out.typeB = { nz: 0, base: B0.local, bks, chk: ck.local, yz: N.z0 + 13 + SIGHT, bx };
    return out;
  }
  function chWorldBuild(M, SRC, zones, cross, seed, rnd) {""")
rep("      if (c.x) { out.passes2.push({ axis: 'v',", "      if (c.wk) out.passWk = c.wk;\n      if (c.x) { out.passes2.push({ axis: 'v',")
# 건물 종류 · 벽 · 문
rep("store: { name: '창고', col: '#7d6e5a', roof: 0x34302a },", "store: { name: '창고', col: '#7d6e5a', roof: 0x34302a }, mbase: { name: '군사기지', col: '#4d5b26', roof: 0x232b14 }, bks: { name: '막사', col: '#6b7b3f', roof: 0x2a3218 }, chk: { name: '검문소', col: '#c9a227', roof: 0x3a321a },   /* c539 */")
rep("    else if (type === 'army') star(64, 66, 38);", "    else if (type === 'army' || type === 'mbase') star(64, 66, 38);\n    else if (type === 'bks') text('막', 70);\n    else if (type === 'chk') text('검', 70);")
rep("police: 4.2, army: 4.2 };", "police: 4.2, army: 4.2, mbase: 3 * 0.7 * 1.5 * 4, bks: 4.2, chk: 4.2 };   /* c539: 메인 기지 벽 = 창고의 4배 */")
rep("if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5;", "if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5; if (CHAPTER && B.type === 'mbase') o.hp = o.maxHp = MY_DAMAGE * 19.5 * 4;   /* c539: 메인 기지 문 = 창고 문의 4배 */")
# 검문소 폭 1.5배 (CH_BAR_HALF) · 차 없는 구역
rep("CH_BAR_ROWS = 2, CH_BAR_HALF = 4;", "CH_BAR_ROWS = 2, CH_BAR_HALF = 4 * (CH_MAP.passWk || 1);")
rep("    chTr = { cars: [], Z: CH_MAP.zones.map(() => ({ n: 0, want: chTrWant(), t: 0 })), gone: CH_MAP.zones.map(() => []) };",
    "    chTr = { cars: [], Z: CH_MAP.zones.map((_, zi) => ({ n: 0, want: CH_MAP.net[zi] && CH_MAP.net[zi].nodes.length ? chTrWant() : 0, t: 0 })), gone: CH_MAP.zones.map(() => []) };   /* c539: 길 없는 구역은 차 없음 */")
rep("Z.n--; Z.want = chTrWant();", "Z.n--; Z.want = CH_MAP.net[T.zone] && CH_MAP.net[T.zone].nodes.length ? chTrWant() : 0;")
rep("    const [x, z] = chBarXZ(X, 0, CH_BAR_HALF - 0.75), t = addCitizen(x, z, square(x, z), 'soldier');",
    "    const [x, z] = chBarXZ(X, CH_TYPEB ? 2.6 * (X.side ? 1 : -1) : 0, CH_BAR_HALF - 0.75), t = addCitizen(x, z, square(x, z), 'soldier');   /* c539: Type B — 기본 2기 옆에 하나 더 */")

# ═══ 2. 배치 · 진행 ═══
rep("chDecoPlace(); if (!CH_TUT) chCull15(); chStartW = {", "chDecoPlace(); if (!CH_TUT) chCull15(); if (CH_TYPEB) chTypeBSetup(); chStartW = {")
rep("    if (CH_RUN) chRunTick(dt);", "    if (CH_RUN) chRunTick(dt);\n    if (CH_TYPEB) { chTypeBTick(dt); chSfHud(); return; }   // c539: Type B — 특공대 없음")
rep("    if (!chMis[0].done && chAL >= CH_MIS[0][0] && chRunT <= CH_MIS[0][1] * 60) chMis[0].done = true;\n",
    "    if (CH_TYPEB) { const B = CH_MIS_B[CH_DIF]; if (!chMis[0].done && chB && chB.chkCap && chRunT <= B[0] * 60) chMis[0].done = true; if (!chMis[1].done && chSf.won && chRunT <= B[1] * 60) chMis[1].done = true; }\n    else if (!chMis[0].done && chAL >= CH_MIS[0][0] && chRunT <= CH_MIS[0][1] * 60) chMis[0].done = true;\n")
rep("    if (!chMis[1].done && zombies.length - 1 >= CH_MIS[1]) chMis[1].done = true;", "    if (!CH_TYPEB && !chMis[1].done && zombies.length - 1 >= CH_MIS[1]) chMis[1].done = true;")
rep("  function chMisText(i) {", "  function chMisText(i) { if (CH_TYPEB) return (chMis[i].done ? '✓ ' : '· ') + chMisTxt(CH_DIF, i);   /* c539 */")
rep("  function chObjText() {\n", "  function chObjText() {\n    if (CH_TYPEB) { if (!chB) return '메인 기지 점령하기'; if (!chB.entered) return '메인 기지 점령하기'; return `기지 안 적 처치 · 남은 ${chB.inside.filter((c) => c.kind === 'citizen' && chExists(c)).length}`; }   // c539\n")
rep("    if (!CH_RUN || chSf.won) return P;", "    if (!CH_RUN || chSf.won) return P;\n    if (CH_TYPEB) { if (chB) P.push([(chB.base.x0 + chB.base.x1) / 2, (chB.base.z0 + chB.base.z1) / 2]); return P; }   // c539: 거점 하나")
rep("  function chMadRoll(c) {", r"""  let chB = null;
  function chTypeBSetup() {                     // c539: 군사기지 — 메인 기지 안 고정 병력 · 막사 · 마당 4팀 · 검문소 터렛 2기
    const T = CH_MAP.typeB, nzR = CH_MAP.zones[T.nz], inN = (x, z) => x >= nzR[0] && x <= nzR[2] && z >= nzR[1] && z <= nzR[3];
    { const cut = bodies.filter((b) => b.kind === 'citizen' && inN(b.foot.x, b.foot.z)); for (const b of cut) { for (const o of [b.mesh, b.hpBar, b.icon, b.gauge, b.mark, b.tracer, b.tracer2]) if (o && o.parent) o.parent.remove(o); b.kind = 'gone'; } bodies.splice(0, bodies.length, ...bodies.filter((b) => b.kind !== 'gone')); }
    const B0 = buildings.find((B) => B.local === T.base), BK = T.bks.map((l) => buildings.find((B) => B.local === l));
    const man = (B, type, x, z, r) => { const A = { x0: x - r, z0: z - r, x1: x + r, z1: z + r }, c = addCitizen(x, z, A, type); c.area = A; c.home = B || undefined; c.space = B || null; c.post = A; if (type === 'soldier' || type === 'robot') c.noMaster = true; enterNormal(c); return c; };
    const inside = [];
    { const kinds = ['soldier', ...Array(8).fill('robot')];
      kinds.forEach((t, i) => { const a = i / kinds.length * Math.PI * 2, x = (B0.x0 + B0.x1) / 2 + Math.cos(a) * 3.2, z = (B0.z0 + B0.z1) / 2 + Math.sin(a) * 2.6; inside.push(man(B0, t, x, z, 0.9)); });
      if (CH_DIF === 'h') { const c = man(B0, 'robot', (B0.x0 + B0.x1) / 2, (B0.z0 + B0.z1) / 2, 0.6); c.bBoss = true; c.hp = c.maxHp = c.maxHp / CH_SK * 5; chBossLook(c); inside.push(c); }   // 어려움 보스 — 덩치 크기 · 공격 2배 · 체력 사각의 5배 (스테이지 강화 빼고)
    }
    for (const B of BK) { const n = 2 + Math.floor(Math.random() * 3);
      for (let i = 0; i < n; i++) {
        if (Math.random() < 0.5) { const g = pickGoal(B); man(B, 'soldier', g.x, g.y, 0.8); }
        else { const left = B.doors.some((D) => D.s === 'e' || (D.L && D.L.side === 'e')) || (B.x0 + B.x1) / 2 < (nzR[0] + nzR[2]) / 2, A = left ? { x0: B.x1 + 0.7, z0: B.z0 - 0.6, x1: B.x1 + 3.2, z1: B.z1 + 0.6 } : { x0: B.x0 - 3.2, z0: B.z0 - 0.6, x1: B.x0 - 0.7, z1: B.z1 + 0.6 };
          const g = pickGoal(A), c = addCitizen(g.x, g.y, A, 'soldier'); c.area = A; c.noMaster = true; enterNormal(c); }   // 밖 — 자기 막사 둘레를 돈다
      } }
    { const sb = BK[Math.floor(Math.random() * BK.length)]; addSafe(sb); const s = sb.safe; s.B = sb; s.loot = chLoot(CH_DROP.army ? 'army' : 'store'); s.dud = !s.loot; s.room = null; }   // 막사 하나에 보물상자
    const teams = [], yard = [], zb = T.yz;
    for (const dx of [-12, -4, 4, 12]) { const tx = T.bx + dx; chParked(tx - 1.03, zb, 0, true); chParked(tx + 1.03, zb, 0, true);
      const hz = zb - 1.7; teams.push({ x: tx, z: hz });
      for (const [t, ox, oz] of [['soldier', -1, 0], ['soldier', 1, 0], ['robot', 0, -1]]) { const c = man(null, t, tx + ox, hz + oz, 0.7); c.yardT = teams.length - 1; c.lastHp = c.hp; yard.push(c); } }
    const X = chBar && chBar.X[0], turrets = [];
    if (X) for (const sgn of [-1, 1]) { const [x, z] = chBarXZ(X, 0, sgn * (CH_BAR_HALF - 0.75)), t = addCitizen(x, z, square(x, z), 'soldier');   // 검문소 기본 터렛 2기 (양쪽 벽)
      t.robot = t.turret = true; chRobotAny = true; t.noLure = true; t.fixed = true; t.met = true; t.sleep = false; t.tick = 0; t.hp = t.maxHp = t.maxHp * 3; t.r = BODY * 1.35; t.halfH = RADIUS * 1.35; t.mesh.scale.setScalar(1.35); t.mesh.geometry = chSqGeo; t.mesh.material.color.setHex(0x4d5560); chAddGun(t, 0.6, 0.2, 0x1a1d21); turrets.push(t); }
    const soHp = (() => { const c = addCitizen(0, 0, square(0, 0), 'soldier'), h = c.maxHp; for (const o of [c.mesh, c.hpBar, c.icon, c.gauge]) if (o && o.parent) o.parent.remove(o); c.kind = 'gone'; bodies.splice(bodies.indexOf(c), 1); return h; })();
    chB = { base: B0, inside, teams, yard, pool: 0, cd: 0, thr: soHp * 0.5, entered: false, waveT: 0, X, turrets, chkCap: false, nzR, inN };
  }
  function chBossLook(c) {                      // 기지 수호 로봇 — 덩치 크기 · 검붉은 몸 · 두꺼운 검은 테 · 쌍포 · 빨간 눈
    c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5); c.mesh.material.color.setHex(0x7a1212);
    const fr = new THREE.Mesh(chSqGeo, new THREE.MeshBasicMaterial({ color: 0x0b0b0b, transparent: true, depthTest: false, depthWrite: false })); fr.scale.setScalar(1.22); fr.position.z = -0.002; fr.renderOrder = c.mesh.renderOrder - 0.01; c.mesh.add(fr);
    for (const g of c.mesh.children.filter((o) => o !== fr)) if (g.geometry && g.geometry.type === 'PlaneGeometry') g.visible = false;
    for (const oy of [-0.2, 0.2]) { const g = new THREE.Mesh(new THREE.PlaneGeometry(0.75, 0.13).translate(0.375 + 0.05, 0, 0), new THREE.MeshBasicMaterial({ color: 0x111111, transparent: true, depthTest: false, depthWrite: false })); g.position.set(0.3, oy, 0.003); g.renderOrder = c.mesh.renderOrder + 0.02; c.mesh.add(g); }
    const eye = new THREE.Mesh(new THREE.CircleGeometry(0.13, 16), new THREE.MeshBasicMaterial({ color: 0xff2a2a, transparent: true, depthTest: false, depthWrite: false })); eye.position.set(0.05, 0, 0.004); eye.renderOrder = c.mesh.renderOrder + 0.03; c.mesh.add(eye);
  }
  function chBDispatch() {                      // 기지에서 1기 — 군인 60 · 사각 30 · 저격수 10 · 문 셋 중 아무 데 → 마당 4자리 중 아무 데를 지킨다
    const B = chB.base, r = Math.random(), type = r < 0.6 ? 'soldier' : r < 0.9 ? 'robot' : 'sniper';
    const L = B.locks[Math.floor(Math.random() * B.locks.length)], x = L.cx + (L.nx || 0) * 1.3, z = L.cz + (L.nz || 0) * 1.3;
    const T = chB.teams[Math.floor(Math.random() * chB.teams.length)], hx = T.x + rand(-1.2, 1.2), hz = T.z + rand(-1.0, 0.4), A = { x0: hx - 0.7, z0: hz - 0.7, x1: hx + 0.7, z1: hz + 0.7 };
    const c = addCitizen(x, z, A, type); c.area = A; c.post = A; c.met = true; c.noMaster = true; c.goal = pickGoal(A); c.back = true; c.lastHp = c.hp; c.yardT = chB.teams.indexOf(T); chB.yard.push(c);
  }
  function chBWaveSpot() {                      // 주기 팀이 나올 자리 — 검문소 앞 (우리 쪽). 우리가 검문소를 보거나 · 위에 있거나 · 북쪽에 있으면 북쪽 구역 바깥쪽 안 보이는 데
    const P = CH_MAP.passes2[0], nIsA = chB.inN(P.ax, P.az), sx = nIsA ? P.bx : P.ax, sz = nIsA ? P.bz : P.az, ux = Math.sign(sx - (nIsA ? P.ax : P.bx)) || 0, uz = Math.sign(sz - (nIsA ? P.az : P.bz)) || 0;
    const pts = [[(P.ax + P.bx) / 2, (P.az + P.bz) / 2], [sx, sz], [nIsA ? P.ax : P.bx, nIsA ? P.az : P.bz]], hw = CH_MAP.passW / 2;
    const onX = (z) => P.axis === 'h' ? Math.abs(z.foot.x - P.c) < hw + 0.5 && z.foot.z > Math.min(P.az, P.bz) - 0.5 && z.foot.z < Math.max(P.az, P.bz) + 0.5 : Math.abs(z.foot.z - P.c) < hw + 0.5 && z.foot.x > Math.min(P.ax, P.bx) - 0.5 && z.foot.x < Math.max(P.ax, P.bx) + 0.5;
    const danger = zombies.some((z) => chB.inN(z.foot.x, z.foot.z) || onX(z) || pts.some(([x, q]) => Math.hypot(x - z.foot.x, q - z.foot.z) <= z.sense && !blocked(z.foot.x, z.foot.z, x, q)));
    if (!danger) return [sx + ux * 5, sz + uz * 5];
    const R = chB.nzR; let best = null;
    for (let t = 0; t < 120; t++) { const e = Math.floor(Math.random() * 4), k = Math.random(), x = e === 0 ? R[0] + 1.5 : e === 1 ? R[2] - 1.5 : R[0] + 1.5 + k * (R[2] - R[0] - 3), z = e === 2 ? R[1] + 1.5 : e === 3 ? R[3] - 1.5 : R[1] + 1.5 + k * (R[3] - R[1] - 3);
      if (spaceOf(x, z) || !freeSpot(x, z, null)) continue;
      if (zombies.every((zz) => Math.hypot(x - zz.foot.x, z - zz.foot.z) > zz.sense + 2 || blocked(zz.foot.x, zz.foot.z, x, z))) { best = [x, z]; break; } }
    if (best) return best;
    const L = chB.base.locks[0]; return [L.cx + (L.nx || 0) * 1.5, L.cz + (L.nz || 0) * 1.5];
  }
  function chBWave() {                          // 주기 팀 — 경찰 3 + 사각 1 또는 사각 2 + 군인 1 (보통 · 어려움은 군인 2 더) → 나를 향해
    const comp = Math.random() < 0.5 ? ['police', 'police', 'police', 'robot'] : ['robot', 'robot', 'soldier']; if (CH_DIF !== 'e') comp.push('soldier', 'soldier');
    const [x0, z0] = chBWaveSpot();
    comp.forEach((t, i) => { const a = i / comp.length * Math.PI * 2; let x = x0 + Math.cos(a) * 1.2, z = z0 + Math.sin(a) * 1.2; if (!freeSpot(x, z, null)) { x = x0; z = z0; }
      const c = addCitizen(x, z, square(x, z), t); c.met = true; c.tkU = true; c.noMaster = true; c.bWave = true; c.tick = 0; });
  }
  function chTypeBTick(dt) {
    if (!chB) return;
    if (!chB.entered && zombies.some((z) => z.space === chB.base)) chB.entered = true;   // 기지 안으로 들어가면 출동 · 주기 팀 끝
    let lost = 0; chB.yard = chB.yard.filter((u) => { const ok = u.kind === 'citizen' && chExists(u); if (!ok) { lost += Math.max(0, u.lastHp || 0); return false; } if (u.hp < u.lastHp) lost += u.lastHp - u.hp; u.lastHp = u.hp; return true; });
    if (chB.cd > 0) chB.cd -= dt;
    if (!chB.entered) { if (chB.cd > 0) chB.pool = 0; else { chB.pool += lost; if (chB.pool >= chB.thr) { chB.pool = 0; chB.cd = rand(1, 2); chBDispatch(); } } }   // 마당 합산 피해 = 군인 체력의 50% → 1기 (1~2초 동안 다시 안 나온다)
    if (chAL >= 1 && !chB.entered) { const iv = CH_DIF === 'h' ? 40 : 60; if ((chB.waveT += dt) >= iv) { chB.waveT -= iv; chBWave(); } }   // 수상함부터 1분 (어려움 40초)마다 팀
    if (!chB.chkCap) { const tOk = chB.turrets.every((t) => !(t.kind === 'citizen' && chExists(t))), gOk = !chB.X || chB.X.units.every((c) => !(c.kind === 'citizen' && chExists(c))); if (tOk && gOk) chB.chkCap = true; }   // 검문소 점령
    if (!chSf.won && chB.inside.every((c) => !(c.kind === 'citizen' && chExists(c)))) chSf.won = true;   // 기지 안 병력까지 다 없애면 클리어
  }
  function chMadRoll(c) {""")
# 보스 로봇 공격 2배
rep("  function landHit(a, v, dmg = DAMAGE) {\n", "  function landHit(a, v, dmg = DAMAGE) {\n    if (a && a.bBoss) dmg *= 2;   // c539: 기지 수호 로봇 공격 2배\n")
# 일반 시작 자리 — Type B는 남쪽 구역에서
rep("      if (B.type === 'hill' || B.parent || CH_TUTT.has(B.type) || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;", "      if (B.type === 'hill' || B.parent || CH_TUTT.has(B.type) || B.type === 'mbase' || B.type === 'bks' || B.type === 'chk' || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;   /* c539: 군사기지 건물은 따로 */")
rep("B.sign = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 3.4),", "B.sign = new THREE.Mesh(new THREE.PlaneGeometry(B.type === 'chk' ? 1.7 : 3.4, B.type === 'chk' ? 1.7 : 3.4),")   # c539: 검문소 초소는 작은 표시
rep("  const CH_CLR_G = { e: 300, n: 300, h: 1000 };", "  const CH_CLR_G = { e: 300, n: 300, h: 1000 };\n  const CH_BBOT_IMG = '" + pathlib.Path('bbot_img.txt').read_text() + "';   // c539")
rep("<img src=\"${CH_BOSS_IMG[I.boss[2]]}\" alt=\"\">", "<img src=\"${I.boss[2] === 'bbot' ? CH_BBOT_IMG : CH_BOSS_IMG[I.boss[2]]}\" alt=\"\">")
pathlib.Path('c539_patch.py').write_text('C539_R = ' + repr(R) + '\n')
print(len(R))
