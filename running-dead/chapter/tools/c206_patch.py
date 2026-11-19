# c206: 동료는 벽을 먼저 치지 않는다 — 내가 때리는 동안만 그 면(같은 변의 토막들)이 동료 공격 대상 · 범위는 문과 같다 (공격 거리 4배)
#   · 동료 수에 따라 넓어지던 어그로(3배 → 반씩)는 없앴다 · 나는 지금과 같다 (사물의 70% 거리)
C206_R = [
 ("if (a) { v.F.wHit.set(a, clock); if (a === me) v.F.meT = clock; }", "if (a === me) v.F.meT = clock;   /* c206: 나만 센다 */"),
 ('  function chWallLim(z, o) { if (z === me) return chReach(z) * 0.7; const F = o.F, b = chReach(z) * 0.7 * CH_WALL_AG[Math.min(5, chWallN(F))];   /* c204: 1마리 3배 · 2마리 4.5배 · 3마리 5.25배 · 4마리 5.625배 · 5마리부터 5.8125배 (늘어나는 양이 반씩) */ return z !== me && clock - F.meT < 1.5 && clock >= F.meT ? Math.max(b, 4 * MELEE) : b; }', '  function chWallLim(z, o) { if (z === me) return chReach(z) * 0.7; const F = o.F; return clock - F.meT < 1.5 && clock >= F.meT ? 4 * MELEE : -1; }   // c206: 동료 = 내가 치는 면만, 문과 같은 범위 (먼저 치지 않는다)'),
]
