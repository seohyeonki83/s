# c86 패치 만들기 — c85.mjs(빌드된 c85 스크립트)에서 고칠 줄을 찾아 c86_patch.py 로 적는다
import pprint
S = open('c85.mjs', encoding='utf8').read(); L = S.split('\n'); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
def line(prefix):
    m = [l for l in L if l.startswith(prefix)]; assert len(m) == 1, (len(m), prefix[:80]); return m[0]

# 1. 미니맵: 수송차 물음표는 안 그린다
rep("    for (const c of cars) if (c.loot && c.seenQ && !c.looted) {", "    for (const c of cars) if (false && c.loot && c.seenQ && !c.looted) {   /* c86: 미니맵에 차 물음표 안 띄운다 */")

# 2. 경보단계: 수상함(1단계)까지는 그대로, 그 뒤 단계로 넘어가는 조건(감염 수)은 2배
a = line("  const STAR_AT = (() => {")
rep(a, a + "\n  for (let i = 1; i < STAR_AT.length; i++) STAR_AT[i] *= 2;   // c86: [10, 62, 150, 336, 724]")

# 3. 자폭: 범위 안 적의 점수 합이 가장 큰 동료 (노랑 1 · 주황 3 · 빨강 4 · 경찰 6 · 군인 8 · 저격수 40 · 나머지 0). 동점이면 아무나
rep("    let best = null, bT = -1, bN = -1, bD = Infinity;", "    let best = null, bT = -1, bN = -1, bD = Infinity, bS = -1, ties = [];")
rep("      let top = -1, n = 0, d = Infinity;\n      for (const c of nearIn(cCells, z.foot.x, z.foot.z, R, mutBuf)) {", "      let top = -1, n = 0, d = Infinity, sc = 0;\n      for (const c of nearIn(cCells, z.foot.x, z.foot.z, R, mutBuf)) {")
rep("        n++; const t = tier(c);", "        n++; const t = tier(c); if (CHAPTER) sc += CH_BOMB_PT[t];")
rep("      if (top < 0) continue;\n      if (top > bT ||", "      if (top < 0) continue;\n      if (CHAPTER) { if (sc > bS) { bS = sc; ties = [z]; } else if (sc === bS) ties.push(z); continue; }   // c86: 점수 합\n      if (top > bT ||")
rep("    if (!best) best = al.reduce(", "    if (CHAPTER && ties.length) best = ties[Math.floor(Math.random() * ties.length)];\n    if (!best) best = al.reduce(")

# 4. 사물·차·문·금고·바리케이트 통일: 공격 거리 안에 들어와야만 친다 (쫓아가지 않는다) · 갈 곳이 있으면 가면서 친다 (치는 순간 0.05초만 선다)
rep("      if (g > (z === me || hotObj(o) ? z.sense : OBJ_SEE) || (g >= bd && g >= ad)) continue;", "      if (g > (CHAPTER ? chObjLim(z, o) : z === me || hotObj(o) ? z.sense : OBJ_SEE) || (g >= bd && g >= ad)) continue;   /* c86 */")
rep("(z === me || n < CROWD_MAX)", "(CHAPTER || z === me || n < CROWD_MAX)", 2)
rep("const lim = z === me || hotObj(o) ? z.sense : OBJ_SEE;", "const lim = chReach(z);   /* c86 */")
rep("      if (Math.hypot(b.foot.x - z.foot.x, b.foot.z - z.foot.z) - (z === me ? 0 : b.r) <= (z === me || hotObj(b) ? z.sense : OBJ_SEE)) return b;",
    "      if (Math.hypot(b.foot.x - z.foot.x, b.foot.z - z.foot.z) - (CHAPTER || z !== me ? b.r : 0) <= (CHAPTER ? (z !== me && !b.dud && hotObj(b) ? 4 * MELEE : MELEE) : z === me || hotObj(b) ? z.sense : OBJ_SEE)) return b;   /* c86: 붙어야 친다 · 내가 치는 (아이템 든) 금고만 공격 거리 4배 안 동료를 부른다 */")
rep("  const hotObj = (o) => o.hotF !== undefined && o.hotF >= objFrame - 1;", "  const hotObj = (o) => o.hotF !== undefined && o.hotF >= objFrame - (CHAPTER ? 45 : 1);   /* c86: 가면서 칠 때는 한 대씩 띄엄띄엄 치므로 1.5초 동안 '치는 중' */")
rep(line("    if (z !== me) { const p = chHotOut; return p && !p.dead") + "\n", "")
rep("        const sf = !t && !noObj ? nearSafe(z) : null;", "        let sf = !t && !noObj && !(CHAPTER && go) ? nearSafe(z) : null;")
rep("          if (z.carT >= 1.25) forced = z.carHold; if (noObj) forced = null; }", "          if (z.carT >= 1.25) forced = z.carHold; if (noObj || CHAPTER) forced = null; }")
rep("        let ob = forced || (!t && !noObj ? nearObj(z) : null);", "        let ob = forced || (!t && !noObj && !(CHAPTER && go) ? nearObj(z) : null);\n        if (CHAPTER && z !== me && z.phase === 'track') { if (ob && objGap(ob, z) <= chReach(z)) ob = null; if (sf && Math.hypot(sf.foot.x - z.foot.x, sf.foot.z - z.foot.z) - sf.r <= MELEE) sf = null; }   // c86: 자리로 가는 중인 동료는 서서 치지 않는다 (가면서 친다)")
rep("        if (!noObj && !t && !ob && !go && !sf) ob = nearObj.any;", "        if (!CHAPTER && !noObj && !t && !ob && !go && !sf) ob = nearObj.any;")
rep("        else if (CHAPTER && !noObj && (z.propT = chNearFurn(z))) chHitFurn(z, z.propT, dt);", "        else if (CHAPTER && !noObj && (z === me || z.phase !== 'track') && (z.propT = chNearFurn(z))) chHitFurn(z, z.propT, dt);")
rep(line("    if (CHAPTER && z !== me && !z.space && z.mode === 'free' && !z.pick && chOutBlock(z, dt)) return;") + "\n", "")
a = "        else allyIdle(z, dt);\n      }\n    }\n"
rep(a, a + "    if (CHAPTER && z.mode === 'free') chMoveHit(z, dt);   // c86: 가는 길에 몸에 닿은 사물·차·문은 가면서 친다\n")
rep("  function showDud() {", r'''  // ── c86: 사물·차·문·금고·바리케이트를 한 가지 규칙으로 ──
  const CH_BOMB_PT = [0, 1, 3, 4, 6, 8, 40];   // 자폭 점수 (chTier 순서): 하양 0 · 노랑 1 · 주황 3 · 빨강 4 · 경찰 6 · 군인 8 · 저격수 40
  const CH_HIT_STOP = 0.05;                    // 가면서 칠 때 휘두르는 순간 서는 시간 (초)
  function chReach(z) { return MELEE - RADIUS + Math.max(0, (z.r || BODY) - BODY); }   // 사물 겉면까지 공격 거리
  function chObjLim(z, o) { return o.type === 'door' && z !== me && hotObj(o) ? 4 * MELEE : chReach(z); }   // 내가 치는 문만 공격 거리 4배 안 동료를 부른다
  function chTouch(z) {                        // 지금 손 닿는 것 하나 (차·문·바리케이트 → 금고 → 둥근·네모 사물)
    const o = nearObj(z); if (o && objGap(o, z) <= chReach(z)) return o;
    const s = nearSafe(z); if (s && Math.hypot(s.foot.x - z.foot.x, s.foot.z - z.foot.z) - s.r <= MELEE) return s;
    return chNearFurn(z);
  }
  function chMoveHit(z, dt) {                  // 갈 곳이 있어서 서지 않는 좀비 — 공격 쿨타임이 찼고 손 닿는 사물이 있으면 한 대 치고(그 순간만 선다) 다시 간다
    if (z.stopT > 0) { z.stopT -= dt; z.vel.set(0, 0); }
    if (z.atkT > 0 || (z.mhT = (z.mhT || 0) - dt) > 0) return;
    const th = chTouch(z); if (!th) { z.mhT = 0.12; return; }
    strike(z, th); z.atkT = HIT_EVERY; z.stopT = CH_HIT_STOP; z.vel.set(0, 0);
    if (th.kind === 'obj') { z.objT = th; z.objF = objFrame; }
    if (z === me) th.hotF = objFrame;
  }
  function showDud() {''')

rep("    steer(z.vel, wantV.set(0, 0), ACCEL * dt);\n    if (z === me && c.kind === 'safe') c.hotF = objFrame;",
    "    if (CHAPTER && c.kind === 'citizen' && chWallCut(z.foot.x, z.foot.z, c.foot.x, c.foot.z)) { steer(z.vel, toward(z, c.foot.x, c.foot.z, z.speed), ACCEL * dt); return; }   // c86: 바리케이트 너머 사람은 못 친다 — 계속 밀어붙이면서 (가면서 치기로) 바리케이트를 친다\n    steer(z.vel, wantV.set(0, 0), ACCEL * dt);\n    if (z === me && c.kind === 'safe') c.hotF = objFrame;")
# 5. 포인트(주유소·버스킹 둘레·농구장·공사 현장)에 하양·노랑이 더 모인다 — 길거리 하양·노랑의 10%(24명)를 판마다 다르게 나눠 얹는다. 주황은 가끔 한 명. 빨강은 없다
rep("    for (const S of CH_MAP.spots || []) {\n      const list = []; for (const [type, a, b] of S.mix) for (let k = N(a, b); k > 0; k--) list.push(type);",
    "    const SP = (CH_MAP.spots || []).filter((S) => S.k !== 'busker'), ex = SP.map(() => []), sw = SP.map(() => Math.random() ** 2 + 0.05), ws = sw.reduce((a, b) => a + b, 0);   // c86\n"
    "    for (let n = 24; n > 0; n--) { let r = Math.random() * ws, i = 0; while (i < sw.length - 1 && (r -= sw[i]) > 0) i++; ex[i].push(Math.random() < 0.68 ? '' : 'guard'); }\n"
    "    SP.forEach((S, i) => { if (Math.random() < 0.35) ex[i].push('attacker'); });\n"
    "    for (const S of CH_MAP.spots || []) {\n      const list = []; for (const [type, a, b] of S.mix) { if (type === 'vig') continue; for (let k = N(a, b); k > 0; k--) list.push(type); }\n      if (SP.includes(S)) list.push(...ex[SP.indexOf(S)]);")
rep("r = rand(r0, r1); x = cx + sg * Math.cos(a) * r;", "r = rand(r0, r1 + 1.2); x = cx + sg * Math.cos(a) * r;")
rep("r = S.rad * Math.sqrt(Math.random()); x = S.at[0]", "r = S.rad * 1.4 * Math.sqrt(Math.random()); x = S.at[0]")
open('c86_patch.py', 'w', encoding='utf8').write('# c86: 사물·차 통일 규칙(가면서 치기) · 경보단계 조건 2배 · 포인트 군집 · 자폭 점수 · 미니맵 물음표 제거 (gen_c86.py가 만든다)\nC86_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
