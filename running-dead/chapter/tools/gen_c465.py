import pathlib
s = pathlib.Path('c464.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
# 적이 우리 편(나 · 동료)을 못 본다
rep("const sees = (c, z) => z && isZombie(z) && !(CH_TOUR && z === me) &&", "const sees = (c, z) => z && isZombie(z) && !(CH_TOUR && z === me) && !CH_ET   /* c465: 적 테스트 — 서로 안 싸운다 */ &&")
rep("      if (!isZombie(z) || (CH_TOUR && z === me)) continue;   /* c407", "      if (!isZombie(z) || (CH_TOUR && z === me) || CH_ET) continue;   /* c465 · c407")
rep("if (isZombie(z) && !(CH_TOUR && z === me) && z.space === c.space && Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z) <= ER)", "if (isZombie(z) && !(CH_TOUR && z === me) && !CH_ET && z.space === c.space && Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z) <= ER)")
rep("for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && z.space", "for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && !CH_ET && z.space")
# 나는 이동만 · 동료는 나를 따라다니기만 (자폭 돌진은 위에서 먼저 처리)
rep("    if (CH_TOUR && z === me) { const on = pid !== null;",
    "    if (CH_ET) { z.pick = null; z.aim = null; z.engaging = null; if (z === me) { const on = pid !== null; steer(z.vel, wantV.set(on ? move.x * z.speed : 0, on ? move.y * z.speed : 0), ACCEL * 3 * dt); return; }   // c465: 적 테스트 — 공격 안 함\n      const dx = me.foot.x - z.foot.x, dz = me.foot.z - z.foot.z, d = Math.hypot(dx, dz) || 1, w = d > 2.4 ? Math.min(1, (d - 2.4) / 1.5) * z.speed : 0; steer(z.vel, wantV.set(dx / d * w, dz / d * w), ACCEL * dt); return; }   // 동료 — 나를 따라다니기만\n    if (CH_TOUR && z === me) { const on = pid !== null;")
# 우리 편은 피해 안 받음 · 적은 피해를 주지 않음 (내 스킬 — 산성 · 감전 등은 따로 들어간다)
rep("    if (((TEST_MAP && !CHAPTER) || CH_ET) && v === me) dmg = 0;", "    if (((TEST_MAP && !CHAPTER) && v === me) || (CH_ET && (isZombie(v) || isZombie(a)))) dmg = 0;   /* c465: 적 테스트 — 우리 편은 안 다치고, 우리 편 공격도 안 들어간다 */")
# 동료 10마리 (적 다시 누를 때도 10마리로 채운다) · 동료도 체력 가득
rep("    chNoMix = false;\n  }\n  function chETSet(",
    "    chNoMix = false;\n    for (let k = 0, n = zombies.filter((q) => q !== me).length; n < 10 && k < 3000; k++) {   // c465: 나를 따라다니는 동료 10\n      const a = Math.random() * Math.PI * 2, r = rand(1.2, 3.5), x = me.foot.x + Math.cos(a) * r, z = me.foot.z + Math.sin(a) * r;\n      if (spaceOf(x, z) || !freeSpot(x, z, null) || bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.85)) continue;\n      const c = addCitizen(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, ''); c.met = true; c.disc = true; makeZombie(c); n++;\n    }\n  }\n  function chETSet(")
rep("    me.hp = me.maxHp; me.stunT = 0; me.knockT = 0;   // 무적 · 아무 영향 없음",
    "    for (const z of zombies) if (!z.bombing) { z.hp = z.maxHp; z.stunT = 0; }   // c465: 동료도 무적\n    me.hp = me.maxHp; me.stunT = 0; me.knockT = 0;   // 무적 · 아무 영향 없음")
pathlib.Path('c465_patch.py').write_text('C465_R = ' + repr(R) + '\n')
