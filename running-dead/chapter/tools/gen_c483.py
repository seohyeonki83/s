import pathlib
s = pathlib.Path('c482.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("    const R = 1.5 + chLvB('bomb');", "    const R = 2 + chLvB('bomb');   /* c483: 2칸 · 1칸씩 · ★5 7칸 */")
rep("    bomb: (n) => `터지는 범위 ${1.5 + Math.min(5, n)}칸", "    bomb: (n) => `터지는 범위 ${2 + Math.min(5, n)}칸")
rep("    bomb: ['', (n) => `${1.5 + Math.min(5, n)}칸·", "    bomb: ['', (n) => `${2 + Math.min(5, n)}칸·")
pathlib.Path('c483_patch.py').write_text('C483_R = ' + repr(R) + '\n')
