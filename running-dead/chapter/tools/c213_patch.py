# c213: 벽 체력 다시 — 집 = 지금의 70% (집 문의 2.1배) · 창고 = 집 벽의 150% · 랜드마크 전부(경찰서·군부대 포함) = 집 벽의 2배
C213_R = [
 ("const CH_WALL_T = { store: 9,   /* c208 */ house: 3, bank: 6, fire: 6, mart: 6, hospital: 6, library: 6, conv: 6, gym: 6, police: 9, army: 12 };",
  "const CH_WALL_T = { house: 3 * 0.7, store: 3 * 0.7 * 1.5, bank: 4.2, fire: 4.2, mart: 4.2, hospital: 4.2, library: 4.2, conv: 4.2, gym: 4.2, police: 4.2, army: 4.2 };   /* c213: 집 70% · 창고 집의 1.5배 · 랜드마크 집의 2배 */"),
]
