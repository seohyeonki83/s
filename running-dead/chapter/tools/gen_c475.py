import pathlib, re
s = pathlib.Path('c474.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
# 자폭 산성 도트 2 → 3
rep("c.hp = Math.max(0, c.hp - 2 - chAcidB());   /* c123: 도트 2", "c.hp = Math.max(0, c.hp - 3 - chAcidB());   /* c475: 도트 3 · c123: 도트 2")
rep("chDotPop(c.foot.x + 0.6, c.foot.z, 2 + chAcidB());   // c265", "chDotPop(c.foot.x + 0.6, c.foot.z, 3 + chAcidB());   // c475 · c265")
rep("d.gooT -= CH_DOT_T; const n = 2 + chAcidB();", "d.gooT -= CH_DOT_T; const n = 3 + chAcidB();   /* c475 */")
rep("car.gooT -= CH_DOT_T; const gd = 2 + chAcidB();", "car.gooT -= CH_DOT_T; const gd = 3 + chAcidB();   /* c475 */")
# 새끼 좀비가 터지는 산성 폭발 — 터질 때 피해 3 고정
rep("  const chAcidHit = () => Math.round(3 + 7 * lv('acid') / 5);", "  let chAcidMiniF = false;   // c475: 새끼 좀비 산성 폭발 중\n  const chAcidHit = () => chAcidMiniF ? 3 : Math.round(3 + 7 * lv('acid') / 5);   /* c475: 새끼 좀비는 3 고정 */")
rep("    const n = lv('acid'); if (Math.random() >= 0.3 + 0.1 * n) return;", "    const n = lv('acid'); if (Math.random() >= 0.3 + 0.1 * n) return;\n    chAcidMiniF = !!z.mini;   // c475")
rep("  }\n  window.__kz = (z) => killZombie(z);", "    chAcidMiniF = false;   // c475\n  }\n  window.__kz = (z) => killZombie(z);")
pathlib.Path('c475_patch.py').write_text('C475_R = ' + repr(R) + '\n')
