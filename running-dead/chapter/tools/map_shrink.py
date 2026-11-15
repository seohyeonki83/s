# c89: 맵을 넓이 4분의 3으로 줄이고 집을 4분의 1 줄인다 — map_c83.json → map_c89_base.json (그 다음 map_deco.py가 꾸민다)
#   · 길·강·다리·산길(건널목)은 폭과 길이를 그대로 두고, 그 사이의 '블록'만 줄인다 (x·z 따로, 구간별 직선 변환)
#   · 건물은 크기를 그대로 두고 자리만 옮긴다 (길에 가까운 쪽 변을 기준으로). 겹치면 조금씩 밀고, 안 되면 집을 뺀다
import json, math, random, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'map_c83.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'map_c89_base.json'
M = json.load(open(SRC)); rnd = random.Random(89)
ZK = 0.85                                                 # 구역 한 변을 이만큼으로 (넓이 0.72 — 강·산은 그대로라 맵 전체는 약 0.75)
# 줄이는 구간 [a, b] (나머지는 그대로). x는 좌우 대칭이라 |x|로 본다
XC = [(15.35, 32.5), (40.5, 62.0)]
ZB = [(-8.65, 26.5), (34.5, 66.5)]                         # 큰 구역 (위)
ZS = [(-66.5, -39.35)]                                     # 작은 구역 (아래)
kx = 1 - 60 * (1 - ZK) / sum(b - a for a, b in XC)
kb = 1 - 96 * (1 - ZK) / sum(b - a for a, b in ZB)
ks = 1 - 48 * (1 - ZK) / sum(b - a for a, b in ZS)
def pw(v, segs, k):                                       # v ≥ 기준점 쪽으로 가면서 줄이는 구간을 k배로
    out = v
    for a, b in segs:
        if v > a: out -= (min(v, b) - a) * (1 - k)
    return out
def fx(x): return math.copysign(pw(abs(x), XC, kx), x)
def fz(z):
    if z >= -8.65: return pw(z, ZB, kb)
    if z <= -39.35: return -pw(-z, [(-b, -a) for a, b in ZS], ks)
    return z
def edge_d(v, segs):                                      # 가장 가까운 '그대로인 띠'까지 거리 (줄이는 구간 안에서)
    for a, b in segs:
        if a <= v <= b: return min(v - a, b - v)
    return 0
XS = XC + [(-b, -a) for a, b in XC]; ZSEG = ZB + ZS
def rigid(a, b, f, segs):                                 # 길이를 지키는 구간 [a, b] — 길(띠)에 가까운 쪽 끝을 기준으로 옮긴다
    L = b - a
    if edge_d(a, segs) <= edge_d(b, segs): n = f(a); return n, n + L
    n = f(b); return n - L, n
def P(x, z): return [round(fx(x), 3), round(fz(z), 3)]
def RP(r): return [round(fx(r[0]), 3), round(fz(r[1]), 3), round(fx(r[2]), 3), round(fz(r[3]), 3)]
def RR(r):
    x0, x1 = rigid(r[0], r[2], fx, XS); z0, z1 = rigid(r[1], r[3], fz, ZSEG); return [round(x0, 3), round(z0, 3), round(x1, 3), round(z1, 3)]
rect = lambda b: [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]

# ── 꾸밈 자리 (map_deco.py의 옛 자리) — 주유소·농구장·공사 현장은 크기 그대로, 공원은 블록과 같이 줄어든다 ──
OLD = dict(gas=[[-50.5, 33.6, -40.0, 44.1], [23.3, 17.8, 33.0, 27.5]], park=[[-61.5, 8.4, -40.5, 17.8], [41.0, 3.6, 61.5, 13.6]], court=[[18.5, -65.6, 28.5, -56.2]],
           site=[[-32.5, 48.7, -23.2, 56.9], [24.2, 47.4, 32.5, 55.5], [-50.0, -56.5, -40.5, -47.3], [52.0, -61.2, 61.5, -55.6]])
AREAS = {k: [(RP(r) if k == 'park' else RR(r)) for r in v] for k, v in OLD.items()}
GAS_HOUSES = [(-46.66, 37.26), (26.83, 17.95), (27.95, 24.2)]   # 주유소 자리의 집 (map_deco.py가 치운다) — 빼거나 옮기지 않는다

# ── 땅 ──
for k in ('zones', 'roads', 'rivers', 'bridges', 'lots'): M[k] = [RP(r) for r in M[k]]
mm = M['mm']; M['mm'] = dict(x0=fx(mm['x0']), z0=round(fz(mm['z0']), 3), x1=fx(mm['x1']), z1=round(fz(mm['z1']), 3))
M['start'] = P(*M['start']); M['zrMid'] = fz(M['zrMid'])
M['passes'] = [[a, round(fz(c) if a == 'v' else fx(c), 3)] for a, c in M['passes']]
for p in M['passes2']:
    p['ax'], p['az'] = P(p['ax'], p['az']); p['bx'], p['bz'] = P(p['bx'], p['bz']); p['c'] = round(fz(p['c']) if p['axis'] == 'v' else fx(p['c']), 3)
for p in M['passPts']: p['x'], p['z'] = P(p['x'], p['z'])
for p in M['paths']: p['pts'] = [P(*q) for q in p['pts']]
M['curves'] = [P(c[0], c[1]) + P(c[2], c[3]) + c[4:] for c in M['curves']]
for N in M['net']: N['nodes'] = [P(*n[:2]) + n[2:] for n in N['nodes']]
for A in M['ave']:
    V, H = A['V'], A['H']
    if V: V['c'] = round(fx(V['c']), 3); V['a'] = round(fz(V['a']), 3); V['b'] = round(fz(V['b']), 3)
    if H: H['c'] = round(fz(H['c']), 3); H['a'] = round(fx(H['a']), 3); H['b'] = round(fx(H['b']), 3)
M['cross']['ends'] = [[zi, sd, round(fz(c) if sd in 'EW' else fx(c), 3), o] for zi, sd, c, o in M['cross']['ends']]

# ── 건물 ──
B = M['b']; TR = []
AK = math.sqrt(0.85)                                      # c95: 모든 건물 넓이를 15% 더 줄인다 (한 변 0.922배. 랜드마크·방 포함, 주유소 사무실만 그대로)
HK = math.sqrt(0.8)                                       # c93: 집은 넓이 80% (한 변 0.894배) — 차고·주유소 사무실은 그대로. 한 변이 4.4칸보다 짧아지지는 않게 (문 폭 3.4칸)
for b in B:
    if b['t'] == 'house' and not b.get('garage') and not any(abs(b['x'] - x) < 0.6 and abs(b['z'] - z) < 0.6 for x, z in GAS_HOUSES) and not any(c.get('parent') == B.index(b) for c in B):
        b['w'] = round(max(min(b['w'], 3.6), b['w'] * HK * AK), 2); b['d'] = round(max(min(b['d'], 3.6), b['d'] * HK * AK), 2)
    elif b['t'] in ('store', 'conv') or b.get('garage'):   # c95: 창고·편의점·차고도 15%
        b['w'] = round(max(min(b['w'], 3.6), b['w'] * AK), 2); b['d'] = round(max(min(b['d'], 3.6), b['d'] * AK), 2)
LK = math.sqrt(0.75)                                    # 랜드마크(창고·집·편의점 빼고)는 넓이를 4분의 3으로 — 한 변 0.866배. 방은 크기 그대로, 붙어 있던 벽에 그대로 붙인다
for i, b in enumerate(B):
    if b['t'] not in ('army', 'fire', 'mart', 'gym', 'bank', 'hospital', 'library', 'police'): continue
    ow, od = b['w'], b['d']; b['w'], b['d'] = round(ow * LK * AK, 2), round(od * LK * AK, 2)
    for c in B:
        if c.get('parent') != i: continue
        cw, cd = c['w'], c['d']; c['w'], c['d'] = round(cw * AK, 2), round(cd * AK, 2)   # 방도 15% (벽에 붙은 쪽은 그대로 붙게 가운데를 옮긴다)
        for ax, o_, n_ in (('x', cw, c['w']), ('z', cd, c['d'])):
            lo, hi = c[ax] - o_ / 2, c[ax] + o_ / 2; pc, ph = b[ax], (ow if ax == 'x' else od) / 2
            if abs(lo - (pc - ph)) < 0.06: c[ax] = round(lo + n_ / 2, 2)
            elif abs(hi - (pc + ph)) < 0.06: c[ax] = round(hi - n_ / 2, 2)
        for ax, sz, o, n in (('x', 'w', ow, b['w']), ('z', 'd', od, b['d'])):
            c0, c1 = c[ax] - c[sz] / 2, c[ax] + c[sz] / 2
            if abs(c0 - (b[ax] - o / 2)) < 0.06: c[ax] = round(b[ax] - n / 2 + c[sz] / 2, 2)
            elif abs(c1 - (b[ax] + o / 2)) < 0.06: c[ax] = round(b[ax] + n / 2 - c[sz] / 2, 2)
            else: c[ax] = round(b[ax] + (c[ax] - b[ax]) * LK, 2)
for i, b in enumerate(B):
    if b['t'] == 'hill': r = RP(rect(b)); b['x'], b['z'], b['w'], b['d'] = round((r[0] + r[2]) / 2, 3), round((r[1] + r[3]) / 2, 3), round(r[2] - r[0], 3), round(r[3] - r[1], 3)
for i, b in enumerate(B):
    if b['t'] == 'hill' or 'parent' in b: continue
    ox, oz = b['x'], b['z']; r = RR(rect(b)); b['x'], b['z'] = round((r[0] + r[2]) / 2, 2), round((r[1] + r[3]) / 2, 2); b['_o'] = (ox, oz)
top = [b for b in B if b['t'] != 'hill' and 'parent' not in b]
for b in top: b['_g'] = any(abs(b['_o'][0] - x) < 0.6 and abs(b['_o'][1] - z) < 0.6 for x, z in GAS_HOUSES)
isgas = lambda b: b['_g']
hills = [rect(b) for b in B if b['t'] == 'hill']; arects = AREAS['gas'] + AREAS['park']                    # 건물을 놓을 때 피할 자리 (공사 현장·농구장은 건물을 다 놓은 뒤 빈 데를 찾아 놓는다)
def seg_d(x, z, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]; L = dx * dx + dz * dz; t = max(0, min(1, ((x - a[0]) * dx + (z - a[1]) * dz) / L)) if L else 0; return math.hypot(x - a[0] - dx * t, z - a[1] - dz * t)
def gap(r, q): return max(q[0] - r[2], r[0] - q[2], q[1] - r[3], r[1] - q[3])   # 두 네모 사이 (겹치면 음수)
def rect_path(r, p):                                      # 네모와 휜 길 사이 (대충 — 네모 둘레 점들)
    bb = p.get('_bb') or p.setdefault('_bb', [min(q[0] for q in p['pts']) - p['hw'], min(q[1] for q in p['pts']) - p['hw'], max(q[0] for q in p['pts']) + p['hw'], max(q[1] for q in p['pts']) + p['hw']])
    if gap(r, bb) > 1: return 9
    pts = [(r[0] + (r[2] - r[0]) * i / 4, r[1] + (r[3] - r[1]) * j / 4) for i in range(5) for j in range(5)]
    return min(seg_d(x, z, p['pts'][k], p['pts'][k + 1]) for x, z in pts for k in range(len(p['pts']) - 1)) - p['hw']
DOORD = 2.4
def door_box(b):
    x0, z0, x1, z1 = rect(b); s = b['doors'][0]; cx, cz = b['x'], b['z']
    return dict(n=[cx - 1.9, z0 - DOORD, cx + 1.9, z0], s=[cx - 1.9, z1, cx + 1.9, z1 + DOORD], w=[x0 - DOORD, cz - 1.9, x0, cz + 1.9], e=[x1, cz - 1.9, x1 + DOORD, cz + 1.9])[s]
G_B, G_R, G_A = 2.1, 0.3, 0.4                               # c93: 건물 사이(골목) 최소 간격 1.0 → 1.3칸
def front(b):                                             # 정문 쪽 벽 앞 띠 — 랜드마크·창고는 여기에 어울리는 사물을 놓는다 (다른 건물·길·자리가 들어오면 안 된다)
    if b['t'] == 'house': return None
    x0, z0, x1, z1 = rect(b); s = b['doors'][0]; D = 1.5 if b['t'] == 'store' else 1.8
    return dict(n=[x0, z0 - D, x1, z0], s=[x0, z1, x1, z1 + D], w=[x0 - D, z0, x0, z1], e=[x1, z0, x1 + D, z1])[s]
def bad(b, others):                                       # 이 건물 자리가 얼마나 나쁜가 (0 = 괜찮다)
    r = rect(b); v = 0; zr = M['zones'][b['zone']]
    if r[0] < zr[0] + 0.3 or r[2] > zr[2] - 0.3 or r[1] < zr[1] + 0.3 or r[3] > zr[3] - 0.3: v += 5
    for q in M['roads']: v += max(0, G_R - gap(r, q))
    for q in M['rivers']: v += max(0, 1.0 - gap(r, q))
    for q in hills: v += max(0, 0.3 - gap(r, q))
    for p in M['paths']: v += max(0, G_R - rect_path(r, p))
    if not isgas(b):
        for q in arects: v += max(0, (G_B if q in AREAS['gas'] else G_A) - gap(r, q))   # 주유소 둘레도 골목 폭만큼
    d = door_box(b); f = front(b)
    if f:
        for q in M['roads'] + M['rivers'] + hills + arects: v += max(0, 0.05 - gap(f, q))
        for p in M['paths']: v += max(0, 0.05 - rect_path(f, p))
    for o in others:
        if o is b or (isgas(b) and isgas(o)): continue
        q = rect(o); v += max(0, G_B - gap(r, q)); fo = front(o)
        if f: v += max(0, 0.05 - gap(f, q))
        if fo: v += max(0, 0.05 - gap(fo, r))
        v += max(0, 0.05 - gap(d, q)) * 2; v += max(0, 0.05 - gap(door_box(o), r)) * 2
    for q in hills + M['rivers'] + ([] if isgas(b) else arects): v += max(0, 0.05 - gap(d, q))
    return v
removed = []
def solve():
    for rnd_i in range(8):
        moved = False
        for b in sorted(top, key=lambda b: -bad(b, top)):
            v0 = bad(b, top)
            if isgas(b) or v0 <= 1e-6: continue
            ox, oz = b['x'], b['z']; best = (v0 + 0.02, 0, 0)
            for i in range(-18, 19):
                for j in range(-18, 19):
                    dx, dz = i * 0.5, j * 0.5; cost = math.hypot(dx, dz) * 0.01
                    if cost >= best[0]: continue
                    b['x'], b['z'] = round(ox + dx, 2), round(oz + dz, 2)
                    sc = bad(b, top) + cost
                    if sc < best[0]: best = (sc, dx, dz)
            b['x'], b['z'] = round(ox + best[1], 2), round(oz + best[2], 2)
            if best[1] or best[2]: moved = True
        if not moved: break
solve()
houses = lambda: [b for b in top if b['t'] == 'house' and not b.get('garage') and not isgas(b) and not any(c.get('parent') == B.index(b) for c in B)]
WANT = round(sum(1 for b in top if b['t'] == 'house' and not b.get('garage') and not isgas(b)) / 4)
def free(b): return min([gap(rect(b), rect(o)) for o in top if o is not b] + [gap(rect(b), q) for q in arects])
QUOTA = {0: 3, 1: 2, 2: 1, 3: 1}                          # 구역마다 고르게 (큰 구역 3·2, 작은 구역 1·1 = 7채)
while len(removed) < WANT:                                # 집을 4분의 1 뺀다 — 그 구역에서 자리가 가장 안 나오는 집부터, 다 풀렸으면 가장 끼어 있는 집
    hs = [b for b in houses() if QUOTA[b['zone']] > 0]
    pick = max(hs, key=lambda b: (bad(b, top), -free(b)))
    QUOTA[pick['zone']] -= 1; top.remove(pick); removed.append(pick); print('remove', pick['t'], pick['zone'], round(bad(pick, top), 2), flush=True); solve()
for extra in range(6):                                    # 그래도 길·건물과 겹치는 것이 남으면 — 빼지 않고 같은 구역의 빈 땅을 찾아 옮긴다 (가장 가까운 데로). 정말 없을 때만 집을 뺀다
    worst = max(top, key=lambda b: bad(b, top)); w = bad(worst, top)
    if w <= 0.25: break
    ox, oz, ozn = worst['x'], worst['z'], worst['zone']; best = None
    for zi in [ozn] + ([k for k in range(4) if k != ozn] if worst['t'] == 'house' else []):   # 집은 제 구역에 자리가 없으면 다른 구역으로
        zr = M['zones'][zi]; worst['zone'] = zi
        x = zr[0] + 4.9 + worst['w'] / 2
        while x <= zr[2] - 4.9 - worst['w'] / 2:
            z = zr[1] + 4.9 + worst['d'] / 2
            while z <= zr[3] - 4.9 - worst['d'] / 2:
                worst['x'], worst['z'] = round(x, 2), round(z, 2)
                if bad(worst, top) <= 1e-6:
                    c = math.hypot(x - ox, z - oz)
                    if best is None or c < best[0]: best = (c, round(x, 2), round(z, 2), zi)
                z += 0.5
            x += 0.5
        if best: break
    worst['zone'] = best[3] if best else ozn
    if best: worst['x'], worst['z'] = best[1], best[2]; print('moved far', worst['t'], worst['zone'], round(best[0], 1), flush=True); continue
    worst['x'], worst['z'] = ox, oz
    pick = worst if worst in houses() else min(houses(), key=lambda h: gap(rect(h), rect(worst)))
    top.remove(pick); removed.append(pick); print('remove extra', pick['t'], pick['zone'], round(w, 2), flush=True); solve()
# 차고: 가장 가까운 집이 빠졌으면 같이 뺀다 (집에서 6칸 넘게 떨어진 차고)
for g in [b for b in top if b.get('garage')]:
    if min(gap(rect(g), rect(h)) for h in top if h['t'] == 'house' and not h.get('garage')) > 6: top.remove(g); removed.append(g)
# 지운 건물을 목록에서 빼고 번호를 당긴다
keep = [b for b in B if b not in removed]; idx = {id(b): i for i, b in enumerate(keep)}
for b in keep:
    if 'parent' in b: b['parent'] = idx[id(B[b['parent']])]
for i, b in enumerate(keep): b['local'] = i
for b in keep:                                            # 방은 제 건물을 따라간다
    if 'parent' in b: p = keep[b['parent']]; b['x'] = round(b['x'] + p['x'] - p['_o'][0], 2); b['z'] = round(b['z'] + p['z'] - p['_o'][1], 2)
print('left bad', [(b['t'], b['x'], b['z'], round(bad(b, top), 2)) for b in top if bad(b, top) > 1e-6])
M['_tr'] = [[b['_o'][0], b['_o'][1], b['x'], b['z']] for b in keep if '_o' in b]
for b in keep: b.pop('_o', None); b.pop('_g', None)
AM = 1
def area_bad(r, zi, others):
    zr = M['zones'][zi]; v = 0
    if r[0] < zr[0] + 4.9 or r[2] > zr[2] - 4.9 or r[1] < zr[1] + 4.9 or r[3] > zr[3] - 4.9: v += 5   # 순환도로 안쪽
    for q in M['roads']: v += max(0, 0.5 - gap(r, q))
    for q in M['rivers']: v += max(0, 1.0 - gap(r, q))
    for q in hills: v += max(0, 0.5 - gap(r, q))
    for p in M['paths']: v += max(0, 0.5 - rect_path(r, p))
    for q in others: v += max(0, 0.6 * AM - gap(r, q))
    for b in top: v += max(0, 0.7 * AM - gap(r, rect(b))) + max(0, 0.05 - gap(door_box(b), r)) * 2 + (max(0, 0.05 - gap(front(b), r)) if front(b) else 0)
    return v
zone_of = lambda r: next(i for i, z in enumerate(M['zones']) if z[0] <= (r[0] + r[2]) / 2 <= z[2] and z[1] <= (r[1] + r[3]) / 2 <= z[3])
placed = AREAS['gas'] + AREAS['park']
for k in ('court', 'site'):
    for n, r in enumerate(AREAS[k]):
        zi = zone_of(r); best = None
        for shr, AM in ((1, 1), (0.92, 1), (0.85, 1), (0.78, 1), (0.72, 1), ((9.0, 5.2), 1), ((8.0, 4.8), 1), (0.85, 0.5), (0.72, 0.5), ((8.0, 4.8), 0.5)):                           # 자리가 없으면 조금 줄여서
            w, d = shr if isinstance(shr, tuple) else ((r[2] - r[0]) * shr, (r[3] - r[1]) * shr); zr = M['zones'][zi]
            x = zr[0] + 4.9
            while x + w <= zr[2] - 4.9:
                z = zr[1] + 4.9
                while z + d <= zr[3] - 4.9:
                    q = [x, z, x + w, z + d]
                    if area_bad(q, zi, placed) <= 1e-6:
                        c = math.hypot(x - r[0], z - r[1])
                        if best is None or c < best[0]: best = (c, [round(v, 2) for v in q])
                    z += 0.5
                x += 0.5
            if best: break
        if best: AREAS[k][n] = best[1]; placed.append(best[1]); print('place', k, n, best[1], 'moved', round(best[0], 1), 'shrink', shr)
        else: print('!! no room for', k, n, r)
M['b'] = keep; M['_areas'] = AREAS
# 공터: 건물·자리와 겹치는 쪽을 잘라 낸다 (큰 쪽을 남긴다). 너무 작아지면 없앤다
def cut(l, a, m):
    if gap(l, a) >= m: return l
    opts = [[l[0], l[1], min(l[2], a[0] - m), l[3]], [max(l[0], a[2] + m), l[1], l[2], l[3]], [l[0], l[1], l[2], min(l[3], a[1] - m)], [l[0], max(l[1], a[3] + m), l[2], l[3]]]
    return max(opts, key=lambda q: max(0, q[2] - q[0]) * max(0, q[3] - q[1]))
lots = []
for l in M['lots']:
    for b in keep:
        if b['t'] != 'hill' and 'parent' not in b: l = cut(l, rect(b), 0.6)
    for q in placed: l = cut(l, q, 0.3)
    if l[2] - l[0] >= 4 and l[3] - l[1] >= 4: lots.append([round(v, 2) for v in l])
AM = 1                                                    # 빈 땅에 주차장을 더 — 구역마다 넓은 것부터 찾아 넣는다 (맵이 줄면서 원래 공터가 많이 깎였다)
for zi in range(4):
    for n in range(3 if zi < 2 else 2):
        best = None; zr = M['zones'][zi]
        for w, d in ((14, 5.2), (5.2, 14), (11, 5.2), (5.2, 11), (8.5, 5.2), (5.2, 8.5), (6.5, 4.8), (4.8, 6.5)):
            x = zr[0] + 4.9
            while x + w <= zr[2] - 4.9 and not best:
                z = zr[1] + 4.9
                while z + d <= zr[3] - 4.9:
                    q = [round(x, 2), round(z, 2), round(x + w, 2), round(z + d, 2)]
                    if area_bad(q, zi, placed + lots) <= 1e-6: best = q; break
                    z += 0.5
                x += 0.5
            if best: break
        if not best: break
        lots.append(best); print('lot+', zi, best)
M['lots'] = lots
for p in M['paths']: p.pop('_bb', None)
json.dump(M, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print('kx', round(kx, 3), 'kb', round(kb, 3), 'ks', round(ks, 3), 'mm', M['mm'], 'area', round((M['mm']['x1'] - M['mm']['x0']) * (M['mm']['z1'] - M['mm']['z0']) / (139 * 163), 3))
print('removed', [(b['t'], 'garage' if b.get('garage') else '', b['zone']) for b in removed], 'want', WANT, 'lots', len(lots))
print('areas', AREAS)
