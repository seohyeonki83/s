# c130: 길거리를 배회하는 경찰 10%를 노랑으로 (처음 놓을 때 · 다시 채울 때)
C130_R = [
 ("chReg(chPut(p[0], p[1], chRoamArea(p[0], p[1]), 'police'), 'police')", "chReg(chCop(p), 'police')"),
 ("P.list.push(chPut(p[0], p[1], chRoamArea(p[0], p[1]), type))", "P.list.push(type === 'police' ? chCop(p) : chPut(p[0], p[1], chRoamArea(p[0], p[1]), type))"),
 ("  let chNoW = false;\n", "  let chNoW = false;\n  function chCop(p) { const y = Math.random() < 0.1; if (y) chExact = true; const c = chPut(p[0], p[1], chRoamArea(p[0], p[1]), y ? 'guard' : 'police'); if (y) chExact = false; return c; }   // c130: 배회 경찰 열에 하나는 노랑\n"),
]
