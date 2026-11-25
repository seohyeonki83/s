import pathlib
s = pathlib.Path('c454.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("if (car.dozer) { const pool = CH_ITEMS.filter((k) => !chFull(k)); if (pool.length) dropPickup(",
    "if (car.dozer) { const pool = CH_ITEMS.filter((k) => !chFull(k)); if (pool.length && chTanks.every((t) => t.wreck || t === car)) dropPickup(")   # c455: 마지막으로 부순 불도저만 아이템
pathlib.Path('c455_patch.py').write_text('C455_R = ' + repr(R) + '\n')
