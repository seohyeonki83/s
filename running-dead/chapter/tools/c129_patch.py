# c129: 길거리의 빨강 10% · 주황 10%를 하양으로 — 무리에 있던 자리면 무리에서 빠져 혼자 돌아다닌다
C129_R = [
 ("  function chPut(x, z, area, type, B) {\n", "  let chNoW = false;\n  function chPut(x, z, area, type, B) {\n    let wOut = false; if (!chExact && !chNoW && !B && (type === 'vig' || type === 'attacker') && Math.random() < 0.1) { type = ''; wOut = true; }   // c129: 길거리 빨강·주황 열에 하나는 하양\n"),
 ("    const c = addCitizen(x, z, area, type === 'vig' ? 'attacker' : type);\n    if (type === 'police') { c.post = area;", "    const c = addCitizen(x, z, area, type === 'vig' ? 'attacker' : type); if (wOut) c.wOut = true;\n    if (type === 'police') { c.post = area;"),
 ("      G.members.push(chPut(x, z, area, t));", "      { const c = chPut(x, z, area, t); if (c.wOut) c.area = chRoamArea(x, z); else G.members.push(c); }   // c129: 하양이 된 자리는 무리에서 빠진다"),
 ("chExact = car.loot === 'cash'; const c = chPut(x, z, chSideArea(x, z), w, null); chExact = false;", "chExact = car.loot === 'cash'; chNoW = true; const c = chPut(x, z, chSideArea(x, z), w, null); chExact = false; chNoW = false;"),
]
