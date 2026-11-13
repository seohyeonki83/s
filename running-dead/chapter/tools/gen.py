# 챕터 맵 생성기 — 구역 4개 (큰 구역 2 · 작은 구역 2), 건물만. 씨앗이 같으면 늘 같은 맵 (맵은 외우는 패턴)
import json, random, sys
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rng = random.Random(SEED)
ZW, BIG_H, SMALL_H, GAP = 60.0, 96.0, 48.0, 10.0       # c2: 넓이를 3분의 2로 (한 변 0.816배) — 큰 구역 60×96, 작은 구역은 그 절반. 구역 사이 = 산줄기 10칸
PASS, EDGE = 8.0, 3.5                                   # 산을 넘는 길목 폭, 지도 가장자리 여유 (산은 가장자리 끝까지 막는다)
ZPAD = 2.0
AVE_V, AVE_H, PAD = 6.0, 5.0, 1.5                      # 구역 안 대로 폭 (세로·가로), 블록 안쪽 여백
W, H = ZW * 2 + GAP, SMALL_H + GAP + BIG_H
X0, Z0 = -W / 2, -H / 2
ZONES = [  # 남쪽(z+)에 큰 구역 둘, 북쪽에 작은 구역 둘
    dict(id=0, big=True,  r=(X0, Z0 + SMALL_H + GAP, X0 + ZW, Z0 + H)),
    dict(id=1, big=True,  r=(X0 + ZW + GAP, Z0 + SMALL_H + GAP, X0 + W, Z0 + H)),
    dict(id=2, big=False, r=(X0, Z0, X0 + ZW, Z0 + SMALL_H)),
    dict(id=3, big=False, r=(X0 + ZW + GAP, Z0, X0 + W, Z0 + SMALL_H)),
]
COUNTS = {0: (3, 3, 18), 1: (3, 3, 18), 2: (2, 1, 9), 3: (1, 1, 9)}     # 랜드마크 · 창고 · 집 (합 9 · 8 · 54) — c2: 집 80 → 54
LM = {'bank': (11.0, 8.0), 'police': (11.9, 8.5), 'fire': (12.5, 8.5), 'mart': (13.6, 9.5), 'hospital': (13.6, 10.2),
      'army': (14.0, 10.2), 'library': (11.9, 8.5), 'conv': (8.5, 6.5), 'gym': (10.5, 7.5)}
STORE = (9.4, 6.8)
MIN_GAP = 2.0                                           # 건물 사이 골목 최소 폭 (c5: 덩어리 안은 2.0~2.3칸)

# ── 구역 사이 = 산줄기 (c2). 문 없는 덩어리를 조금씩 겹쳐 이어 붙인다 — 길목(PASS)만 비운다. 길목은 구역마다 1~2곳 ──
ZR0, ZR1 = Z0 + SMALL_H, Z0 + SMALL_H + GAP               # 가로 산줄기가 차지하는 z
BIG_AVE = ZR1 + (BIG_H - AVE_H) / 2 + AVE_H / 2           # 큰 구역 가로 대로 한가운데 z
PASSES = [('v', BIG_AVE), ('v', Z0 + H - 8.0),             # 남서 ↔ 남동: 대로가 만나는 곳 + 남쪽 끝 (2곳) — 앞길이 동네를 가르지 않게 가장자리로
          ('v', Z0 + 8.0),                                 # 북서 ↔ 북동: 북쪽 끝 (1곳)
          ('h', X0 + ZW / 2), ('h', GAP / 2 + ZW / 2)]     # 남서 ↔ 북서, 남동 ↔ 북동: 세로 대로가 지나는 곳 (1곳씩). 'v' = 다리, 'h' = 산 길목
APPROACH = 16.0                                          # c3: 다리·길목 앞은 이만큼 길로 비워 둔다 (건물이 길목을 막지 않게)
RESERVED = []
for a, c in PASSES:
    if a == 'v': RESERVED += [(-GAP / 2 - APPROACH, c - PASS / 2, -GAP / 2, c + PASS / 2), (GAP / 2, c - PASS / 2, GAP / 2 + APPROACH, c + PASS / 2)]
    else: RESERVED += [(c - PASS / 2, ZR0 - APPROACH, c + PASS / 2, ZR0), (c - PASS / 2, ZR1, c + PASS / 2, ZR1 + APPROACH)]

def house():
    w, d = rng.uniform(4.8, 7.4), rng.uniform(3.8, 5.6)   # c4: 집만 한 변을 4분의 1쯤 줄였다 (평균 7.8×6.1 → 6.1×4.7). 문 폭 3.4칸이 들어가게 긴 변은 4.8 이상
    if rng.random() < 0.2: w, d = d, w                  # 세로로 긴 집
    return ('house', round(w * 2) / 2, round(d * 2) / 2)

def blocks_of(z):
    x0, z0, x1, z1 = z['r']
    cx = (x0 + x1) / 2
    cols = [(x0 + ZPAD, cx - AVE_V / 2), (cx + AVE_V / 2, x1 - ZPAD)]   # c2: 구역 가장자리(산·지도 끝)에서 2칸 띄운다
    n = 2 if z['big'] else 1                              # 동네를 크게 묶는다 — 블록 하나에 건물 8채쯤 (골목이 생기게)
    bh = ((z1 - z0) - AVE_H * (n - 1)) / n
    rows = [(z0 + i * (bh + AVE_H) + (ZPAD if i == 0 else 0), z0 + i * (bh + AVE_H) + bh - (ZPAD if i == n - 1 else 0)) for i in range(n)]
    roads = [(cx - AVE_V / 2, z0, cx + AVE_V / 2, z1)] + [(x0, rows[i][1], x1, rows[i + 1][0]) for i in range(n - 1)]
    return [(c[0], r[0], c[1], r[1]) for r in rows for c in cols], roads

def unit_of(specs):                                       # 한 덩어리 — 랜드마크·창고는 혼자, 집은 1~4채를 바짝 붙여서 (c5: 간격 2.0~2.3칸)
    g = lambda: rng.uniform(MIN_GAP, 2.3)
    n = len(specs)
    if n == 1: rects = [(specs[0], 0.0, 0.0)]
    elif n == 4:                                           # 네 채 = 2 × 2
        a, b, c, d = specs
        x2 = max(a[1], c[1]) + g(); z2 = max(a[2], b[2]) + g()
        rects = [(a, rng.uniform(0, max(a[1], c[1]) - a[1]), 0.0), (b, x2, rng.uniform(0, 0.8)), (c, rng.uniform(0, max(a[1], c[1]) - c[1]), z2), (d, x2 + rng.uniform(0, 0.6), z2 + rng.uniform(0, 0.8))]
    else:
        shape = rng.choice(['row', 'col']) if n == 2 else rng.choice(['row', 'col', 'L', 'L'])
        rects, x, z = [], 0.0, 0.0
        if shape == 'row':
            for sp in specs: rects.append((sp, x, rng.uniform(0, 1.2))); x += sp[1] + g()
        elif shape == 'col':
            for sp in specs: rects.append((sp, rng.uniform(0, 1.2), z)); z += sp[2] + g()
        else:                                             # ㄱ자: 둘은 나란히, 하나는 그중 한 채의 아래
            a, b, c = specs
            rects = [(a, 0.0, 0.0), (b, a[1] + g(), rng.uniform(0, 1.0))]
            under = rng.choice([0, 1]); bx = rects[under][1]; bz = max(a[2], b[2] + 1.0) + g()
            rects.append((c, bx + rng.uniform(-0.5, 0.5), bz))
    mx, mz = min(r[1] for r in rects), min(r[2] for r in rects)
    rects = [(sp, x - mx, z - mz) for sp, x, z in rects]
    return dict(rects=rects, W=max(x + sp[1] for sp, x, z in rects), D=max(z + sp[2] for sp, x, z in rects))

LOTS = []
def pack(block, specs):                                  # c5: 블록마다 공터 띠를 먼저 비우고, 덩어리들은 그 위아래에 모아 놓는다
    bx0, bz0, bx1, bz1 = block[0] + PAD, block[1] + PAD, block[2] - PAD, block[3] - PAD
    solo = [sp for sp in specs if sp[0] != 'house']; houses = [sp for sp in specs if sp[0] == 'house']
    hit = lambda r, q, m: r[0] < q[2] + m and r[2] > q[0] - m and r[1] < q[3] + m and r[3] > q[1] - m
    for attempt in range(4000):
        hL = rng.uniform(9.0, 12.5) if attempt < 2000 else rng.uniform(7.5, 9.5)     # 공터 = 블록을 가로지르는 띠
        zL = rng.uniform(bz0 + 6.5, bz1 - 6.5 - hL)
        lot = (block[0] + 0.5, zL, block[2] - 0.5, zL + hL)
        if any(hit(lot, q, 0) for q in RESERVED): continue
        hs = houses[:]; rng.shuffle(hs)
        groups = []
        while hs:                                         # 집을 1 · 2 · 3 · 4채 묶음으로
            k = min(len(hs), rng.choices([1, 2, 3, 4], [0.15, 0.3, 0.3, 0.25])[0]); groups.append(hs[:k]); hs = hs[k:]
        units = [unit_of([sp]) for sp in solo] + [unit_of(gp) for gp in groups]
        if any(u['W'] > bx1 - bx0 or u['D'] > bz1 - bz0 for u in units): continue
        sep = rng.uniform(3.0, 4.2) if attempt < 2500 else rng.uniform(2.5, 3.0)     # 덩어리 사이 (덩어리 안 2.0~2.3보다 넓게)
        placed, ok = [], True
        for u in sorted(units, key=lambda u: -u['W'] * u['D']):
            for t in range(150):
                x, z = rng.uniform(bx0, bx1 - u['W']), rng.uniform(bz0, bz1 - u['D'])
                r = (x, z, x + u['W'], z + u['D'])
                if hit(r, lot, 0.8) or any(hit(r, p, sep) for p in placed) or any(hit(r, q, 1.0) for q in RESERVED): continue
                placed.append(r); u['x'], u['z'] = x, z; break
            else: ok = False; break
        if not ok: continue
        if not any(p[3] < lot[1] for p in placed) or not any(p[1] > lot[3] for p in placed): continue   # 공터 위아래에 다 건물이 있어야 (공터가 동네 한가운데에 놓이게)
        return [dict(t=sp[0], x=u['x'] + x + sp[1] / 2, z=u['z'] + z + sp[2] / 2, w=sp[1], d=sp[2]) for u in units for sp, x, z in u['rects']], lot
    return None

types = list(LM); rng.shuffle(types)
bld, roads = [], list(RESERVED)
hills = []
def ridge(axis, s0, s1):                                 # 줄기 한 토막 [s0, s1] — axis 'v' = 세로 줄기(x가 폭), 'h' = 가로 줄기(z가 폭)
    c0 = -GAP / 2 if axis == 'v' else ZR0
    p, first = s0, True
    while p < s1 - 0.01:
        L = rng.uniform(7, 12)
        if s1 - (p + L) < 5: L = s1 - p                   # 끝에 자투리가 남지 않게
        last = p + L >= s1 - 0.01
        wd = GAP if first or last else rng.uniform(7.5, GAP)   # 길목 옆은 폭을 꽉 채워 깔끔한 절벽으로
        off = rng.uniform(0, GAP - wd)
        a0, a1 = p - (0 if first else 0.8), p + L          # 앞 덩어리와 0.8칸 겹쳐 틈이 없게
        if axis == 'v': hills.append((c0 + off, a0, c0 + off + wd, a1))
        else: hills.append((a0, c0 + off, a1, c0 + off + wd))
        p += L; first = False
def cut(axis, lo, hi):                                   # 그 범위에서 길목 자리를 빼고 토막마다 산
    cs = sorted(c for a, c in PASSES if a == axis and lo < c < hi)
    edges = [lo] + [v for c in cs for v in (c - PASS / 2, c + PASS / 2)] + [hi]
    for i in range(0, len(edges), 2): ridge(axis, edges[i], edges[i + 1])
# c3: 세로 경계 = 강 (지도를 북에서 남으로 가로지른다, 다리로만 건넌다 · 건너편이 보인다), 가로 경계 = 산 (길목으로만 넘는다 · 시야도 막힌다)
rivers, bridges = [], []
vs = sorted(c for a, c in PASSES if a == 'v')
edges = [Z0 - EDGE] + [v for c in vs for v in (c - PASS / 2, c + PASS / 2)] + [Z0 + H + EDGE]
for i in range(0, len(edges), 2): rivers.append((-GAP / 2, edges[i], GAP / 2, edges[i + 1]))
for c in vs: bridges.append((-GAP / 2 - 1.5, c - PASS / 2, GAP / 2 + 1.5, c + PASS / 2))
cut('h', X0 - EDGE, -GAP / 2 + 0.5); cut('h', GAP / 2 - 0.5, X0 + W + EDGE)   # 가로 산줄기: 서쪽 · 동쪽 (강가까지, 반 칸 겹쳐 틈 없이)
for a, c in PASSES:                                      # 산 길목 = 큰 길
    if a == 'h': roads.append((c - PASS / 2, ZR0 - 1, c + PASS / 2, ZR1 + 1))
for z in ZONES:
    nL, nW, nH = COUNTS[z['id']]
    blocks, rds = blocks_of(z); roads += rds
    order = list(range(len(blocks))); rng.shuffle(order)
    base = {i: [] for i in order}
    for k in range(nL): t = types.pop(); base[order[k % len(order)]].append((t,) + LM[t])
    for k in range(nW): base[order[(nL + k) % len(order)]].append(('store',) + STORE)
    for tries in range(200):                               # c4: 집은 블록마다 고르게 나누지 않는다 — 많은 동네와 적은 동네가 생기게
        load = {i: base[i][:] for i in order}
        cap = {i: [8, 6, 3][len(base[i])] for i in order}   # 랜드마크·창고가 든 블록은 집을 적게 (공터 자리를 남긴다)
        for k in range(nH):
            free = [i for i in order if sum(1 for sp in load[i] if sp[0] == 'house') < cap[i]]
            load[rng.choices(free, [1.6 - 0.45 * len(base[i]) for i in free])[0]].append(house())
        res = [pack(blocks[i], load[i]) for i in order]
        if all(r is not None for r in res): break
    else: raise SystemExit('zone pack failed')
    for r, lot in res:
        LOTS.append(lot)
        for b in r: b['zone'] = z['id']; bld.append(b)

def clear(b, side):                                    # 그 벽 문 앞이 얼마나 트여 있나
    lim = {'n': b['z'] - b['d'] / 2 - Z0, 's': Z0 + H - (b['z'] + b['d'] / 2), 'w': b['x'] - b['w'] / 2 - X0, 'e': X0 + W - (b['x'] + b['w'] / 2)}[side]
    for o in bld + HILLS + RIVERS:
        if o is b: continue
        if side in 'ns':
            if abs(o['x'] - b['x']) > o['w'] / 2 + 1.9: continue
            g = (b['z'] - b['d'] / 2) - (o['z'] + o['d'] / 2) if side == 'n' else (o['z'] - o['d'] / 2) - (b['z'] + b['d'] / 2)
        else:
            if abs(o['z'] - b['z']) > o['d'] / 2 + 1.9: continue
            g = (b['x'] - b['w'] / 2) - (o['x'] + o['w'] / 2) if side == 'w' else (o['x'] - o['w'] / 2) - (b['x'] + b['w'] / 2)
        if g >= 0: lim = min(lim, g)
    return lim
RIVERS = [dict(x=(h[0] + h[2]) / 2, z=(h[1] + h[3]) / 2, w=h[2] - h[0], d=h[3] - h[1]) for h in rivers]
HILLS = [dict(x=(h[0] + h[2]) / 2, z=(h[1] + h[3]) / 2, w=h[2] - h[0], d=h[3] - h[1]) for h in hills]   # 문 앞 트임을 잴 때 산도 막힌 것으로 본다
# c5: 집 가운데 몇 채는 차고 — 한쪽 벽이 통째로 뚫려 있고(디귿자), 맞은편에 문 하나. 지붕은 있다
hs_all = [b for b in bld if b['t'] == 'house']
gar = set()
for zid in range(4):
    zh = [b for b in hs_all if b['zone'] == zid]
    for b in rng.sample(zh, max(1, round(len(zh) * 0.15))): gar.add(id(b))
OPP = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
for b in bld:
    ok = [s for s in 'nesw' if (b['w'] if s in 'ns' else b['d']) >= 4.6]   # 문 폭 3.4칸이 들어가는 벽만
    assert len(ok) >= 2, b
    front = max(ok, key=lambda s: (clear(b, s), s == 's'))
    if id(b) in gar:                                    # 가장 트인 쪽이 뚫린 쪽, 그 맞은편이 문
        b['garage'] = True; b['open'] = [front]; b['doors'] = [OPP[front]]; b['locks'] = []; b['sideK'] = None
        continue
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
print(' 차고', sum(1 for b in bld if b.get('garage')), ' 공터', len(LOTS), [round((l[2] - l[0]) * (l[3] - l[1])) for l in LOTS])
print(' 산 덩어리', len(hills), ' 강 토막', len(rivers), ' 다리', len(bridges), ' 산 길목', sum(1 for a, c in PASSES if a == 'h'))
print(' 정문 방향', dict(Counter(b['doors'][0] for b in bld)), ' 가장 좁은 정문 앞', round(min(clear(b, b['doors'][0]) for b in bld), 2))
A = ZONES[0]['r']
out = dict(seed=SEED, mm=dict(x0=X0 - 3, z0=Z0 - 3, x1=X0 + W + 3, z1=Z0 + H + 3), start=[(A[0] + A[2]) / 2, A[3] - 3],
           zones=[[round(v, 2) for v in z['r']] for z in ZONES], roads=[[round(v, 2) for v in r] for r in roads],
           passes=[[a, round(c, 2)] for a, c in PASSES], passPts=[dict(x=0.0 if a == 'v' else round(c, 2), z=round(c, 2) if a == 'v' else round((ZR0 + ZR1) / 2, 2), dir='h' if a == 'v' else 'v') for a, c in PASSES], rivers=[[round(v, 2) for v in r] for r in rivers], bridges=[[round(v, 2) for v in r] for r in bridges],
           lots=[[round(v, 2) for v in l] for l in LOTS],
           b=[dict(dict(x=b['x'], z=b['z'], w=b['w'], d=b['d'], doors=b['doors'], kinds={}, local=i, block=-1, t=b['t'], zone=b['zone']), **(dict(garage=True, open=b['open'], locks=[]) if b.get('garage') else dict(sideK=b['sideK']))) for i, b in enumerate(bld)] +
             [dict(x=round((h[0] + h[2]) / 2, 2), z=round((h[1] + h[3]) / 2, 2), w=round(h[2] - h[0], 2), d=round(h[3] - h[1], 2), doors=[], locks=[], kinds={}, local=len(bld) + i, block=-1, t='hill', zone=-1) for i, h in enumerate(hills)])
json.dump(out, open('map.json', 'w'), ensure_ascii=False, separators=(',', ':'))
# 그림으로 확인
from PIL import Image, ImageDraw
S = 5
im = Image.new('RGB', (int((W + 6) * S), int((H + 6) * S)), (150, 150, 150)); dr = ImageDraw.Draw(im)
P = lambda x, z: ((x - X0 + 3) * S, (z - Z0 + 3) * S)
for l in LOTS: dr.rectangle([P(l[0], l[1]), P(l[2], l[3])], fill=(172, 166, 150))
for r in roads: dr.rectangle([P(r[0], r[1]), P(r[2], r[3])], fill=(120, 120, 120))
for h in hills: dr.rectangle([P(h[0], h[1]), P(h[2], h[3])], fill=(70, 100, 62))
for h in rivers: dr.rectangle([P(h[0], h[1]), P(h[2], h[3])], fill=(60, 120, 170))
for h in bridges: dr.rectangle([P(h[0], h[1]), P(h[2], h[3])], fill=(150, 130, 105))
COL = {'house': (45, 42, 40), 'store': (125, 110, 90), 'bank': (46, 158, 91), 'police': (59, 111, 212), 'fire': (226, 69, 44), 'mart': (240, 138, 36), 'hospital': (244, 244, 246),
       'army': (91, 107, 47), 'library': (139, 90, 43), 'conv': (24, 166, 166), 'gym': (176, 64, 143)}
for b in bld:
    dr.rectangle([P(b['x'] - b['w'] / 2, b['z'] - b['d'] / 2), P(b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)], fill=COL[b['t']], outline=(0, 0, 0))
    marks = [(b['doors'][0], (255, 220, 60), 1.7)] + ([(b['open'][0], (255, 255, 255), (b['w'] if b['open'][0] in 'ns' else b['d']) / 2 - 0.25)] if b.get('garage') else [([q for q in 'nesw' if q != b['doors'][0]][b['sideK']], (255, 120, 120), 1.7)])
    for s, c, hw in marks:
        nx, nz = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}[s]
        cx, cz = b['x'] + nx * b['w'] / 2, b['z'] + nz * b['d'] / 2
        dr.line([P(cx - abs(nz) * hw, cz - abs(nx) * hw), P(cx + abs(nz) * hw, cz + abs(nx) * hw)], fill=c, width=3)
sx, sz = out['start']; dr.ellipse([P(sx - 1, sz - 1), P(sx + 1, sz + 1)], fill=(60, 110, 255))
im.save('map.png'); print('map.png', im.size)
