# c76: 차 무게는 경찰차가 가장 가볍다 (소형차·스포츠카도 경찰차와 같게) · 편의점에 두 번에 한 번 경찰 한 명 · 길거리 주황의 5분의 1은 노랑
C76_R = [
  ("hp: 0.8, mass: 0.8, col: [0xe9e9e4", "hp: 0.8, mass: 1, col: [0xe9e9e4"),     # 소형차 0.8 → 1
  ("hp: 0.8, mass: 0.9, col: [0xe22828", "hp: 0.8, mass: 1, col: [0xe22828"),     # 스포츠카 0.9 → 1
  ("    conv: [['', 1, 3], ['guard', 1, 2]],", "    conv: [['', 1, 3], ['guard', 1, 2], ['police', 0, 1]],   // c76: 두 번에 한 번은 경찰 한 명"),
  ("    const centers = [];\n    for (const types of groups.sort(() => Math.random() - 0.5)) {",
   "    {                                          // c76: 길거리 주황(전부 무리 안에 있다)의 5분의 1은 노랑으로 — 주황·빨강 무리에 노랑이 섞여 다닌다\n"
   "      const at = []; groups.forEach((g, i) => g.forEach((t, j) => { if (t === 'attacker') at.push([i, j]); }));\n"
   "      for (let n = Math.round(at.length / 5); n > 0; n--) { const [i, j] = at.splice(Math.floor(Math.random() * at.length), 1)[0]; groups[i][j] = 'guard'; }\n"
   "    }\n"
   "    const centers = [];\n    for (const types of groups.sort(() => Math.random() - 0.5)) {"),
]
