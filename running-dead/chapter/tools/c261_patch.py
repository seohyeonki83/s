# c261: 산성 폭발 — 겹치지 않는다. 다시 맞으면 남은 시간만 새로 (더 긴 쪽), 피해는 늘 한 겹 (1 + 산성 강도)
C261_R = [
 ("(e.acid || (e.acid = [])).push(T);", "if (!e.acid) e.acid = []; if (e.acid.length) e.acid[0] = Math.max(e.acid[0], T); else e.acid.push(T);   /* c261: 겹치지 않음 */"),
 ("const d = e.acid.length * (1 + chAcidB());   // c259: 겹마다 1 + 산성 강도", "const d = 1 + chAcidB();   // c259 · c261: 한 겹만 — 1 + 산성 강도"),
 ("    acid: (n) => `범위 = 근접 거리 x${(1.2 * (1 + 0.15 * n)).toFixed(2)} · ${3 + n}초 · 0.5초마다 1 (겹치면 쌓임)`,", "    acid: (n) => `범위 = 근접 거리 x${(1.2 * (1 + 0.15 * n)).toFixed(2)} · ${3 + n}초 · 0.5초마다 1`,   /* c261: 겹치지 않음 */"),
]
