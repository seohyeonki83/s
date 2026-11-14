# c72: 건널목(다리·산 길목) 수비대 인원 절반 (단계마다 느는 수도 절반) · 바리케이트 조각 3분의 1 줄임
C72_R = [
  # 첫 줄 — 조각 3개(가끔 4개) → 2개(열에 둘은 3개). 평균 3.3 → 2.2
  ("kinds = q < 0.7 ? [true, true, false] : q < 0.85 ? [true, true, false, false] : [true, true, true, false];",
   "kinds = q < 0.55 ? [true, false] : q < 0.8 ? [true, true] : [true, true, false];   /* c72: 3분의 1 줄임 — 바리케이트 1 + 경찰차 1 (넷에 한 번은 바리케이트만 2, 다섯에 한 번은 바리케이트 2 + 경찰차 1) */"),
  # 단계마다 느는 조각 — 3분의 2만 놓는다. 한쪽 끝에 4조각까지 (전에는 자리가 차는 6조각까지)
  ("for (let i = 0; i < k; i++) chBarAdd(X, e, true); if (Math.random() < 0.2) chBarAdd(X, e, false); }",
   "const live = () => X.rows[e].reduce((n, row) => n + (row || []).filter(chBarLive).length, 0);   /* c72 */\n"
   "          for (let i = 0; i < k; i++) if (Math.random() < 2 / 3 && live() < CH_BAR_MAX) chBarAdd(X, e, true); if (Math.random() < 0.2 * 2 / 3 && live() < CH_BAR_MAX) chBarAdd(X, e, false); }"),
  # 수비대 — 뽑힌 수의 절반 (홀수는 반반으로 올리거나 내린다: 평균이 정확히 절반)
  ("for (const type of ['police', 'soldier', 'sniper']) for (let i = 0; i < (add[type] || 0); i++) {",
   "for (const type of ['police', 'soldier', 'sniper']) for (let i = 0, n = chHalf(add[type] || 0); i < n; i++) {   /* c72: 인원 절반 */"),
  ("  function chBarGrow(s) {",
   "  const CH_BAR_MAX = 4, chHalf = (n) => Math.floor(n / 2) + (n % 2 && Math.random() < 0.5 ? 1 : 0);   // c72: 한쪽 끝 조각 수 한계 (6의 3분의 2) · 인원 절반\n  function chBarGrow(s) {"),
]
