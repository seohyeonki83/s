# c111: 주유소 기둥과 지붕 그림자도 없앤다
import pprint
S = open('c110.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("    for (const [t, x, z, inv] of CH_MAP.props || []) {\n      const P = CH_PROP[t]; if (!P) continue;", "    for (const [t, x, z, inv] of CH_MAP.props || []) {\n      const P = CH_PROP[t]; if (!P || t === 'pillar') continue;   /* c111: 지붕이 없으니 기둥도 안 세운다 */")
rep("const [c0, c1, c2, c3] = A.can; g.fillStyle = 'rgba(0, 0, 0, 0.12)';", "const [c0, c1, c2, c3] = A.can; g.fillStyle = 'rgba(0, 0, 0, 0)';   /* c111: 지붕 그림자도 없앤다 */")
open('c111_patch.py', 'w', encoding='utf8').write('# c111: 주유소 기둥·지붕 그림자 없앰 (gen_c111.py가 만든다)\nC111_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
