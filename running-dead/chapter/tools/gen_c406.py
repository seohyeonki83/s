# c406: 새 본 맵 — 시작할 때마다 새로 만드는 랜덤 9그룹 월드 (gen9.js) + 구역 4개를 가정한 곳 일반화
src = open('c405.mjs').read()
GEN = open('world/gen9.js').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))

# ── 1. 맵 데이터: 큰 맵을 따로 떼고, 본 맵은 그걸 재료로 만든다 ──
i0 = src.index('  const CH_MAP = CH_BASE ? '); i1 = src.index('\n', i0); L = src[i0:i1]
depth = 0; spans = []
for p, ch in enumerate(L):
    if ch == '{':
        if depth == 0: st = p
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0: spans.append((st, p + 1))
assert len(spans) == 3
BIG = L[spans[2][0]:spans[2][1]]
new = (GEN.rstrip('\n') + '\n'
  + '  const CH_BIGMAP = ' + BIG + ';   /* c366: 큰 맵 (map_main1.py) — c406: 본 맵의 재료이기도 하다 */\n'
  + "  const CH_SEED = CH_MAIN ? (window.__seed !== undefined ? window.__seed >>> 0 : Math.floor(Math.random() * 1e6)) : 0;   // c406: 본 맵 씨앗 — 시작할 때마다 새로 (같은 씨앗 = 같은 월드)\n"
  + L[:spans[2][0]] + 'CH_MAIN ? chWorldGen(CH_BIGMAP, CH_SEED) : CH_BIGMAP' + L[spans[2][1]:] + '\n'
  + "  if (CH_MAIN) { const v = document.getElementById('ver'); if (v) v.textContent += ' #' + CH_SEED; }\n"
  + "  for (const P of CH_MAP.passes2) if (P.mid === undefined) P.mid = P.axis === 'v' ? 0 : CH_MAP.zrMid;   // c406: 건널목마다 틈 한가운데 좌표 (큰 맵: 강 x = 0 · 산 z = zrMid)")
R.append((L, new))
rep("['m', '본 맵', '큰 맵 바탕 · 건널목 일자 · 수비대 가운데']", "['m', '본 맵', '그룹 9개 · 단락 36개 · 시작할 때마다 새로']")

# ── 2. 구역 수 일반화 ──
rep("  const chZoneOf = (x, z) => (x > 0 ? 1 : 0) + (z < CH_MAP.zrMid ? 2 : 0);   // 강 한가운데 x = 0, 산줄기 한가운데 z = zrMid 기준",
    "  const chZoneOf = (x, z) => { const Z = CH_MAP.zones; let bi = 0, bd = Infinity; for (let i = 0; i < Z.length; i++) { const q = Z[i], dx = x < q[0] ? q[0] - x : x > q[2] ? x - q[2] : 0, dz = z < q[1] ? q[1] - z : z > q[3] ? z - q[3] : 0, d = dx * dx + dz * dz; if (d < bd) { bd = d; bi = i; if (d === 0) break; } } return bi; };   // c406: 가장 가까운 구역 (구역이 몇 개든 — 큰 맵에서는 전과 같다: 강 x = 0 · 산 z = zrMid 기준)")
rep("s = Math.abs(v ? x : z - CH_MAP.zrMid)", "s = Math.abs((v ? x : z) - P.mid)")
rep("cx: v ? 0 : P.c, cz: v ? P.c : CH_MAP.zrMid", "cx: v ? P.mid : P.c, cz: v ? P.c : P.mid")
rep("chPopN = (big, small) => CH_BASE ? Math.round(big * CH_POPK) : CH_SMALL ? small : big;", "chPopN = (big, small) => CH_BASE || CH_MAP.world ? Math.round(big * CH_POPK) : CH_SMALL ? small : big;   /* c406: 본 맵도 넓이 비율대로 */")
rep("    const order = CH_MAP.zones.map((Z, i) => i); for (let i = order.length - 1; i > 0; i--) {", "    const order = (CH_MAP.startZ || CH_MAP.zones.map((Z, i) => i)).slice(); for (let i = order.length - 1; i > 0; i--) {   /* c406: 본 맵은 가운데 그룹에서 */")
rep("    return CH_MAP.start;\n  }\n  const CH_PINK", "    if (!CH_MAP.start) { const q = CH_MAP.zones[order[0]]; return [(q[0] + q[2]) / 2, q[1] + CH_MAP.ring / 2]; }\n    return CH_MAP.start;\n  }\n  const CH_PINK")
# 길 찾기: 그 구역·그 길목의 마디만 본다 (마디가 100개가 넘어도 계산이 안 는다) — 결과는 전과 같다
rep("  const chND = chNode.map((a, i) => chNode.map((b, j) =>", "  const chNodeZ = CH_MAP.zones.map(() => []); chNode.forEach((n, i) => chNodeZ[n.zone].push(i));   // c406: 구역마다 그 구역에 닿는 마디\n  const chNI = [], chNJ = [];\n  const chNodesOf = (o, out) => { out.length = 0; if (o.land) for (const i of chNodeZ[o.zone]) out.push(i); if (o.corr >= 0) for (const i of [o.corr * 2, o.corr * 2 + 1]) if (!out.includes(i)) out.push(i); if (o.corr >= 0 && out.length > 2) out.sort((p, q) => p - q); return out; };   // 그 자리에서 곧장 닿는 마디 (chSees와 같은 기준, 번호 순)\n  const chND = chNode.map((a, i) => chNode.map((b, j) =>")
rep("    const N = chNode.length;\n    for (let j = 0; j < N; j++) chTD[j] = chSees(chT, chNode[j]) ? Math.hypot(chNode[j].x - tx, chNode[j].z - tz) : Infinity;\n    let best = Infinity, bi = -1;\n    for (let i = 0; i < N; i++) {\n      const n = chNode[i]; if (!chSees(chS, n)) continue;\n      const d0 = Math.hypot(n.x - px, n.z - pz), d = d0 + (d0 < 0.6 ? 0.05 : 0);   // 이미 그 마디에 와 있으면 다음 마디가 이기게 (제자리에 서지 않게)\n      for (let j = 0; j < N; j++) { const c = d + chND[i][j] + chTD[j]; if (c < best) { best = c; bi = i; } }\n    }",
    "    const NI = chNodesOf(chS, chNI), NJ = chNodesOf(chT, chNJ);   /* c406: 내가 닿는 마디 × 목적지가 닿는 마디만 */\n    for (const j of NJ) chTD[j] = Math.hypot(chNode[j].x - tx, chNode[j].z - tz);\n    let best = Infinity, bi = -1;\n    for (const i of NI) {\n      const n = chNode[i];\n      const d0 = Math.hypot(n.x - px, n.z - pz), d = d0 + (d0 < 0.6 ? 0.05 : 0);   // 이미 그 마디에 와 있으면 다음 마디가 이기게 (제자리에 서지 않게)\n      for (const j of NJ) { const c = d + chND[i][j] + chTD[j]; if (c < best) { best = c; bi = i; } }\n    }")

# ── 3. 그림: 돌린 단락의 바닥 그림 · 물 · 다리 난간 ──
rep("    const mk = (A, draw) => { const [x0, z0, x1, z1] = A.r, W = x1 - x0, D = z1 - z0, tex = chTexOf(Math.round(W * K), Math.round(D * K), (g, w, h) => draw(g, w, h, (x) => (x - x0) * K, (z) => (z - z0) * K));\n      const m = new THREE.Mesh(new THREE.PlaneGeometry(W, D).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthTest: false, depthWrite: false })); m.position.set((x0 + x1) / 2, 0.03, (z0 + z1) / 2); m.renderOrder = -0.92; scene.add(m); };",
    "    const mk = (A, draw) => { const [x0, z0, x1, z1] = (A.src || A).r, W = x1 - x0, D = z1 - z0, tex = chTexOf(Math.round(W * K), Math.round(D * K), (g, w, h) => draw(g, w, h, (x) => (x - x0) * K, (z) => (z - z0) * K));   /* c406: 돌린 단락 — 그림은 원래 방향으로 그리고 판을 돌려(뒤집어) 놓는다 */\n      const m = new THREE.Mesh(new THREE.PlaneGeometry(W, D).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthTest: false, depthWrite: false, side: A.rf ? THREE.DoubleSide : THREE.FrontSide })); m.position.set((A.r[0] + A.r[2]) / 2, 0.03, (A.r[1] + A.r[3]) / 2); if (A.rf) m.scale.x = -1; if (A.rk) m.rotation.y = -A.rk * Math.PI / 2; m.renderOrder = -0.92; chStat(m, Math.hypot(W, D) / 2); };")
rep("        const [c0, c1, c2, c3] = A.can; g.fillStyle = 'rgba(0, 0, 0, 0)';   /* c111: 지붕 그림자도 없앤다 */ g.fillRect(X(c0), Z(c1), (c2 - c0) * K, (c3 - c1) * K);\n        for (const ix of A.isl) { const x = X(ix) - 0.5 * K, y = Z(A.iz) - 1.45 * K;",
    "        const [c0, c1, c2, c3] = (A.src || A).can; g.fillStyle = 'rgba(0, 0, 0, 0)';   /* c111: 지붕 그림자도 없앤다 */ g.fillRect(X(c0), Z(c1), (c2 - c0) * K, (c3 - c1) * K);\n        for (const ix of (A.src || A).isl) { const x = X(ix) - 0.5 * K, y = Z((A.src || A).iz) - 1.45 * K;")
rep("      const m = new THREE.Mesh(geo, waterMat); m.position.set((x0 + x1) / 2, 0.03, (z0 + z1) / 2); m.renderOrder = -0.92; scene.add(m);",
    "      const m = new THREE.Mesh(geo, waterMat); m.position.set((x0 + x1) / 2, 0.03, (z0 + z1) / 2); m.renderOrder = -0.92; chStat(m, Math.hypot(w, d) / 2);   /* c406: 물 토막이 많다 — 단락 묶음에 */")
rep("    for (const [x0, z0, x1, z1] of CH_MAP.bridges) {\n      flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, deckMat, -0.9);",
    "    for (const BR of CH_MAP.bridges) { const [x0, z0, x1, z1] = BR;\n      flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, deckMat, -0.9);")
rep("      const a0 = W.length ? Math.max(along ? x0 : z0, Math.min(...W.map((r) => along ? r[0] : r[1]))) : along ? x0 : z0, a1 = W.length ? Math.min(along ? x1 : z1, Math.max(...W.map((r) => along ? r[2] : r[3]))) : along ? x1 : z1;",
    "      const a0 = BR.length > 4 ? BR[4] : W.length ? Math.max(along ? x0 : z0, Math.min(...W.map((r) => along ? r[0] : r[1]))) : along ? x0 : z0, a1 = BR.length > 4 ? BR[5] : W.length ? Math.min(along ? x1 : z1, Math.max(...W.map((r) => along ? r[2] : r[3]))) : along ? x1 : z1;   /* c406: 본 맵 다리는 물 위 구간이 적혀 있다 */")

# ── 4. 다시 하기 — 본 맵은 월드를 새로 만든다 (화면을 다시 불러 본 맵을 바로 고른다. 안 되면 같은 월드에서 새 판) ──
rep("  retryEl.addEventListener('click', spawn);   // 다시 하기 = 처음부터와 같은 새 판 (v225)",
    "  retryEl.addEventListener('click', () => { if (!CH_MAP.world || window.__noReload) { spawn(); return; } try { window.name = 'rd-map:m'; setTimeout(spawn, 2500); location.reload(); } catch (e) { spawn(); } });   // 다시 하기 = 처음부터와 같은 새 판 (v225) · c406: 본 맵은 새 월드")
rep("  const CH_PICK = (window.__map || await new Promise((res) => {", "  const CH_PICK = (window.__map || (() => { try { if (window.name === 'rd-map:m') { window.name = ''; return 'm'; } } catch (e) {} return null; })() || await new Promise((res) => {   /* c406: 본 맵 '다시 하기'로 다시 불러온 화면은 바로 본 맵 */")

# ── 5. 본 맵 깔기 빠르게 — '가까이 누가 있나'를 전체를 훑지 않고 격자로 (본 맵을 깔 때만. 다른 맵은 전과 똑같이 전체를 훑는다) ──
rep("  var chBG = null, chBGn = 0, chRG = null, chRGn = 0, chRivL = null;\n",
    "  var chBG = null, chBGn = 0, chRG = null, chRGn = 0, chRivL = null;\n"
    "  var chSwG = null; const chSwA = [], chSwB = [], chSwC = [];   // c406: 본 맵을 까는 동안만 켜는 몸 자리 격자 (4칸)\n"
    "  function chSwAdd(b) { const k = Math.floor(b.foot.x / 4) * 8192 + Math.floor(b.foot.z / 4); let L = chSwG.get(k); if (!L) chSwG.set(k, L = []); L.push(b); }\n"
    "  function chSwNear(x, z, r, out) {            // (x, z) 둘레 r칸에 걸칠 수 있는 몸들 — 격자가 꺼져 있으면 전부 (전과 같다)\n"
    "    if (!chSwG) return bodies;\n"
    "    out.length = 0;\n"
    "    for (let cx = Math.floor((x - r) / 4), cxe = Math.floor((x + r) / 4); cx <= cxe; cx++) for (let cz = Math.floor((z - r) / 4), cze = Math.floor((z + r) / 4); cz <= cze; cz++) { const L = chSwG.get(cx * 8192 + cz); if (L) for (let i = 0; i < L.length; i++) out.push(L[i]); }\n"
    "    return out;\n"
    "  }\n")
rep("    b.space = spaceOf(x, z);                  // 들어 있는 건물 (밖이면 null) — 같은 공간끼리만 서로 본다\n    bodies.push(b);\n", "    b.space = spaceOf(x, z);                  // 들어 있는 건물 (밖이면 null) — 같은 공간끼리만 서로 본다\n    bodies.push(b); if (chSwG) chSwAdd(b);\n")
rep("new THREE.MeshBasicMaterial({ color: COLOR[kind], transparent: true, depthTest: false, depthWrite: false })", "new THREE.MeshBasicMaterial({ color: COLOR[kind] === undefined ? 0xffffff : COLOR[kind], transparent: true, depthTest: false, depthWrite: false })   /* c406: 색이 없는 종류(사물)는 흰색 — 전에도 흰색이었다 (경고만 안 뜬다) */")
rep("    if (CHAPTER) { chRoomDoors(); { const st = chStart(); me.foot.set(st[0], 0, st[1]); }", "    if (CHAPTER) { chRoomDoors(); { const st = chStart(); me.foot.set(st[0], 0, st[1]); } if (CH_MAP.world) chSwG = new Map();   /* c406 */")
rep("chTrReset(); return; }", "chTrReset(); chSwG = null; return; }")
rep("      if (Math.hypot(x - me.foot.x, z - me.foot.z) < keepStart || bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < minOwn)) continue;", "      if (Math.hypot(x - me.foot.x, z - me.foot.z) < keepStart || chSwNear(x, z, minOwn, chSwA).some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < minOwn)) continue;")
rep("!bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)", "!chSwNear(x, z, 0.9, chSwA).some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)")
rep("bodies.some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.0)", "chSwNear(g.x, g.y, 1.0, chSwA).some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.0)")
rep("bodies.some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.4)", "chSwNear(g.x, g.y, 1.4, chSwA).some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.4)")
rep("      if (bodies.some((b) => Math.hypot(b.foot.x - x, b.foot.z - z) < 1.2)) continue;\n      chReg(chPut(x, z, chRoamArea(x, z), ''), ''); w++;", "      if (chSwNear(x, z, 1.2, chSwA).some((b) => Math.hypot(b.foot.x - x, b.foot.z - z) < 1.2)) continue;\n      chReg(chPut(x, z, chRoamArea(x, z), ''), ''); w++;")
rep("!bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < (o.r || BODY) + BODY + 0.22);", "!chSwNear(x, z, 4, chSwA).some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < (o.r || BODY) + BODY + 0.22);")
rep("      for (const c of bodies) {               // 금고 자리에 겹친 사람은 옆으로", "      for (const c of chSwNear(s.foot.x, s.foot.z, 4, chSwB)) {               // 금고 자리에 겹친 사람은 옆으로")
rep("bodies.some((o) => o !== c && o.kind === 'citizen' && Math.hypot(o.foot.x - c.foot.x, o.foot.z - c.foot.z) < 1.0)", "chSwNear(c.foot.x, c.foot.z, 1.0, chSwC).some((o) => o !== c && o.kind === 'citizen' && Math.hypot(o.foot.x - c.foot.x, o.foot.z - c.foot.z) < 1.0)")
# 빈자리 판정: 건물 전체 대신 그 자리 둘레 건물만 (결과는 같다)
rep("    return buildings.every((B) => x <= B.x0 - 0.6 || x >= B.x1 + 0.6 || z <= B.z0 - 0.6 || z >= B.z1 + 0.6);", "    if (CHAPTER) { for (const B of chBNear(x - 0.6, z - 0.6, x + 0.6, z + 0.6, chQ14)) if (!(x <= B.x0 - 0.6 || x >= B.x1 + 0.6 || z <= B.z0 - 0.6 || z >= B.z1 + 0.6)) return false; return true; }   /* c406 */\n    return buildings.every((B) => x <= B.x0 - 0.6 || x >= B.x1 + 0.6 || z <= B.z0 - 0.6 || z >= B.z1 + 0.6);")
rep("chQ13 = [], chQR1 = []", "chQ13 = [], chQ14 = [], chQR1 = []")

# ── 6. 건널목 수비대 — 본 맵은 건널목이 60개쯤이라, 깨어 있는 곳의 건널목만 바로 늘리고 나머지는 그 건널목이 깨어날 때 밀린 단계를 한꺼번에 놓는다 ──
rep("  function chBarGrow(s) {                      // 경보 s단계가 됐다 — 건널목마다 바리케이트와 수비대를 늘린다 (말한 수에서 조금씩 다르게)\n    const N = (a, b) => a + Math.floor(Math.random() * (b - a + 1));\n    for (const X of chBar.X) {\n",
    "  function chBarGrow(s) {                      // 경보 s단계가 됐다 — 건널목마다 바리케이트와 수비대를 늘린다 (말한 수에서 조금씩 다르게)\n"
    "    for (const X of chBar.X) { if (CH_MAP.world && CH_SEC && !chSecAwake(X.cx, X.cz)) { (X.pend = X.pend || []).push(s); continue; } chBarGrowX(X, s); }   /* c406: 자고 있는 건널목은 미뤄 둔다 */\n"
    "    updateCarObs();\n"
    "  }\n"
    "  function chBarCatch() {                      // c406: 깨어난 건널목에 밀린 단계를 차례로 놓는다 (내 눈에 들어오기 전이다 — 단락은 12칸 밖에서 깨어난다)\n"
    "    if (!chBar) return; let n = 0;\n"
    "    for (const X of chBar.X) if (X.pend && X.pend.length && chSecAwake(X.cx, X.cz)) { for (const s of X.pend) chBarGrowX(X, s); X.pend.length = 0; n++; }\n"
    "    if (n) updateCarObs();\n"
    "  }\n"
    "  function chBarGrowX(X, s) {                  // 건널목 하나를 s단계만큼\n    const N = (a, b) => a + Math.floor(Math.random() * (b - a + 1));\n    {\n")
rep("c.gar = X; c.fresh = true; X.units.push(c); }\n      chBarForm(X);\n    }\n    updateCarObs();\n  }", "c.gar = X; c.fresh = true; X.units.push(c); }\n      chBarForm(X);\n    }\n  }")
rep("    if (woke) chSecWake(false);\n", "    if (woke) { chSecWake(false); if (CH_MAP.world) chBarCatch(); }\n")

# ── 7. 배회 경찰 — 본 맵은 자고 있는 구역 몫을 적어만 두고, 그 구역이 깨어날 때 세운다 (구역마다 수는 같다) ──
rep("      const p = chHiddenSpot(zi, 1.2); if (!p) continue; chReg(chCop(p), 'police'); chPop.copN = (chPop.copN || 0) + 1; }",
    "      if (CH_MAP.world && CH_SEC && !chSecs[zi].live) { (chPop.copOwe = chPop.copOwe || [])[zi] = (chPop.copOwe[zi] || 0) + 1; chPop.copN = (chPop.copN || 0) + 1; continue; }   /* c406 */\n"
    "      const p = chHiddenSpot(zi, 1.2); if (!p) continue; chReg(chCop(p), 'police'); chPop.copN = (chPop.copN || 0) + 1; }")
R.append(("  function chBarCatch() {", "  function chCopCatch() {                      // c406: 깨어난 구역에 밀린 배회 경찰을 세운다\n    const O = chPop && chPop.copOwe; if (!O) return;\n    for (let zi = 0; zi < O.length; zi++) if (O[zi] > 0 && chSecs[zi].live) { for (let n = O[zi]; n > 0; n--) { const p = chHiddenSpot(zi, 1.2); if (p) chReg(chCop(p), 'police'); } O[zi] = 0; }\n  }\n  function chBarCatch() {"))
R.append(("if (CH_MAP.world) chBarCatch(); }", "if (CH_MAP.world) { chBarCatch(); chCopCatch(); } }"))

# ── 8. 드론 길 찾기 격자 — 큰 지도에서는 칸마다 건물을 묻지 않고 건물 자리만 막는다 (결과는 같다) · 탐색은 2만 칸까지만 ──
rep("    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) free[j * W + i] = chDroneFree(x0 + i + 0.5, z0 + j + 0.5) ? 1 : 0;",
    "    if (CH_MAP.world) {                         // c406\n"
    "      for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) { const x = x0 + i + 0.5, z = z0 + j + 0.5; free[j * W + i] = x < MM.x0 + 0.5 || x > MM.x1 - 0.5 || z < MM.z0 + 0.5 || z > MM.z1 - 0.5 ? 0 : 1; }\n"
    "      for (const B of buildings) { if (B.parent) continue; for (let j = Math.max(0, Math.floor(B.z0 - 1 - z0)), je = Math.min(H - 1, Math.ceil(B.z1 + 1 - z0)); j <= je; j++) for (let i = Math.max(0, Math.floor(B.x0 - 1 - x0)), ie = Math.min(W - 1, Math.ceil(B.x1 + 1 - x0)); i <= ie; i++) { const x = x0 + i + 0.5, z = z0 + j + 0.5; if (x > B.x0 - 0.45 && x < B.x1 + 0.45 && z > B.z0 - 0.45 && z < B.z1 + 0.45) free[j * W + i] = 0; } }\n"
    "    } else\n"
    "    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) free[j * W + i] = chDroneFree(x0 + i + 0.5, z0 + j + 0.5) ? 1 : 0;")
rep("      while (h < e) { const c = q[h++]; if (c === g) { hit = c; break; } const ci0 = c % W, cj0 = (c - ci0) / W;", "      while (h < e && h < 20000) { const c = q[h++]; if (c === g) { hit = c; break; } const ci0 = c % W, cj0 = (c - ci0) / W;   /* c406: 2만 칸까지만 (큰 맵 전체 = 1만 7천 칸이라 다른 맵은 전과 같다) */")
open('c406_patch.py', 'w').write("# c406: 새 본 맵 — 랜덤 9그룹 월드\nC406_R = " + repr(R) + "\n")
print(len(R), 'entries')
