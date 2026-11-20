# c217: 체력바 — 4겹(초록·파랑·보라·빨강)을 넘는 최대 체력이면 가로를 늘린다 (최대 2배 = 8겹까지). 한 겹도 그 배율만큼 커진다
C217_R = [
 ("    const U = b === me ? MY_HP : ALLY_HP * 0.9, M = [b.hpMat0, chHpMat2, chHpMat3, chHpMat4];",
  "    const U = chBarU(b), M = [b.hpMat0, chHpMat2, chHpMat3, chHpMat4];   // c217: 넓어진 바는 한 겹도 그만큼"),
 ("  function chHpFill(b) {",
  "  const chBarK = (b) => { const U0 = b === me ? MY_HP : ALLY_HP * 0.9; return Math.min(2, Math.max(1, (b.maxHp || 0) / (4 * U0))); };   // c217: 4겹을 넘으면 가로 배율 (최대 2)\n"
  "  const chBarU = (b) => (b === me ? MY_HP : ALLY_HP * 0.9) * chBarK(b);\n"
  "  function chHpFill(b) {"),
 ("CHAPTER && !b.oneBar ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 : 2 * 0.5 / POLICE_HP * ALLY_HP * 0.9)",
  "CHAPTER && !b.oneBar ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 : 2 * 0.5 / POLICE_HP * ALLY_HP * 0.9) * chBarK(b)"),
]
