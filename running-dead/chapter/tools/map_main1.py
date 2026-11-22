# 본 맵 1 — 큰 맵(map_c107.json)을 그대로 가져와 건널목만 일자로 편다 (c359)
#   · 강·산이 구역 쪽으로 튀어나온 덩어리를 깎는다 (강은 폭 13 그대로 곧게, 산은 두 구역 사이 띠 안에서만)
#   · 순환도로가 건널목 앞에서 휘어 들어가던 길(paths · curves)을 없애고 구역 가장자리를 따라 곧게
#   · 다리·산길은 두 구역의 순환도로를 곧장 잇는다 (길이 = 강·산 폭 13 + 양쪽 순환도로 반폭)
import json
M = json.load(open('map_c107.json'))
RW = M['ring']; r = RW / 2; G = M['gap']; PW = M['passW']
ov = lambda a, b, m=0: a[0] < b[2] + m and b[0] < a[2] + m and a[1] < b[3] + m and b[1] < a[3] + m
# 강: 가운데 줄기(x -6.5 ~ 6.5)만
M['rivers'] = [q for q in M['rivers'] if q[0] == -G / 2 and q[2] == G / 2]
# 산: 두 구역 사이 띠(zrMid ± 6.5) 밖으로 튀어나온 덩어리는 뺀다
zm = M['zrMid']; hills = []
for b in M['b']:
    if b['t'] != 'hill': continue
    z0, z1 = b['z'] - b['d'] / 2, b['z'] + b['d'] / 2
    if (z0 < zm - G / 2 - 0.05 or z1 > zm + G / 2 + 0.05) and z1 > M['mm']['z0'] + 3.5 and z0 < M['mm']['z1'] - 3.5 and abs(b['x']) < 58: hills.append(b); continue
keep = [b for b in M['b'] if not any(b is h for h in hills)]
gone = len(M['b']) - len(keep)
idx = {id(b): i for i, b in enumerate(keep)}
old = M['b']; remap = {i: idx[id(b)] for i, b in enumerate(old) if id(b) in idx}
for b in keep:
    if 'parent' in b: b['parent'] = remap[b['parent']]
for i, b in enumerate(keep): b['local'] = i
M['b'] = keep
# 길: 구역마다 순환도로 네 변 + 큰길 (휜 길 없이)
roads = []; nets = []
for zi, (x0, z0, x1, z1) in enumerate(M['zones']):
    roads += [[x0, z0, x1, z0 + RW], [x0, z1 - RW, x1, z1], [x0, z0, x0 + RW, z1], [x1 - RW, z0, x1, z1]]
    A = M['ave'][zi]; V, H = A['V'], A['H']
    L, R, T, B_ = x0 + r, x1 - r, z0 + r, z1 - r
    N = [[L, T], [R, T], [R, B_], [L, B_]]; E = []
    def node(p): N.append(p); return len(N) - 1
    top, bot, lft, rgt = [0], [3], [0], [1]
    if V:
        V['a'], V['b'] = T, B_; roads.append([V['c'] - V['hw'], T, V['c'] + V['hw'], B_])
        vt, vb = node([V['c'], T]), node([V['c'], B_])
    if H:
        H['a'], H['b'] = L, R; roads.append([L, H['c'] - H['hw'], R, H['c'] + H['hw']])
        hl, hr = node([L, H['c']]), node([R, H['c']])
    ring = lambda a, b: E.append([a, b, r, r / 2])
    if V: ring(0, vt); ring(vt, 1); ring(2, vb); ring(vb, 3)
    else: ring(0, 1); ring(2, 3)
    if H: ring(1, hr); ring(hr, 2); ring(3, hl); ring(hl, 0)
    else: ring(1, 2); ring(3, 0)
    if V and H:
        c = node([V['c'], H['c']]); E += [[vt, c, V['hw'], 1.3], [c, vb, V['hw'], 1.3], [hl, c, H['hw'], 1.25], [c, hr, H['hw'], 1.25]]
    elif V: E.append([vt, vb, V['hw'], 1.3])
    elif H: E.append([hl, hr, H['hw'], 1.25])
    nets.append(dict(nodes=[[round(x, 3), round(z, 3)] for x, z in N], edges=E))
M['net'] = nets
# 건널목: 다리(강) · 산길(산) — 양쪽 순환도로 한가운데를 곧장 잇는다
P2 = []; M['bridges'] = []
for P in M['passes2']:
    if P['axis'] == 'v':
        a, b = -(G / 2 + r), G / 2 + r
        P.update(ax=a, bx=b, az=P['c'], bz=P['c'], len=b - a, pin=G / 2)
        M['bridges'].append([a, P['c'] - PW / 2, b, P['c'] + PW / 2])
    else:
        a, b = zm + G / 2 + r, zm - G / 2 - r
        P.update(ax=P['c'], bx=P['c'], az=a, bz=b, len=a - b, pin=G / 2)
        roads.append([P['c'] - PW / 2, b, P['c'] + PW / 2, a])
    P2.append(P)
M['passes2'] = P2
M['roads'] = [[round(v, 3) for v in q] for q in roads]
M['paths'] = []; M['curves'] = []; M['cross'] = dict(M['cross'], ends=[])
# 새 길 · 다리에 걸리는 것 (집 · 공터 · 사물 · 자리)
RB = M['roads'] + M['bridges']
hitB = [(b['t'], b['x'], b['z']) for b in M['b'] if b['t'] not in ('hill', 'room', 'jail') and any(ov([b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2], q, 0.3) for q in RB)]
n0 = len(M['props']); PRr = lambda t: M['pr'].get(t, 0.4); M['props'] = [p for p in M['props'] if not any(ov([p[1], p[2], p[1], p[2]], q, PRr(p[0]) - 0.1) for q in RB)]   # 가운데가 길(반지름만큼 넓힌)에 들어가면 뺀다 — 길가에 바짝 선 가로등·신호등은 남는다
l0 = len(M['lots']); M['lots'] = M['lots']   # 공터는 큰 맵 그대로 (원래도 순환도로 밑으로 조금 들어가 있다)
hitA = [A['k'] for A in M['areas'] if any(ov(A['r'], q) for q in RB)]
M['pr'] = {t: M['pr'][t] for t in sorted(set(p[0] for p in M['props']))}
json.dump(M, open('../map_m1.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('뺀 산 덩어리', gone, '· 길에 걸린 건물', hitB, '· 뺀 사물', n0 - len(M['props']), '· 뺀 공터', l0 - len(M['lots']), '· 걸린 자리', hitA)
print('passes2', [(P['axis'], P['ax'], P['az'], P['bx'], P['bz']) for P in P2])
