# c104: 감염시켜 얻은 변이 좀비 — 다이아몬드 표시를 그대로 달고 다닌다 · 덩치 체력 1.2배 더 (2 → 2.4배) · 히드라 체력 1.5배
import pprint
S = open('c103.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("    if (b.gem) { b.mesh.remove(b.gem); b.gem = null; }\n    b.r = BODY;", "    // c104: 다이아몬드 표시는 떼지 않는다 (얻은 변이 좀비 표시)\n    b.r = BODY;")
rep("    if (t === 'armor') { b.maxHp *= 2; b.hp = b.maxHp; }   // c100: 얻은 덩치는 체력 2배", "    b.maxHp *= t === 'armor' ? 2 * 1.2 : 1.5; b.hp = b.maxHp;   // c100 · c104: 얻은 덩치는 체력 2.4배 · 얻은 히드라는 1.5배")
open('c104_patch.py', 'w', encoding='utf8').write('# c104: 얻은 변이 좀비 — 다이아몬드 유지 · 덩치 체력 2.4배 · 히드라 1.5배 (gen_c104.py가 만든다)\nC104_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
