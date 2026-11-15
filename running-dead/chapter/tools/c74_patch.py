# c74: 레벨업 — 처음 10명, 그 뒤로 1.3배씩 (c28~c73은 처음 20명, 1.2배씩) · 길거리 무리 — 가장 큰 무리(6명)에서 빨강 한 명을 뺀다
C74_R = [
  ("CHAPTER ? Math.round(20 * Math.pow(1.2, L)) : Math.round(10 * Math.pow(1.3, L));   /* c28: 챕터는 처음 20명, 1.2배씩 */",
   "Math.round(10 * Math.pow(1.3, L));   /* c74: 챕터도 처음 10명, 1.3배씩 (c28~c73은 처음 20명, 1.2배씩) */"),
  ("    let mo = Math.round(CH_GANG / 3), mr = Math.round(CH_GANG * CH_RED_K / 3);",
   "    let redCut = 0;                            // c74: 가장 큰 무리에서 뺀 빨강 수 (다른 무리로 안 간다 — 길거리 인구가 그만큼 준다)\n"
   "    let mo = Math.round(CH_GANG / 3), mr = Math.round(CH_GANG * CH_RED_K / 3);"),
  ("      groups.push([...Array(o).fill('attacker'), ...Array(r).fill('vig')]); mo -= o; mr -= r;",
   "      const cut = o + r >= 6 ? 1 : 0;          // c74: 가장 큰 무리(6명)는 빨강을 한 명 뺀다 → 가장 큰 무리 = 5명\n"
   "      groups.push([...Array(o).fill('attacker'), ...Array(r - cut).fill('vig')]); mo -= o; mr -= r; redCut += cut;"),
  ("let left = (t === 'vig' ? Math.round(CH_GANG * CH_RED_K) : CH_GANG) - groups.flat().filter((x) => x === t).length;",
   "let left = (t === 'vig' ? Math.round(CH_GANG * CH_RED_K) - redCut : CH_GANG) - groups.flat().filter((x) => x === t).length;"),
]
