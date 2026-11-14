# c54: 타겟이 생기면 시야 1.3배 · 주황·빨강 경계 시간 = 경찰 · 문이 부서진 뒤 안 사람이 감염되면 두 번째 출동 · 금고가 방 안일 때 길 찾기 · 감전 뒤 색
C54_FN = r"""  // ── c54: 타겟이 생기면 시야 1.3배 ──
  //   먼저 덤비는 사람(주황·빨강·경찰·군인·저격수)은 싸움을 시작하는 순간(타겟이 없다가 생긴 순간) 시야가 1.3배가 된다. 사거리는 그대로 (원래 시야)
  //   원래 시야(1배) 안에 좀비가 없어진 때부터 2~5초(그때마다 랜덤)가 지나면 다시 1배. 그 전에 다시 들어오면 그대로 유지한다
  function chSafeReach(z, s) { return CHAPTER && !!s.room && linked(z.space, s.space) && !fireBlocked(z.foot.x, z.foot.z, s.foot.x, s.foot.z); }   // 방 안 금고 — 문이 뚫려 있고 사이에 벽이 없으면 문간에서 때릴 수 있다 (작은 방은 금고가 꽉 차서 못 들어간다)
  function chFightBoost(c) {
    if (!c.fb) { c.sight0 = c.sight; c.sight = c.sight0 * 1.3; c.fb = true; }
    c.fbT = -1; c.fbTick = 0;
  }
  function chFightBoostTick(c, dt) {
    if ((c.fbTick -= dt) <= 0) { c.fbTick = 0.2; c.fbNear = !!nearestZombie(c, c.sight0); }
    if (c.fbNear) { c.fbT = -1; return; }                      // 원래 시야 안에 타겟이 있다 → 유지
    if (c.fbT < 0) c.fbT = rand(2, 5);                         // 없어진 순간부터 2~5초
    if ((c.fbT -= dt) <= 0) { c.fb = false; c.sight = c.sight0; if (c.chaseR > c.sight0) c.chaseR = c.sight0; }   // 다시 1배 — 더 못 보면 쫓기를 그만둔다 (경찰이 늘어난 시야로 쫓던 거리도 같이 줄인다)
  }
"""
C54_R = [
  ("  function enterAlert(c) { c.state = 'alert'; c.timer = rand(...ALERT_TIME) * (c.police ? POLICE_ALERT : 1); }", "  function enterAlert(c) { c.state = 'alert'; c.timer = rand(...ALERT_TIME) * (c.police || (CHAPTER && c.attacker) ? POLICE_ALERT : 1); }   /* c54: 주황·빨강도 경찰만큼 짧게 경계 (3분의 1) */"),
  ("    c.state = 'fight';\n    c.foe = z || null;", "    c.state = 'fight';\n    if (CHAPTER && (c.police || c.attacker)) chFightBoost(c);   // c54: 타겟이 생긴 순간 시야 1.3배\n    c.foe = z || null;"),
  ("    if (c.sniper) sniperSpeed(c, dt);        // v411", "    if (c.fb) chFightBoostTick(c, dt);   // c54\n    if (c.sniper) sniperSpeed(c, dt);        // v411"),
  ("    const range = c.boostT > 0 ? c.boostSight : c.sight;   // 사거리 = 원래(1배) 시야 (v159)", "    const range = c.boostT > 0 ? c.boostSight : c.fb ? c.sight0 : c.sight;   // 사거리 = 원래(1배) 시야 (v159 · c54: 늘어난 시야는 사거리가 아니다)"),
  ("    const z = nearestZombie(c, c.boostT > 0 ? c.boostSight : c.sight, true);", "    const z = nearestZombie(c, c.boostT > 0 ? c.boostSight : c.fb ? c.sight0 : c.sight, true);"),
  ("    if (!S || S.dead || b === S || Math.hypot(tx - S.foot.x, tz - S.foot.z) < 0.05) return wp.set(tx, tz);", "    if (!S || S.dead || b === S || (S.room && S.room !== B) || Math.hypot(tx - S.foot.x, tz - S.foot.z) < 0.05) return wp.set(tx, tz);   /* c54: 금고가 방 안이면 복도에서는 안 피한다 */"),
  ("        const base = COLOR[b.sniper ? 'sniper' : b.soldier ? 'soldier' : b.police ? 'police' : b.attacker ? 'attacker' : b.guard ? 'guard' : 'citizen'];", "        const base = b.vig || b.boss ? 0xc62828 : COLOR[b.sniper ? 'sniper' : b.soldier ? 'soldier' : b.police ? 'police' : b.attacker ? 'attacker' : b.guard ? 'guard' : 'citizen'];   /* c54: 빨강은 감전 뒤에도 빨강 */"),
  ("  function makeZombie(b) {\n", "  function makeZombie(b) {\n    if (CHAPTER && b.home && b.home.x0 !== undefined) { const P = b.home.parent || b.home; if (P.called === 1) P.lost = true; }   // c54: 문이 부서진 건물 안 사람이 감염됐다 → 두 번째 출동\n"),
  ("      if (!b || b.dead || b.space !== z.space) continue;", "      if (!b || b.dead || (b.space !== z.space && !chSafeReach(z, b))) continue;   /* c54: 방 안 금고는 열린 문 너머로도 */"),
  ("    if (d > MELEE + (c.kind === 'safe' ? c.r : 0) || c.space !== z.space) { steer(z.vel, toward(z, c.foot.x, c.foot.z, z.speed), ACCEL * dt); return; }", "    if (d > MELEE + (c.kind === 'safe' ? c.r : 0) || (c.space !== z.space && !(c.kind === 'safe' && chSafeReach(z, c)))) { steer(z.vel, toward(z, c.foot.x, c.foot.z, z.speed), ACCEL * dt); return; }   /* c54: 방을 꽉 채운 금고는 문간에서 때린다 */"),
  ("  function pickGoal(a) {                      // 영역 안 아무 곳 — 밖 영역이면 건물 근처는 빼고\n    let g;", "  function pickGoal(a) {                      // 영역 안 아무 곳 — 밖 영역이면 건물 근처는 빼고\n    if (CHAPTER && a.guardB && a.guardB.doors.length && Math.random() < 0.4) return pickGoal(a.guardB);   // c54: 사수 경찰 — 그 건물 문이 뚫려 있으면 열 번에 네 번은 건물 안을 돈다\n    let g;"),
  ("  function showDud() {", C54_FN + "  function showDud() {"),
]
