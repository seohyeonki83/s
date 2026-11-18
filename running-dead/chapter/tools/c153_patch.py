# c153: 적 전체 체력 5% 줄임 (노랑·주황·빨강·분홍·경찰·군인·저격수·장갑차)
C153_R = [
 ("      addHpBar(c, hpFoeMat);\n    }\n    if (c.police) {                      // 쏠 때 번쩍이는 노란 선", "      if (CHAPTER) c.hp = c.maxHp = c.maxHp * 0.95;   // c153: 적 체력 5% 줄임\n      addHpBar(c, hpFoeMat);\n    }\n    if (c.police) {                      // 쏠 때 번쩍이는 노란 선"),
 ("c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2); c.hpDisp = c.hp;", "c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2) * 0.95; c.hpDisp = c.hp;   /* c153 */"),
 ("car.massK = 4; car.hpK = 10;", "car.massK = 4; car.hpK = 10 * 0.95;   /* c153 */"),
]
