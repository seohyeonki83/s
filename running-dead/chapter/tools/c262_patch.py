# c262: 처음 발견 — 주황 4명은 100% 노랑으로 · (원래) 노랑 3명은 100% 하양으로 (빨강·배회 경찰 굴림은 그대로)
C262_R = [
 ("""    if (chDiscR >= CH_DISC_N) return;
    if ((chDiscT -= dt) > 0) return; chDiscT = 0.1;
    for (const c of bodies) {
      if (c.kind !== 'citizen' || c.disc || c.boss || !(c.hp > 0)) continue;
      const red = c.attacker && c.vig, cop = c.police && !c.military && c.street;   /* c238: 배회 경찰만 */
      if (!red && !cop) continue;
      if (!(iSee(c) || zSeen(c))) continue;
      c.disc = true;
      const r = Math.random(); if (r < 0.7) chDemote(c, r < 0.35 ? 'guard' : ''); else chDiscR++;""",
  """    if (chDiscR >= CH_DISC_N && chDiscO >= 4 && chDiscY >= 3) return;
    if ((chDiscT -= dt) > 0) return; chDiscT = 0.1;
    for (const c of bodies) {
      if (c.kind !== 'citizen' || c.disc || c.boss || !(c.hp > 0)) continue;
      const red = c.attacker && c.vig && chDiscR < CH_DISC_N, cop = c.police && !c.military && c.street && chDiscR < CH_DISC_N;   /* c238: 배회 경찰만 */
      const org = c.attacker && !c.vig && chDiscO < 4, yel = c.guard && !c.demoted && chDiscY < 3;   // c262: 주황 4명 · 원래 노랑 3명
      if (!red && !cop && !org && !yel) continue;
      if (!(iSee(c) || zSeen(c))) continue;
      c.disc = true;
      if (org) { chDiscO++; chDemote(c, 'guard'); continue; }   // c262: 100% 노랑
      if (yel) { chDiscY++; chDemote(c, ''); continue; }        // c262: 100% 하양
      const r = Math.random(); if (r < 0.7) chDemote(c, r < 0.35 ? 'guard' : ''); else chDiscR++;"""),
 ("      if (chDiscR >= CH_DISC_N) return;\n    }\n  }\n  function chSfTick(dt) {", "    }\n  }\n  function chSfTick(dt) {"),
 ("  function chDemote(c, to) {                   // c220: 그 자리에서 노랑('guard') 또는 하양('')으로\n", "  function chDemote(c, to) {                   // c220: 그 자리에서 노랑('guard') 또는 하양('')으로\n    c.demoted = true;   // c262: 바뀐 노랑은 '처음 만나는 노랑'에 안 센다\n"),
 ("  let chDiscR = 0, chDiscP = 0, chDiscT = 0;", "  let chDiscR = 0, chDiscP = 0, chDiscT = 0, chDiscO = 0, chDiscY = 0;"),
 ("chDiscR = chDiscP = 0; chDiscT = 0;   // c220", "chDiscR = chDiscP = chDiscO = chDiscY = 0; chDiscT = 0;   // c220 · c262"),
]
