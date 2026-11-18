# c142: 금고에 꽝 없음 (창고의 꽝 10%를 없앤다 — 그 몫은 나머지 아이템이 비율대로 나눠 갖는다)
C142_R = [
 ("let r = Math.random() * (CH_LM.has(type) ? T.spec.length * T.p + T.rest : 100);", "let r = Math.random() * (T.spec.length * T.p + T.rest);   /* c142: 어느 금고든 꽝 없음 */"),
]
