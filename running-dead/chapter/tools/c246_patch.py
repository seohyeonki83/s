# c246: 처음 발견 굴림 다시 — 빨강·배회 경찰을 한데 묶어, 발견할 때마다 노랑 30% · 하양 30% · 그대로 40%. 그대로 남은 수(빨강+경찰 합)가 7명이 될 때까지
C246_R = [
 ("const CH_DISC_R = 5, CH_DISC_P = 4;   // c237: 그대로 남은 빨강 5명 · 경찰 4명이 될 때까지", "const CH_DISC_N = 7;   // c246: 그대로 남은 빨강·경찰 합이 7명이 될 때까지"),
 ("    if (chDiscR >= CH_DISC_R && chDiscP >= CH_DISC_P) return;\n    if ((chDiscT -= dt) > 0) return;", "    if (chDiscR >= CH_DISC_N) return;\n    if ((chDiscT -= dt) > 0) return;"),
 ("      if (!(red && chDiscR < CH_DISC_R) && !(cop && chDiscP < CH_DISC_P)) continue;", "      if (!red && !cop) continue;"),
 ("const r = Math.random(); if (r < 0.5) chDemote(c, r < 0.25 ? 'guard' : ''); else if (red) chDiscR++; else chDiscP++;   /* c237: 25% · 25% · 50% — 그대로 남은 수를 센다 */",
  "const r = Math.random(); if (r < 0.6) chDemote(c, r < 0.3 ? 'guard' : ''); else chDiscR++;   /* c246: 30% · 30% · 40% — 그대로 남은 수(빨강+경찰)를 센다 */"),
 ("      if (chDiscR >= CH_DISC_R && chDiscP >= CH_DISC_P) return;\n", "      if (chDiscR >= CH_DISC_N) return;\n"),
]
