# c190: 길거리 배회 경찰 시간표 다시 — 처음 0 · 수상함 = 기본의 절반 · 수상함과 난리남 사이 한가운데 = 기본 · 난리남 = 기본의 1.5배 (전부 '맵에 있는 총수')
C190_R = [
 ("const base = CH_COPS * CH_ONE_K * 0.8 * 0.9 * 0.9, mid = Math.round((STAR_AT[1] + STAR_AT[2]) / 2);\n    const k = deaths >= mid ? 1.5 : stars >= 2 ? 1 : stars >= 1 ? 0.5 : 0;",
  "const base = CH_COPS * CH_ONE_K * 0.8 * 0.9 * 0.9, mid = Math.round((STAR_AT[0] + STAR_AT[1]) / 2);   /* c190 */\n    const k = stars >= 2 ? 1.5 : deaths >= mid ? 1 : stars >= 1 ? 0.5 : 0;"),
]
