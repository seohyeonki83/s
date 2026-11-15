# c85: 마을 꾸미기 — map_c83.json → map_c85.json
#   · 주유소 2 (큰 구역마다 큰 네거리 모퉁이 — 집을 치운 자리): 사무실(집 종류 건물) + 지붕 덮인 주유기 자리
#   · 공원 2 (큰 구역의 빈터): 분수/동상 · 벤치 · 가로등 · 쓰레기통 · 자판기 · 공중전화 · 버스킹
#   · 농구장 1 (작은 구역) · 공사 현장 4 (구역마다)
#   · 건물마다 어울리는 길거리 사물 (마트 = 쇼핑카트, 은행 = 현금인출기 …) · 큰길 가로등·신호등·버스 정류장
#   사물은 [종류, x, z] — 건물·길·물·문 앞·서로 겹치지 않게 검사해서 통과한 것만 적는다 (씨앗 고정: 판마다 같은 마을)
import json, math, random, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'map_c83.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'map_c85.json'
M = json.load(open(SRC)); rnd = random.Random(85)
B = M['b']
rect = lambda b: [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]
def mk(x0, z0, x1, z1, **k):
    d = dict(x=round((x0 + x1) / 2, 2), z=round((z0 + z1) / 2, 2), w=round(x1 - x0, 2), d=round(z1 - z0, 2), kinds={}, local=0, block=-1, t='house', sideK=0); d.update(k); return d

# ── 1. 주유소: 집 12 (구역 0) · 집 34·35 (구역 1)를 치운다 ──
TRM = M.pop('_tr', None); NEWA = M.pop('_areas', None)       # c89: 줄인 맵 (map_shrink.py) — 건물의 옛 자리 → 새 자리, 새 자리 네모들
def find(t, x, z):
    if TRM: x, z = next((q[2], q[3]) for q in TRM if abs(q[0] - x) < 0.6 and abs(q[1] - z) < 0.6)
    return next(i for i, b in enumerate(B) if b['t'] == t and abs(b['x'] - x) < 0.6 and abs(b['z'] - z) < 0.6)
i12, i34, i35 = find('house', -46.66, 37.26), find('house', 26.83, 17.95), find('house', 27.95, 24.2)
# 사무실은 어느 변이든 4칸 이상 (문 폭이 3.4칸이라 그보다 짧은 벽은 문 양옆 벽 토막이 0이 돼서 벽 부딪힘 계산이 깨진다)
GAS = [dict(zone=0, r=[-50.5, 33.6, -40.0, 44.1], off=[-50.2, 40.0, -45.2, 44.0], door='e', can=[-48.3, 34.4, -40.6, 39.6], isl=[-46.3, -42.6], iz=37.0, sign=[-40.7, 43.4], yardp=[('tires', -41.85, 43.4), ('bin', -41.9, 40.75), ('drum', -41.45, 41.95), ('cone', -49.3, 34.9), ('cone', -49.3, 36.3)]),
       dict(zone=1, r=[23.3, 17.8, 33.0, 27.5], off=[23.6, 18.0, 28.6, 22.0], door='e', can=[25.0, 22.35, 32.4, 27.2], isl=[27.0, 30.6], iz=24.78, sign=[32.4, 18.5], yardp=[('tires', 32.3, 19.6), ('drum', 32.55, 20.72), ('bin', 23.95, 22.7), ('cone', 24.05, 24.2), ('cone', 24.05, 25.6)])]
if NEWA:                                                  # 주유소는 통째로 옮긴다
    for G, nr in zip(GAS, NEWA['gas']):
        dx, dz = nr[0] - G['r'][0], nr[1] - G['r'][1]; sh = lambda r: [round(r[0] + dx, 2), round(r[1] + dz, 2), round(r[2] + dx, 2), round(r[3] + dz, 2)]
        G['r'] = sh(G['r']); G['off'] = sh(G['off']); G['can'] = sh(G['can']); G['isl'] = [round(v + dx, 2) for v in G['isl']]; G['iz'] = round(G['iz'] + dz, 2); G['sign'] = [round(G['sign'][0] + dx, 2), round(G['sign'][1] + dz, 2)]
        G['yardp'] = [(t, round(px + dx, 2), round(pz + dz, 2)) for t, px, pz in G['yardp']]
B[i12] = mk(*GAS[0]['off'], doors=[GAS[0]['door']], zone=0, local=B[i12]['local'], gas=1, sideK=1)   # 쪽문은 남쪽 벽 (주유기 반대쪽)
B[i34] = mk(*GAS[1]['off'], doors=[GAS[1]['door']], zone=1, local=B[i34]['local'], gas=1)
del B[i35]
for b in B:                                               # 방(부모 번호)·제 번호를 당긴다
    if 'parent' in b and b['parent'] > i35: b['parent'] -= 1
    if b.get('local', 0) > i35: b['local'] -= 1

# ── 2. 자리들 ──
AREAS = []
for G in GAS: AREAS.append(dict(k='gas', r=G['r'], can=G['can'], isl=G['isl'], iz=G['iz'], zone=G['zone']))
PARKS = [dict(k='park', r=[-61.5, 8.4, -40.5, 17.8], zone=0, v='fountain', gate='e'), dict(k='park', r=[41.0, 3.6, 61.5, 13.6], zone=1, v='statue', gate='w')]
if NEWA:
    for P_, nr in zip(PARKS, NEWA['park']): P_['wk'] = (nr[2] - nr[0]) / (P_['r'][2] - P_['r'][0]); P_['r'] = nr
AREAS += PARKS
COURT = dict(k='court', r=[18.5, -65.6, 28.5, -56.2], zone=3); AREAS.append(COURT)
if NEWA: COURT['r'] = NEWA['court'][0]
SITES = [dict(k='site', r=[-32.5, 48.7, -23.2, 56.9], zone=0), dict(k='site', r=[24.2, 47.4, 32.5, 55.5], zone=1), dict(k='site', r=[-50.0, -56.5, -40.5, -47.3], zone=2), dict(k='site', r=[52.0, -61.2, 61.5, -55.6], zone=3)]
if NEWA:
    for S_, nr in zip(SITES, NEWA['site']): S_['r'] = nr
AREAS += SITES
# 공터: 자리가 들어선 곳은 지우거나 줄인다
def cut_lot(l, a):                                        # 공터 l 에서 네모 a 와 겹치는 쪽을 잘라 낸다 (남는 쪽이 큰 것 하나만)
    if l[2] <= a[0] or l[0] >= a[2] or l[3] <= a[1] or l[1] >= a[3]: return [l]
    c = [[l[0], l[1], a[0] - 0.5, l[3]], [a[2] + 0.5, l[1], l[2], l[3]], [l[0], l[1], l[2], a[1] - 0.5], [l[0], a[3] + 0.5, l[2], l[3]]]
    c = [q for q in c if q[2] - q[0] >= 3.6 and q[3] - q[1] >= 3.6]
    return [max(c, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))] if c else []
lots = M['lots']
for A in AREAS: lots = [q for l in lots for q in cut_lot(l, A['r'])]
M['lots'] = [[round(v, 2) for v in l] for l in lots]

# ── 3. 검사 도구 ──
from map_radii import PR, WH
ROADS, PATHS, RIV = M['roads'], M['paths'], M['rivers']
def seg_d(x, z, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]; l2 = dx * dx + dz * dz; t = max(0, min(1, ((x - a[0]) * dx + (z - a[1]) * dz) / l2)) if l2 else 0
    return math.hypot(x - a[0] - dx * t, z - a[1] - dz * t)
def on_road(x, z, m=0):
    if any(x > r[0] - m and x < r[2] + m and z > r[1] - m and z < r[3] + m for r in ROADS): return True
    return any(seg_d(x, z, p['pts'][i], p['pts'][i + 1]) < p['hw'] + m for p in PATHS for i in range(len(p['pts']) - 1))
def in_rects(x, z, R, m=0): return any(x > r[0] - m and x < r[2] + m and z > r[1] - m and z < r[3] + m for r in R)
BR = lambda: [rect(b) for b in B if b['t'] not in ('room', 'jail')]
DW, DD = 1.9, 2.4                                         # 문 앞: 문 반폭(문 폭 3.4의 절반 + 여유) · 깊이 — 게임(chOutPlace)이 비우는 자리보다 조금 넉넉히
def door_box(b, s):
    nx, nz = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}[s]; cx, cz = b['x'] + nx * b['w'] / 2, b['z'] + nz * b['d'] / 2
    if nx: return [min(cx, cx + nx * DD), cz - DW, max(cx, cx + nx * DD), cz + DW]
    return [cx - DW, min(cz, cz + nz * DD), cx + DW, max(cz, cz + nz * DD)]
def side_door(b):                                         # 쪽문이 나는 벽 — 게임과 같은 규칙 (정문 없는 벽들 가운데 sideK번째. 챕터 맵은 고정)
    if b.get('locks') is not None or b.get('sideK') is None: return None
    cand = [d for d in 'nesw' if d not in b['doors']]
    return cand[b['sideK'] % len(cand)] if cand else None
DOORS = []
for b in B:
    if b['t'] in ('hill', 'room', 'jail') or not b.get('doors'): continue
    for d in b['doors']: DOORS.append(door_box(b, d))
    sd = side_door(b)
    if sd: DOORS.append(door_box(b, sd))
    for d in b.get('open', []):                           # 차고: 뚫린 벽 앞 전체
        q = door_box(b, d); r = rect(b); DOORS.append([r[0], q[1], r[2], q[3]] if d in 'ns' else [q[0], r[1], q[2], r[3]])
PROPS = []                                                # [종류, x, z]
mmx = M['mm']
def ok(t, x, z, road=0.3, wall=0.3, lot=True, door=True, gap=0.25, area=None, am=0.3):
    r = PR[t]
    if x - r < mmx['x0'] + 1.5 or x + r > mmx['x1'] - 1.5 or z - r < mmx['z0'] + 1.5 or z + r > mmx['z1'] - 1.5: return False
    if on_road(x, z, r + road) or in_rects(x, z, RIV, r + 0.5) or in_rects(x, z, BR(), r + wall - 0.01): return False
    if door and in_rects(x, z, DOORS, r): return False
    if lot and in_rects(x, z, M['lots'], r + 0.2): return False
    for A in AREAS:
        if A is not area and A['k'] != 'park' and in_rects(x, z, [A['r']], r + am): return False
    return all(math.hypot(x - p[1], z - p[2]) >= r + PR[p[0]] + gap for p in PROPS)
def put(t, x, z, **k):
    if not ok(t, x, z, **k): return False
    PROPS.append([t, round(x, 2), round(z, 2)]); return True
def force(t, x, z, inv=0): PROPS.append([t, round(x, 2), round(z, 2)] + ([1] if inv else []))   # inv = 이 자리의 것은 부술 수 없다 (공사 현장)
MISS = []
THIN = dict(lamp=0.3, tlight=0.34, pillar=0.3, flag=0.3)   # 기둥뿐인 것 — 가리는 폭
HK = 1.5                                                  # 세워 놓은 그림은 제 키의 1.5배만큼 뒤(북쪽) 바닥을 가린다
def hid(front, back):                                     # front가 back을 가리는 몫 (0~1)
    a, c = WH[front[0]], WH[back[0]]; dz = front[2] - back[2]
    if front[0] in THIN: a = (THIN[front[0]], a[1])
    if dz <= 0.05: return 0
    cover = HK * a[1] - dz; ox = min(front[1] + a[0] / 2, back[1] + c[0] / 2) - max(front[1] - a[0] / 2, back[1] - c[0] / 2)
    if cover <= 0 or ox <= 0: return 0
    return (ox / c[0]) * min(1, cover / (HK * c[1]))
def hides(t, x, z, lim=0.3):                              # 이 자리에 놓으면 이미 놓인 것에 가려지거나, 이미 놓인 것을 가리나
    p = [t, x, z]
    return any(hid(q, p) > lim or hid(p, q) > lim for q in PROPS)
def wall_pt(b, side, t, r, off=0.3):                      # 그 벽에 바짝 (밖에서 벽을 볼 때 왼쪽 끝 t = 0)
    x0, z0, x1, z1 = rect(b)
    if side == 'n': return x1 - (x1 - x0) * t, z0 - off - r
    if side == 's': return x0 + (x1 - x0) * t, z1 + off + r
    if side == 'w': return x0 - off - r, z0 + (z1 - z0) * t
    return x1 + off + r, z1 - (z1 - z0) * t
REL = {'n': dict(F='n', B='s', L='e', R='w'), 's': dict(F='s', B='n', L='w', R='e'), 'w': dict(F='w', B='e', L='n', R='s'), 'e': dict(F='e', B='w', L='s', R='n')}
def pack(b, rel, frm, types, start=0.5, gap=0.3):          # 그 벽을 따라 차례로 — frm: 'l' 왼쪽 끝에서 · 'r' 오른쪽 끝에서 · 'c' 한가운데에 모아서. 자리가 안 되면 조금씩 밀어 본다
    s = REL[b['doors'][0]][rel]; x0, z0, x1, z1 = rect(b); L = (x1 - x0) if s in 'ns' else (z1 - z0)
    if s in 'ew':                                         # 세로 벽: 키 큰 것이 북쪽에 오게 (남쪽의 큰 것이 뒤의 작은 것을 가리지 않게)
        north_first = (s == 'w') != (frm == 'r')         # 서쪽 벽은 왼쪽 끝(t = 0)이 북쪽 · 동쪽 벽은 남쪽
        types = sorted(types, key=lambda t: -WH[t][1] if north_first else WH[t][1])
    tot = sum(2 * PR[t] for t in types) + gap * (len(types) - 1); pos = (L - tot) / 2 if frm == 'c' else start; prev = None
    for typ in types:
        r = PR[typ]; pos += r if prev is None else prev + gap + r; done = False
        for sl in (0, .35, .7, 1.05, 1.4):
            u = pos + sl
            if u > L - 0.3: break
            t = (u / L) if frm != 'r' else 1 - u / L
            x, z = wall_pt(b, s, t, r)
            if put(typ, x, z, gap=gap if gap < 0.2 else 0.25): done = True; pos = u; break   # 줄지어 놓는 것(쇼핑카트 — 간격 0.2 미만으로 부른 것)만 바짝 붙인다
        if not done: MISS.append((b['t'], rel, frm, typ)); pos -= (r if prev is None else prev + gap + r); continue
        prev = r
def by_door(b, typ, sd):                                   # 정문 바로 옆 (문 가운데에서 벽을 따라 1.95칸)
    s = b['doors'][0]; x0, z0, x1, z1 = rect(b); L = (x1 - x0) if s in 'ns' else (z1 - z0)
    for d in (DW + PR[typ] + 0.08, DW + PR[typ] + 0.45):
        t = 0.5 + sd * d / L
        if 0.05 < t < 0.95 and put(typ, *wall_pt(b, s, t, PR[typ])): return True
    MISS.append((b['t'], 'door', sd, typ)); return False

# ── 4. 주유소 ──
SPOTS, FUEL = [], []
for G in GAS:
    A = next(a for a in AREAS if a['k'] == 'gas' and a['zone'] == G['zone']); c = G['can']
    for px, pz in ((c[0] + .35, c[1] + .7), (c[2] - .35, c[1] + .7), (c[0] + .35, c[3] - .7), (c[2] - .35, c[3] - .7)): force('pillar', px, pz)   # c89: 기둥을 지붕 안쪽으로 (사무실 벽과 기둥 사이에 몸이 끼지 않게 — 틈 1칸 이상)
    for ix in G['isl']:
        force('pump', ix, G['iz'] - 0.85); force('pump', ix, G['iz'] + 0.85)
    force('gsign', *G['sign'])
    for t, px, pz in G['yardp']:
        if not put(t, px, pz, area=A, wall=0.2): MISS.append(('gas', t, px, pz))
    mid = (G['isl'][0] + G['isl'][1]) / 2
    FUEL.append(dict(zone=G['zone'], slots=[[round(mid, 2), G['iz'], 1.5708], [round(G['isl'][0] - 1.45, 2), G['iz'], 1.5708], [round(G['isl'][1] + 1.45, 2), G['iz'], 1.5708]]))
    # 사람: 하양 2~3 · 노랑 2~3 · 빨강 0~1 · 경찰 0~1 — 주유기 둘레와 사무실 앞에 뭉쳐서
    SPOTS.append(dict(k='gas', zone=G['zone'], at=[round(mid, 2), round(G['iz'] + (2.2 if G['zone'] == 0 else -2.2), 2)], rad=2.3, mix=[['vig', 0, 1], ['police', 0, 1], ['', 2, 3], ['guard', 2, 3]]))

# ── 5. 공원 ──
for P in PARKS:
    x0, z0, x1, z1 = P['r']; cx, cz = (x0 + x1) / 2, (z0 + z1) / 2; wk = P.get('wk', 1); hk = min(1, (z1 - z0) / 9.4)
    force(P['v'], cx, cz - 0.2)
    for bx, bz in ((cx - 3.6 * wk, cz - 2.9 * hk), (cx + 3.6 * wk, cz - 2.9 * hk), (cx - 3.6 * wk, cz + 3.0 * hk), (cx + 3.6 * wk, cz + 3.0 * hk)): put('bench', bx, bz, area=P)
    for lx, lz in ((cx - 6.2 * wk, z0 + 0.7), (cx + 6.2 * wk, z0 + 0.7), (cx - 6.2 * wk, z1 - 0.7), (cx + 6.2 * wk, z1 - 0.7)):
        if not put('lamp', lx, lz, area=P): put('lamp', lx + 1.6, lz + (1.6 if lz < cz else -1.6), area=P)
    sg = 1 if P['gate'] == 'e' else -1                    # 큰길 쪽 (들머리)
    ex = x1 if sg > 0 else x0
    put('vending', ex - sg * 1.0, z0 + 1.0, area=P); put('booth', ex - sg * 1.0, z1 - 1.0, area=P); put('bin', ex - sg * 2.3, z0 + 0.7, area=P)
    bx = cx - sg * 6.6 * wk                                    # 버스킹: 들머리 반대쪽 잔디밭 — 하양(기타) + 앰프, 둘레에 하양·노랑
    put('amp', bx - sg * 0.2, cz - 1.0, area=P); put('bench', bx - sg * 2.6, z1 - 1.2, area=P); put('bin', bx - sg * 3.2, z0 + 0.7, area=P)
    SPOTS.append(dict(k='busker', zone=P['zone'], at=[round(bx - sg * 0.9, 2), round(cz - 0.2, 2)], tool='guitar', mix=[['', 1, 1]]))
    SPOTS.append(dict(k='crowd', zone=P['zone'], ring=[round(bx - sg * 0.9, 2), round(cz - 0.2, 2), 2.2, 3.7, sg], mix=[['', 3, 4], ['guard', 2, 3]]))

# ── 6. 농구장 ──
x0, z0, x1, z1 = COURT['r']; cx = (x0 + x1) / 2
force('hoop', cx, z0 + 0.55); put('bench', x1 - 0.9, z1 - 2.2, area=COURT); put('bin', x0 + 0.7, z1 - 0.7, area=COURT)
SPOTS.append(dict(k='court', zone=3, at=[round(cx, 2), round(z0 + 3.6, 2)], rad=1.9, mix=[['guard', 2, 3], ['', 2, 3], ['attacker', 2, 3]]))

# ── 7. 공사 현장 ──
for S in SITES:
    x0, z0, x1, z1 = S['r']; cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    dz = min(2.0, (z1 - z0) * 0.3)
    force('excavator', x0 + 2.2, z0 + dz, 1); force('pile', x1 - 1.9, z0 + dz - 0.2, 1); force('mixer', x0 + 1.4, z1 - 1.3, 1); force('toilet', x1 - 1.0, z1 - 1.3, 1)
    force('csign', cx, z1 - 0.6, 1); force('cone', cx - 1.4, z1 - 0.5, 1); force('cone', cx + 1.4, z1 - 0.5, 1); force('cone', cx + 2.4, z1 - 0.5, 1)
    SPOTS.append(dict(k='site', zone=S['zone'], at=[round(cx + 0.4, 2), round(cz + 0.6, 2)], rad=1.9, tool='work', mix=[['', 2, 3], ['guard', 2, 3]]))

# ── 8. 건물마다 어울리는 사물 ──
SETS = dict(
    mart=[('F', 'l', ['cart', 'cart', 'cart'], 0.3, 0.12), ('F', 'r', ['bench', 'vending'], 0.4, 0.2), ('B', 'l', ['dumpster', 'crate']), ('B', 'r', ['box', 'box'])],
    bank=[('F', 'l', ['bench']), ('F', 'r', ['atm', 'atm'])],   # 현금인출기는 공원 벤치를 가리지 않는 쪽에
    police=[('F', 'l', ['flag', 'board']), ('F', 'r', ['cone', 'barrier', 'barrier'])],
    fire=[('F', 'l', ['hydrant', 'hose', 'exting']), ('F', 'r', ['cone', 'cone']), ('R', 'c', ['hydrant'])],
    hospital=[('F', 'l', ['wheelchair', 'wheelchair']), ('F', 'r', ['vending']), ('L', 'c', ['gurney', 'bench'])],
    army=[('F', 'l', ['flag', 'sbag']), ('F', 'r', ['ammo', 'drum'], 0.4, 0.2), ('L', 'l', ['sbag', 'crate']), ('L', 'r', ['drum']), ('R', 'c', ['drum'])],
    gym=[('F', 'l', ['bike', 'bike', 'bike']), ('F', 'r', ['bench', 'vending'])],
    library=[('F', 'l', ['bench', 'bookdrop']), ('L', 'c', ['bike', 'bike'])],
    conv=[('F', 'l', ['parasol']), ('F', 'r', ['freezer']), ('R', 'l', ['parasol', 'claw', 'bin']), ('B', 'c', ['crate'])],
    store=[('F', 'l', ['crate'], 0.35), ('F', 'r', ['drum'], 0.35), ('L', 'l', ['box'])],
)
for b in list(B):
    if b['t'] in SETS:
        for rel, frm, types, *o in SETS[b['t']]: pack(b, rel, frm, types, *o)
    if b['t'] in ('bank', 'library'): by_door(b, 'planter', 1); by_door(b, 'planter', -1)   # 문 양옆 화분
ks = 0
for b in B:                                               # 창고 둘에 하나는 뒤에 큰 쓰레기통 · 집: 우편함(문 옆) + 화분·자전거·쓰레기 봉지 가운데 하나쯤
    if b['t'] == 'store':
        ks += 1
        if ks % 2: pack(b, 'B', 'c', ['dumpster'])
    if b['t'] == 'house' and not b.get('gas'):
        if not b.get('garage') and rnd.random() < 0.7: by_door(b, 'mailbox', 1 if rnd.random() < .5 else -1)
        q = rnd.random()
        if q < 0.22: pack(b, 'F', rnd.choice('lr'), ['planter'])
        elif q < 0.36: pack(b, rnd.choice('LR'), 'c', ['bike'])
        elif q < 0.52: pack(b, rnd.choice('LRB'), rnd.choice('lr'), ['bags'])

# ── 9. 큰길: 신호등 · 가로등 · 버스 정류장 · 소화전 · 우체통 ──
TL = dict(road=-0.05, wall=0.05, lot=False, door=False, am=-0.3)
for zi, A in enumerate(M['ave']):
    V, H = A['V'], A['H']; r = M['ring'] / 2
    if V and H:                                           # 큰 네거리: 신호등 둘 (마주 보는 모퉁이)
        put('tlight', V['c'] + V['hw'] + 0.3, H['c'] - H['hw'] - 0.3, **TL)
        put('tlight', V['c'] - V['hw'] - 0.3, H['c'] + H['hw'] + 0.3, **TL)
    if V:                                                 # 대로가 순환도로와 만나는 곳마다 하나
        put('tlight', V['c'] + V['hw'] + 0.3, V['a'] + r + 0.5, **TL)
        put('tlight', V['c'] - V['hw'] - 0.3, V['b'] - r - 0.5, **TL)
    if H:
        put('tlight', H['a'] + r + 0.5, H['c'] - H['hw'] - 0.3, **TL)
        put('tlight', H['b'] - r - 0.5, H['c'] + H['hw'] + 0.3, **TL)
    def lamps(vert, c, hw, a, b, skip):
        n = max(1, int((b - a) / 15)); k = 0
        for i in range(n + 1):
            u = a + 4 + (b - a - 8) * i / max(1, n)
            if any(abs(u - s) < 4.2 for s in skip): continue
            sd = 1 if k % 2 == 0 else -1; k += 1
            for s2 in (sd, -sd):                          # 신호등 바로 앞(남쪽)이면 기둥이 신호등을 가린다 → 길 건너편에 세운다
                x, z = (c + s2 * (hw + 0.28), u) if vert else (u, c + s2 * (hw + 0.28))
                if any(q[0] == 'tlight' and hid(['lamp', x, z], q) > 0.3 for q in PROPS): continue
                if put('lamp', x, z, **TL): break
    if V: lamps(True, V['c'], V['hw'], V['a'], V['b'], [H['c']] if H else [])
    if H: lamps(False, H['c'], H['hw'], H['a'], H['b'], [V['c']] if V else [])
    if V:
        sd = -1 if V['c'] < 0 else 1                      # 버스 정류장: 세로 대로 바깥쪽 인도, 구역 한가운데쯤 (+ 쓰레기통)
        um = (V['a'] + V['b']) / 2 + (9 if H else 0)
        for du in (0, 2, -2, 4, -4, 6):
            x, z = V['c'] + sd * (V['hw'] + 1.0), um + du
            if hides('busstop', x, z): continue
            if put('busstop', x, z, road=0.05, wall=0.2, lot=False): put('bin', V['c'] + sd * (V['hw'] + 0.6), um + du + 1.5, road=0.05, wall=0.1, lot=False); break
        for du in (0, 1.5, -1.5, 3, -3):                  # 소화전 · 우체통
            x, z = V['c'] - sd * (V['hw'] + 0.45), um - 14 + du
            if not hides('hydrant', x, z) and put('hydrant', x, z, road=0.0, wall=0.1, lot=False): break
        for du in (0, 1.5, -1.5, 3, -3):
            x, z = V['c'] - sd * (V['hw'] + 0.6), um + 12 + du
            if not hides('postbox', x, z) and put('postbox', x, z, road=0.0, wall=0.1, lot=False): break

M['areas'] = [dict(k=a['k'], r=a['r'], zone=a['zone'], **{q: a[q] for q in ('can', 'isl', 'iz', 'v', 'gate') if q in a}) for a in AREAS]
M['props'] = PROPS; M['spots'] = SPOTS; M['fuel'] = FUEL; M['pr'] = {t: PR[t] for t in sorted(set(p[0] for p in PROPS))}
json.dump(M, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
from collections import Counter
print('wrote', OUT, 'buildings', len(B), 'lots', len(M['lots']), 'props', len(PROPS), 'spots', len(SPOTS))
print(sorted(Counter(p[0] for p in PROPS).items(), key=lambda q: -q[1]))
print('못 놓은 것', MISS)
HP = sorted(((round(hid(p, q), 2), p[0], q[0], q[1], q[2], round(p[2] - q[2], 2)) for p in PROPS for q in PROPS if p is not q and hid(p, q) > 0.25), reverse=True)
print('가려짐 (앞, 뒤, 뒤 자리, 앞뒤 거리)', len(HP))
for h in HP: print('  ', h)
