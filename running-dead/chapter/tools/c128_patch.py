# c128: 보스는 혼자 나온다 (호위 없음) · 40초 군인차 대신 15초마다 가장 약한 특공대 1팀 (저격수 1 + 군인 2, 걸어서) — 보스와 동시에 첫 팀
C128_R = [
 ("    for (let i = 0; i < 5; i++) {\n      const a = h + i / 5 * Math.PI * 2, R = GUARD_NEAR * CH_TK_ESC", "    for (let i = 0; i < 0; i++) {   /* c128: 호위 없음 */\n      const a = h + i / 5 * Math.PI * 2, R = GUARD_NEAR * CH_TK_ESC"),
 ("    chSf.waveT = 0;\n  }\n  function chTankFoe(car) {", "    chSf.waveT = CH_SF_WAVE;   // c128: 보스와 동시에 첫 팀\n  }\n  function chTankFoe(car) {"),
 ("CH_SF_WAVE = 40,", "CH_SF_WAVE = 15,"),
 ("teamWait.push({ car: [S_, G_, G_, G_, S_, G_, G_], t: 0, seg: teamSeg(), tk: true });", "teamWait.push({ comp: [S_, G_, G_], t: 0, first: false, seg: teamSeg(), tk: true });   /* c128: 1팀 (가장 약한 팀) */"),
 ("else spawnTeam(w.comp, w.first, w.seg); }", "else { chTkMark = !!w.tk; spawnTeam(w.comp, w.first, w.seg); chTkMark = false; } }"),
 ("      if (CHAPTER) c.met = true;   // c59: 출동한 군인은 멀리 있어도 서 있지 않는다", "      if (CHAPTER) c.met = true;   // c59: 출동한 군인은 멀리 있어도 서 있지 않는다\n      if (CHAPTER && chTkMark) c.tkU = true;   // c128: 보스 뒤에 온 팀 = 잡아야 이긴다"),
 ("  function chQueueTeam(i) {\n", "  let chTkMark = false;\n  function chQueueTeam(i) {\n"),
 ("'<div class=\"rbox\"><div class=\"rt\">군부대 출동</div><div class=\"rd\" style=\"color:#ff4a3a\">보스</div></div>'", "'<div class=\"rbox\"><div class=\"rt\">보스 출동</div></div>'"),
]
