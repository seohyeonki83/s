import pathlib, re
s = pathlib.Path('c469.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
key = "4 + 2 * chLvB('bomb')"
for m in re.finditer(re.escape(key), s):
    a = s[m.start() - 45:m.end()]
    rep(a, a[:-len(key)] + "7 + 2 * chLvB('bomb')")   # c470: 산성 4 → 7초부터
rep("    bomb: (n) => `터지는 범위 ${1.5 + n}칸 · 산성 ${4 + 2 * n}초`,", "    bomb: (n) => `터지는 범위 ${1.5 + n}칸 · 산성 ${7 + 2 * n}초`,   /* c470 */")
rep("    bomb: ['', (n) => `${1.5 + n}칸·${4 + 2 * n}초`],", "    bomb: ['', (n) => `${1.5 + n}칸·${7 + 2 * n}초`],")
pathlib.Path('c470_patch.py').write_text('C470_R = ' + repr(R) + '\n')
print(len(R))
