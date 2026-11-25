# c444: 자동차 부딪힘 크기(콜라이더) 10% 줄임 — 모든 차 (경찰차 · 군인차 · 민간 차 · 주차된 차 · 바리케이트 · 보스). 그림은 그대로
src = open('c443.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
K = "CH_CC"
rep("  const ck = (c) => c.kw || (c.mil ? MIL_K : 1), ckl = (c) => c.kl || (c.mil ? MIL_K : 1);", "  const ck = (c) => c.kw || (c.mil ? MIL_K : 1), ckl = (c) => c.kl || (c.mil ? MIL_K : 1);\n  const CH_CC = CHAPTER ? 0.9 : 1;   // c444: 차 부딪힘 크기 10% 줄임 (그림은 그대로)")
rep("const L = CAR_L * ckl(c) * PARKED_K / 2, W = CAR_W * ck(c) * PARKED_K / 2, cs =", "const L = CAR_L * ckl(c) * PARKED_K / 2 * CH_CC, W = CAR_W * ck(c) * PARKED_K / 2 * CH_CC, cs =")
rep("r: CAR_W * ck(c) / 2 * PARKED_K * 0.8 *", "r: CAR_W * ck(c) / 2 * PARKED_K * 0.8 * CH_CC *")
rep("const m = CAR_W * ck(car) / 2 * (CHAPTER ? 2 / 3 : 1) + 0.2;", "const m = CAR_W * ck(car) / 2 * (CHAPTER ? 2 / 3 : 1) * CH_CC + 0.2;")
rep("const ha = [CAR_L / 2 * kA * ckl(A), CAR_W / 2 * kA * ck(A) * (A.barr ? CH_BARR_W : 1)], hb = [CAR_L / 2 * kB * ckl(B), CAR_W / 2 * kB * ck(B) * (B.barr ? CH_BARR_W : 1)];", "const ha = [CAR_L / 2 * kA * ckl(A) * CH_CC, CAR_W / 2 * kA * ck(A) * (A.barr ? CH_BARR_W : 1) * CH_CC], hb = [CAR_L / 2 * kB * ckl(B) * CH_CC, CAR_W / 2 * kB * ck(B) * (B.barr ? CH_BARR_W : 1) * CH_CC];   /* c444 */")
rep("hu = CAR_L * ckl(car) / 2 * k + b.r, hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) + b.r;", "hu = CAR_L * ckl(car) / 2 * k * CH_CC + b.r, hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) * CH_CC + b.r;   /* c444 */")
rep("      const m = CAR_W * ck(car) / 2 + 0.2;\n", "      const m = CAR_W * ck(car) / 2 * CH_CC + 0.2;   /* c444 */\n")
rep("    const box = (car) => { const hu = CAR_L * ckl(car) / 2, hv = CAR_W * ck(car) / 2 * (car.barr ? CH_BARR_W : 1), m = hu + hv;", "    const box = (car) => { const hu = CAR_L * ckl(car) / 2 * CH_CC, hv = CAR_W * ck(car) / 2 * (car.barr ? CH_BARR_W : 1) * CH_CC, m = hu + hv;   /* c444 */")
rep("const u = Math.abs(dx * fx + dz * fz) - CAR_L * ckl(c) / 2, v = Math.abs(-dx * fz + dz * fx) - CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1);", "const u = Math.abs(dx * fx + dz * fz) - CAR_L * ckl(c) / 2 * CH_CC, v = Math.abs(-dx * fz + dz * fx) - CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1) * CH_CC;   /* c444 */")
rep("hu = CAR_L * ckl(car) / 2 * k + p.r, hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) + p.r;", "hu = CAR_L * ckl(car) / 2 * k * CH_CC + p.r, hv = CAR_W * ck(car) / 2 * k * (car.barr ? CH_BARR_W : 1) * CH_CC + p.r;   /* c444 */")
rep("    const hl = CAR_L * ckl(car) / 2, hw = CAR_W * ck(car) / 2, u = dx * fx + dz * fz, v = dx * rx + dz * rz;", "    const hl = CAR_L * ckl(car) / 2 * CH_CC, hw = CAR_W * ck(car) / 2 * CH_CC, u = dx * fx + dz * fz, v = dx * rx + dz * rz;   /* c444 */")
rep("hl = CAR_L * ckl(car) / 2, hw = CAR_W * ck(car) / 2, cx = Math.floor(car.x / 4)", "hl = CAR_L * ckl(car) / 2 * CH_CC, hw = CAR_W * ck(car) / 2 * CH_CC, cx = Math.floor(car.x / 4)")
open('c444_patch.py', 'w').write("# c444: 차 콜라이더 10% 줄임\nC444_R = " + repr(R) + "\n")
print(len(R))
