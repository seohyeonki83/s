import pathlib, re
s = pathlib.Path('c470.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
key = "7 + 2 * chLvB('bomb')"
for m in re.finditer(re.escape(key), s):
    a = s[m.start() - 45:m.end()]
    rep(a, a[:-len(key)] + "8 + 2 * chLvB('bomb')")   # c471: 산성 8초부터
rep("산성 ${7 + 2 * n}초`,   /* c470 */", "산성 ${8 + 2 * n}초`,   /* c471 */")
rep("    bomb: ['', (n) => `${1.5 + n}칸·${7 + 2 * n}초`],", "    bomb: ['', (n) => `${1.5 + n}칸·${8 + 2 * n}초`],")
pathlib.Path('c471_patch.py').write_text('C471_R = ' + repr(R) + '\n')
print(len(R))
