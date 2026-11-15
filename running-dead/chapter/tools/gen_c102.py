# c102: 변이 줄기세포 — 체력 100%로 되살아난다 (전엔 30%)
import pprint
S = open('c101.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("  const reviveHp = (n = CHAPTER ? 0 : up.brain) => Math.min(1, 0.3 + 0.1 * n);", "  const reviveHp = (n = up.brain) => CHAPTER ? 1 : Math.min(1, 0.3 + 0.1 * n);   /* c102: 챕터는 체력 가득 */")
rep("    revive: (n) => `체력 30%로 부활 · 쿨타임 ${Math.round(120 * Math.pow(0.9, n))}초`,", "    revive: (n) => `체력 가득으로 부활 · 쿨타임 ${Math.round(120 * Math.pow(0.9, n))}초`,")
open('c102_patch.py', 'w', encoding='utf8').write('# c102: 변이 줄기세포 — 체력 100%로 부활 (gen_c102.py가 만든다)\nC102_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
