# 챕터 맵 생성기 — 구역 4개 (큰 구역 2 · 작은 구역 2), 건물만. 씨앗이 같으면 늘 같은 맵 (맵은 외우는 패턴)
import json, random, sys
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rng = random.Random(SEED)
ZW, BIG_H, SMALL_H, GAP = 60.0, 96.0, 48.0, 13.0       # c2: 넓이를 3분의 2로 (한 변 0.816배) — 큰 구역 60×96, 작은 구역은 그 절반. 구역 사이 = 산줄기 10칸
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
COUNTS = {0: (3, 3, 18), 1: (3, 3, 18), 2: (2, 1, 9), 3: (1, 1, 9)}     # 랜드마크 · 창고 · 집 (합 9 · 8 · 54) — c2: 집 80 → 54 — c17: 다 놓은 뒤에 집만 3분의 1을 뺀다 (54 → 36, 맨 아래 thin_zone)
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
        return [dict(t=sp[0], x=u['x'] + x + sp[1] / 2, z=u['z'] + z + sp[2] / 2, w=sp[1], d=sp[2], u=ui) for ui, u in enumerate(units) for sp, x, z in u['rects']], lot   # u = 그 블록 안에서 몇 번째 덩어리인가 (집 줄이기에 쓴다)
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
        wd = GAP if first or last else rng.uniform(GAP * 0.75, GAP)   # 길목 옆은 폭을 꽉 채워 깔끔한 절벽으로
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
    for bi, (r, lot) in enumerate(res):
        LOTS.append(lot)
        for b in r: b['zone'] = z['id']; b['unit'] = (z['id'], bi, b.pop('u')); b['_blk'] = blocks[order[bi]]; b['_lot'] = lot; bld.append(b)   # c52: 블록·공터를 적어 둔다 (크기 바꿀 때 쓴다)

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
# c17: 집을 3분의 1 줄인다 (54 → 36). 다 만든 뒤에 집만 골라 빼서 나머지(랜드마크·창고·공터·길, 남는 집의 자리·문·차고)는 그대로 둔다
#   ① 외딴 집(한 채짜리)부터 — 가장 외딴 것부터, 그 블록에 집이 두 채는 남게   ② 네 채짜리 덩어리는 세 채로
#   ③ 그래도 모자라면 집이 가장 많은 블록의 세 채짜리를 통째로, 한두 채만 모자라면 큰 덩어리에서 한 채씩
#   차고는 남는 집의 15%쯤 (구역마다 적어도 하나) 남게 고른다. 덩어리에서 뺄 때는 가장 바깥 집을 뺀다 (남는 집들이 붙어 있게)
HOUSE_CUT = 1 / 3
def thin_zone(zid):
    hs = [b for b in bld if b['zone'] == zid and b['t'] == 'house']
    need = round(len(hs) * HOUSE_CUT); keepG = max(1, round((len(hs) - need) * 0.15))
    gone = set()
    alive = lambda: [b for b in hs if id(b) not in gone]
    dist = lambda a, b: ((a['x'] - b['x']) ** 2 + (a['z'] - b['z']) ** 2) ** 0.5
    def units():
        d = {}
        for b in alive(): d.setdefault(b['unit'], []).append(b)
        return d
    in_block = lambda bi: [b for b in alive() if b['unit'][1] == bi]
    gar_n = lambda: sum(1 for b in alive() if b.get('garage'))
    crowd = lambda b: sum(1 for o in bld if o is not b and id(o) not in gone and dist(o, b) < 14)
    def ok(bs):                                           # 이 집들을 빼도 되나 — 차고 수와 블록에 남는 집 수
        if gar_n() - sum(1 for b in bs if b.get('garage')) < keepG: return False
        for bi in set(b['unit'][1] for b in bs):
            left = len(in_block(bi)) - sum(1 for b in bs if b['unit'][1] == bi)
            if left < min(2, len(in_block(bi))) and left < 2: return False
        return True
    def outer(bs):                                        # 덩어리에서 가장 바깥 집 (차고는 되도록 남긴다)
        c = [b for b in bs if not b.get('garage')] or bs
        return max(c, key=lambda b: (round(sum(dist(b, o) for o in bs if o is not b), 2), crowd(b), b['x'], b['z']))
    def drop(bs):
        nonlocal need
        for b in bs: gone.add(id(b))
        need -= len(bs)
    # ① 외딴 집
    lone = [bs[0] for bs in units().values() if len(bs) == 1]
    iso = lambda b: min([dist(b, o) for o in in_block(b['unit'][1]) if o is not b] or [99])
    for b in sorted(lone, key=lambda b: (-round(iso(b), 2), b['x'], b['z'])):
        if need > 0 and ok([b]): drop([b])
    # ② 네 채 → 세 채
    for u, bs in sorted(units().items()):
        if need > 0 and len(bs) >= 4:
            b = outer(bs)
            if ok([b]): drop([b])
    # ③ 세 채짜리 통째로 (집이 가장 많은 블록부터, 차고가 남는 몫보다 많으면 차고 낀 덩어리부터)
    while need >= 3:
        c = [bs for bs in units().values() if len(bs) == 3 and ok(bs)]
        if not c: break
        over = gar_n() > keepG
        drop(max(c, key=lambda bs: (len(in_block(bs[0]['unit'][1])), any(b.get('garage') for b in bs) == over, sum(crowd(b) for b in bs), bs[0]['x'])))
    while need > 0:                                       # 한두 채 모자라면 큰 덩어리에서 한 채씩
        c = [bs for bs in units().values() if len(bs) >= 2 and ok([outer(bs)])]
        if not c: break
        drop([outer(max(c, key=lambda bs: (len(bs), len(in_block(bs[0]['unit'][1])), bs[0]['x'])))])
    assert need == 0, (zid, need)
    return gone
_gone = set()
for zid in range(4): _gone |= thin_zone(zid)
CUT = [b for b in bld if id(b) in _gone]
bld[:] = [b for b in bld if id(b) not in _gone]
# c52: 랜드마크 크기만 바꾼다 (넓이 기준) — 마트 = 전의 1.2배 · 헬스장·은행·병원·소방서·경찰서·군부대 = 마트의 3분의 2 · 도서관 = 그 90% · 편의점·창고·집은 그대로
#   맵을 새로 뽑지 않는다: 위에서 옛 크기로 똑같이 만든 뒤 (난수 흐름 그대로 = 건물 자리·집·공터·길이 전부 그대로) 여기서 크기만 바꾼다.
#   정문이 난 벽은 제자리에 두고 뒤쪽으로만 커지거나 줄어든다 (정문 자리 그대로 — 가운데 기준으로 키우면 마트 정문이 시작 자리의 인지거리 7.2 안으로 들어와서, 시작하자마자 내가 문을 때리러 간다).
#   옆으로는 가운데 기준. 그 자리가 이웃·공터·길목·블록 가장자리와 너무 붙으면 가장 조금만 옮긴다. 정문·쪽문 방향도 그대로
LM2 = {'mart': (14.9, 10.4), 'gym': (12.0, 8.6), 'bank': (12.0, 8.6), 'hospital': (12.0, 8.6), 'fire': (12.0, 8.6), 'police': (12.0, 8.6), 'army': (12.0, 8.6), 'library': (11.4, 8.15)}
RESIZED = []
def resize(b):
    w, d = LM2[b['t']]
    blk, lot, E = b['_blk'], b['_lot'], 0.011
    f = b['doors'][0]                                    # 정문 벽은 제자리
    px = b['x'] + (b['w'] - w) / 2 if f == 'e' else b['x'] - (b['w'] - w) / 2 if f == 'w' else b['x']
    pz = b['z'] + (b['d'] - d) / 2 if f == 's' else b['z'] - (b['d'] - d) / 2 if f == 'n' else b['z']
    hit = lambda r, q, m: r[0] < q[2] + m and r[2] > q[0] - m and r[1] < q[3] + m and r[3] > q[1] - m
    others = [(o['x'] - o['w'] / 2, o['z'] - o['d'] / 2, o['x'] + o['w'] / 2, o['z'] + o['d'] / 2) for o in bld if o is not b]
    def ok(x, z, gap, pad):
        r = (x - w / 2, z - d / 2, x + w / 2, z + d / 2)
        if r[0] < blk[0] + pad - E or r[2] > blk[2] - pad + E or r[1] < blk[1] + pad - E or r[3] > blk[3] - pad + E: return False
        if hit(r, lot, 0.8 - E) or any(hit(r, q, 1.0 - E) for q in RESERVED): return False
        return not any(hit(r, o, gap - E) for o in others)
    for gap, pad in [(2.5, 1.5), (2.0, 1.5), (2.0, 1.0)]:
        best = None
        for i in range(-40, 41):
            for j in range(-40, 41):
                dx, dz = i * 0.1, j * 0.1
                if ok(px + dx, pz + dz, gap, pad):
                    k = (round(dx * dx + dz * dz, 4), abs(i) + abs(j), i, j)
                    if best is None or k < best[0]: best = (k, dx, dz)
        if best: break
    else: raise SystemExit('resize failed: ' + b['t'])
    RESIZED.append((b['t'], b['w'], b['d'], w, d, round(best[1], 1), round(best[2], 1), gap, pad))
    b['x'], b['z'], b['w'], b['d'] = round(px + best[1], 2), round(pz + best[2], 2), w, d
for b in bld:
    if b['t'] in LM2: resize(b)
for i, a in enumerate(bld):                              # 다시 검사
    for b in bld[i + 1:]:
        gx = abs(a['x'] - b['x']) - (a['w'] + b['w']) / 2; gz = abs(a['z'] - b['z']) - (a['d'] + b['d']) / 2
        assert max(gx, gz) >= MIN_GAP - 0.02, (a, b)
# c53: 건물 안 방 — 마트(창고 방 1 + 바깥으로 난 작은 쪽문) · 병원(방 2, 붙여서) · 군부대(작은 방 1 + 쪽문) · 경찰서(철창 1, 벽 너머가 보인다)
#   방은 건물 구석(병원은 문 없는 벽 한가운데)에 붙인다. 건물 정문·쪽문과 그 안쪽 길(2.4칸)은 비운다.
#   방문 = 방 안쪽 벽 한가운데 (폭 2.0) · 바깥 쪽문 = 방의 바깥벽 한가운데 (폭 1.5, 문 앞이 가장 트인 쪽) · 철창은 정문에서 가장 먼 구석
#   난수는 따로 쓴다 (맵의 나머지는 그대로)
ROOM_SPEC = {'mart': dict(n=1, size=(5.0, 3.0), ext=True, kind='room'), 'hospital': dict(n=2, size=(3.0, 3.0), ext=False, kind='room'),
             'army': dict(n=1, size=(3.6, 3.2), ext=True, kind='room'), 'police': dict(n=1, size=(3.6, 3.2), ext=False, kind='jail')}
IN_W, EXT_W = 2.0, 1.5
NRM = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}
rr = random.Random(SEED * 1000 + 53)
b_rect = lambda b: (b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)
b_doors = lambda b: [b['doors'][0], [q for q in 'nesw' if q != b['doors'][0]][b['sideK']]]
def side_mid(r, sd):                                      # 그 벽의 한가운데와 반 길이
    x0, z0, x1, z1 = r
    return {'n': ((x0 + x1) / 2, z0, (x1 - x0) / 2), 's': ((x0 + x1) / 2, z1, (x1 - x0) / 2), 'w': (x0, (z0 + z1) / 2, (z1 - z0) / 2), 'e': (x1, (z0 + z1) / 2, (z1 - z0) / 2)}[sd]
ovl = lambda q, o, m=0.0: q[0] < o[2] + m - 1e-6 and q[2] > o[0] - m + 1e-6 and q[1] < o[3] + m - 1e-6 and q[3] > o[1] - m + 1e-6
def corridors(b):                                         # 건물 문과 그 안쪽 길 — 방이 걸치면 안 된다
    R, out = b_rect(b), []
    for sd in b_doors(b):
        cx, cz, _ = side_mid(R, sd); nx, nz = NRM[sd]
        out.append((cx - 2.2, min(cz, cz - nz * 2.4), cx + 2.2, max(cz, cz - nz * 2.4)) if nx == 0 else (min(cx, cx - nx * 2.4), cz - 2.2, max(cx, cx - nx * 2.4), cz + 2.2))
    return out
def out_clear(b, cx, cz, sd, half=1.2, maxd=8.0):         # 그 문 앞 바깥이 얼마나 트였나
    nx, nz = NRM[sd]; best = maxd
    for o in [b_rect(o) for o in bld if o is not b] + list(hills) + list(rivers):
        if nx == 0:
            if o[2] < cx - half or o[0] > cx + half: continue
            g = (cz - o[3]) if nz < 0 else (o[1] - cz)
        else:
            if o[3] < cz - half or o[1] > cz + half: continue
            g = (cx - o[2]) if nx < 0 else (o[0] - cx)
        if g >= -1e-6: best = min(best, g)
    return min(best, {'n': cz - Z0, 's': Z0 + H - cz, 'w': cx - X0, 'e': X0 + W - cx}[sd] + 3.0)   # 지도는 구역 끝에서 3칸 더 나간다
def room_doors(b, q, sibs, ext):                          # 방문(안쪽) · 쪽문(바깥) 자리 — 못 놓으면 None
    R = b_rect(b); inner, outer = [], []
    for sd in 'nesw':
        cx, cz, hl = side_mid(q, sd); nx, nz = NRM[sd]
        on_wall = abs({'n': q[1] - R[1], 's': q[3] - R[3], 'w': q[0] - R[0], 'e': q[2] - R[2]}[sd]) < 1e-6
        if on_wall:
            if not ext or hl * 2 < EXT_W + 0.8: continue
            if sd in b_doors(b):                           # 그 벽에 건물 문이 있으면 1칸 넘게 떨어져야
                mx, mz, _ = side_mid(R, sd)
                if abs((cx - mx) if nx == 0 else (cz - mz)) < 1.7 + EXT_W / 2 + 1.0: continue
            outer.append((sd not in b_doors(b), min(out_clear(b, cx, cz, sd), 6.0), sd))   # 건물 문이 없는 벽이 먼저, 그다음 문 앞이 트인 쪽
        else:
            if hl * 2 < IN_W + 0.8: continue
            fx, fz = cx + nx * 1.0, cz + nz * 1.0          # 문 앞 (복도 쪽)
            if not (R[0] + 0.6 < fx < R[2] - 0.6 and R[1] + 0.6 < fz < R[3] - 0.6): continue
            if any(o[0] - 0.3 < fx < o[2] + 0.3 and o[1] - 0.3 < fz < o[3] + 0.3 for o in sibs): continue
            inner.append((hl, (b['x'] - cx) * nx + (b['z'] - cz) * nz, sd))
    if not inner or (ext and not outer): return None
    ins = max(inner)[2]; res = [dict(s=ins, w=IN_W, ext=False)]; clr = None
    if ext:
        best = max(outer); clr = best[1]
        if clr < 2.5: return None                          # 쪽문 앞이 막혀 있다
        res.append(dict(s=best[2], w=EXT_W, ext=True))
    return res, clr
ROOMS = []
for bi, b in enumerate(bld):
    sp = ROOM_SPEC.get(b['t'])
    if not sp: continue
    R, cors, cands = b_rect(b), corridors(b), []
    a, d = sp['size']
    if sp['n'] == 1:                                       # 구석 방 — 네 구석 × 두 방향
        for (w_, d_) in ((a, d), (d, a)):
            for cx_, cz_ in ((R[0], R[1]), (R[2] - w_, R[1]), (R[0], R[3] - d_), (R[2] - w_, R[3] - d_)):
                cands.append([(cx_, cz_, cx_ + w_, cz_ + d_)])
    else:                                                  # 방 둘 — 한 벽 한가운데에 나란히
        for sd in 'nswe':
            if sd in 'ns':
                x0 = b['x'] - a; z0 = R[1] if sd == 'n' else R[3] - d
                cands.append([(x0, z0, x0 + a, z0 + d), (x0 + a, z0, x0 + 2 * a, z0 + d)])
            else:
                z0 = b['z'] - a; x0 = R[0] if sd == 'w' else R[2] - d
                cands.append([(x0, z0, x0 + d, z0 + a), (x0, z0 + a, x0 + d, z0 + 2 * a)])
    good = []
    for qs in cands:
        if any(q[0] < R[0] - 1e-6 or q[2] > R[2] + 1e-6 or q[1] < R[1] - 1e-6 or q[3] > R[3] + 1e-6 for q in qs): continue
        if any(ovl(q, c) for q in qs for c in cors): continue
        ds = [room_doors(b, q, [o for o in qs if o is not q], sp['ext']) for q in qs]
        if any(x is None for x in ds): continue
        fx, fz, _ = side_mid(R, b['doors'][0])              # 정문에서 방까지
        far = min(((q[0] + q[2]) / 2 - fx) ** 2 + ((q[1] + q[3]) / 2 - fz) ** 2 for q in qs) ** 0.5
        clr = min([x[1] for x in ds if x[1] is not None] or [0])
        good.append(((round(min(clr, 6.0), 1), round(far, 1)) if sp['ext'] else (round(far, 1), 0), rr.random(), qs, ds))
    assert good, ('방 자리 없음', b['t'])
    _, _, qs, ds = max(good, key=lambda g: (g[0], g[1]))
    for q, (doors, clr) in zip(qs, ds):
        ROOMS.append(dict(t=sp['kind'], x=round((q[0] + q[2]) / 2, 2), z=round((q[1] + q[3]) / 2, 2), w=round(q[2] - q[0], 2), d=round(q[3] - q[1], 2), parent=bi, zone=b['zone'], doors=[x['s'] for x in doors], rdoors=doors, clr=clr, pt=b['t']))
from collections import Counter
print('방', [(r['pt'], r['t'], (r['x'], r['z']), (r['w'], r['d']), [(x['s'], x['w'], 'ext' if x['ext'] else 'in') for x in r['rdoors']], '쪽문 앞 트임 %s' % r['clr']) for r in ROOMS])
print('크기 바꿈 (종류, 옛 가로·세로, 새 가로·세로, 옮긴 x·z, 이웃 간격, 블록 여백)')
for r in RESIZED: print('  ', r)
print('건물', len(bld), dict(Counter(b['t'] for b in bld)))
for z in ZONES: print(' 구역', z['id'], '큰' if z['big'] else '작은', dict(Counter(b['t'] for b in bld if b['zone'] == z['id'])))
print(' 차고', sum(1 for b in bld if b.get('garage')), ' 공터', len(LOTS), [round((l[2] - l[0]) * (l[3] - l[1])) for l in LOTS])
print(' 뺀 집', len(CUT), [(b['zone'], round(b['x']), round(b['z']), 'G' if b.get('garage') else '') for b in CUT])
print(' 산 덩어리', len(hills), ' 강 토막', len(rivers), ' 다리', len(bridges), ' 산 길목', sum(1 for a, c in PASSES if a == 'h'))
def door_gap(b, side, x, z):                             # (x, z)에서 그 벽 문(폭 3.4, 벽 한가운데)까지
    nx, nz = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}[side]
    cx, cz = b['x'] + nx * b['w'] / 2, b['z'] + nz * b['d'] / 2
    if nx: return ((x - cx) ** 2 + max(0, abs(z - cz) - 1.7) ** 2) ** 0.5
    return (max(0, abs(x - cx) - 1.7) ** 2 + (z - cz) ** 2) ** 0.5
_A = ZONES[0]['r']; _sx, _sz = (_A[0] + _A[2]) / 2, _A[3] - 3
_dg = []
for b in bld:
    sides = b['doors'] + ([] if b.get('garage') else [[q for q in 'nesw' if q != b['doors'][0]][b['sideK']]])
    for sd in sides: _dg.append((round(door_gap(b, sd, _sx, _sz), 2), b['t'], sd))
print(' 시작 자리에서 가장 가까운 문', sorted(_dg)[:3], '(내 인지거리 7.2 밖이어야 한다)')
assert min(_dg)[0] > 7.2, min(_dg)
print(' 정문 방향', dict(Counter(b['doors'][0] for b in bld)), ' 가장 좁은 정문 앞', round(min(clear(b, b['doors'][0]) for b in bld), 2))
A = ZONES[0]['r']
out = dict(seed=SEED, mm=dict(x0=X0 - 3, z0=Z0 - 3, x1=X0 + W + 3, z1=Z0 + H + 3), start=[(A[0] + A[2]) / 2, A[3] - 3],
           zones=[[round(v, 2) for v in z['r']] for z in ZONES], roads=[[round(v, 2) for v in r] for r in roads],
           passes=[[a, round(c, 2)] for a, c in PASSES], gap=GAP, passW=PASS, zrMid=round((ZR0 + ZR1) / 2, 2),
           passes2=[dict(axis=a, c=round(c, 2), len=GAP + 5.0,
                         **(dict(ax=-GAP / 2 - 2.5, az=round(c, 2), bx=GAP / 2 + 2.5, bz=round(c, 2), za=0 if c > (ZR0 + ZR1) / 2 else 2, zb=1 if c > (ZR0 + ZR1) / 2 else 3) if a == 'v' else
                            dict(ax=round(c, 2), az=ZR1 + 2.5, bx=round(c, 2), bz=ZR0 - 2.5, za=0 if c < 0 else 1, zb=2 if c < 0 else 3))) for a, c in PASSES],   # 먼 길 찾기용 — 길목의 양 끝과 이어진 두 구역 (구역 0 남서 · 1 남동 · 2 북서 · 3 북동)
           passPts=[dict(x=0.0 if a == 'v' else round(c, 2), z=round(c, 2) if a == 'v' else round((ZR0 + ZR1) / 2, 2), dir='h' if a == 'v' else 'v') for a, c in PASSES], rivers=[[round(v, 2) for v in r] for r in rivers], bridges=[[round(v, 2) for v in r] for r in bridges],
           lots=[[round(v, 2) for v in l] for l in LOTS],
           b=[dict(dict(x=b['x'], z=b['z'], w=b['w'], d=b['d'], doors=b['doors'], kinds={}, local=i, block=-1, t=b['t'], zone=b['zone']), **(dict(garage=True, open=b['open'], locks=[]) if b.get('garage') else dict(sideK=b['sideK']))) for i, b in enumerate(bld)] +
             [dict(x=round((h[0] + h[2]) / 2, 2), z=round((h[1] + h[3]) / 2, 2), w=round(h[2] - h[0], 2), d=round(h[3] - h[1], 2), doors=[], locks=[], kinds={}, local=len(bld) + i, block=-1, t='hill', zone=-1) for i, h in enumerate(hills)] +
             [dict(x=r['x'], z=r['z'], w=r['w'], d=r['d'], doors=r['doors'], locks=[], kinds={}, local=len(bld) + len(hills) + i, block=-1, t=r['t'], zone=r['zone'], parent=r['parent'], room=dict(doors=r['rdoors'])) for i, r in enumerate(ROOMS)])   # c53: 방 (건물 안의 작은 건물)
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
for r in ROOMS:
    dr.rectangle([P(r['x'] - r['w'] / 2, r['z'] - r['d'] / 2), P(r['x'] + r['w'] / 2, r['z'] + r['d'] / 2)], outline=(255, 255, 255))
    for x in r['rdoors']:
        nx, nz = NRM[x['s']]; cx, cz = r['x'] + nx * r['w'] / 2, r['z'] + nz * r['d'] / 2; hw = x['w'] / 2
        dr.line([P(cx - abs(nz) * hw, cz - abs(nx) * hw), P(cx + abs(nz) * hw, cz + abs(nx) * hw)], fill=(80, 255, 255) if x['ext'] else (255, 80, 255), width=3)
sx, sz = out['start']; dr.ellipse([P(sx - 1, sz - 1), P(sx + 1, sz + 1)], fill=(60, 110, 255))
im.save('map.png'); print('map.png', im.size)
