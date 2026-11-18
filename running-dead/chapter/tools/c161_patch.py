# c161: 레벨업의 '무기 강화' 카드가 나올 확률 2배 (무기를 가진 뒤에만 나온다 — 전과 같다)
C161_R = [
 ("let pool = chUpPool().concat(Array(chWupN()).fill('__w'));", "let pool = chUpPool().concat(Array(chWupN() * 2).fill('__w'));   /* c161: 2배 */"),
]
