# c405 (2단계): 내가 있는 단락만 돌린다 — 다른 단락의 사람·사물·차·문은 목록과 장면에서 빼 둔다
src = open('c405a.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))

MOD = r"""  // ── c405 (2단계): 내가 있는 단락만 돌린다 ──
  //   단락(구역)은 강·산으로 갈려 있어서 서로 물리적으로 영향을 주지 않는다. 나와 동료가 있는 단락(가까이 다가간 단락 포함)만 깨워 두고,
  //   나머지 단락의 사람·사물·차·문은 목록과 장면에서 통째로 빼 둔다 — 그대로 멈춰 있다가, 그 단락에 다가가면 그 자리에서 다시 나온다.
  //   빼지 않는 것: 나·동료 · 싸우거나 쫓거나 도망치는 중인 사람 · 사건 자리로 가는 출동 경찰 · 달리는 경찰차 · 보스 · 드론. 다시 채우기·경보·출동 시계는 그대로 돈다
  const CH_SEC_IN = 12, CH_SEC_OUT = 16, CH_SEC_GAP = 24;   // 좀비가 단락에서 12칸 안에 오면 깨운다 · 전부 16칸 밖으로 나가면 재운다 · 단락 사이 틈(건널목)은 깨어 있는 단락에서 24칸 안이면 깨어 있다
  const chSecs = CHAPTER ? CH_MAP.zones.map(([x0, z0, x1, z1], i) => ({ i, x0, z0, x1, z1, live: true })) : [];
  const CH_SEC = CHAPTER && chSecs.length > 1 && !CH_TUT;   // 단락이 하나뿐인 맵은 늘 전부 켜 둔다
  const chDormB = [], chDormC = [], chDormO = [], chSecZB = [];   // 빼 둔 몸 · 차 · 문·탁자
  let chSecT = 0, chSecK = 0;
  const chExists = (c) => !!c.dorm || bodies.includes(c), chExistsCar = (c) => !!c.dorm || cars.includes(c);   // 빼 둔 것도 '있는' 것이다
  function chSecAwake(x, z) {                  // 이 자리가 깨어 있는 곳인가 — 단락 안이면 그 단락이 깨어 있나, 단락 사이 틈이면 깨어 있는 단락에서 24칸 안인가
    for (let i = 0; i < chSecs.length; i++) { const S = chSecs[i]; if (x >= S.x0 && x <= S.x1 && z >= S.z0 && z <= S.z1) return S.live; }
    for (let i = 0; i < chSecs.length; i++) { const S = chSecs[i]; if (S.live && x > S.x0 - CH_SEC_GAP && x < S.x1 + CH_SEC_GAP && z > S.z0 - CH_SEC_GAP && z < S.z1 + CH_SEC_GAP) return true; }
    return false;
  }
  function chSecIdle(b) {                      // 깨어 있지만 아무 일도 없는 사람 (다른 단락에 남겨진 사람 — 좀비가 전부 20칸 밖)
    if (b.state !== 'normal' || b.boss || b.boarding || b.infect > 0 || b.stunT > 0 || b.knockT > 0 || b.pushT > 0 || b.lureAlert || b.goo || b.marked || b.heading || (b.calls && b.calls.length)) return false;
    const far = (z) => { const dx = z.foot.x - b.foot.x, dz = z.foot.z - b.foot.z; return dx * dx + dz * dz > CH_SLEEP * CH_SLEEP; };
    return far(me) && (G_W ? nearIn(zCells, b.foot.x, b.foot.z, CH_SLEEP, chSecZB).every((z) => !isZombie(z) || far(z)) : zombies.every(far));
  }
  const chBodyDormable = (b) => b.kind === 'safe' ? !(b.knockT > 0) : b.kind === 'citizen' && (b.sleep || chSecIdle(b));
  const chCarDormable = (c) => !c.tank && (c.state === 'parked' ? !!c.wreck || !!c.done || !c.crew || !c.crew.length : c.state === 'civ');   // 서 있는 차(꾸밈·바리케이트·잔해) · 돌아다니는 민간 차. 달리는 경찰차·사람이 다시 탈 차·보스는 그대로
  function chSceneCut() {                      // 장면에서 한꺼번에 뺀다 (dCut 표시한 것) — 하나씩 빼면 그때마다 장면 전체를 훑는다
    const ch = scene.children; let w = 0;
    for (let i = 0; i < ch.length; i++) { const o = ch[i]; if (o.dCut) { o.dCut = false; o.parent = null; } else ch[w++] = o; }
    ch.length = w;
  }
  function chSecOff(e, list) { e.dorm = true; e.dScn = []; let n = 0; for (const o of list) if (o && o.parent === scene) { o.dCut = true; e.dScn.push(o); n++; } return n; }
  function chSecOn(e) { e.dorm = false; if (e.dScn) for (const o of e.dScn) scene.add(o); e.dScn = null; }
  function chBigRebuild() { chBigOut.length = 0; for (const p of chOutProps) { const P = CH_PROP[p.prop]; if (P && P.r > 0.6) chBigOut.push(p); } }
  function chSecSleep() {                      // 깨어 있지 않은 곳에 있는 재울 수 있는 것들을 빼 둔다
    let cut = 0, nb = 0, nc = 0, w = 0;
    for (let i = 0; i < bodies.length; i++) { const b = bodies[i];
      if (b !== me && chBodyDormable(b) && !chSecAwake(b.foot.x, b.foot.z)) { cut += chSecOff(b, [b.mesh, b.hpBar, b.icon, b.gauge, b.mark, b.tracer, b.tracer2]); b.dP = 0; chDormB.push(b); nb++; continue; }
      bodies[w++] = b; }
    bodies.length = w;
    if (nb) { [chProps, chOutProps].forEach((L, bit) => { let k = 0; for (let i = 0; i < L.length; i++) { const p = L[i]; if (p.dorm) p.dP |= 1 << bit; else L[k++] = p; } L.length = k; }); chBigRebuild(); }
    w = 0;
    for (let i = 0; i < cars.length; i++) { const c = cars[i];
      if (chCarDormable(c) && !chSecAwake(c.x, c.z)) { cut += chSecOff(c, [c.g, c.tracer, c.obj && c.obj.hpBar]); c.dOL = 0; c.dTr = false; chDormC.push(c); nc++; continue; }
      cars[w++] = c; }
    cars.length = w;
    if (nc) {
      [objs, chDecoObjs].forEach((L, li) => { let k = 0; for (let i = 0; i < L.length; i++) { const o = L[i]; if (o.type === 'car' && o.car && o.car.dorm) o.car.dOL = li + 1; else L[k++] = o; } L.length = k; });
      if (chTr) { const T = chTr.cars; let k = 0; for (let i = 0; i < T.length; i++) { if (T[i].dorm) T[i].dTr = true; else T[k++] = T[i]; } T.length = k; }
      updateCarObs();
    }
    w = 0;
    for (let i = 0; i < objs.length; i++) { const o = objs[i], door = o.type === 'door';
      if ((door || (o.type === 'table' && o.t)) && !chSecAwake(door ? o.L.cx : o.t.x, door ? o.L.cz : o.t.z)) { cut += chSecOff(o, [o.hpBar]); chDormO.push(o); continue; }
      objs[w++] = o; }
    objs.length = w;
    if (cut) chSceneCut();
  }
  function chSecWake(all) {                    // 깨어 있는 곳에 있는 것들을 되돌린다 (all = 전부)
    let k = 0, nb = 0, nc = 0;
    for (let i = 0; i < chDormB.length; i++) { const b = chDormB[i];
      if (all || chSecAwake(b.foot.x, b.foot.z)) { chSecOn(b); b.offView = false; bodies.push(b); if (b.dP & 1) chProps.push(b); if (b.dP & 2) chOutProps.push(b); nb++; }
      else chDormB[k++] = b; }
    chDormB.length = k;
    if (nb) chBigRebuild();
    k = 0;
    for (let i = 0; i < chDormC.length; i++) { const c = chDormC[i];
      if (all || chSecAwake(c.x, c.z)) { chSecOn(c); cars.push(c); if (c.dOL === 1) objs.push(c.obj); else if (c.dOL === 2) chDecoObjs.push(c.obj); if (c.dTr && chTr) chTr.cars.push(c); nc++; }
      else chDormC[k++] = c; }
    chDormC.length = k;
    if (nc) updateCarObs();
    k = 0;
    for (let i = 0; i < chDormO.length; i++) { const o = chDormO[i], door = o.type === 'door';
      if (all || chSecAwake(door ? o.L.cx : o.t.x, door ? o.L.cz : o.t.z)) { chSecOn(o); objs.push(o); }
      else chDormO[k++] = o; }
    chDormO.length = k;
  }
  function chSecTick(dt) {                     // 0.2초마다: 어느 단락이 깨어 있나 → 새로 깬 단락은 되돌리고, 나머지는 빼 둔다
    if (!CH_SEC || window.__secOff) return;
    if ((chSecT -= dt) > 0) return;
    chSecT = 0.2;
    let woke = false, slept = false, any = false;
    for (const S of chSecs) {
      const m = S.live ? CH_SEC_OUT : CH_SEC_IN, near = (p) => p.foot.x > S.x0 - m && p.foot.x < S.x1 + m && p.foot.z > S.z0 - m && p.foot.z < S.z1 + m;
      let on = near(me); if (!on) for (let i = 0; i < zombies.length; i++) if (near(zombies[i])) { on = true; break; }
      if (on !== S.live) { if (on) woke = true; else slept = true; S.live = on; }
      if (on) any = true;
    }
    if (!any) { let bS = chSecs[0], bd = Infinity; for (const S of chSecs) { const dx = Math.max(S.x0 - me.foot.x, 0, me.foot.x - S.x1), dz = Math.max(S.z0 - me.foot.z, 0, me.foot.z - S.z1), d = dx * dx + dz * dz; if (d < bd) { bd = d; bS = S; } } if (!bS.live) { bS.live = true; woke = true; } }   // 어디에도 안 걸치면 가장 가까운 단락
    if (woke) chSecWake(false);
    if (slept || woke || ++chSecK >= 5) { chSecK = 0; if (chSecs.some((S) => !S.live)) chSecSleep(); }   // 재우기는 단락이 바뀐 때와 1초마다 (그 사이 잠든 사람·새로 나온 사람)
  }
  function chSecWakeAll() { if (!CH_SEC) return; for (const S of chSecs) S.live = true; chSecWake(true); chSecT = 0; chSecK = 0; }   // 새 판 — 전부 되돌려 놓고 처음부터
"""
rep("  function stepWorld(dt) {\n    clock += dt;\n", MOD + "  function stepWorld(dt) {\n    clock += dt;\n    if (CHAPTER) chSecTick(dt);   // c405: 내가 있는 단락만 돌린다\n")
# 새 판: 전부 되돌린 다음, 장면에서 몸 그림을 한꺼번에 뺀다 (하나씩 빼면 큰 지도에서 몇 초가 걸린다)
rep("  function spawn() {\n    for (const b of bodies) {\n",
    "  function spawn() {\n    if (CHAPTER) { chSecWakeAll(); for (const b of bodies) for (const o of [b.mesh, b.icon, b.gauge, b.hpBar, b.mark, b.tracer, b.tracer2]) if (o && o.parent === scene) o.dCut = true; for (const car of cars) if (car.g.parent === scene) car.g.dCut = true; chSceneCut(); }   // c405\n    for (const b of bodies) {\n")
# 장면에 없는 것을 빼라고 하면 바로 넘어간다 (찾느라 장면 전체를 훑지 않게)
rep("scene.remove = function (...os) { for (const o of os) { if (o && o.parent && o.parent !== scene) o.parent.remove(o); else rm0(o); } return scene; }; }",
    "scene.remove = function (...os) { for (const o of os) { if (!o || !o.parent) continue; if (o.parent !== scene) o.parent.remove(o); else rm0(o); } return scene; }; }")
# '있나' 확인 — 빼 둔 것도 있는 것
rep("      const crew = car.crew.filter((c) => bodies.includes(c) && c.kind === 'citizen' && c.hp > 0);", "      const crew = car.crew.filter((c) => chExists(c) && c.kind === 'citizen' && c.hp > 0);   /* c405 */")
rep("    X.units = X.units.filter((c) => c.kind === 'citizen' && bodies.includes(c));", "    X.units = X.units.filter((c) => c.kind === 'citizen' && chExists(c));   /* c405 */")
rep("  const chBarLive = (p) => !p.car.wreck && cars.includes(p.car);", "  const chBarLive = (p) => !p.car.wreck && chExistsCar(p.car);   /* c405 */")
rep("    for (let k = Q.length - 1; k >= 0; k--) if (!cars.includes(Q[k]) || Q[k].wreck) Q.splice(k, 1);", "    for (let k = Q.length - 1; k >= 0; k--) if (!chExistsCar(Q[k]) || Q[k].wreck) Q.splice(k, 1);")
# '나에게 오는 길' 거리 지도 — 큰 지도에서는 내 둘레만
rep("  function cfCompute() {                      // 나(안에 있으면 그 건물의 열린 문 앞)에서 모든 빈 칸까지 걸어서 가는 거리 — 곧은 걸음 5, 대각선 7\n    if (!cfBlock) cfInit();\n",
    "  const CF_WIN = 100;                         // c405: 지도가 이 창(내 둘레 ±100칸)보다 크면 창 안만 퍼뜨린다 — 창 테두리 칸을 잠깐 막았다가 되돌린다. 지도가 창보다 작으면 전과 똑같다\n"
    "  function cfCompute() {\n"
    "    if (!cfBlock) cfInit();\n"
    "    if (cfW - 2 <= CF_WIN * 2 && cfH - 2 <= CF_WIN * 2) { cfCompute0(); return; }\n"
    "    const cx = Math.floor((me.foot.x - MM.x0) / CF) + 1, cz = Math.floor((me.foot.z - MM.z0) / CF) + 1, ax = Math.max(0, cx - CF_WIN), bx = Math.min(cfW - 1, cx + CF_WIN), az = Math.max(0, cz - CF_WIN), bz = Math.min(cfH - 1, cz + CF_WIN), ring = [];\n"
    "    const put = (i) => { if (!cfBlock[i]) { cfBlock[i] = 1; ring.push(i); } };\n"
    "    for (let x = ax; x <= bx; x++) { put(az * cfW + x); put(bz * cfW + x); }\n"
    "    for (let z = az; z <= bz; z++) { put(z * cfW + ax); put(z * cfW + bx); }\n"
    "    cfCompute0();\n"
    "    for (const i of ring) cfBlock[i] = 0;\n"
    "  }\n"
    "  function cfCompute0() {                     // 나(안에 있으면 그 건물의 열린 문 앞)에서 모든 빈 칸까지 걸어서 가는 거리 — 곧은 걸음 5, 대각선 7\n    if (!cfBlock) cfInit();\n")
rep("  window.__rd = { get me() { return me; },", "  window.__rd = { get me() { return me; }, sec: () => ({ on: CH_SEC, secs: chSecs, dormB: chDormB, dormC: chDormC, dormO: chDormO, objs, props: chProps, outProps: chOutProps, big: chBigOut, scene, wakeAll: chSecWakeAll }),")
rep("'ms · 동료 ' + Math.max(0, zombies.length - 1);", "'ms · 동료 ' + Math.max(0, zombies.length - 1) + (CH_SEC ? ' · 단락 ' + chSecs.filter((S) => S.live).length + '/' + chSecs.length + ' · 몸 ' + bodies.length + '/' + (bodies.length + chDormB.length) : '');   /* c405: 깨어 있는 단락 수 · 돌고 있는 몸 수 */")
open('c405b_patch.py', 'w').write("# c405 (2단계): 내가 있는 단락만 돌린다\nC405B_R = " + repr(R) + "\n")
print(len(R), 'entries')
