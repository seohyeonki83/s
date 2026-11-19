# c210: 내가 벽을 치면 — 치는 면 = 문과 같은 범위 (공격 거리 4배) · 같은 건물의 다른 면들도 공격 대상이 되는데 범위는 절반 (공격 거리 2배)
C210_R = [
 ("if (a === me) v.F.meT = clock;   /* c206: 나만 센다 */", "if (a === me) { v.F.meT = clock; v.B.meT = clock; }   /* c206: 나만 센다 · c210: 건물도 */"),
 ("const F = o.F; return clock - F.meT < 1.5 && clock >= F.meT ? 4 * MELEE : -1; }",
  "const F = o.F, B = o.B; return clock - F.meT < 1.5 && clock >= F.meT ? 4 * MELEE : B.meT !== undefined && clock - B.meT < 1.5 && clock >= B.meT ? 2 * MELEE : -1; }   /* c210: 같은 건물 다른 면 = 절반 */"),
 ("for (const F of Object.values(B.faces)) { F.wHit.clear(); F.wN = 0; F.meT = -9; }", "for (const F of Object.values(B.faces)) { F.wHit.clear(); F.wN = 0; F.meT = -9; } B.meT = -9;"),
]
