# c236: 빨강 — 처음 발견하는 빨강마다 노랑 20% · 하양 20% · 그대로 60%를 굴리고, 실제로 바뀐 빨강이 5명이 될 때까지 계속 (경찰은 그대로: 처음 발견 1명만 굴림)
C236_R = [
 ("      c.disc = true; if (red) chDiscR++; else chDiscP++;\n      const r = Math.random(); if (r < 0.2) chDemote(c, 'guard'); else if (r < 0.4) chDemote(c, '');   /* c221: 20% · 20% */",
  "      c.disc = true; if (!red) chDiscP++;\n      const r = Math.random(); if (r < 0.4) { chDemote(c, r < 0.2 ? 'guard' : ''); if (red) chDiscR++; }   /* c221: 20% · 20% · c236: 빨강은 바뀐 수를 센다 */"),
 ("const CH_DISC_R = 4, CH_DISC_P = 1;   // c234: 빨강 4명 · 경찰 1명", "const CH_DISC_R = 5, CH_DISC_P = 1;   // c236: 빨강 = 바뀐 수 5명까지 · 경찰 = 처음 발견 1명"),
]
