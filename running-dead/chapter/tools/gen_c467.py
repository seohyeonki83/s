import pathlib
s = pathlib.Path('c466.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
# 숙주 감전 +0.5초씩
rep("T = (CH_WV('taserT', lv('taser')) + 0.3 * r) * chLingK();", "T = (CH_WV('taserT', lv('taser')) + 0.5 * r) * chLingK();   /* c467: 0.3 → 0.5초씩 */")
# 감전되면 공격을 끊는다 (연사 · 돌진 · 쿨타임 처음부터)
rep("  function chChainTick(dt) {", "  function chStunCut(c) { c.lungeT = -1; c.burstN = 0; c.shotStop = 0; c.atkT = Math.max(c.atkT || 0, HIT_EVERY * (c.sniper ? 4 : 1)); }   // c467: 감전 = 하던 공격을 끊고 공격 쿨타임이 처음부터\n  function chChainTick(dt) {")
# 번지는 감전 0.2 → 0.3초 · 진짜 감전과 같은 효과 (숙주에서 번개 줄기 · 깜빡임 · 공격 끊기)
rep("c.stunT = Math.max(c.stunT || 0, 0.2); c.vel.set(0, 0); c.lungeT = -1; zap(c.foot.x, c.foot.z); }",
    "c.stunT = Math.max(c.stunT || 0, 0.3); c.vel.set(0, 0); chStunCut(c); zaps.push({ to: c, t: 0.3, fx: x, fz: z }); zap(c.foot.x, c.foot.z); }   /* c467: 0.3초 · 진짜 감전처럼 */")
rep("d.stunT = Math.max(d.stunT || 0, 0.2); zap(d.x, d.z); }", "d.stunT = Math.max(d.stunT || 0, 0.3); zaps.push({ to: d, t: 0.3, fx: x, fz: z }); zap(d.x, d.z); }")
rep("T.stunT = Math.max(T.stunT || 0, 0.2); T.vx = T.vz = 0; zap(T.x, T.z); }", "T.stunT = Math.max(T.stunT || 0, 0.3); T.vx = T.vz = 0; T.burstN = 0; zap(T.x, T.z); }")
rep("// c431: 숙주가 감전된 동안 0.8초마다 둘레 적 0.2초 감전", "// c467: 0.3초 · c431: 숙주가 감전된 동안 0.8초마다 둘레 적 0.2초 감전")
# 테이저 · 전기폭탄도 공격을 끊는다
rep("c.stunT = chTaserT(c);   /* c431 */   /* c139 */ c.vel.set(0, 0); zaps.push({ to: c, t: 0.45 }); }", "c.stunT = chTaserT(c);   /* c431 */   /* c139 */ c.vel.set(0, 0); chStunCut(c); zaps.push({ to: c, t: 0.45 }); }")
rep("c.stunT = Math.max(c.stunT || 0, T); c.vel.set(0, 0); zaps.push({ to: c, t: 0.3", "c.stunT = Math.max(c.stunT || 0, T); c.vel.set(0, 0); chStunCut(c); zaps.push({ to: c, t: 0.3")
# 번개 줄기 — 시작점을 줄 수 있게 (번지는 감전은 숙주에서)
rep("      const [ax, ay] = toScreen(me.foot.x, me.foot.z, W, H);\n      const [bx, by] = zp.to ? (zp.to.drone",
    "      const [ax, ay] = zp.fx !== undefined ? toScreen(zp.fx, zp.fz, W, H) : toScreen(me.foot.x, me.foot.z, W, H);   // c467\n      const [bx, by] = zp.to ? (zp.to.drone")
pathlib.Path('c467_patch.py').write_text('C467_R = ' + repr(R) + '\n')
rep("그 적 둘레의 적들도 0.8초마다 0.2초씩 감전됩니다.', line: (r) => `감전 ${(3.5 + 0.3 * r).toFixed(1)}초 · 둘레 ${(MELEE * (1 + 0.2 * (r - 1))).toFixed(1)}칸 안 적 0.8초마다 0.2초 감전`",
    "그 적 둘레의 적들도 0.8초마다 0.3초씩 감전됩니다.', line: (r) => `감전 ${(3.5 + 0.5 * r).toFixed(1)}초 · 둘레 ${(MELEE * (1 + 0.2 * (r - 1))).toFixed(1)}칸 안 적 0.8초마다 0.3초 감전`")
pathlib.Path('c467_patch.py').write_text('C467_R = ' + repr(R) + '\n')
