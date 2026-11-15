# c87: 내가 차를 칠 때도 문처럼 공격 거리 4배 안 동료를 부른다 (안 치면 다시 손 닿는 거리)
C87_R = [
 ("function chObjLim(z, o) { return o.type === 'door' && z !== me && hotObj(o) ? 4 * MELEE : chReach(z); }",
  "function chObjLim(z, o) { return (o.type === 'door' || o.type === 'car') && z !== me && hotObj(o) ? 4 * MELEE : chReach(z); }   /* c87: 차도 */"),
 ("const lim = chReach(z);   /* c86 */", "const lim = chObjLim(z, o);   /* c86 · c87 */"),
]
