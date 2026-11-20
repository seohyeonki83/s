# c230: 나를 뺀 모든 유닛(동료·변이·시민·경찰·군인·저격수·분홍·보스) 최대 체력 10% 줄임 · 체력바 한 겹 기준도 동료 체력에 맞춰 같이
C230_R = [
 ("      if (CHAPTER) c.hp = c.maxHp = c.maxHp * 0.95;   // c153: 적 체력 5% 줄임", "      if (CHAPTER) c.hp = c.maxHp = c.maxHp * 0.95 * 0.9;   // c153: 적 체력 5% 줄임 · c230: 10% 더"),
 ("    c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2) * 0.95; c.hpDisp = c.hp;", "    c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2) * 0.95 * 0.9; c.hpDisp = c.hp;   /* c230 */"),
 ("    if (to === 'guard') { c.hp = c.maxHp = GUARD_HP * 0.95 * 0.9 * 0.95;", "    if (to === 'guard') { c.hp = c.maxHp = GUARD_HP * 0.95 * 0.9 * 0.95 * 0.9;   /* c230 */"),
 ("  const allyMaxHp = () => ALLY_HP * 0.9 * (1 + 0.07 * up.skin);", "  const allyMaxHp = () => ALLY_HP * 0.9 * 0.9 * (1 + 0.07 * up.skin);   /* c230: 10% 줄임 */"),
 ("car.hpK = 10 * 0.95 * 3 * 0.9 * 1.5;", "car.hpK = 10 * 0.95 * 3 * 0.9 * 1.5 * 0.9;   /* c230: 10% 줄임 */"),
 ("const U0 = b === me ? MY_HP : ALLY_HP * 0.9; return", "const U0 = b === me ? MY_HP : ALLY_HP * 0.9 * 0.9; return"),
 ("  const chBarU = (b) => (b === me ? MY_HP : ALLY_HP * 0.9) * chBarK(b);", "  const chBarU = (b) => (b === me ? MY_HP : ALLY_HP * 0.9 * 0.9) * chBarK(b);   // c230: 동료 체력에 맞춤"),
]
