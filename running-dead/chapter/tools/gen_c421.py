# c421: 자폭 산성(산성 덩어리)의 둔화 없앰 — 사람 이동·공격 속도, 장갑차 이동·공격·특수기 (도트 피해는 그대로)
src = open('c420.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
G = "(c.goo && !CHAPTER ? 0.56 : 1)"
rep("c.atkT -= dt * (c.goo ? 0.56 : 1) * chDownK(c);", "c.atkT -= dt * " + G + " * chDownK(c);   /* c421: 챕터 — 산성 둔화 없음 */", 4)
rep("-dt * (c.goo ? 0.56 : 1) * chDownK(c) : 0;", "-dt * " + G + " * chDownK(c) : 0;   /* c421 */")
rep("const gk = (b.goo ? 0.56 : 1) * (b.rage", "const gk = (b.goo && !CHAPTER ? 0.56 : 1)   /* c421 */ * (b.rage")
rep("car.spAcc += dt * CH_SP_RATE * (car.goo ? 0.56 : 1);", "car.spAcc += dt * CH_SP_RATE;   /* c421: 산성 둔화 없음 */")
rep("* (car.goo ? 0.8 : 1);   /* c179", "/* c421: 산성 둔화 없음 */;   /* c179")
rep("car.atkT -= dt * (car.goo ? 0.56 : 1);", "car.atkT -= dt;   /* c421: 산성 둔화 없음 */")
open('c421_patch.py', 'w').write("# c421: 자폭 산성 둔화 없앰\nC421_R = " + repr(R) + "\n")
