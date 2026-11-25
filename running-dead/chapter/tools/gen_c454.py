# c454: 불도저 2대 (체력 20% 더 깎음 = 장갑차의 64%) — 보스를 여럿 다루게 (chTanks)
src = open('c453.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  let chTank = null;", "  let chTank = null; const chTanks = [];   // c454: 보스 여럿 (불도저 2대)")
rep("if (CHAPTER) { car.dozer = true; car.hpK *= 0.8; car.tint0 = 0xd9a21b; }", "if (CHAPTER) { car.dozer = true; car.hpK *= 0.8 * 0.8; car.tint0 = 0xd9a21b; }   /* c454: 체력 20% 더 깎음 */")
rep("    chTank = car;\n", "    chTank = car; chTanks.push(car);   // c454\n")
rep("if (w.boss) chBossSpawn(w.seg);", "if (w.boss) { chBossSpawn(w.seg); chBossSpawn(w.seg); }   /* c454: 불도저 2대 */")
# 감전 대상
rep("      if (CHAPTER && chTank && !chTank.wreck && !(chTank.stunT > 0)) {   /* c194: 건물 안이어도 (공격선만 본다) */ const T = chTank, d =", "      if (CHAPTER) for (const T of chTanks) if (!T.wreck && !(T.stunT > 0)) {   /* c454 */   /* c194: 건물 안이어도 (공격선만 본다) */ const d =")
# 금
rep("    const tk = chTank; if (tk && !tk.wreck) { const k = chNearFresh(fresh, tk.x, tk.z, SIGHT * cashK() + 4, null);", "    for (const tk of chTanks) if (!tk.wreck) { const k = chNearFresh(fresh, tk.x, tk.z, SIGHT * cashK() + 4, null);   /* c454 */")
# 자폭 고르기
rep("    const tk = chTank && !chTank.wreck ? chTank : null, drones = chDroneSeen();", "    const tks = chTanks.filter((t) => !t.wreck), drones = chDroneSeen();   /* c454 */")
rep("if (tk && Math.hypot(tk.x - x, tk.z - z) <= R + 1.4) sc += 80; }", "for (const tk of tks) if (Math.hypot(tk.x - x, tk.z - z) <= R + 1.4) sc += 80; }")
rep("    if (tk) { const q = Math.max(0, Math.hypot(tk.x - me.foot.x, tk.z - me.foot.z) - CAR_L * CH_TK_KL / 2);", "    for (const tk of tks) { const q = Math.max(0, Math.hypot(tk.x - me.foot.x, tk.z - me.foot.z) - CAR_L * CH_TK_KL / 2);")
rep("else B.drone = { get x() { return tk.x; }, get z() { return tk.z; }, get dead() { return tk.wreck; } };", "else { const tk = T.tk; B.drone = { get x() { return tk.x; }, get z() { return tk.z; }, get dead() { return tk.wreck; } }; }")
# 자폭 산성 · 전이 감전 · 전기폭탄 · 산성 폭발
rep("    if (CHAPTER && chTank && !chTank.wreck && Math.hypot(chTank.x - x, chTank.z - zz) <= R + 1.4) chTankGoo(chTank);", "    if (CHAPTER) for (const T of chTanks) if (!T.wreck && Math.hypot(T.x - x, T.z - zz) <= R + 1.4) chTankGoo(T);   /* c454 */")
rep("      const T = chTank; if (T && T !== e && !T.wreck && Math.hypot(T.x - x, T.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) {", "      for (const T of chTanks) if (T !== e && !T.wreck && Math.hypot(T.x - x, T.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) {   /* c454 */")
rep("    const tk = chTank; if (tk && !tk.wreck && Math.hypot(tk.x - x, tk.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) {", "    for (const tk of chTanks) if (!tk.wreck && Math.hypot(tk.x - x, tk.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) {   /* c454 */")
rep("    const tk = chTank; if (tk && !tk.wreck && !z.space && Math.hypot(tk.x - x, tk.z - zz) - CAR_L * CH_TK_KL / 2 <= R) {", "    for (const tk of chTanks) if (!tk.wreck && !z.space && Math.hypot(tk.x - x, tk.z - zz) - CAR_L * CH_TK_KL / 2 <= R) {   /* c454 */")
# 새 판 · 특공대 · 호위 · 죽음 · 차 부딪힘
rep("    if (chTank) chTank.tkPh = null; Object.assign(chSf,", "    for (const t of chTanks) t.tkPh = null; Object.assign(chSf,")
rep("    if (chTank && chTank.tracer) scene.remove(chTank.tracer);\n    chTank = null;", "    for (const t of chTanks) if (t.tracer) scene.remove(t.tracer);\n    chTank = null; chTanks.length = 0;   // c454")
rep("    } else {\n      const T = chTank;\n", "    } else {\n      const T = chTanks.find((t) => !t.wreck) || chTanks[0];   // c454: 하나라도 살아 있으면 특공대 · 다 부서져야 끝\n")
rep("  function chTankMaster(c) {                   // 군부대 호위: 군인 → 제 저격수 (죽으면 장갑차) · 저격수 → 장갑차 · 장갑차가 죽으면 아무도 호위 안 한다\n    const T = chTank;", "  function chTankMaster(c) {                   // 군부대 호위: 군인 → 제 저격수 (죽으면 장갑차) · 저격수 → 장갑차 · 장갑차가 죽으면 아무도 호위 안 한다\n    const T = chTanks.find((t) => !t.wreck) || null;   // c454")
rep("    if (!CHAPTER || car !== chTank) return;", "    if (!CHAPTER || !chTanks.includes(car)) return;   // c454")
rep("  function chTankCar(o) {", "  function chTankCar(o, T0) {")
rep("    const T = chTank, ds = T && T.tkPh === 'dash';", "    const T = T0 || chTank, ds = T && T.tkPh === 'dash';   // c454: 닿은 그 보스")
rep("if (A.tank || B.tank) chTankCar(A.tank ? B : A);", "if ((A.tank || B.tank) && !(A.tank && B.tank)) chTankCar(A.tank ? B : A, A.tank ? A : B);   /* c454: 보스끼리는 안 부순다 */")
open('c454_patch.py', 'w').write("# c454: 불도저 2대\nC454_R = " + repr(R) + "\n")
print(len(R))
