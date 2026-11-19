# c205: 계산 정리 (결과 같게)
#   ① 벽이 뚫린 건물 시야: 이어 붙은 벽 토막을 한 줄로 합쳐서 시야 벽을 만든다 (토막마다 네모 4변·모서리 4개 → 줄마다 한 번)
C205_R = [
 ("    const W = [], C = [], k = WALL / 2;\n    for (const sg of B.walls) {",
  "    const W = [], C = [], k = WALL / 2;\n    for (const sg of chMergeSegs(B.walls)) {"),
 ("  function chSightCut(B) {",
  """  function chMergeSegs(L) {                   // c205: 같은 줄 위에서 끝이 닿는 토막은 하나로 (모양은 그대로)
    const G = new Map(), out = [];
    for (const s of L) { const hz = s[1] === s[3], vt = s[0] === s[2]; if (!hz && !vt) { out.push(s); continue; } const key = (hz ? 'h' : 'v') + (hz ? s[1] : s[0]); let g = G.get(key); if (!g) G.set(key, g = []); g.push(hz ? [Math.min(s[0], s[2]), Math.max(s[0], s[2])] : [Math.min(s[1], s[3]), Math.max(s[1], s[3])]); }
    for (const [key, g] of G) {
      const hz = key[0] === 'h', c = +key.slice(1); g.sort((a, b) => a[0] - b[0]);
      let [a, b] = g[0];
      for (let i = 1; i <= g.length; i++) { if (i < g.length && g[i][0] <= b + 1e-6) { b = Math.max(b, g[i][1]); continue; } out.push(hz ? [a, c, b, c] : [c, a, c, b]); if (i < g.length) [a, b] = g[i]; }
    }
    return out;
  }
  function chSightCut(B) {"""),
]
# ② 이하: 결과가 같은 순서 바꾸기 · 안 쓰는 계산 빼기
C205_R += [
 # 경찰·군인 표적: 거리부터 보고 (더 먼 좀비는) 벽 검사를 안 한다
 ("      if (clear && fireBlocked(c.foot.x, c.foot.z, z.foot.x, z.foot.z)) continue;\n      const d = Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z);\n      if (d <= bd) { bd = d; best = z; }",
  "      const d = Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z);\n      if (d > bd || (clear && fireBlocked(c.foot.x, c.foot.z, z.foot.x, z.foot.z))) continue;   // c205: 거리 먼저\n      bd = d; best = z;"),
 # segRect: 부를 때마다 만들던 함수(clip)를 풀어 쓴다 (같은 식)
 ("""    let t0 = 0, t1 = 1;
    const dx = qx - px, dz = qz - pz;
    const clip = (k, q) => {
      if (Math.abs(k) < 1e-9) return q >= 0;
      const r = q / k;
      if (k < 0) { if (r > t1) return false; if (r > t0) t0 = r; } else { if (r < t0) return false; if (r < t1) t1 = r; }
      return true;
    };
    return clip(-dx, px - (B.x0 - pad)) && clip(dx, B.x1 + pad - px) && clip(-dz, pz - (B.z0 - pad)) && clip(dz, B.z1 + pad - pz) ? t0 : Infinity;""",
  """    let t0 = 0, t1 = 1, k, q, r;   // c205: clip 함수를 풀어 씀 (같은 식)
    const dx = qx - px, dz = qz - pz;
    k = -dx; q = px - (B.x0 - pad); if (Math.abs(k) < 1e-9) { if (q < 0) return Infinity; } else { r = q / k; if (k < 0) { if (r > t1) return Infinity; if (r > t0) t0 = r; } else { if (r < t0) return Infinity; if (r < t1) t1 = r; } }
    k = dx; q = B.x1 + pad - px; if (Math.abs(k) < 1e-9) { if (q < 0) return Infinity; } else { r = q / k; if (k < 0) { if (r > t1) return Infinity; if (r > t0) t0 = r; } else { if (r < t0) return Infinity; if (r < t1) t1 = r; } }
    k = -dz; q = pz - (B.z0 - pad); if (Math.abs(k) < 1e-9) { if (q < 0) return Infinity; } else { r = q / k; if (k < 0) { if (r > t1) return Infinity; if (r > t0) t0 = r; } else { if (r < t0) return Infinity; if (r < t1) t1 = r; } }
    k = dz; q = B.z1 + pad - pz; if (Math.abs(k) < 1e-9) { if (q < 0) return Infinity; } else { r = q / k; if (k < 0) { if (r > t1) return Infinity; if (r > t0) t0 = r; } else { if (r < t0) return Infinity; if (r < t1) t1 = r; } }
    return t0;"""),
 # around: 선분이 건물 근처에도 안 가면 segRect를 안 부른다
 ("      if (B.parent) continue;   // c53: 방은 건물 안이라 밖 길 찾기에서 뺀다\n      const t = segRect(px, pz, tx, tz, B, pad);",
  "      if (B.parent) continue;   // c53: 방은 건물 안이라 밖 길 찾기에서 뺀다\n      if (Math.min(px, tx) > B.x1 + pad || Math.max(px, tx) < B.x0 - pad || Math.min(pz, tz) > B.z1 + pad || Math.max(pz, tz) < B.z0 - pad) continue;   // c205\n      const t = segRect(px, pz, tx, tz, B, pad);"),
 ("    for (const O of aroundCars && !CHAPTER ? carObs : []) {", "    for (const O of aroundCars && !CHAPTER ? carObs : chNoObs) {   /* c205: 빈 배열을 매번 안 만든다 */"),
 ("  let aroundCars = true;", "  const chNoObs = [];\n  let aroundCars = true;"),
 # chLos: 같은 방식
 ("      if (segRect(px, pz, tx, tz, R, GAP) < Infinity) return false;",
  "      if (Math.min(px, tx) > R.x1 + GAP || Math.max(px, tx) < R.x0 - GAP || Math.min(pz, tz) > R.z1 + GAP || Math.max(pz, tz) < R.z0 - GAP) continue;   // c205\n      if (segRect(px, pz, tx, tz, R, GAP) < Infinity) return false;"),
 # chSlotFix: 근처가 아니면 segRect 생략 · 첫 바퀴에 바뀐 게 없으면 두 번째 바퀴 생략
 ("""    for (let k = 0; k < 2; k++) for (const R of chBlocks) {
      const t = segRect(mx, mz, x, y, R, 0);  // 나 → 자리 선이 강·산에 처음 닿는 곳
      if (t < Infinity) { x = mx + (x - mx) * t; y = mz + (y - mz) * t; }
      if (x <= R.x0 - m || x >= R.x1 + m || y <= R.z0 - m || y >= R.z1 + m) continue;""",
  """    for (let k = 0, ch = true; k < 2 && ch; k++) { ch = false; for (const R of chBlocks) {   // c205: 첫 바퀴에 안 바뀌면 두 번째는 같은 결과라 생략
      const t = Math.min(mx, x) > R.x1 || Math.max(mx, x) < R.x0 || Math.min(mz, y) > R.z1 || Math.max(mz, y) < R.z0 ? Infinity : segRect(mx, mz, x, y, R, 0);  // 나 → 자리 선이 강·산에 처음 닿는 곳
      if (t < Infinity) { const nx = mx + (x - mx) * t, ny = mz + (y - mz) * t; if (nx !== x || ny !== y) ch = true; x = nx; y = ny; }
      if (x <= R.x0 - m || x >= R.x1 + m || y <= R.z0 - m || y >= R.z1 + m) continue;
      ch = true;"""),
 ("      if (q === l) x = R.x0 - m; else if (q === r) x = R.x1 + m; else if (q === u) y = R.z0 - m; else y = R.z1 + m;\n    }\n    chSlotOut[0] = x;",
  "      if (q === l) x = R.x0 - m; else if (q === r) x = R.x1 + m; else if (q === u) y = R.z0 - m; else y = R.z1 + m;\n    } }\n    chSlotOut[0] = x;"),
 # 좀비: 쫓을 사람이 이미 있으면 '근접 거리 안 적' 찾기는 결과에 안 쓰여서 생략
 ("const adj = CHAPTER ? chAdjFoe(z) : null, go = t || prey || adj;", "const adj = CHAPTER && !t && !prey ? chAdjFoe(z) : null, go = t || prey || adj;   /* c205: t·prey가 있으면 안 쓰인다 */"),
 # 근접 적 찾기: 거리부터 보고 바리케이트 검사
 ("      if (c.kind !== 'citizen' || !(c.hp > 0) || c.space !== z.space || c.marked || chWallCut(z.foot.x, z.foot.z, c.foot.x, c.foot.z)) continue;   // 바리케이트 너머는 빼고\n      const d = Math.hypot(c.foot.x - z.foot.x, c.foot.z - z.foot.z);\n      if (d <= MELEE + Math.max(0, (z.r || BODY) - BODY) + Math.max(0, (c.r || BODY) - BODY) && d < bd) { bd = d; best = c; }",
  "      if (c.kind !== 'citizen' || !(c.hp > 0) || c.space !== z.space || c.marked) continue;\n      const d = Math.hypot(c.foot.x - z.foot.x, c.foot.z - z.foot.z);\n      if (d <= MELEE + Math.max(0, (z.r || BODY) - BODY) + Math.max(0, (c.r || BODY) - BODY) && d < bd && !chWallCut(z.foot.x, z.foot.z, c.foot.x, c.foot.z)) { bd = d; best = c; }   // 바리케이트 너머는 빼고 (c205: 거리 먼저)"),
 # 시야: 내가 좀비면(거의 늘) eyes 목록 전체 검색을 안 한다
 ("    if (eyes.includes(me) && !isZombie(me)) {", "    if (!isZombie(me) && eyes.includes(me)) {   /* c205: 순서만 */"),
 # 주유소 지붕: 챕터는 늘 열려 있다 → 밑에 있나 검사 생략
 ("chCanopies.push({ x0: c0, z0: c1, x1: c2, z1: c3, m, open: false });", "chCanopies.push({ x0: c0, z0: c1, x1: c2, z1: c3, m, open: CHAPTER });   /* c205: 챕터는 처음부터 열림 */"),
 ("  const chUnderRoof = (x, z) => { for", "  const chUnderRoof = (x, z) => { if (CHAPTER) return false; for"),
 # 금고: 거리부터 (먼 금고는 문 너머 검사 안 함)
 ("      if (!b || b.dead || (b.space !== z.space && !chSafeReach(z, b))) continue;   /* c54: 방 안 금고는 열린 문 너머로도 */\n      if (Math.hypot(b.foot.x - z.foot.x, b.foot.z - z.foot.z) - (CHAPTER || z !== me ? b.r : 0) <= (CHAPTER ? (z !== me && !b.dud && hotObj(b) ? 4 * MELEE : MELEE) : z === me || hotObj(b) ? z.sense : OBJ_SEE)) return b;",
  "      if (!b || b.dead) continue;\n      if (Math.hypot(b.foot.x - z.foot.x, b.foot.z - z.foot.z) - (CHAPTER || z !== me ? b.r : 0) <= (CHAPTER ? (z !== me && !b.dud && hotObj(b) ? 4 * MELEE : MELEE) : z === me || hotObj(b) ? z.sense : OBJ_SEE) && (b.space === z.space || chSafeReach(z, b))) return b;   /* c54: 방 안 금고는 열린 문 너머로도 · c205: 거리 먼저 */"),
 # 챕터에서 안 쓰는 '차에 막힘' 블록 · 3명 제한 계산
 ("        { let cb = null, cd = Infinity; const reach = MELEE - RADIUS + Math.max(0, (z.r || BODY) - BODY);", "        if (!CHAPTER) { let cb = null, cd = Infinity; const reach = MELEE - RADIUS + Math.max(0, (z.r || BODY) - BODY);   /* c205: 챕터에선 결과가 늘 null */"),
 ("      if (g < ad) { ad = g; any = o; }\n      const n = (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0);\n      if (g < bd && (CHAPTER || z === me || n < CROWD_MAX)) { bd = g; best = o; }",
  "      if (g < ad) { ad = g; any = o; }\n      if (g < bd && (CHAPTER || z === me || (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0) < CROWD_MAX)) { bd = g; best = o; }   /* c205: 챕터는 3명 제한을 안 센다 */"),
 ("if (g < ad) { ad = g; any = o; } const n = (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0); if (g < bd && (CHAPTER || z === me || n < CROWD_MAX)) { bd = g; best = o; } }",
  "if (g < ad) { ad = g; any = o; } if (g < bd) { bd = g; best = o; } }   /* c205 */"),
 # 길거리 경찰: 1.5배(최대)에 닿으면 더 계산할 게 없다
 ("    if (!chPop || CH_BT) return;\n    const base = CH_COPS", "    if (!chPop || CH_BT || chPop.copK === 1.5) return;   // c205: 최대에 닿으면 끝\n    const base = CH_COPS"),
 # 소개: 챕터(시험 맵)는 판 시작에 전부 본 것으로 → 매 프레임 사람 전체 훑기 생략
 ("  function checkTut() {                       // 처음으로 내 시야에 들어온 종류 → 소개 줄 세우기\n    for (const b of bodies) {",
  "  function checkTut() {                       // 처음으로 내 시야에 들어온 종류 → 소개 줄 세우기\n    if (!TEST_MAP) for (const b of bodies) {   /* c205: 챕터는 판 시작에 전부 본 것 */"),
]
