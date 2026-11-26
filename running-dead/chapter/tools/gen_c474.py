import pathlib, re
s = pathlib.Path('c473.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
key = "(3 + chLvB('bomb'))"
for m in re.finditer(re.escape(key), s):
    a = s[m.start() - 45:m.end()]
    rep(a, a[:-len(key)] + "(4 + 0.6 * chLvB('bomb'))")   # c474: 산성 4초 시작 · ★5 7초 (0.6초씩)
rep("산성 ${3 + Math.min(5, n)}초`,   /* c473 */", "산성 ${+(4 + 0.6 * Math.min(5, n)).toFixed(1)}초`,   /* c474 */")
rep("    bomb: ['', (n) => `${1.5 + n}칸·${3 + Math.min(5, n)}초`],", "    bomb: ['', (n) => `${1.5 + n}칸·${+(4 + 0.6 * Math.min(5, n)).toFixed(1)}초`],")
pathlib.Path('c474_patch.py').write_text('C474_R = ' + repr(R) + '\n')
print(len(R))
