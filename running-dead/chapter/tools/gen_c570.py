import pathlib
s = pathlib.Path('c569.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("      p.s.position.set(p.x, 0, p.z).addScaledVector(UP, (p.kind === 'gene' ? 0.7 : 1.0) + Math.sin(p.t * 3) * 0.12);",
    """      if (CHAPTER && isZombie(me)) {   /* c570: 자석 — 내 공격 거리의 1.5배 안이면 나한테 끌려온다 (벽에 안 가렸을 때) */
        const dx = me.foot.x - p.x, dz = me.foot.z - p.z, d = Math.hypot(dx, dz);
        if (!p.mag && d <= CH_MAG_R * (MELEE + Math.max(0, (me.r || BODY) - BODY)) && (chSameSp(me.space, p.space) || !fireBlocked(me.foot.x, me.foot.z, p.x, p.z))) { p.mag = true; p.magV = 4; }
        if (p.mag && d > 0.01) { p.magV = Math.min(30, p.magV + 40 * dt); const st = Math.min(d, p.magV * dt); p.x += dx / d * st; p.z += dz / d * st; p.space = me.space; }
      }
      p.s.position.set(p.x, 0, p.z).addScaledVector(UP, (p.kind === 'gene' ? 0.7 : 1.0) + Math.sin(p.t * 3) * 0.12);""")
rep("  function dropPickup(kind, x, z, space) {", "  const CH_MAG_R = 1.5;   /* c570: 자석 거리 = 내 공격 거리 × 1.5 */\n  function dropPickup(kind, x, z, space) {")
pathlib.Path('c570_patch.py').write_text('C570_R = ' + repr(R) + '\n')
print(len(R))
