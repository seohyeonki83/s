# c432: 자폭 지정 동료 체력 가득 · 받는 피해 절반
C432_R = [('    z.bombing = { R, t: 0, tg: null };\n', '    z.bombing = { R, t: 0, tg: null };\n    if (CHAPTER) { z.hp = z.maxHp; if (z.hpBar) z.hpDisp = z.hp; }   // c432: 지정되는 순간 체력 가득\n'), ('    if (isZombie(v) && v.mut) dmg *=', '    if (CHAPTER && isZombie(v) && v.bombing) dmg *= 0.5;   // c432: 자폭하러 가는 동료는 받는 피해 절반\n    if (isZombie(v) && v.mut) dmg *=')]
