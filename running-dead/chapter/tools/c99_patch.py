# c99: 수상함 뒤 경보단계 조건을 1.3배 더 (10, 62, 150, 336, 724 → 10, 81, 195, 437, 941)
C99_R = [
 ("  for (let i = 1; i < STAR_AT.length; i++) STAR_AT[i] *= 2;", "  for (let i = 1; i < STAR_AT.length; i++) STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3);   /* c99: 1.3배 더 → [10, 81, 195, 437, 941] */"),
]
