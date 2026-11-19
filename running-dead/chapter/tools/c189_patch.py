# c189: 길거리 배회 경찰 — 처음엔 없다. 수상함 = 지금 수의 절반 · 난리남 = 지금 수 · 난리남과 개판 사이 한가운데 = 1.5배 (그때 내 화면·좀비 시야 밖 길거리에 새로 뿌린다)
#       레벨업 무기 강화 카드 확률 25% 줄임 (뽑기 몫 2배 → 1.5배)
C189_R = [
 ("for (let k = 0, nCop = chRoundP(CH_COPS * CH_ONE_K * 0.8 * 0.9 * 0.9); k < nCop; k++)", "for (let k = 0, nCop = 0; k < nCop; k++)   /* c189: 처음엔 없다 (chCopTick이 경보에 맞춰 뿌린다) */"),
 ("  function chHiddenSpot(zi, minOwn) {", """  function chCopTick() {                       // c189: 경보 단계에 맞춰 길거리 배회 경찰을 늘린다
    if (!chPop || CH_BT) return;
    const base = CH_COPS * CH_ONE_K * 0.8 * 0.9 * 0.9, mid = Math.round((STAR_AT[1] + STAR_AT[2]) / 2);
    const k = deaths >= mid ? 1.5 : stars >= 2 ? 1 : stars >= 1 ? 0.5 : 0;
    if (chPop.copK === k) return;
    if (chPop.copK !== undefined && k < chPop.copK) return;   // 줄지는 않는다
    chPop.copK = k; const goal = chRoundP(base * k), add = goal - (chPop.copN || 0); if (add <= 0) return;
    const Z = CH_MAP.zones, area = Z.map(([a, b, c, d]) => (c - a) * (d - b)), tot = area.reduce((s, v) => s + v, 0);
    for (let n = 0; n < add; n++) { let r = Math.random() * tot, zi = 0; while (zi < Z.length - 1 && (r -= area[zi]) > 0) zi++;
      const p = chHiddenSpot(zi, 1.2); if (!p) continue; chReg(chCop(p), 'police'); chPop.copN = (chPop.copN || 0) + 1; }
  }
  function chHiddenSpot(zi, minOwn) {"""),
 ("  function chDispatchTick(dt) {\n", "  function chDispatchTick(dt) {\n    chCopTick();   // c189\n"),
 ("Array(chWupN() * 2).fill('__w')", "Array(chWupN() * 1.5 | 0).fill('__w').concat(chWupN() % 2 && Math.random() < 0.5 ? ['__w'] : [])   /* c189: 25% 줄임 (몫 2배 → 1.5배) */"),
]
