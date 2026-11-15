# 작은 맵 s1 패치 만들기 — 큰 맵 최신판(c119) 위에: 맵을 map_s1.json으로 바꾸고, 길거리 사람 수를 구역 몫(6분의 1)으로 줄인다
import json, pprint
S = open('c119.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
old = [l for l in S.split('\n') if l.startswith('  const CH_MAP = ')]; assert len(old) == 1
i = old[0].index('{'); j = old[0].rindex('}')
M = json.load(open('map_s1.json', encoding='utf8'))
R.append((old[0], old[0][:i] + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + old[0][j + 1:]))
rep("  const CH_WHITE = 145, CH_YELLOW = 48, CH_YELLOW_IN = 12, CH_GANG = 48, CH_COPS = 20, CH_ROOM = 45;", "  const CH_WHITE = 145, CH_YELLOW = 48, CH_YELLOW_IN = 12, CH_GANG = 8, CH_COPS = 3, CH_ROOM = 45;   /* s1: 구역 하나 몫 (무리 48 → 8 · 배회 경찰 20 → 3) */")
rep("  const CH_WHITE_OUT = 81, CH_YELLOW_OUT = 36;", "  const CH_WHITE_OUT = 14, CH_YELLOW_OUT = 6;   /* s1: 길거리 하양 81 → 14 · 노랑 36 → 6 */")
rep("    for (let n = 24; n > 0; n--) { let r = Math.random() * ws", "    for (let n = 4; n > 0; n--) { let r = Math.random() * ws")
open('s1_patch.py', 'w', encoding='utf8').write('# s1: 작은 맵 (구역 하나) — gen_s1.py가 만든다\nS1_R = ' + pprint.pformat(R, width=10**7) + '\n')
print('replacements', len(R))
