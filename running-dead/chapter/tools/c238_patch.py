# c238: 처음 발견 굴림 — 경찰은 길거리 배회 경찰만 (출동한 경찰·경찰차·랜드마크 경찰은 빼고)
C238_R = [
 ("const red = c.attacker && c.vig, cop = c.police && !c.military;", "const red = c.attacker && c.vig, cop = c.police && !c.military && c.street;   /* c238: 배회 경찰만 */"),
 ("  function chCop(p) { const y = Math.random() < 0.1; if (y) chExact = true; const c = chPut(p[0], p[1], chRoamArea(p[0], p[1]), y ? 'guard' : 'police'); if (y) chExact = false; return c; }",
  "  function chCop(p) { const y = Math.random() < 0.1; if (y) chExact = true; const c = chPut(p[0], p[1], chRoamArea(p[0], p[1]), y ? 'guard' : 'police'); if (y) chExact = false; c.street = true; return c; }   /* c238: 길거리 배회 */"),
]
