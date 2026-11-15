# c83: 건널목을 길게 — 다리·산 길목 자리에서만 강·산이 구역 안쪽으로 파고들고 (맵 크기는 그대로), 순환도로는 그 둘레를 곡선으로 돌아간다.
#   map.json (c82까지의 맵) → map_c83.json   (python3 map_cross.py map.json map_c83.json)
#   · 강: 다리마다 양쪽 구역으로 네모난 만(灣) 두 단 (깊이 6칸 · 3칸) — 다리가 13칸 → 25칸
#   · 산: 길목마다 양쪽 구역으로 산 덩어리 두 단 — 길목이 13칸 → 25칸
#   · 순환도로: 그 자리에서 안쪽으로 6.6칸 부드럽게 휘어 돌아간다 (곡선 구간은 paths 로 따로 적는다). 걸리는 건물·공터는 가장 가까운 빈자리로 옮긴다
#   · 교통망 net: 구역마다 마디·길 (곡선 구간은 짧은 직선 여러 토막)
import json, math, sys
M = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'map.json'))   # map.json = c82까지의 맵
OUT = sys.argv[2] if len(sys.argv) > 2 else 'map_c83.json'
HALF, PW, RW = M['gap'] / 2, M['passW'], M['ring']
ZR0, ZR1 = M['zrMid'] - HALF, M['zrMid'] + HALF          # 산줄기 z 범위
AB, AB2, S1, S2 = 6.0, 3.0, 7.0, 10.0                     # 만·산 덩어리: |s| ≤ 7 은 6칸 깊이, |s| ≤ 10 은 3칸 깊이 (s = 건널목 한가운데에서 둑을 따라 잰 거리)
AR, FR, WR = 6.6, 6.2, 9.0                                # 순환도로: 6.6칸 안쪽으로 · |s| ≤ 6.2 는 다 들어간 채로 · 그 바깥 9칸에 걸쳐 제자리로
SPAN = FR + WR
HW = RW / 2
def bump(s, open_side=0):                                  # 0~1 — open_side: +1 이면 s > 0 쪽은 구역 끝까지 계속 들어가 있다 (구석 다리)
    if open_side and s * open_side > 0: return 1.0
    t = (abs(s) - FR) / WR
    return 1.0 if t <= 0 else 0.0 if t >= 1 else 0.5 * (1 + math.cos(math.pi * t))
Z = M['zones']
# 건널목 끝: zone, side(둑이 어느 쪽 변인가), c(둑을 따라 잰 자리), open(구석 다리면 구역 끝 쪽 ±1), kind
ENDS = []
for a, c in M['passes']:
    if a == 'v':                                           # 다리 — 강 양쪽 구역
        for zi in ((0, 1) if c > M['zrMid'] else (2, 3)):
            z0, z1 = Z[zi][1], Z[zi][3]; op = 1 if z1 - c < SPAN else -1 if c - z0 < SPAN else 0
            ENDS.append(dict(zone=zi, side='E' if zi in (0, 2) else 'W', c=c, open=op, kind='bridge'))
    else:                                                  # 산 길목 — 산 양쪽 구역
        for zi in ((0, 2) if c < 0 else (1, 3)):
            ENDS.append(dict(zone=zi, side='N' if zi in (0, 1) else 'S', c=c, open=0, kind='pass'))
def frame(e):                                              # 그 끝의 좌표틀: 둑 위의 점 P0 (s = 0), 둑 방향 t (s가 느는 쪽), 안쪽 방향 n
    zx0, zz0, zx1, zz1 = Z[e['zone']]
    if e['side'] == 'E': return (zx1, e['c']), (0, 1), (-1, 0)
    if e['side'] == 'W': return (zx0, e['c']), (0, 1), (1, 0)
    if e['side'] == 'N': return (e['c'], zz0), (1, 0), (0, 1)
    return (e['c'], zz1), (1, 0), (0, -1)
def P(e, s, d):
    (px, pz), (tx, tz), (nx, nz) = frame(e)
    return (round(px + tx * s + nx * d, 3), round(pz + tz * s + nz * d, 3))
def rect_sd(e, s0, s1, d0, d1):                            # 그 틀에서 [s0,s1] × [d0,d1] → 맵 네모
    a, b = P(e, s0, d0), P(e, s1, d1)
    return [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
def s_range(e):                                            # 그 변에서 s가 갈 수 있는 범위 (구역 끝까지)
    zx0, zz0, zx1, zz1 = Z[e['zone']]
    return (zz0 - e['c'], zz1 - e['c']) if e['side'] in 'EW' else (zx0 - e['c'], zx1 - e['c'])
EDGE = 3.5
bays, hills_new, decks = [], [], {}
for e in ENDS:
    lo, hi = s_range(e)
    for half, dep in ((S1, AB), (S2, AB2)):
        a, b = max(-half, lo), min(half, hi)
        if e['open'] > 0: b = hi + (EDGE if e['kind'] == 'bridge' else 0)
        if e['open'] < 0: a = lo - (EDGE if e['kind'] == 'bridge' else 0)
        if e['kind'] == 'bridge':                          # 만도 다리 밑(폭 8)은 비운다 — 강 네모가 다리 자리를 비워 두는 것과 같다 (다리 위는 걸어 다닌다)
            bays.append(rect_sd(e, a, -PW / 2, 0, dep)); bays.append(rect_sd(e, PW / 2, b, 0, dep))
        else:                                              # 산 덩어리는 길목(폭 8) 양옆으로 나눈다 — 산 쪽으로 0.6칸 겹쳐 틈이 없게
            hills_new.append(rect_sd(e, a, -PW / 2, -0.6, dep)); hills_new.append(rect_sd(e, PW / 2, b, -0.6, dep))
# 순환도로 가운데 선 (변마다) — 구역 변을 따라 s 를 훑으며 안쪽으로 얼마나 들어가나
def side_line(zi, side):
    zx0, zz0, zx1, zz1 = Z[zi]
    es = [e for e in ENDS if e['zone'] == zi and e['side'] == side]
    if side in 'EW': u0, u1 = zz0 + HW, zz1 - HW           # 그 변의 순환도로가 달리는 범위 (양 끝 = 구석 마디)
    else: u0, u1 = zx0 + HW, zx1 - HW
    def off(u): return max([AR * bump(u - e['c'], e['open']) for e in es] or [0.0])
    def pt(u):
        d = HW + off(u)
        if side == 'E': return (round(zx1 - d, 3), round(u, 3))
        if side == 'W': return (round(zx0 + d, 3), round(u, 3))
        if side == 'N': return (round(u, 3), round(zz0 + d, 3))
        return (round(u, 3), round(zz1 - d, 3))
    return es, u0, u1, off, pt

# ── 대로 (구역을 끝에서 끝까지 가로지르는 길) ──
AVE = {}                                                   # zone → dict(V=(c, hw) | None, H=(c, hw) | None)
for zi, (zx0, zz0, zx1, zz1) in enumerate(Z):
    AVE[zi] = dict(V=None, H=None)
    for a, b, c, d in M['roads']:
        if b <= zz0 + 0.01 and d >= zz1 - 0.01 and a > zx0 + 6 and c < zx1 - 6: AVE[zi]['V'] = ((a + c) / 2, (c - a) / 2)
        if a <= zx0 + 0.01 and c >= zx1 - 0.01 and b > zz0 + 6 and d < zz1 - 6: AVE[zi]['H'] = ((b + d) / 2, (d - b) / 2)
# ── 순환도로 가운데 선: 변마다 점 목록 (구석 → 구석) ──
SIDES = {}
def build_side(zi, side):
    zx0, zz0, zx1, zz1 = Z[zi]
    es, u0, u1, off, pt = side_line(zi, side)
    # 구석: 이웃 변이 그 구석에서 안쪽으로 들어가 있으면 그만큼 일찍 끝난다
    def adj_off(nb, at_u): return side_line(zi, nb)[3](at_u)
    if side in 'NS':
        vz = zz0 + HW if side == 'N' else zz1 - HW
        u0 += adj_off('W', vz); u1 -= adj_off('E', vz)
    else:
        vx = zx0 + HW if side == 'W' else zx1 - HW
        u0 += adj_off('N', vx); u1 -= adj_off('S', vx)
    marks = {round(u0, 3), round(u1, 3)}
    ave = AVE[zi]['V' if side in 'NS' else 'H']
    if ave: marks.add(round(ave[0], 3))
    for e in es:
        for k in range(0, int(SPAN / 1.5) + 1):
            for sg in (-1, 1):
                for uu in (e['c'] + sg * (FR + k * 1.5), e['c'] + sg * SPAN, e['c'] + sg * FR, e['c']):
                    if u0 - 1e-6 <= uu <= u1 + 1e-6: marks.add(round(uu, 3))
    us = sorted(marks)
    # 곧은 구간(안 들어간 곳)의 가운데 점은 필요 없다 — 들어간 정도가 바뀌는 점만 남긴다
    pts = [(u, off(u)) for u in us]
    keep = [pts[0]]
    for i in range(1, len(pts) - 1):
        (ua, oa), (ub, ob), (uc, oc) = keep[-1], pts[i], pts[i + 1]
        flat = abs(oa - ob) < 1e-6 and abs(ob - oc) < 1e-6
        if flat and not (ave and abs(ub - ave[0]) < 1e-6): continue
        keep.append(pts[i])
    keep.append(pts[-1])
    SIDES[(zi, side)] = dict(us=[u for u, o in keep], offs=[o for u, o in keep], pts=[pt(u) for u, o in keep], pt=pt, off=off, u0=u0, u1=u1)
for zi in range(4):
    for side in 'NESW': build_side(zi, side)
# ── 길 네모 · 곡선 구간 ──
roads, paths = [], []
# 건널목 앞에 따로 깔려 있던 넓은 길(16칸)은 없앤다 — 휘어 들어온 순환도로가 그 자리를 지난다
for a, c in M['passes']:
    if a == 'h': roads.append([c - PW / 2, ZR0 - AR - 0.2, c + PW / 2, ZR1 + AR + 0.2])
bridges = [[-(HALF + AB + 1.5), c - PW / 2, HALF + AB + 1.5, c + PW / 2] for a, c in M['passes'] if a == 'v']
for zi, (zx0, zz0, zx1, zz1) in enumerate(Z):
    V, H = AVE[zi]['V'], AVE[zi]['H']
    if V: roads.append([V[0] - V[1], SIDES[(zi, 'N')]['pt'](V[0])[1], V[0] + V[1], SIDES[(zi, 'S')]['pt'](V[0])[1]])
    if H: roads.append([SIDES[(zi, 'W')]['pt'](H[0])[0], H[0] - H[1], SIDES[(zi, 'E')]['pt'](H[0])[0], H[0] + H[1]])
    for side in 'NESW':
        S = SIDES[(zi, side)]; us, offs, pts = S['us'], S['offs'], S['pts']
        i = 0
        while i < len(us) - 1:
            j = i
            if offs[i] < 1e-6 and offs[i + 1] < 1e-6:      # 곧은 구간 → 네모
                while j < len(us) - 1 and offs[j] < 1e-6 and offs[j + 1] < 1e-6: j += 1
                a, b = us[i], us[j]
                if i == 0: a -= HW                          # 구석까지
                if j == len(us) - 1: b += HW
                if side == 'E': roads.append([zx1 - RW, a, zx1, b])
                elif side == 'W': roads.append([zx0, a, zx0 + RW, b])
                elif side == 'N': roads.append([a, zz0, b, zz0 + RW])
                else: roads.append([a, zz1 - RW, b, zz1])
            else:                                          # 휜 구간 → 곡선 (점 목록)
                while j < len(us) - 1 and not (offs[j] < 1e-6 and offs[j + 1] < 1e-6): j += 1
                paths.append(dict(pts=[list(p) for p in pts[i:j + 1]], hw=HW))
            i = j
roads = [[round(v, 2) for v in r] for r in roads]
# ── 교통망: 구역마다 마디·길 ──
NET = []
for zi in range(4):
    nodes, idx, edges = [], {}, []
    def nid(p):
        k = (round(p[0], 2), round(p[1], 2))
        if k not in idx: idx[k] = len(nodes); nodes.append([k[0], k[1]])
        return idx[k]
    def edge(a, b, hw, lane):
        if a != b and not any((x[0] == a and x[1] == b) or (x[0] == b and x[1] == a) for x in edges): edges.append([a, b, hw, lane])
    for side in 'NESW':
        pts = SIDES[(zi, side)]['pts']
        for i in range(len(pts) - 1): edge(nid(pts[i]), nid(pts[i + 1]), HW, HW / 2)
    V, H = AVE[zi]['V'], AVE[zi]['H']
    mid = (V[0], H[0]) if V and H else None
    if V:
        a, b = SIDES[(zi, 'N')]['pt'](V[0]), SIDES[(zi, 'S')]['pt'](V[0]); lane = min(1.3, V[1] / 2)
        if mid: edge(nid(a), nid(mid), V[1], lane); edge(nid(mid), nid(b), V[1], lane)
        else: edge(nid(a), nid(b), V[1], lane)
    if H:
        a, b = SIDES[(zi, 'W')]['pt'](H[0]), SIDES[(zi, 'E')]['pt'](H[0]); lane = min(1.3, H[1] / 2)
        if mid: edge(nid(a), nid(mid), H[1], lane); edge(nid(mid), nid(b), H[1], lane)
        else: edge(nid(a), nid(b), H[1], lane)
    NET.append(dict(nodes=nodes, edges=edges))
print('roads', len(roads), 'paths', len(paths), [len(p['pts']) for p in paths], 'net', [(len(n['nodes']), len(n['edges'])) for n in NET])

# ── 걸리는 건물·공터 옮기기 ──
B = M['b']
top = [i for i, b in enumerate(B) if b['t'] != 'hill' and b.get('parent') is None]
rect = lambda b: (b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)
def rgap(a, b):                                            # 두 네모 사이 거리 (겹치면 음수)
    dx = max(b[0] - a[2], a[0] - b[2], 0); dz = max(b[1] - a[3], a[1] - b[3], 0)
    return math.hypot(dx, dz) if (dx > 0 or dz > 0) else -min(min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1]))
def seg_rect_dist(p, q, r):                                # 선분 pq 와 네모 r 사이 거리 (촘촘히 찍어서)
    n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 0.25) + 1); best = 1e9
    for k in range(n + 1):
        x = p[0] + (q[0] - p[0]) * k / n; z = p[1] + (q[1] - p[1]) * k / n
        dx = max(r[0] - x, 0, x - r[2]); dz = max(r[1] - z, 0, z - r[3]); best = min(best, math.hypot(dx, dz))
    return best
SEGS = [(p['pts'][k], p['pts'][k + 1], p['hw']) for p in paths for k in range(len(p['pts']) - 1)]
water = [list(r) for r in M['rivers']] + bays
hills_all = [list(rect(b)) for b in B if b['t'] == 'hill'] + hills_new
gap0 = {(i, j): rgap(rect(B[i]), rect(B[j])) for i in top for j in top if i < j}
lots = [list(l) for l in M['lots']]
def trouble(r, me, moved_ok=True, lots_too=True):          # 그 네모 자리가 왜 안 되나 (되면 None)
    for q in roads:
        if rgap(r, q) < 0.5 - 1e-6: return 'road'
    for p, q, hw in SEGS:
        if seg_rect_dist(p, q, r) < hw + 0.5: return 'curve'
    for q in water:
        if rgap(r, q) < 0.8: return 'water'
    for q in hills_all:
        if rgap(r, q) < 0.8: return 'hill'
    for q in bridges:
        if rgap(r, q) < 0.5: return 'deck'
    if lots_too:
        for q in lots:
            if rgap(r, q) < 0.8 - 1e-6: return 'lot'
    zx0, zz0, zx1, zz1 = Z[B[me]['zone']]
    if r[0] < zx0 + RW + 0.5 or r[2] > zx1 - RW - 0.5 or r[1] < zz0 + RW + 0.5 or r[3] > zz1 - RW - 0.5: return 'zone'
    for j in top:
        if j == me: continue
        T = min(gap0[(min(me, j), max(me, j))], 2.0)
        if rgap(r, rect(B[j])) < T - 1e-6: return 'bld'
    return None
def shift(i, dx, dz):
    for j, c in enumerate(B):
        if j == i or c.get('parent') == i: c['x'] = round(c['x'] + dx, 2); c['z'] = round(c['z'] + dz, 2)
# 공터부터: 새 길·만·산에 걸리면 걸린 쪽을 잘라 낸다 (남은 넓이가 작으면 없앤다)
def lot_bad(l):                                            # 새로 생긴 것(휜 길·만·산 덩어리·긴 다리)에 걸리나 — 예전부터 순환도로와 겹쳐 있던 건 그대로 둔다
    for p, q, hw in SEGS:
        if seg_rect_dist(p, q, l) < hw + 0.2: return True
    return any(rgap(l, q) < 0.3 for q in bays + hills_new + bridges)
new_lots, lot_log = [], []
for l in lots:
    if not lot_bad(l): new_lots.append(l); continue
    best = None
    for side in range(4):                                  # 한 변을 0.25칸씩 당겨 본다
        c = list(l)
        for k in range(200):
            c[side] += 0.25 if side < 2 else -0.25
            if c[2] - c[0] < 6 or c[3] - c[1] < 6: break
            if not lot_bad(c):
                a = (c[2] - c[0]) * (c[3] - c[1])
                if best is None or a > best[0]: best = (a, [round(v, 2) for v in c])
                break
    if best and best[0] >= 60: new_lots.append(best[1]); lot_log.append(('trim', l, best[1]))
    else: lot_log.append(('drop', l))
lots = new_lots
# 건물: 걸리는 것들을 한꺼번에 들어냈다가, 큰 것부터 가장 가까운 빈자리에 다시 놓는다
bad = [i for i in top if trouble(rect(B[i]), i, lots_too=False)]
print('걸리는 건물', [(B[i]['t'], B[i]['zone'], trouble(rect(B[i]), i, lots_too=False)) for i in bad])
orig = {i: (B[i]['x'], B[i]['z']) for i in bad}
for i in bad: shift(i, 5000 + 40 * i, 0)                   # 잠깐 멀리 치워 둔다
moved, dropped = [], []
for i in sorted(bad, key=lambda i: -B[i]['w'] * B[i]['d']):
    ox, oz = orig[i]; b = B[i]; best = None
    for R in [x * 0.25 for x in range(1, 73)]:              # 가까운 자리부터 (0.25칸 간격, 18칸까지)
        n = max(8, int(2 * math.pi * R / 0.25))
        for k in range(n):
            a = 2 * math.pi * k / n; dx, dz = round(R * math.cos(a) * 4) / 4, round(R * math.sin(a) * 4) / 4
            r = (ox + dx - b['w'] / 2, oz + dz - b['d'] / 2, ox + dx + b['w'] / 2, oz + dz + b['d'] / 2)
            b['x'], b['z'] = ox + dx, oz + dz
            t = trouble(r, i)
            if t is None or (t == 'lot' and trouble(r, i, lots_too=False) is None):
                key = ((6.0 if t == 'lot' else 0.0) + abs(dx) + abs(dz) + (0 if dx == 0 or dz == 0 else 0.3), R)
                if best is None or key < best[0]: best = (key, dx, dz, t)
        if best and (best[3] is None or R >= 10): break
    b['x'], b['z'] = ox + 5000 + 40 * i, oz                # 치워 둔 자리로 되돌린다 (딸린 방은 그대로 거기 있다)
    if best is None:
        if b['t'] == 'house': dropped.append(i); continue
        from collections import Counter
        cn = Counter()
        for dx in range(-72, 73, 2):
            for dz in range(-72, 73, 2):
                r = (ox + dx / 4 - b['w'] / 2, oz + dz / 4 - b['d'] / 2, ox + dx / 4 + b['w'] / 2, oz + dz / 4 + b['d'] / 2); b['x'], b['z'] = ox + dx / 4, oz + dz / 4; cn[trouble(r, i)] += 1
        raise SystemExit('자리 없음: ' + b['t'] + str(orig[i]) + ' ' + str(dict(cn)) + ' size ' + str((b['w'], b['d'])))
    shift(i, ox + best[1] - b['x'], oz + best[2] - b['z']); moved.append((b['t'], b['zone'], best[1], best[2], best[3]))
    if best[3] == 'lot':                                   # 그 건물 자리에 걸친 공터는 건물에서 0.8칸 떨어지게 잘라 낸다
        br = rect(b); nl2 = []
        for l in lots:
            if rgap(br, l) >= 0.8 - 1e-6: nl2.append(l); continue
            cands = [[l[0], l[1], min(l[2], br[0] - 0.8), l[3]], [max(l[0], br[2] + 0.8), l[1], l[2], l[3]], [l[0], l[1], l[2], min(l[3], br[1] - 0.8)], [l[0], max(l[1], br[3] + 0.8), l[2], l[3]]]
            cands = [c for c in cands if c[2] - c[0] >= 6 and c[3] - c[1] >= 6]
            if cands: c = max(cands, key=lambda c: (c[2] - c[0]) * (c[3] - c[1])); nl2.append([round(v, 2) for v in c]); lot_log.append(('trim for ' + b['t'], l, c))
            else: lot_log.append(('drop for ' + b['t'], l))
        lots[:] = nl2
print('옮긴 건물', len(moved)); [print('  ', m) for m in moved]
print('뺀 집', [(B[i]['t'], orig[i]) for i in dropped]); print('공터', lot_log)
if dropped:                                                # 뺀 집과 그 집에 딸린 것 지우기 — 번호(parent · local)를 다시 맞춘다
    gone = set(dropped) | {j for j, c in enumerate(B) if c.get('parent') in dropped}
    remap = {}; nb = []
    for j, c in enumerate(B):
        if j in gone: continue
        remap[j] = len(nb); nb.append(c)
    for c in nb:
        if c.get('parent') is not None: c['parent'] = remap[c['parent']]
    B[:] = nb
for k, c in enumerate(B): c['local'] = k
# 문 앞이 막히지 않았나
NRM = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}
for b in B:
    if b['t'] == 'hill' or b.get('parent') is not None or not b.get('doors'): continue
    nx, nz = NRM[b['doors'][0]]; cx, cz = b['x'] + nx * (b['w'] / 2 + 1.0), b['z'] + nz * (b['d'] / 2 + 1.0)
    pr = (cx - 1.2, cz - 1.2, cx + 1.2, cz + 1.2)
    if any(rgap(pr, q) < 0 for q in water + hills_all): print('  문 앞 막힘', b['t'], b['x'], b['z'], b['doors'][0])
# ── 내보내기 ──
M['roads'] = roads; M['paths'] = paths; M['rivers'] = [[round(v, 2) for v in r] for r in water]; M['bridges'] = [[round(v, 2) for v in r] for r in bridges]
M['lots'] = lots; M['net'] = NET
M['b'] = [c for c in B if c['t'] != 'hill' or True]
nl = len(M['b'])
for k, h in enumerate(hills_new):
    M['b'].append(dict(x=round((h[0] + h[2]) / 2, 2), z=round((h[1] + h[3]) / 2, 2), w=round(h[2] - h[0], 2), d=round(h[3] - h[1], 2), doors=[], locks=[], kinds={}, local=nl + k, block=-1, t='hill', zone=-1))
for P in M['passes2']:                                     # 길목 양 끝 = 새 어귀에서 2.5칸 (순환도로 위)
    P['pin'] = HALF + AB; P['len'] = 2 * (HALF + AB) + 5.0
    if P['axis'] == 'v': P['ax'], P['bx'] = -(HALF + AB + 2.5), HALF + AB + 2.5
    else: P['az'], P['bz'] = ZR1 + AB + 2.5, ZR0 - AB - 2.5
M['cross'] = dict(ab=AB, ar=AR, fr=FR, wr=WR, ends=[[e['zone'], e['side'], e['c'], e['open']] for e in ENDS])   # ends: 건널목 끝마다 [구역, 변(E·W·N·S), 둑을 따라 잰 자리, 구석 다리면 ±1]
M['ave'] = []                                             # 대로: 구역마다 세로(V)·가로(H) — 가운데 선 c · 반폭 hw · 양 끝(순환도로와 만나는 자리) a, b
for zi in range(4):
    V, H = AVE[zi]['V'], AVE[zi]['H']
    M['ave'].append(dict(V=dict(c=V[0], hw=V[1], a=SIDES[(zi, 'N')]['pt'](V[0])[1], b=SIDES[(zi, 'S')]['pt'](V[0])[1]) if V else None,
                         H=dict(c=H[0], hw=H[1], a=SIDES[(zi, 'W')]['pt'](H[0])[0], b=SIDES[(zi, 'E')]['pt'](H[0])[0]) if H else None))
M['curves'] = [[p['pts'][i][0], p['pts'][i][1], p['pts'][i + 1][0], p['pts'][i + 1][1], p['hw']] for p in paths for i in range(len(p['pts']) - 1)]   # 그림용
json.dump(M, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print('wrote', OUT, 'buildings', len(M['b']), 'lots', len(lots))
