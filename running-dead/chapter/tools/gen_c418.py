# c418: 체력이 다한 적(체력이 있던 사람이 0이 됨)은 공격 속도·이동 속도가 반
src = open('c417.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  function updateCitizen(c, dt) {", "  function chDownK(b) { return CHAPTER && b.kind === 'citizen' && b.maxHp > 0 && b.hp <= 0 ? 0.5 : 1; }   // c418: 체력이 다한 적 — 공격 속도·이동 속도 반\n  function updateCitizen(c, dt) {")
rep("c.atkT -= dt * (c.goo ? 0.56 : 1);", "c.atkT -= dt * (c.goo ? 0.56 : 1) * chDownK(c);   /* c418 */", 4)
rep("c.atkT += own ? -dt * (c.goo ? 0.56 : 1) : 0;", "c.atkT += own ? -dt * (c.goo ? 0.56 : 1) * chDownK(c) : 0;   /* c418 */")
rep("const gk = (b.goo ? 0.56 : 1) * (b.rage ? 1 + rageK() : 1);", "const gk = (b.goo ? 0.56 : 1) * (b.rage ? 1 + rageK() : 1) * chDownK(b);   /* c418: 체력이 다한 적은 반 */")
open('c418_patch.py', 'w').write("# c418: 체력이 다한 적 공격·이동 속도 반\nC418_R = " + repr(R) + "\n")
