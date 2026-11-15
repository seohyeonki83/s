# c121: 자폭 점수 — 변이 좀비가 될 사람(분홍)은 저격수와 같은 40점
C121_R = [
 ("if (CHAPTER) sc += CH_BOMB_PT[t];", "if (CHAPTER) sc += c.boss ? 40 : CH_BOMB_PT[t];   /* c121: 분홍 = 저격수와 같은 40점 */"),
]
