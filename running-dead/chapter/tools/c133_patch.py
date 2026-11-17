# c133: 보이지 않는 길거리 사물 고침 (c110에서 그림 차례 세는 수가 멈춰 4개 중 3개가 처음 판정에 굳어 있었다) · 길거리 빨강 · 배회 경찰 10% 더 줄임 (경찰 수는 소수점을 확률로 살린다)
C133_R = [
 ("    if (CHAPTER) { for (const C of chCanopies) { C.open = true; C.m.visible = false; } return; }   // c110", "    if (CHAPTER) { chDrawF++; for (const C of chCanopies) { C.open = true; C.m.visible = false; } return; }   /* c133: 그림 차례는 계속 세야 한다 — 안 세면 길거리 사물 4개 중 3개가 안 보이는 채로 굳는다 */   // c110"),
 ("      if (t === 'vig' && Math.random() < 0.1) return;   // c131", "      if (t === 'vig' && Math.random() < 0.19) return;   /* c133: 10% 더 (합쳐서 19%) */   // c131"),
 ("for (let k = 0; k < Math.round(CH_COPS * CH_ONE_K * 0.8 * 0.9); k++)", "for (let k = 0, nCop = chRoundP(CH_COPS * CH_ONE_K * 0.8 * 0.9 * 0.9); k < nCop; k++)   /* c133: 10% 더 — 소수점은 확률로 (14.26명 = 14명 또는 15명) */"),
 ("  let chNoW = false;\n", "  let chNoW = false;\n  const chRoundP = (x) => Math.floor(x) + (Math.random() < x - Math.floor(x) ? 1 : 0);   // c133: 소수점 아래는 그 확률로 한 명\n"),
]
