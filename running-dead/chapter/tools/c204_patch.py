# c204: 벽 어그로를 면 단위로 — 동료가 때리면 1마리 3배 · 그다음부터 늘어나는 양이 반씩 (4.5배 · 5.25배 … 최대 6배), 내가 때릴 때 문처럼 공격 거리 4배 안 동료를 부르는 것도 그 면(같은 변의 토막들)에만
C204_R = [
 ("B.walls = out; B.wos = []; B.wHit = new Map(); B.wN = 0; B.wNF = -1; add.push(...out); chWallBs.push(B);",
  "B.walls = out; B.wos = []; B.faces = {}; add.push(...out); chWallBs.push(B);"),
 ("      for (const q of out) { const o = { kind: 'obj', type: 'wall', B, seg: q,",
  "      for (const q of out) { const sd = q[1] === q[3] ? (Math.abs(q[1] - B.z0) < 1e-6 ? 'n' : 's') : (Math.abs(q[0] - B.x0) < 1e-6 ? 'w' : 'e'), F = B.faces[sd] || (B.faces[sd] = { wHit: new Map(), wN: 0, wNF: -1, meT: -9 }); const o = { F, kind: 'obj', type: 'wall', B, seg: q,"),
 ("if (a) v.B.wHit.set(a, clock);", "if (a) { v.F.wHit.set(a, clock); if (a === me) v.F.meT = clock; }"),
 ("      const lim0 = chReach(z) * 0.7 * (1 + 0.2 * chWallN(B)), m = Math.max(lim0, z !== me ? 4 * MELEE : 0) + 0.5;",
  "      const m = 4 * MELEE + 0.5;"),
 ("        if (o.dead) continue; const lim = z !== me && hotObj(o) ? Math.max(lim0, 4 * MELEE) : lim0, g = objGap(o, z);",
  "        if (o.dead) continue; const lim = chWallLim(z, o), g = objGap(o, z);"),
 ("    for (const B of chWallBs) { B.wHit.clear(); B.wN = 0;", "    for (const B of chWallBs) { for (const F of Object.values(B.faces)) { F.wHit.clear(); F.wN = 0; F.meT = -9; }"),
 ("  function chWallN(B) { if (B.wNF !== objFrame) { B.wNF = objFrame; let n = 0; for (const [z, t] of B.wHit) { if (clock - t > 1.5 || clock < t) B.wHit.delete(z); else if (z !== me) n++; } B.wN = n; } return B.wN; }",
  "  function chWallN(F) { if (F.wNF !== objFrame) { F.wNF = objFrame; let n = 0; for (const [z, t] of F.wHit) { if (clock - t > 1.5 || clock < t) F.wHit.delete(z); else if (z !== me) n++; } F.wN = n; } return F.wN; }   // c204: 이 면을 지금 때리는 동료 수\n"
  "  const CH_WALL_AG = [1, 3, 4.5, 5.25, 5.625, 5.8125];\n"
  "  function chWallLim(z, o) { if (z === me) return chReach(z) * 0.7; const F = o.F, b = chReach(z) * 0.7 * CH_WALL_AG[Math.min(5, chWallN(F))];   /* c204: 1마리 3배 · 2마리 4.5배 · 3마리 5.25배 · 4마리 5.625배 · 5마리부터 5.8125배 (늘어나는 양이 반씩) */ return z !== me && clock - F.meT < 1.5 && clock >= F.meT ? Math.max(b, 4 * MELEE) : b; }   // c204: 내가 이 면을 때리는 중이면 문처럼 · 나는 늘 기본 거리 (동료가 넓힌 건 안 받는다)"),
 ("if (o.type === 'wall') return z !== me && hotObj(o) ? 4 * MELEE : chReach(z) * 0.7 * (1 + 0.2 * chWallN(o.B));", "if (o.type === 'wall') return chWallLim(z, o);"),
]
