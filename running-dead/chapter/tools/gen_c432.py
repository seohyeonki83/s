# c432: 자폭하라고 지정된 동료 — 그 순간 체력 100%로 차고, 받는 피해 절반 (터질 때까지)
src = open('c431.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    z.bombing = { R, t: 0, tg: null };\n", "    z.bombing = { R, t: 0, tg: null };\n    if (CHAPTER) { z.hp = z.maxHp; if (z.hpBar) z.hpDisp = z.hp; }   // c432: 지정되는 순간 체력 가득\n")
rep("    if (isZombie(v) && v.mut) dmg *=", "    if (CHAPTER && isZombie(v) && v.bombing) dmg *= 0.5;   // c432: 자폭하러 가는 동료는 받는 피해 절반\n    if (isZombie(v) && v.mut) dmg *=")
open('c432_patch.py', 'w').write("# c432: 자폭 지정 동료 체력 가득 · 받는 피해 절반\nC432_R = " + repr(R) + "\n")
