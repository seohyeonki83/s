# c228: 죽은 시민 다시 채우기 속도 절반 — 한 명짜리 40 → 80초, 무리 60 → 120초
C228_R = [
 ("  const CH_RE_ONE = 40, CH_RE_GANG = 60;", "  const CH_RE_ONE = 40 * 2, CH_RE_GANG = 60 * 2;   /* c228: 절반 속도 */"),
]
