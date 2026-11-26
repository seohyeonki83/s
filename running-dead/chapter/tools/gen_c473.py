import pathlib, re
s = pathlib.Path('c472.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
key = "8 + 2 * chLvB('bomb')"
for m in re.finditer(re.escape(key), s):
    a = s[m.start() - 45:m.end()]
    rep(a, a[:-len(key)] + "(3 + chLvB('bomb'))")   # c473: 산성 3초 시작 · 1초씩 · ★5 8초
rep("산성 ${8 + 2 * n}초`,   /* c471 */", "산성 ${3 + Math.min(5, n)}초`,   /* c473 */")
rep("    bomb: ['', (n) => `${1.5 + n}칸·${8 + 2 * n}초`],", "    bomb: ['', (n) => `${1.5 + n}칸·${3 + Math.min(5, n)}초`],")
pathlib.Path('c473_patch.py').write_text('C473_R = ' + repr(R) + '\n')
print(len(R))
