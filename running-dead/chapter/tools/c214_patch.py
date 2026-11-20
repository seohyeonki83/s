# c214: 모든 벽 체력 25% 줄임
C214_R = [
 ("for (const o of chWallObjs) { o.dead = false; o.hp = o.maxHp = u * o.k;", "for (const o of chWallObjs) { o.dead = false; o.hp = o.maxHp = u * o.k * 0.75;   /* c214: 25% 줄임 */"),
]
