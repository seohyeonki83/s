import pathlib
s = pathlib.Path('c500.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("    const R = 2 + chLvB('bomb');", "    const R = 1.7 + 0.5 * chLvB('bomb');   /* c501: 1.7칸 · 0.5칸씩 · ★5 4.2칸 */")
rep("    bomb: (n) => `터지는 범위 ${2 + Math.min(5, n)}칸", "    bomb: (n) => `터지는 범위 ${+(1.7 + 0.5 * Math.min(5, n)).toFixed(1)}칸")
rep("    bomb: ['', (n) => `${2 + Math.min(5, n)}칸·", "    bomb: ['', (n) => `${+(1.7 + 0.5 * Math.min(5, n)).toFixed(1)}칸·")
pathlib.Path('c501_patch.py').write_text('C501_R = ' + repr(R) + '\n')
