# c188: 사람 수 · 문
#   · 랜드마크 안: 빨강 절반 · 주황 3분의 1 줄임 (집·창고는 그대로)
#   · 길거리 하양 25% 줄임 (혼자 · 무리 · 포인트 다)
#   · 건물 안 하양 3분의 1 늘림 (랜드마크 · 창고 · 집 다)
#   · 판을 깔 때 문이 이미 부서져(열려) 있다 — 창고 문 50% · 집 등 그 밖의 건물 문 25% (문마다 따로) · 랜드마크는 안 연다
C188_R = [
 ("if (type === 'vig') k = chRedN(k);", "if (type === 'vig') k = chRedN(k); if (CH_LM.has(B.type)) { if (type === 'vig') k = chRoundP(k * 0.5); else if (type === 'attacker') k = chRoundP(k * 2 / 3); }   /* c188: 랜드마크 빨강 절반 · 주황 3분의 1 줄임 */ if (type === '') k = chRoundP(k * 4 / 3);   /* c188: 건물 안 하양 3분의 1 늘림 */"),
 ("houseSlots.slice(houseOut).forEach((B) => { const q = Math.random(); B.res.push(inPut(B, q < 0.15 ? 'attacker' : q < 0.15 + 0.15 * CH_RED_K ? 'vig' : '')); });",
  "houseSlots.slice(houseOut).forEach((B) => { const q = Math.random(), t = q < 0.15 ? 'attacker' : q < 0.15 + 0.15 * CH_RED_K ? 'vig' : ''; B.res.push(inPut(B, t)); if (t === '' && Math.random() < 1 / 3) B.res.push(inPut(B, '')); });   /* c188: 집 안 하양 3분의 1 늘림 */"),
 ("* 1.15 * CH_ONE_K * 1.2 * 0.775);", "* 1.15 * CH_ONE_K * 1.2 * 0.775 * 0.75);   /* c188: 길거리 하양 25% 더 줄임 */"),
 ("if (Math.random() >= 0.2) ex[i].push(q); }", "if (Math.random() >= (q === '' ? 0.4 : 0.2)) ex[i].push(q); }   /* c188: 포인트 하양 25% 더 */"),
 ("if (!((type === 'guard' || type === 'attacker' || type === '') && Math.random() < 0.2)) list.push(type); }", "if (!((type === 'guard' || type === 'attacker' || type === '') && Math.random() < (type === '' ? 0.4 : 0.2))) list.push(type); }"),
 ("    for (const B of buildings) if (B.type === 'house' && !B.garage && !B.gas && !B.parent && Math.random() < 0.2) { const L = B.locks.find((q) => q.front); if (L && L.obj && !L.obj.dead && !L.obj.off) chOpenDoor(L.obj); } }",
  "    for (const B of buildings) { if (B.type === 'hill' || B.parent || CH_LM.has(B.type)) continue; const pO = B.type === 'store' ? 0.5 : 0.25;   // c188: 창고 문 50% · 그 밖의 건물 문 25% (문마다) · 랜드마크 제외\n      for (const L of B.locks.slice()) if (L.obj && !L.obj.dead && !L.obj.off && Math.random() < pO) chOpenDoor(L.obj); } }"),
]
