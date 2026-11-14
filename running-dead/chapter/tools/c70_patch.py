# c70: 건물 안 사물 (본게임 튜토리얼의 책상·의자·큰 탁자 방식) · 부서질 때 조각 · 하트 (보관함 50번에 한 번, 최대 체력의 절반)
import pathlib
C70_FN = pathlib.Path(__file__).with_name('c70_fn.js').read_text(encoding='utf8')
C70_R = [
  # 둥근 사물도 몸끼리 부딪힘에 들어간다 (가장 큰 반지름 0.6)
  ("    for (const B of buildings) if (B.safe && !B.safe.dead && B.safe.r > rBig) rBig = B.safe.r;",
   "    for (const B of buildings) if (B.safe && !B.safe.dead && B.safe.r > rBig) rBig = B.safe.r;\n    if (CHAPTER && rBig < 0.6) rBig = 0.6;   // c70: 사물"),
  # 부서짐 — 사물은 먼지 + 조각 (전리품 없음, 보관함이면 가끔 하트)
  ("    if (CHAPTER && b.B) b.B.done = true;       // c19: 금고를 깬 건물 = 잠식 (지붕·미니맵 아이콘이 X로)",
   "    if (b.prop) { const P = CH_PROP[b.prop]; chFurnBreak(b.foot.x, b.foot.z, P, b.space, P.r > 0.45 ? 14 : 9, P.r > 0.45 ? 0.36 : 0.28); if (b.space) b.space.navDirty = true; return; }   // c70\n"
   "    if (CHAPTER) for (const Q of chFurnSpaces) if (Q === b.B || Q.parent === b.B) Q.navDirty = true;   // c70: 금고가 사라졌다 → 길 찾기 격자 다시\n"
   "    if (CHAPTER && b.B) b.B.done = true;       // c19: 금고를 깬 건물 = 잠식 (지붕·미니맵 아이콘이 X로)"),
  ("    } else {                                  // 경찰차: 폭발 + 연기 + 먼지 → 잔해만 남는다 (부딪힘 1/5)",
   "    } else if (o.type === 'table') {          // c70: 네모 사물 — 먼지와 조각을 남기고 사라진다\n"
   "      const t = o.t, k = chSlabs.indexOf(t), j = t.B.fs.indexOf(t), q = objs.indexOf(o);\n"
   "      if (k >= 0) chSlabs.splice(k, 1); if (j >= 0) t.B.fs.splice(j, 1); if (q >= 0) objs.splice(q, 1);\n"
   "      t.B.navDirty = true; scene.remove(t.m); chFurnBreak(t.x, t.z, CH_SLAB[t.type], t.B, 20, 0.42);\n"
   "    } else {                                  // 경찰차: 폭발 + 연기 + 먼지 → 잔해만 남는다 (부딪힘 1/5)"),
  ("else { boom(c.x, c.z); dust(c.x, c.z, 14, 2); }", "else { boom(c.x, c.z); dust(c.x, c.z, 14, 2); debris(c.x, c.z, 16, [c.col !== undefined ? c.col : c.mil ? 0x4a5a32 : 0x24305a, 0x151515, 0xa9bde8, 0x6c7386], 0.4, 7); }   /* c70: 차 조각 */"),
  ("      if (o.type === 'car') { if (o.hpBar) scene.remove(o.hpBar); objs.splice(i, 1); continue; }", "      if (o.type === 'car' || o.type === 'table') { if (o.hpBar) scene.remove(o.hpBar); objs.splice(i, 1); continue; }"),
  ("    if (o.type === 'door') { o.mesh.material = on ? lockRedMat : lockMat;", "    if (o.type === 'table') { o.t.m.material.color.setHex(on ? TARGET_RED : 0xffffff); return; }   // c70\n    if (o.type === 'door') { o.mesh.material = on ? lockRedMat : lockMat;"),
  ("o.hpBar.visible = !o.dead && o.hp < o.maxHp && !(o.L && o.L.out && !o.L.out.open);", "o.hpBar.visible = !o.dead && o.hp < o.maxHp && !(o.L && o.L.out && !o.L.out.open) && !(o.type === 'table' && !(o.B.parent || o.B).open);"),
  # 사물 모양
  ("    if (o.type === 'car') return [o.car.x, o.car.z];", "    if (o.type === 'car') return [o.car.x, o.car.z];\n    if (o.type === 'table') return [o.t.x, o.t.z];   // c70"),
  ("  function objGap(o, z) {                     // 좀비 몸 가운데에서 사물 겉면까지\n",
   "  function objGap(o, z) {                     // 좀비 몸 가운데에서 사물 겉면까지\n"
   "    if (o.type === 'table') {                 // c70: 네모 사물 (경찰차와 같은 방식)\n"
   "      const t = o.t, fx = Math.cos(t.h), fz = Math.sin(t.h), dx = z.foot.x - t.x, dz = z.foot.z - t.z;\n"
   "      const u = Math.abs(dx * fx + dz * fz) - t.L / 2, v = Math.abs(-dx * fz + dz * fx) - t.W / 2;\n"
   "      return Math.hypot(Math.max(u, 0), Math.max(v, 0));\n"
   "    }\n"),
  # 공격 순위 — 사물은 맨 마지막, 이미 닿는 것만. 길을 막으면 그것부터
  ("    for (const o of objs) {\n      if (o.dead || o.off) continue;\n      if (o.type === 'car' ? z.space :", "    for (const o of objs) {\n      if (o.dead || o.off || o.type === 'table') continue;   // c70: 건물 안 사물은 따로 (맨 마지막 순위)\n      if (o.type === 'car' ? z.space :"),
  ("{ const g = objGap(o, z); if (g <= reach && g < cd) { cd = g; cb = o; } }\n",
   "{ const g = objGap(o, z); if (g <= reach && g < cd) { cd = g; cb = o; } }\n"
   "          if (CHAPTER && z.space && z.space.fs) for (const t of z.space.fs) { if (t.obj.dead) continue; const g = objGap(t.obj, z); if (g <= reach && g < cd) { cd = g; cb = t.obj; } }   // c70: 네모 사물이 가로막고 있으면\n"),
  ("        else if (z === me) steer(z.vel, wantV.set(0, 0), ACCEL * dt);   // 나는 타겟이 없으면 살짝 미끄러지며 선다",
   "        else if (CHAPTER && !noObj && (z.propT = chNearFurn(z))) chHitFurn(z, z.propT, dt);   // c70: 건물 안 사물 — 정말 때릴 게 없을 때만 (맨 마지막 순위)\n"
   "        else if (z === me) steer(z.vel, wantV.set(0, 0), ACCEL * dt);   // 나는 타겟이 없으면 살짝 미끄러지며 선다"),
  ("if (!t) { const ob = nearObj(z), sf = nearSafe(z); if (ob) fightObj(z, ob, dt); else if (sf) fight(z, sf, dt); else allyIdle(z, dt); return; }",
   "if (!t) { const ob = nearObj(z), sf = nearSafe(z); if (ob) fightObj(z, ob, dt); else if (sf) fight(z, sf, dt); else if (CHAPTER && (z.propT = chNearFurn(z))) chHitFurn(z, z.propT, dt); else allyIdle(z, dt); return; }"),
  # 걸음마다
  ("    carCollide();                             // 경찰차에 겹친 몸은 밀어낸다", "    carCollide();                             // 경찰차에 겹친 몸은 밀어낸다\n    if (CHAPTER) chSlabCollide();             // c70: 건물 안 네모 사물"),
  ("    if (CHAPTER) chBarTick(dt);   // c59: 건널목 바리케이트와 수비대", "    if (CHAPTER) chFurnTick(dt);  // c70\n    if (CHAPTER) chBarTick(dt);   // c59: 건널목 바리케이트와 수비대"),
  ("chSafes(); chDispReset(); chBarReset(); chDecoPlace(); return; }", "chSafes(); chFurnPlace(); chDispReset(); chBarReset(); chDecoPlace(); return; }"),
  # 사람은 사물을 돌아간다 · 사물 자리는 배회 목표로 안 뽑는다
  ("if (a.doors ? !(a.rooms && a.rooms.some((R) => g.x > R.x0 - 0.6 && g.x < R.x1 + 0.6 && g.y > R.z0 - 0.6 && g.y < R.z1 + 0.6)) :",
   "if (a.doors ? !(a.rooms && a.rooms.some((R) => g.x > R.x0 - 0.6 && g.x < R.x1 + 0.6 && g.y > R.z0 - 0.6 && g.y < R.z1 + 0.6)) && !(CHAPTER && a.fs && n < 18 && chGoalBad(a, g.x, g.y, who)) :"),
  ("  function insideVia(b, B, tx, tz) {\n", "  function insideVia(b, B, tx, tz) {\n    if (CHAPTER && b.kind === 'citizen') { const w = chNav(b, B, tx, tz); if (w) return w; }   // c70: 사물·금고·방을 격자 길로 돌아간다\n"),
  ("  function pickGoal(a) {", "  function pickGoal(a, who) {"),
  ("return pickGoal(a.guardB);", "return pickGoal(a.guardB, who);"),
  ("    c.goal = inArea(c) ? null : pickGoal(c.area);", "    c.goal = inArea(c) ? null : pickGoal(c.area, c);"),
  ("if (CHAPTER && c.area.roam) chRoam(c); c.goal = pickGoal(c.area);", "if (CHAPTER && c.area.roam) chRoam(c); c.goal = pickGoal(c.area, c);"),
  # 건물 안 — 못 가는 목표는 바로 버리고, 막혔는지는 더 자주 본다 (1초에 0.2칸)
  ("      else toward(c, c.goal.x, c.goal.y, Math.min((c.back ? WALK_SPEED : CIT_WANDER) * (c.police ? POLICE_PACE : 1), d * 3));",
   "      else { toward(c, c.goal.x, c.goal.y, Math.min((c.back ? WALK_SPEED : CIT_WANDER) * (c.police ? POLICE_PACE : 1), d * 3)); if (CHAPTER && c.space) chSidestep(c); }   // c70: 건물 안에서는 앞사람을 비켜 간다"),
  ("c.gkT = clock + 2.5; c.gkX = c.foot.x; c.gkZ = c.foot.z; }   // c69: 이 목표까지 넉넉히 걸릴 시간", "c.gkT = clock + (c.space ? 1 : 2.5); c.gkX = c.foot.x; c.gkZ = c.foot.z; }   // c69: 이 목표까지 넉넉히 걸릴 시간\n      if (CHAPTER && c.navBad) { c.navBad = false; c.goalT = 0; }   // c70: 격자 길이 없는 목표"),
  ("if (Math.hypot(c.foot.x - c.gkX, c.foot.z - c.gkZ) < 0.3) c.goalT = 0; c.gkT = clock + 2.5;", "if (Math.hypot(c.foot.x - c.gkX, c.foot.z - c.gkZ) < (c.space ? 0.2 : 0.3)) c.goalT = 0; c.gkT = clock + (c.space ? 1 : 2.5);"),
  # 하트
  ("        pendingAward.push(p.kind);", "        if (p.kind === 'heart') chHeartEat(); else pendingAward.push(p.kind);   // c70"),
  ("bar: () => chBar, deco: () => chDeco,", "bar: () => chBar, furn: () => ({ props: chProps, slabs: chSlabs, n: chFurnN }), heart: chHeartDrop, nav: chNavOf, navPlan: chNavPlan, hearts: () => pickups.filter((q) => q.kind === 'heart').length, deco: () => chDeco,"),
  ("civ: type, kl: T.kl, kw: T.kw,", "civ: type, col, kl: T.kl, kw: T.kw,"),
  ("  function showDud() {", C70_FN + "  function showDud() {"),
]
