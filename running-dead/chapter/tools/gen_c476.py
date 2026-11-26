import pathlib
s = pathlib.Path('c475.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("  const chAcidHit = () => chAcidMiniF ? 3 : Math.round(3 + 7 * lv('acid') / 5);   /* c475: 새끼 좀비는 3 고정 */", "  const chAcidHit = () => Math.round(3 + 7 * lv('acid') / 5);   /* c476: 새끼 좀비 3 고정 되돌림 (c475) */")
pathlib.Path('c476_patch.py').write_text('C476_R = ' + repr(R) + '\n')
