# c77: 차 크기 등급 — 경찰차 크기(세단·스포츠카) · 군인차 크기(밴·구급차) · 그보다 큰 것(트럭·소방차). 소형차만 경찰차보다 살짝 작다 (무게는 경찰차와 같다)
#      건물 안 사물 — 체력이 높은 것만 20% 깎는다 (둥근 것: 내 기본 공격 4대 이상짜리 · 네모: 큰 탁자의 1.2배 이상짜리)
C77_R = [
  ("kl: 0.82, kw: 0.9,  hp: 0.8", "kl: 0.9, kw: 0.94, hp: 0.8"),      # 소형차 — 경찰차보다 살짝 작게 (전에는 0.82 × 0.9)
  ("kl: 1.06, kw: 0.96, hp: 0.8", "kl: 1.0, kw: 1.0, hp: 0.8"),       # 스포츠카 = 경찰차 크기
  ("kl: 1.22, kw: 1.1,  hp: 1.3", "kl: 1.3, kw: 1.3, hp: 1.3"),       # 밴 = 군인차 크기 (MIL_K 1.3)
  ("kl: 1.25, kw: 1.12, hp: 1.3", "kl: 1.3, kw: 1.3, hp: 1.3"),       # 구급차 = 군인차 크기
  ("kl: 1.58, kw: 1.2,  hp: 1.8", "kl: 1.58, kw: 1.36, hp: 1.8"),     # 트럭 — 군인차보다 길고 넓게
  ("kl: 1.62, kw: 1.25, hp: 2.0", "kl: 1.62, kw: 1.4, hp: 2.0"),      # 소방차 — 가장 크다
  ("  const chProps = [], chSlabs = [];", "  const CH_FURN_CUT = 0.8;                    // c77: 체력이 높은 사물은 20% 깎는다\n  const chProps = [], chSlabs = [];"),
  ("b.hp = b.maxHp = MY_DAMAGE * P.hits; b.sleep = true;", "b.hp = b.maxHp = MY_DAMAGE * P.hits * (P.hits >= 4 ? CH_FURN_CUT : 1); b.sleep = true;   /* c77: 4대 이상짜리(옷장·사물함·냉장고·샌드백·덤벨 거치대·현금인출기·자판기)만 */"),
  ("hp: CH_SLAB_HP * D.hp, maxHp: CH_SLAB_HP * D.hp, dead: false };", "hp: CH_SLAB_HP * D.hp * (D.hp >= 1.2 ? CH_FURN_CUT : 1), maxHp: CH_SLAB_HP * D.hp * (D.hp >= 1.2 ? CH_FURN_CUT : 1), dead: false };   /* c77: 1.2배 이상짜리(책장·냉장 진열대·계산대)만 */"),
]
