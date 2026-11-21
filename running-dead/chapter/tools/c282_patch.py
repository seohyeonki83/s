# c282: 촉매제 — 변이 좀비 공격력 +10%씩 · 최대 체력 +5%씩 (같이 오른다)
C282_R = [
  ("owned.catalyst ? 1 + 0.07 * (1 + lv('catalyst')) : 1", "owned.catalyst ? 1 + 0.1 * (1 + lv('catalyst')) : 1   /* c282: 10%씩 */"),
  ("    z.hp = z.maxHp;                           // 체력 가득", "    if (CHAPTER && owned.catalyst) { z.catK = 1 + 0.05 * (1 + lv('catalyst')); z.maxHp *= z.catK; }   // c282: 촉매제 — 변이하는 동안 최대 체력 +5%씩\n    z.hp = z.maxHp;                           // 체력 가득"),
  ("    me.mesh.material.color.setHex(MUT_COL[type]);", "    if (CHAPTER && owned.catalyst) { me.catK = 1 + 0.05 * (1 + lv('catalyst')); me.maxHp *= me.catK; me.hp *= me.catK; }   // c282: 각성한 나도 (체력 비율은 그대로)\n    me.mesh.material.color.setHex(MUT_COL[type]);"),
  ("if (z === me) { if (CHAPTER) chMeRing(false); me.mut = null;", "if (z === me) { if (me.catK) { me.maxHp /= me.catK; me.hp = Math.min(me.maxHp, me.hp / me.catK); me.catK = 0; }   /* c282 */ if (CHAPTER) chMeRing(false); me.mut = null;"),
  ("    z.mut = null;\n    z.mesh.material.color.setHex(COLOR.ally);", "    z.mut = null;\n    if (z.catK) { z.maxHp /= z.catK; z.hp = Math.min(z.hp, z.maxHp); z.catK = 0; }   // c282: 변이가 풀리면 원래 최대 체력\n    z.mesh.material.color.setHex(COLOR.ally);"),
  ("catalyst: (n) => `변이 좀비 공격력 +${7 * (1 + n)}%`,", "catalyst: (n) => `변이 좀비 공격력 +${10 * (1 + n)}% · 최대 체력 +${5 * (1 + n)}%`,"),
  ("catalyst: ['변이', (n) => `+${7 * (1 + n)}%`]", "catalyst: ['공격', (n) => `+${10 * (1 + n)}%`]"),
  ("catalyst: ['변이한 좀비의 공격력이 오릅니다.', '강화 시 더 오릅니다.'],", "catalyst: ['변이한 좀비의 공격력과 최대 체력이 오릅니다.', '강화 시 더 오릅니다.'],"),
  ("catalyst: '변이한 좀비의 공격력이 오릅니다. 강화하면 더 오릅니다.',", "catalyst: '변이한 좀비의 공격력과 최대 체력이 함께 오릅니다. 강화하면 더 오릅니다.',"),
]
C282_R.append(("catalyst: '변이 좀비 공격력 증가',", "catalyst: '변이 좀비 공격력·체력 증가',"))
C282_R.append(("  function useMutate() {", "  window.__mut = (z) => mutate(z); window.__unmut = (z) => unmutate(z); window.__zd = (z) => zDamage(z);   // 테스트용\n  function useMutate() {"))
