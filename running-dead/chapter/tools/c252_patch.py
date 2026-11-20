# c252: 처음 발견 빨강·배회 경찰 — 바뀔 확률 60 → 70% (노랑 35 · 하양 35 · 그대로 30) · 그대로 남은 합 7 → 14명
C252_R = [
 ("const r = Math.random(); if (r < 0.6) chDemote(c, r < 0.3 ? 'guard' : ''); else chDiscR++;", "const r = Math.random(); if (r < 0.7) chDemote(c, r < 0.35 ? 'guard' : ''); else chDiscR++;   /* c252: 35 · 35 · 30 */"),
 ("const CH_DISC_N = 7;", "const CH_DISC_N = 14;   /* c252: 2배 */"),
]
