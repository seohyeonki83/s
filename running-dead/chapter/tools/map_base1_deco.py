# c357: 거점 맵 꾸미기 — 큰 맵(map_deco.py)과 같은 규칙으로 길거리 사물을 뿌린다 (map_p1.json → map_p1.json)
#   · 건물마다 어울리는 사물 (마트 = 쇼핑카트, 은행 = 현금인출기, 경찰서 = 깃발·게시판·꼬깔 …) · 집 앞 우편함·화분·자전거·쓰레기 봉지
#   · 길: 신호등 · 가로등 · 버스 정류장 · 소화전 · 우체통 — 가운데 가로 길(큰길)과, 큰길이 없는 세로 순환도로 두 변
#   · 공사 현장 1 (남쪽 끝 빈터, 큰 맵처럼 구역마다 하나)
import json, math, random, sys
M = json.load(open('../map_p1.json')); rnd = random.Random(357)
B = M['b']
rect = lambda b: [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]
AREAS = [dict(a) for a in M['areas'] if a['k'] != 'site']
SITE = json.load(open('base1_site.json'))                 # map_base1.py 가 남긴 빈터 (공사 현장 자리)
if SITE: AREAS.append(dict(k='site', r=SITE, zone=0))
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
for p in M['props']:                                      # 이미 있는 것 (공원·주유소 사물) — 신호등은 아래 규칙이 다시 세운다
    if p[0] != 'tlight': PROPS.append(p)
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

# ── 7. 공사 현장 ──
for S in [A for A in AREAS if A['k'] == 'site']:
    x0, z0, x1, z1 = S['r']; cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    dz = min(2.0, (z1 - z0) * 0.3)
    force('excavator', x0 + 2.2, z0 + dz, 1); force('pile', x1 - 1.9, z0 + dz - 0.2, 1); force('mixer', x0 + 1.4, z1 - 1.3, 1); force('toilet', x1 - 1.0, z1 - 1.3, 1)
    force('csign', cx, z1 - 0.6, 1); force('cone', cx - 1.4, z1 - 0.5, 1); force('cone', cx + 1.4, z1 - 0.5, 1); force('cone', cx + 2.4, z1 - 0.5, 1)

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

r_ = M['ring'] / 2; zs = M['zones'][0]
AVE = [dict(V=dict(c=zs[0] + r_, hw=r_, a=zs[1] + r_, b=zs[3] - r_, ring=1), H=None), dict(V=dict(c=zs[2] - r_, hw=r_, a=zs[1] + r_, b=zs[3] - r_, ring=1), H=None)] + M['ave']
# ── 9. 큰길: 신호등 · 가로등 · 버스 정류장 · 소화전 · 우체통 ──
TL = dict(road=-0.05, wall=0.05, lot=False, door=False, am=-0.3)
for zi, A in enumerate(AVE):
    V, H = A['V'], A['H']; r = M['ring'] / 2
    if V and V.get('ring'): pass
    elif V and H:                                           # 큰 네거리: 신호등 둘 (마주 보는 모퉁이)
        put('tlight', V['c'] + V['hw'] + 0.3, H['c'] - H['hw'] - 0.3, **TL)
        put('tlight', V['c'] - V['hw'] - 0.3, H['c'] + H['hw'] + 0.3, **TL)
    if V and not V.get('ring'):                           # 대로가 순환도로와 만나는 곳마다 하나
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


# ── c358: 사람 모이는 자리 — 큰 맵과 같은 규칙 (공원 버스킹 · 구경꾼, 공사 현장 일꾼) ──
SPOTS = [sp for sp in M['spots'] if sp['k'] == 'gas']
for P in [A for A in AREAS if A['k'] == 'park']:
    amp = next(p for p in PROPS if p[0] == 'amp' and P['r'][0] <= p[1] <= P['r'][2] and P['r'][1] <= p[2] <= P['r'][3])
    sg = 1 if P.get('gate', 'e') == 'e' else -1; at = [round(amp[1] - sg * 0.7, 2), round(amp[2] + 0.8, 2)]
    SPOTS.append(dict(k='busker', zone=0, at=at, tool='guitar', mix=[['', 1, 1]]))
    SPOTS.append(dict(k='crowd', zone=0, ring=[at[0], at[1], 2.2, 3.7, sg], mix=[['', 3, 4], ['guard', 2, 3]]))
for S_ in [A for A in AREAS if A['k'] == 'site']:
    x0, z0, x1, z1 = S_['r']; SPOTS.append(dict(k='site', zone=0, at=[round((x0 + x1) / 2 + 0.4, 2), round((z0 + z1) / 2 + 0.6, 2)], rad=1.9, tool='work', mix=[['', 2, 3], ['guard', 2, 3]]))
M['spots'] = SPOTS
M['areas'] = [a for a in M['areas'] if a['k'] != 'site'] + [A for A in AREAS if A['k'] == 'site']
M['props'] = PROPS; M['pr'] = {t: PR[t] for t in sorted(set(p[0] for p in PROPS))}
json.dump(M, open('../map_p1.json', 'w'), ensure_ascii=False, separators=(',', ':'))
from collections import Counter
print('props', len(PROPS), sorted(Counter(p[0] for p in PROPS).items(), key=lambda q: -q[1]))
print('못 놓은 것', MISS); print('spots', [(q['k'], q.get('at') or q.get('ring')) for q in M['spots']])
