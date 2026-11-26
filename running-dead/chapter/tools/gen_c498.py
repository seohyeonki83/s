import pathlib
s = pathlib.Path('c497.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("cashT: [2, 3.3, 4.7, 6, 7.3, 8.7, 10]", "cashT: [2, 2.8, 3.6, 4.4, 5.2, 6]   /* c498: ★5 = 6초 */")
rep("const chNearFresh = (fresh, x, z, R, sp) => { let best = null, bd = R; for (const k of fresh) { if (k.space !== sp) continue; const d = Math.hypot(k.x - x, k.z - z); if (d < bd && !blocked(x, z, k.x, k.z)) { bd = d; best = k; } } return best; };",
    "const chNearFresh = (fresh, x, z, R, sp, fly) => { let best = null, bd = R; for (const k of fresh) { if (k.space !== sp) continue; const d = Math.hypot(k.x - x, k.z - z); if (d < bd && (fly || !blocked(x, z, k.x, k.z))) { bd = d; best = k; } } return best; };   /* c498: fly = 드론 (건물에 안 가린다) */")
rep("for (const d of chDrones) { if (d.dead) continue; const k = chNearFresh(fresh, d.x, d.z, SIGHT * cashK() + 4, null);", "for (const d of chDrones) { if (d.dead) continue; const k = chNearFresh(fresh, d.x, d.z, SIGHT * cashK() + 4, null, true);   /* c498 */")
pathlib.Path('c498_patch.py').write_text('C498_R = ' + repr(R) + '\n')
