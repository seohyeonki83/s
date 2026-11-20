# c237: 처음 발견하는 빨강·경찰 — 노랑 25% · 하양 25% · 그대로 50%. '그대로 남은' 빨강이 5명, 경찰이 4명이 될 때까지 발견할 때마다 굴린다 (평균 빨강 10명 · 경찰 8명 굴림)
C237_R = [
 ("      c.disc = true; if (!red) chDiscP++;\n      const r = Math.random(); if (r < 0.4) { chDemote(c, r < 0.2 ? 'guard' : ''); if (red) chDiscR++; }   /* c221: 20% · 20% · c236: 빨강은 바뀐 수를 센다 */",
  "      c.disc = true;\n      const r = Math.random(); if (r < 0.5) chDemote(c, r < 0.25 ? 'guard' : ''); else if (red) chDiscR++; else chDiscP++;   /* c237: 25% · 25% · 50% — 그대로 남은 수를 센다 */"),
 ("const CH_DISC_R = 5, CH_DISC_P = 1;   // c236: 빨강 = 바뀐 수 5명까지 · 경찰 = 처음 발견 1명", "const CH_DISC_R = 5, CH_DISC_P = 4;   // c237: 그대로 남은 빨강 5명 · 경찰 4명이 될 때까지"),
]
