# 챕터 맵 생성기 — 구역 4개 (큰 구역 2 · 작은 구역 2), 건물만. 씨앗이 같으면 늘 같은 맵 (맵은 외우는 패턴)
import json, random, sys
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rng = random.Random(SEED)
ZW, BIG_H, SMALL_H, GAP = 74.0, 118.0, 59.0, 10.0      # 큰 구역 = 테스트맵 크기, 작은 구역 = 그 절반, 구역 사이 길 10칸
AVE_V, AVE_H, PAD = 6.0, 5.0, 1.5                      # 구역 안 대로 폭 (세로·가로), 블록 안쪽 여백
W, H = ZW * 2 + GAP, SMALL_H + GAP + BIG_H
X0, Z0 = -W / 2, -H / 2
ZONES = [  # 남쪽(z+)에 큰 구역 둘, 북쪽에 작은 구역 둘
    dict(id=0, big=True,  r=(X0, Z0 + SMALL_H + GAP, X0 + ZW, Z0 + H)),
    dict(id=1, big=True,  r=(X0 + ZW + GAP, Z0 + SMALL_H + GAP, X0 + W, Z0 + H)),
    dict(id=2, big=False, r=(X0, Z0, X0 + ZW, Z0 + SMALL_H)),
    dict(id=3, big=False, r=(X0 + ZW + GAP, Z0, X0 + W, Z0 + SMALL_H)),
]
COUNTS = {0: (3, 3, 27), 1: (3, 3, 27), 2: (2, 1, 13), 3: (1, 1, 13)}   # 랜드마크 · 창고 · 집 (합 9 · 8 · 80)
LM = {'bank': (11.0, 8.0), 'police': (11.9, 8.5), 'fire': (12.5, 8.5), 'mart': (13.6, 9.5), 'hospital': (13.6, 10.2),
      'army': (14.0, 10.2), 'library': (11.9, 8.5), 'conv': (8.5, 6.5), 'gym': (10.5, 7.5)}
STORE = (9.4, 6.8)
MIN_GAP = 2.4                                           # 건물 사이 골목 최소 폭

def house():
    w, d = rng.uniform(5.5, 10.0), rng.uniform(4.6, 7.5)
    if rng.random() < 0.2: w, d = max(d, 4.8), w        # 세로로 긴 집
    return ('house', round(w * 2) / 2, round(d * 2) / 2)

def blocks_of(z):
    x0, z0, x1, z1 = z['r']
    cx = (x0 + x1) / 2
    cols = [(x0, cx - AVE_V / 2), (cx + AVE_V / 2, x1)]
    n = 2 if z['big'] else 1                              # 동네를 크게 묶는다 — 블록 하나에 건물 8채쯤 (골목이 생기게)
    bh = ((z1 - z0) - AVE_H * (n - 1)) / n
    rows = [(z0 + i * (bh + AVE_H), z0 + i * (bh + AVE_H) + bh) for i in range(n)]
    roads = [(cx - AVE_V / 2, z0, cx + AVE_V / 2, z1)] + [(x0, rows[i][1], x1, rows[i + 1][0]) for i in range(n - 1)]
    return [(c[0], r[0], c[1], r[1]) for r in rows for c in cols], roads

def pack(block, specs):
    bx0, bz0, bx1, bz1 = block[0] + PAD, block[1] + PAD, block[2] - PAD, block[3] - PAD
    for attempt in range(400):
        order = specs[:]
        rng.shuffle(order)
        order.sort(key=lambda s: -(s[1] * s[2]) if attempt % 2 == 0 else rng.random())   # 큰 것부터 (절반은 아무 순서)
        rows, cur, curw, maxw = [], [], 0.0, (bx1 - bx0) * rng.uniform(0.72, 1.0)   # 동네마다 폭이 다르게
        for s in order:
            g = rng.uniform(MIN_GAP, 3.6) if cur else 0.0
            if cur and curw + g + s[1] > maxw:
                rows.append(cur); cur, curw, g = [], 0.0, 0.0
            cur.append((s, g)); curw += g + s[1]
        if cur: rows.append(cur)
        rng.shuffle(rows)
        gaps = [rng.uniform(MIN_GAP, 3.6) for _ in rows[1:]]
        hs = [max(s[2] for s, _ in r) for r in rows]
        total = sum(hs) + sum(gaps)
        if total > bz1 - bz0: continue
        out, z = [], bz0 + rng.uniform(0, bz1 - bz0 - total)
        for i, r in enumerate(rows):
            roww = sum(g + s[1] for s, g in r)
            x = bx0 + rng.uniform(0, bx1 - bx0 - roww)
            align = rng.choice(['n', 's', 'c'])
            for s, g in r:
                x += g
                dz = 0 if align == 'n' else hs[i] - s[2] if align == 's' else (hs[i] - s[2]) / 2
                out.append(dict(t=s[0], x=x + s[1] / 2, z=z + dz + s[2] / 2, w=s[1], d=s[2]))
                x += s[1]
            z += hs[i] + (gaps[i] if i < len(gaps) else 0)
        return out
    raise SystemExit('pack failed')

types = list(LM); rng.shuffle(types)
bld, roads = [], []
# 구역 사이 길
roads.append((-GAP / 2, Z0, GAP / 2, Z0 + H)); roads.append((X0, Z0 + SMALL_H, X0 + W, Z0 + SMALL_H + GAP))
for z in ZONES:
    nL, nW, nH = COUNTS[z['id']]
    blocks, rds = blocks_of(z); roads += rds
    order = list(range(len(blocks))); rng.shuffle(order)
    load = {i: [] for i in order}
    for k in range(nL): t = types.pop(); load[order[k % len(order)]].append((t,) + LM[t])
    for k in range(nW): load[order[(nL + k) % len(order)]].append(('store',) + STORE)
    for k in range(nH): load[min(order, key=lambda i: (len(load[i]), rng.random()))].append(house())
    for i in order:
        for b in pack(blocks[i], load[i]): b['zone'] = z['id']; bld.append(b)

def clear(b, side):                                    # 그 벽 문 앞이 얼마나 트여 있나
    lim = {'n': b['z'] - b['d'] / 2 - Z0, 's': Z0 + H - (b['z'] + b['d'] / 2), 'w': b['x'] - b['w'] / 2 - X0, 'e': X0 + W - (b['x'] + b['w'] / 2)}[side]
    for o in bld:
        if o is b: continue
        if side in 'ns':
            if abs(o['x'] - b['x']) > o['w'] / 2 + 1.9: continue
            g = (b['z'] - b['d'] / 2) - (o['z'] + o['d'] / 2) if side == 'n' else (o['z'] - o['d'] / 2) - (b['z'] + b['d'] / 2)
        else:
            if abs(o['z'] - b['z']) > o['d'] / 2 + 1.9: continue
            g = (b['x'] - b['w'] / 2) - (o['x'] + o['w'] / 2) if side == 'w' else (o['x'] - o['w'] / 2) - (b['x'] + b['w'] / 2)
        if g >= 0: lim = min(lim, g)
    return lim
for b in bld:
    ok = [s for s in 'nesw' if (b['w'] if s in 'ns' else b['d']) >= 4.6]   # 문 폭 3.4칸이 들어가는 벽만
    front = max(ok, key=lambda s: (clear(b, s), s == 's'))
    cand = [s for s in 'nesw' if s != front]
    side = max(cand, key=lambda s: (clear(b, s) if s in ok else -1))
    b['doors'] = [front]; b['sideK'] = cand.index(side)
    for k in 'xzwd': b[k] = round(b[k], 2)
# 검사
for i, a in enumerate(bld):
    for b in bld[i + 1:]:
        gx = abs(a['x'] - b['x']) - (a['w'] + b['w']) / 2; gz = abs(a['z'] - b['z']) - (a['d'] + b['d']) / 2
        assert max(gx, gz) >= MIN_GAP - 0.02, (a, b)
from collections import Counter
print('건물', len(bld), dict(Counter(b['t'] for b in bld)))
for z in ZONES: print(' 구역', z['id'], '큰' if z['big'] else '작은', dict(Counter(b['t'] for b in bld if b['zone'] == z['id'])))
print(' 정문 방향', dict(Counter(b['doors'][0] for b in bld)), ' 가장 좁은 정문 앞', round(min(clear(b, b['doors'][0]) for b in bld), 2))
A = ZONES[0]['r']
out = dict(seed=SEED, mm=dict(x0=X0 - 3, z0=Z0 - 3, x1=X0 + W + 3, z1=Z0 + H + 3), start=[(A[0] + A[2]) / 2, A[3] - 3],
           zones=[[round(v, 2) for v in z['r']] for z in ZONES], roads=[[round(v, 2) for v in r] for r in roads],
           b=[dict(x=b['x'], z=b['z'], w=b['w'], d=b['d'], doors=b['doors'], kinds={}, local=i, block=-1, t=b['t'], zone=b['zone'], sideK=b['sideK']) for i, b in enumerate(bld)])
json.dump(out, open('map.json', 'w'), ensure_ascii=False, separators=(',', ':'))
# 그림으로 확인
from PIL import Image, ImageDraw
S = 5
im = Image.new('RGB', (int((W + 6) * S), int((H + 6) * S)), (150, 150, 150)); dr = ImageDraw.Draw(im)
P = lambda x, z: ((x - X0 + 3) * S, (z - Z0 + 3) * S)
for r in roads: dr.rectangle([P(r[0], r[1]), P(r[2], r[3])], fill=(120, 120, 120))
COL = {'house': (45, 42, 40), 'store': (125, 110, 90), 'bank': (46, 158, 91), 'police': (59, 111, 212), 'fire': (226, 69, 44), 'mart': (240, 138, 36), 'hospital': (244, 244, 246),
       'army': (91, 107, 47), 'library': (139, 90, 43), 'conv': (24, 166, 166), 'gym': (176, 64, 143)}
for b in bld:
    dr.rectangle([P(b['x'] - b['w'] / 2, b['z'] - b['d'] / 2), P(b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)], fill=COL[b['t']], outline=(0, 0, 0))
    for s, c in [(b['doors'][0], (255, 220, 60)), ([q for q in 'nesw' if q != b['doors'][0]][b['sideK']], (255, 120, 120))]:
        nx, nz = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}[s]
        cx, cz = b['x'] + nx * b['w'] / 2, b['z'] + nz * b['d'] / 2
        dr.line([P(cx - abs(nz) * 1.7, cz - abs(nx) * 1.7), P(cx + abs(nz) * 1.7, cz + abs(nx) * 1.7)], fill=c, width=3)
sx, sz = out['start']; dr.ellipse([P(sx - 1, sz - 1), P(sx + 1, sz + 1)], fill=(60, 110, 255))
im.save('map.png'); print('map.png', im.size)
