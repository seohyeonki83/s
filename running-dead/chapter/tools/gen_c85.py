# c85_patch.py 를 만든다 — 닻은 c84.mjs 에서 그대로 따 와서 개수를 확인한다
src = open('c84.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:100]); R.append((a, b, n))
art = open('c85_art.js').read(); fn = open('c85_fn.js').read()
# 1) 맨 먼저 필요한 것: 주차 칸·주차된 차가 피할 자리
rep("  const chZebras = [];   // c79: 횡단보도 자리 (네모)",
    "  const CH_OUT_KEEP = (CH_MAP.props || []).map(([t, x, z]) => { const r = (CH_MAP.pr || {})[t] || 0.4; return [x - r - 0.1, z - r - 0.1, x + r + 0.1, z + r + 0.1]; }).concat((CH_MAP.areas || []).map((A) => A.r));   // c85: 길거리 사물·자리 — 주차 칸과 주차된 차는 여기에 안 놓인다\n"
    "  const chZebras = [];   // c79: 횡단보도 자리 (네모)")
rep("    if (chBoxOnPath(box, 0.25)) return false;   // c83", "    if (chBoxOnPath(box, 0.25)) return false;   // c83\n    for (const q of CH_OUT_KEEP) if (chBoxHit(box, q, 0.1)) return false;   // c85")
# 2) 그림·사물 표 · 바닥 · 지붕
a = "  for (const P of Object.values(CH_PROP)) { P.geo = new THREE.PlaneGeometry(P.w, P.h); P.tex = chTexOf(P.px[0], P.px[1], P.draw); }"
rep(a, art + a)
# 3) 기능
rep("  function showDud() {", fn + "  function showDud() {")
# 4) 주유소 사무실 (집 종류 건물)
rep("garage: !!s.garage,", "garage: !!s.garage, gas: !!s.gas,")
rep("B.roof.material = flatMat(B.type === 'house' ? CH_HOUSE_ROOF[i % CH_HOUSE_ROOF.length] :", "B.roof.material = flatMat(B.gas ? 0x6e1d17 : B.type === 'house' ? CH_HOUSE_ROOF[i % CH_HOUSE_ROOF.length] :")
rep("      case 'house': wall('slab', P(0.75) ? 'bed' : 'sofa', 1, 0.7);", "      case 'house': if (S.gas) { wall('slab', 'counter', 1, 0.8); wall('slab', 'cooler', 1, 0.8); wall('prop', 'vending', 1); if (P(0.6)) scatter('box', 1); break; }   /* c85: 주유소 사무실 */ wall('slab', P(0.75) ? 'bed' : 'sofa', 1, 0.7);")
# 5) 새 판
rep("chPopulate(); chSafes(); chFurnPlace();", "chOutPlace(); chPopulate(); chSpotPeople(); chSafes(); chFurnPlace();")
rep("chSlabs.length = 0; chProps.length = 0; chFurnSpaces.length = 0; chFurnN = {}; chFurnT = 0;", "chSlabs.length = 0; chProps.length = 0; chFurnSpaces.length = 0; chFurnN = {}; chFurnT = 0; for (const p of chOutProps) chProps.push(p);   /* c85: 길거리 사물은 먼저 세워 뒀다 */")
rep("    for (const b of bodies) {                  // 먼저 깔린 사람이 차 밑에 깔렸으면 차 옆으로 빼 준다", "    chFuelCars();   // c85\n    for (const b of bodies) {                  // 먼저 깔린 사람이 차 밑에 깔렸으면 차 옆으로 빼 준다")
rep("      if (chOnRoad(x, z, 0.8)) continue;   // c71: 도로 위(와 바로 옆)는 뺀다 · c83: 휜 길도",
    "      if (chOnRoad(x, z, 0.8)) continue;   // c71: 도로 위(와 바로 옆)는 뺀다 · c83: 휜 길도\n"
    "      if ((CH_MAP.spots || []).some((S) => { const q = S.at || S.ring; return Math.hypot(x - q[0], z - q[1]) < 12; })) continue;   // c85: 사람이 모여 있는 자리(공원·주유소·농구장·공사장) 12칸 안에서는 시작하지 않는다")
# 6) 깨우기 · 치기
rep("    chFurnT = 0.3;\n", "    chFurnT = 0.3; chOutGrid.clear(); chOutMov.length = 0;   // c85\n")
rep("      if (S && S.fp) { S.fp.push(p);", "      if (!S && p.out && !p.sleep && !p.inv) chOutGridAdd(p);   // c85: 깨어 있는 길거리 사물 (칠 수 있는 것)\n      if (S && S.fp) { S.fp.push(p);")
rep("    const S = z.space; if (!S || !S.fp) return null;", "    const S = z.space; if (!S) return chNearOut(z); if (!S.fp) return null;   /* c85: 밖이면 길거리 사물 */")
rep("  const chHitFurn = (z, f, dt) => { if (f.kind === 'obj') fightObj(z, f, dt); else fight(z, f, dt); };", "  const chHitFurn = (z, f, dt) => { if (f.kind === 'obj') fightObj(z, f, dt); else { if (z === me && f.out) chHotOut = f; fight(z, f, dt); } };   /* c85: 내가 치는 길거리 사물 → 동료도 같이 친다 */")
rep("    if (b.prop) { const P = CH_PROP[b.prop]; chFurnBreak(", "    if (b.prop) { const P = CH_PROP[b.prop]; if (b.prop === 'pump') boom(b.foot.x, b.foot.z);   /* c85: 주유기는 터진다 (보기만) */ chFurnBreak(")
rep("    if (b.stick) { b.mesh.remove(b.stick); b.stick = null; b.vig = false; }", "    if (b.stick) { b.mesh.remove(b.stick); b.stick = null; b.vig = false; } if (b.tool) { b.mesh.remove(b.tool); b.tool = null; }   /* c85: 들고 있던 것(기타·연장)도 사라진다 */")
# 7) 부딪힘
rep("        b.foot.x += nx * push * kb;\n        b.foot.z += nz * push * kb;\n      }\n    }\n  }\n", "        b.foot.x += nx * push * kb;\n        b.foot.z += nz * push * kb;\n      }\n    }\n    if (CHAPTER && chBigOut.length) chBigCollide();   // c85\n  }\n")
rep("        if (b.fixed || (car.tr && b.sleep)) continue;   // c71", "        if (b.fixed) { if (CHAPTER && b.out) chCarSmash(car, b, fx, fz, rx, rz); continue; } if (b.sleep && (car.tr || b.out)) continue;   // c71 · c85: 달리는 차는 박힌 사물을 부수고 지나간다 · 자는 길거리 사물(좀비 시야 밖)은 차와 서로 없는 셈 친다")
a = "  function chCarHit(car, b, u, v, hu, hv, fx, fz, rx, rz, sp) {   // 달리는 차의 네모 안에 든 몸 — 처음 닿은 순간이면 친다 (튕김 + 데미지 + 차 감속). 아니면 밀리기만 한다\n"
rep(a, a + "    if (b.prop) { chCarProp(car, b, sp); return; }   // c85: 사물\n")
# 8) 보이기
rep("    if (b.space && !b.space.open) return false;", "    if (b.space && !b.space.open) return false;\n    if (CHAPTER && !b.space && chUnderRoof(b.foot.x, b.foot.z)) return false;   // c85: 닫힌 주유소 지붕 밑")
rep("      car.g.visible = vis; if (vis && car.loot) car.seenQ = true;   // c80", "      if (vis && CHAPTER && chUnderRoof(car.x, car.z)) vis = false;   // c85\n      car.g.visible = vis; if (vis && car.loot) car.seenQ = true;   // c80")
rep("    if (CHAPTER) chRoomDraw();   // c53", "    if (CHAPTER) { chRoomDraw(); chCanopyDraw(eyes); }   // c53 · c85")
rep("    g.fillStyle = ground; g.fillRect(0, 0, W, H);", "    g.fillStyle = ground; g.fillRect(0, 0, W, H);\n    for (const A of CH_MAP.areas || []) { g.fillStyle = A.k === 'park' ? 'rgba(70, 170, 80, 0.4)' : A.k === 'court' ? 'rgba(215, 115, 55, 0.45)' : A.k === 'site' ? 'rgba(150, 105, 60, 0.5)' : 'rgba(255, 255, 255, 0.16)'; g.fillRect(X(A.r[0]), Z(A.r[1]), (A.r[2] - A.r[0]) * sx, (A.r[3] - A.r[1]) * sz); }   // c85: 공원·농구장·공사장·주유소")
rep("    chDt = dt;   // c79\n    if (!chTr) return;", "    chDt = dt;   // c79\n    if (!chTr) return;\n    chTrProps();   // c85")
a = "    for (const [P, mat, o] of [[pos, lineMat, -0.89], [dp, dashMat, -0.895], [zp, zebraMat, -0.893]])"
rep(a, "    {                                         // c85: 정지선 (교차로로 들어가는 쪽 차선, 횡단보도 바로 앞) · 맨홀 뚜껑 — 꾸밈만\n"
       "      const stopL = (alongZ, c, hw, at, sg) => { const a0 = sg > 0 ? at + 0.95 : at - 1.2, a1 = a0 + 0.25, b0 = (alongZ ? sg > 0 : sg < 0) ? c + 0.12 : c - hw + 0.15, b1 = b0 + hw - 0.27; alongZ ? zq(b0, a0, b1, a1) : zq(a0, b0, a1, b1); };\n"
       "      const mh = [], hole = (x, z) => { if (chZebras.some((q) => x > q[0] - 2 && x < q[2] + 2 && z > q[1] - 2 && z < q[3] + 2)) return; for (let k = 0; k < 12; k++) { const a0 = k / 12 * Math.PI * 2, a1 = (k + 1) / 12 * Math.PI * 2; mh.push(x, 0, z, x + Math.cos(a1) * 0.34, 0, z + Math.sin(a1) * 0.34, x + Math.cos(a0) * 0.34, 0, z + Math.sin(a0) * 0.34); } };\n"
       "      for (const A of CH_MAP.ave) { const r = CH_MAP.ring / 2 + 1.25;\n"
       "        if (A.V) { stopL(true, A.V.c, A.V.hw, A.V.a + r, 1); stopL(true, A.V.c, A.V.hw, A.V.b - r, -1); if (A.H) { stopL(true, A.V.c, A.V.hw, A.H.c - A.H.hw - 1.25, -1); stopL(true, A.V.c, A.V.hw, A.H.c + A.H.hw + 1.25, 1); }\n"
       "          [0.16, 0.41, 0.66, 0.88].forEach((f, i) => hole(A.V.c + (i % 2 ? 1.3 : -1.3), A.V.a + (A.V.b - A.V.a) * f)); }\n"
       "        if (A.H) { stopL(false, A.H.c, A.H.hw, A.H.a + r, 1); stopL(false, A.H.c, A.H.hw, A.H.b - r, -1); if (A.V) { stopL(false, A.H.c, A.H.hw, A.V.c - A.V.hw - 1.25, -1); stopL(false, A.H.c, A.H.hw, A.V.c + A.V.hw + 1.25, 1); }\n"
       "          [0.22, 0.72].forEach((f, i) => hole(A.H.a + (A.H.b - A.H.a) * f, A.H.c + (i % 2 ? 1.2 : -1.2))); }\n"
       "      }\n"
       "      if (mh.length) { const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(mh), 3)); const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x55565a, transparent: true, depthTest: false, depthWrite: false, side: THREE.DoubleSide })); m.position.y = 0.031; m.renderOrder = -0.894; m.frustumCulled = false; scene.add(m); }\n"
       "    }\n" + a)
rep("furn: () => ({ props: chProps, slabs: chSlabs, n: chFurnN })", "furn: () => ({ props: chProps.filter((p) => !p.out), slabs: chSlabs, n: chFurnN })")   # 확인용: 건물 안 사물만 (길거리 사물은 outProps)
a = "    if (z.mut && z !== me && z.mode === 'free') { mutStep(z, dt); return; }"
rep(a, "    if (CHAPTER && z !== me && !z.space && z.mode === 'free' && !z.pick && chOutBlock(z, dt)) return;   // c85: 길을 막은 사물부터 부순다\n" + a)
rep("    for (const b of bodies) {                 // 걸음 전 자리·공간 — 건물 사람이 문 밖으로 나가면 그때부터 활동 영역 제한이 풀린다\n      if (b.sleep) continue;\n",
    "    for (const b of bodies) {                 // 걸음 전 자리·공간 — 건물 사람이 문 밖으로 나가면 그때부터 활동 영역 제한이 풀린다\n      if (b.sleep) continue;\n"
    "      if (b.out && (b.fixed || ((lazyFrame + (b.lazyK === undefined ? (b.lazyK = Math.floor(Math.random() * 8)) : b.lazyK)) & 7))) { b.px = b.foot.x; b.pz = b.foot.z; continue; }   // c85: 길거리 사물 — 박힌 것은 공간이 안 바뀐다 · 안 박힌 것은 8걸음에 한 번만 다시 본다\n")
rep("      const hide = !(b === me || isZombie(b) || seen(b, eyes));", "      const hide = b.out ? chOutHidden(b, eyes) : !(b === me || isZombie(b) || seen(b, eyes));   /* c85 */")
rep("zombies.some((z) => Math.hypot(z.foot.x - p.foot.x, z.foot.z - p.foot.z) < 16)",
    "(p.out ? chOutNearZ(p) : zombies.some((z) => Math.hypot(z.foot.x - p.foot.x, z.foot.z - p.foot.z) < 16))")
rep("    for (const b of bodies) if (!b.fixed && !b.sleep) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게",
    "    for (const b of bodies) if (!b.fixed && !b.sleep && !(b.out && b.foot.x === b.px && b.foot.z === b.pz)) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게 (c85: 이번 걸음에 안 밀린 길거리 사물은 건너뛴다)")
rep("    if (CHAPTER) for (const b of bodies) if (!b.fixed && !b.sleep) riverCollide(b);   // c3: 강",
    "    if (CHAPTER) for (const b of bodies) if (!b.fixed && !b.sleep && !(b.out && b.foot.x === b.px && b.foot.z === b.pz)) riverCollide(b);   // c3: 강")
rep("    if (CHAPTER) chSlabCollide();             // c70: 건물 안 네모 사물", "    if (CHAPTER) { chSlabCollide(); chOutCars(); }   // c70: 건물 안 네모 사물 · c85: 밀린 길거리 사물은 차 밖으로")
# ── 차도 사물처럼 기본 공격 대상 (테스트 맵 경찰차와 같은 규칙. 알아채는 거리만 짧다) ──
rep("    o.foot.set(car.x, 0, car.z); o.off = sp > 1.2;   // 달리는 차는 때릴 대상이 아니다",
    "    o.foot.set(car.x, 0, car.z); o.off = false;   // c85: 달리는 차도 때릴 대상이다 (가까이 있을 때만 알아챈다)")
rep("(CHAPTER && z === me ? chObjLists2 : chObjLists1)", "(CHAPTER ? chObjLists2 : chObjLists1)   /* c85: 동료도 — 서 있는 민간 차에 1.25초 막히면 그 차를 때린다 */")
rep("      if (z === me) { const reach = MELEE - RADIUS + Math.max(0, (z.r || BODY) - BODY);\n        for (const o of chDecoObjs) { if (o.dead || Math.abs(o.car.x - z.foot.x) > 5 || Math.abs(o.car.z - z.foot.z) > 5) continue; const g = objGap(o, z); if (g > reach && !(hotObj(o) && g <= z.sense)) continue; if (g < ad) { ad = g; any = o; } if (g < bd) { bd = g; best = o; } } }\n" + "      else if (chHotDeco && !chHotDeco.dead && hotObj(chHotDeco)) { const o = chHotDeco, g = objGap(o, z);\n        if (g <= z.sense) { const [px, pz] = objPoint(o, z); if (!blocked(z.foot.x, z.foot.z, px, pz)) { if (g < ad) { ad = g; any = o; } const n = (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0); if (g < bd && n < CROWD_MAX) { bd = g; best = o; } } } }\n",
    "      for (const o of chDecoObjs) {   // c85: 서 있는 민간 차도 경찰차와 똑같은 규칙 — 나는 인지거리, 동료는 근접 거리의 1.5배 안 (내가 때리는 차는 인지거리) · 한 대에 동료 3명까지\n"
    "        if (o.dead) continue; const lim = z === me || hotObj(o) ? z.sense : OBJ_SEE; if (Math.abs(o.car.x - z.foot.x) > lim + 3 || Math.abs(o.car.z - z.foot.z) > lim + 3) continue;\n"
    "        const g = objGap(o, z); if (g > lim || (g >= bd && g >= ad)) continue; const [px, pz] = objPoint(o, z); if (blocked(z.foot.x, z.foot.z, px, pz)) continue;\n"
    "        if (g < ad) { ad = g; any = o; } const n = (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0); if (g < bd && (z === me || n < CROWD_MAX)) { bd = g; best = o; } }\n")
rep("bar: () => chBar, trNet:", "bar: () => chBar, outProps: () => chOutProps, canopies: () => chCanopies, propDef: CH_PROP, tool: chTool, trNet:")
out = "# c85: 마을 꾸미기 — 공원 2 · 주유소 2 · 농구장 1 · 공사 현장 4 · 건물마다 어울리는 길거리 사물 · 가로등·신호등·버스 정류장 (map_deco.py · map_c85.json)\nC85_R = [\n"
for a, b, n in R: out += "  (" + repr(a) + ",\n   " + repr(b) + (", %d" % n if n != 1 else "") + "),\n"
out += "]\n"
open('c85_patch.py', 'w').write(out); print('replacements', len(R))
