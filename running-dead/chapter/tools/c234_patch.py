# c234: 처음 발견해서 바뀔 수 있는 수 — 빨강 4명 · 경찰 1명
C234_R = [
 ("    if (chDiscR >= 5 && chDiscP >= 2) return;\n    if ((chDiscT -= dt) > 0) return;", "    if (chDiscR >= CH_DISC_R && chDiscP >= CH_DISC_P) return;\n    if ((chDiscT -= dt) > 0) return;"),
 ("      if (!(red && chDiscR < 5) && !(cop && chDiscP < 2)) continue;", "      if (!(red && chDiscR < CH_DISC_R) && !(cop && chDiscP < CH_DISC_P)) continue;"),
 ("      if (chDiscR >= 5 && chDiscP >= 2) return;\n", "      if (chDiscR >= CH_DISC_R && chDiscP >= CH_DISC_P) return;\n"),
 ("  let chDiscR = 0, chDiscP = 0, chDiscT = 0;", "  let chDiscR = 0, chDiscP = 0, chDiscT = 0;\n  const CH_DISC_R = 4, CH_DISC_P = 1;   // c234: 빨강 4명 · 경찰 1명"),
]
