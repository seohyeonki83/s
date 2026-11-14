# c62: 특수부대 출동 — 차례마다 정해 둔 인원 (하드 코딩)
C62_FN = r"""  // ── c62: 특수부대 출동 차례표 (감염 75명에 처음, 그 뒤로 60명마다) ──
  //   1번째: 걸어서 저격수 1 + 군인 2 · 2번째: 걸어서 저격수 1 + 군인 3 · 3번째: 걸어서 저격수 2 + 군인 4 (분대 둘, 3초 간격)
  //   4·5번째: 군인차 1대 (저격수 2 + 군인 5)
  //   6번째부터: 군인차 2대 — 서로 다른 방향의 가장자리에서 출발, 둘째 차는 0~5초 늦게. 인원은 싣는 방법마다 다르다
  //     싣는 방법: ① 저격수 2 + 군인 3 / 저격수 1 + 군인 3 (35%)  ② 저격수 2 + 군인 3 / 군인 6 (35%)  ③ 군인 6 / 군인 6 — 저격수 없이 군인 12명 (20%)  ④ 군인차 1대만 — 저격수 1 + 군인 3 (10%, 쉬어 가는 차례)
  //   저격수가 없는 차의 군인은 주인 없이 스스로 싸운다 (다른 곳 저격수를 찾아 떠나지 않는다)
  const S_ = 'sniper', G_ = 'soldier';
  function chTeamSeg2(a) {                     // 첫 차와 다른 방향의 가장자리 — 나에게서 본 방향이 가장 많이 벌어진 자리 (90° 넘으면 바로)
    const ang = (p) => Math.atan2(p.z - me.foot.z, p.x - me.foot.x), a0 = ang(a);
    let best = null, bd = -1;
    for (let k = 0; k < 24; k++) { const p = chEdgeSpot(a.zi), d = Math.abs(Math.atan2(Math.sin(ang(p) - a0), Math.cos(ang(p) - a0)));
      if (d > bd) { bd = d; best = p; } if (d > Math.PI / 2) break; }
    return { x: best.x, z: best.z, zi: a.zi };
  }
  function chQueueTeam(i) {
    teamsSpawned++;                            // '특수부대 출동' 알림 한 번 — 알림이 사라지고 2초 뒤부터 나온다
    const seg = teamSeg();
    if (i < 3) { const sq = i === 0 ? [[S_, G_, G_]] : i === 1 ? [[S_, G_, G_, G_]] : [[S_, G_, G_], [S_, G_, G_]];
      sq.forEach((c, k) => teamWait.push({ comp: c, t: k * 3, first: false, seg, hold: true })); return; }
    if (i < 5) { teamWait.push({ car: [S_, G_, G_, G_, S_, G_, G_], t: 0, seg, hold: true }); return; }
    const q = Math.random(), G6 = [G_, G_, G_, G_, G_, G_];
    if (q < 0.1) { teamWait.push({ car: [S_, G_, G_, G_], t: 0, seg, hold: true }); return; }   // 쉬어 가는 차례 — 군인차 1대
    const L = q < 0.3 ? [G6, G6.slice()] : q < 0.65 ? [[S_, G_, G_, S_, G_], [S_, G_, G_, G_]] : [[S_, G_, G_, S_, G_], G6];
    if (Math.random() < 0.5) L.reverse();
    teamWait.push({ car: L[0], t: 0, seg, hold: true }, { car: L[1], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });
  }
"""
C62_R = [
  ("({ at: STAR_AT[2] + CH_TEAM_GAP * i, tier: i < 2 ? 1 : 2 }))", "({ at: STAR_AT[2] + CH_TEAM_GAP * i, tier: i }))   /* c62: tier = 몇 번째 출동인지 (chQueueTeam) */"),
  ("  function queueSquads(tier) {                // v444: 팀을 분대(저격수 하나 + 딸린 군인)로 나눠 10초 간격으로 하나씩\n",
   "  function queueSquads(tier) {                // v444: 팀을 분대(저격수 하나 + 딸린 군인)로 나눠 10초 간격으로 하나씩\n    if (CHAPTER) { chQueueTeam(tier); return; }   // c62\n"),
  ("      if (t === 'sniper') sn = c; else if (sn) { c.master = sn;", "      if (t === 'sniper') sn = c; else if (CHAPTER && !sn) c.noMaster = true; else if (sn) { c.master = sn;"),
  ("    if (CHAPTER && c.gar) { c.master = null; return null; }", "    if (CHAPTER && (c.gar || c.noMaster)) { c.master = null; return null; }   /* c62: 저격수 없는 차에서 내린 군인도 */"),
  ("    for (const b of bodies) if (b.kind === 'citizen' && b.sniper) { const d = Math.hypot(b.foot.x - c.foot.x, b.foot.z - c.foot.z); if (d < bd) { bd = d; best = b; } }",
   "    for (const b of bodies) if (b.kind === 'citizen' && b.sniper && !(CHAPTER && b.gar)) { const d = Math.hypot(b.foot.x - c.foot.x, b.foot.z - c.foot.z); if (d < bd) { bd = d; best = b; } }   /* c62: 주인이 죽어도 다리 수비대 저격수한테는 안 간다 */"),
  ("  function showDud() {", C62_FN + "  function showDud() {"),
]
