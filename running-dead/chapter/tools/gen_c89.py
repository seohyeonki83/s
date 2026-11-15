# c89 패치 만들기 — 줄인 맵(map_c89.json: map_shrink.py → map_deco.py)으로 CH_MAP을 바꾼다
import json, pprint
S = open('c88.mjs', encoding='utf8').read()
old = [l for l in S.split('\n') if l.startswith('  const CH_MAP = ')]; assert len(old) == 1
i = old[0].index('{'); j = old[0].rindex('}')
M = json.load(open('map_c89.json', encoding='utf8'))
new = old[0][:i] + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + old[0][j + 1:]
open('c89_patch.py', 'w', encoding='utf8').write('# c89: 맵 넓이 4분의 3 · 집 4분의 1 빼기 · 랜드마크 크기 4분의 3 (gen_c89.py가 만든다)\nC89_R = ' + pprint.pformat([(old[0], new)], width=10**7) + '\n')
print('ok', len(old[0]), len(new), old[0][j + 1:][:60])
