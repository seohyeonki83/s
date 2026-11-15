# c107 패치 만들기 — 집을 4분의 1 더 뺀 맵(map_c107.json) · 집 다섯 중 하나는 정문이 처음부터 열려 있다
import json, pprint
S = open('c106.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
old = [l for l in S.split('\n') if l.startswith('  const CH_MAP = ')]; assert len(old) == 1
i = old[0].index('{'); j = old[0].rindex('}')
M = json.load(open('map_c107.json', encoding='utf8'))
R.append((old[0], old[0][:i] + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + old[0][j + 1:]))
rep("  function chRoomDoors() { for (const R of chRooms) if (R.type === 'room') for (const L of R.locks) if (L.out && Math.random() < 0.5) chOpenDoor(L.obj); }",
    "  function chRoomDoors() { for (const R of chRooms) if (R.type === 'room') for (const L of R.locks) if (L.out && Math.random() < 0.5) chOpenDoor(L.obj);\n"
    "    for (const B of buildings) if (B.type === 'house' && !B.garage && !B.gas && !B.parent && Math.random() < 0.2) { const L = B.locks.find((q) => q.front); if (L && L.obj && !L.obj.dead && !L.obj.off) chOpenDoor(L.obj); } }   /* c107: 집 다섯 중 하나는 정문이 열려 있다 (문짝 없음) */")
open('c107_patch.py', 'w', encoding='utf8').write('# c107: 집 15채 맵 · 집 정문 20%는 열려 있다 (gen_c107.py가 만든다)\nC107_R = ' + pprint.pformat(R, width=10**7) + '\n')
print('replacements', len(R))
