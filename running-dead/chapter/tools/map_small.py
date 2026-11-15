# 작은 맵 s1 — 큰 맵(map_c107.json)의 작은 구역 하나(구역 2)를 떼어 내 독립 맵으로 만든다
#   · 구역 하나, 건널목 없음(강·다리·산길 없음), 반듯한 네모 순환도로 + 세로 대로 하나, 사방이 산
#   · 랜드마크 2 (편의점·도서관) + 창고 1 + 집 3 + 공사 현장 1 + 공원 1 (주차장 하나를 공원으로)
#   · 사람·차 수는 게임 쪽에서 구역 몫(6분의 1)으로 줄인다 (popK)
import json, math, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'map_c107.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'map_s1.json'
M = json.load(open(SRC)); ZI = 2
Z = M['zones'][ZI]; x0, z0, x1, z1 = Z                    # [-57.5, -71.3, -6.5, -30.5]
RW = M['ring']; r = RW / 2                                # 순환도로 폭 4.5
AV = M['ave'][ZI]['V']; ac, ahw = AV['c'], AV['hw']
MG = 6.0                                                  # 구역 밖 산 띠 폭
rect = lambda b: [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]
inz = lambda x, z, m=0: x0 - m < x < x1 + m and z0 - m < z < z1 + m

S = dict(seed=M['seed'], mm=dict(x0=x0 - MG, z0=z0 - MG, x1=x1 + MG, z1=z1 + MG), zones=[Z], ring=RW, gap=M['gap'], passW=M['passW'], zrMid=-9999,
         passes=[], passes2=[], passPts=[], rivers=[], bridges=[], paths=[], curves=[], cross=dict(M['cross'], ends=[]), fuel=[], pr=M['pr'], popK=1 / 6)
# 길: 네모 순환도로 + 세로 대로 (끝에서 끝까지)
S['roads'] = [[x0, z0, x1, z0 + RW], [x0, z1 - RW, x1, z1], [x0, z0, x0 + RW, z1], [x1 - RW, z0, x1, z1], [ac - ahw, z0 + r, ac + ahw, z1 - r]]
S['ave'] = [dict(V=dict(c=ac, hw=ahw, a=z0 + r, b=z1 - r), H=None)]
L, Rr, T, Bm = x0 + r, x1 - r, z0 + r, z1 - r             # 순환도로 가운데 선
S['net'] = [dict(nodes=[[L, T], [ac, T], [Rr, T], [Rr, Bm], [ac, Bm], [L, Bm]], edges=[[0, 1, r, r / 2], [1, 2, r, r / 2], [2, 3, r, r / 2], [3, 4, r, r / 2], [4, 5, r, r / 2], [5, 0, r, r / 2], [1, 4, ahw, 1.3]])]
S['start'] = [round(ac + 8, 2), round(z1 - RW - 2.5, 2)]

# 건물: 그 구역 것만 (산 덩어리는 새로 두른다)
old = [b for b in M['b'] if b['t'] != 'hill' and b.get('zone') == ZI]
idx = {M['b'].index(b): i for i, b in enumerate(old)}
B = []
for i, b in enumerate(old):
    c = dict(b); c['zone'] = 0; c['local'] = i
    if 'parent' in c: c['parent'] = idx[c['parent']]
    B.append(c)
def hill(a, b2, c, d): B.append(dict(x=round((a + c) / 2, 3), z=round((b2 + d) / 2, 3), w=round(c - a, 3), d=round(d - b2, 3), doors=[], locks=[], kinds={}, local=len(B), block=-1, t='hill', zone=-1))
hill(x0 - MG, z0 - MG, x1 + MG, z0); hill(x0 - MG, z1, x1 + MG, z1 + MG); hill(x0 - MG, z0, x0, z1); hill(x1, z0, x1 + MG, z1)   # 사방의 산
S['b'] = B

# 공원: 도서관 위 주차장 자리 (대로 쪽이 들머리)
PARK = [-28.6, -66.0, -16.8, -58.8]
S['lots'] = [l for l in M['lots'] if inz((l[0] + l[2]) / 2, (l[1] + l[3]) / 2) and not (l[0] < PARK[2] and l[2] > PARK[0] and l[1] < PARK[3] and l[3] > PARK[1])]
site = next(a for a in M['areas'] if a['k'] == 'site' and a['zone'] == ZI)
S['areas'] = [dict(k='site', r=site['r'], zone=0), dict(k='park', r=PARK, zone=0, v='fountain', gate='w')]

# 사물: 그 구역 것 가운데 새 길·공원에 안 걸리는 것 + 공원 것
PR = M['pr']; PR.update(fountain=1.35, booth=0.5, amp=0.34, vending=0.55)
def on_road(x, z, m): return any(q[0] - m < x < q[2] + m and q[1] - m < z < q[3] + m for q in S['roads'])
props = []
for p in M['props']:
    t, x, z = p[0], p[1], p[2]
    if not inz(x, z): continue
    if len(p) < 4 and on_road(x, z, PR.get(t, 0.3) - 0.05) and t not in ('lamp', 'tlight'): continue
    if PARK[0] - 0.3 < x < PARK[2] + 0.3 and PARK[1] - 0.3 < z < PARK[3] + 0.3: continue
    if t in ('tlight', 'lamp', 'hydrant', 'postbox') and (abs(z - (z1 - RW)) < 6.5 and abs(x - ac) < 8): continue   # 옛 산길 들머리(휜 길) 둘레 것은 뺀다
    props.append(p)
cx, cz = (PARK[0] + PARK[2]) / 2, (PARK[1] + PARK[3]) / 2; wk = (PARK[2] - PARK[0]) / 21; hk = (PARK[3] - PARK[1]) / 9.4
def put(t, x, z):
    if any(math.hypot(x - q[1], z - q[2]) < PR[t] + PR.get(q[0], 0.3) + 0.2 for q in props): return
    props.append([t, round(x, 2), round(z, 2)])
props.append(['fountain', round(cx, 2), round(cz - 0.2, 2), 1])
for bx, bz in ((cx - 3.6 * wk, cz - 2.9 * hk), (cx + 3.6 * wk, cz - 2.9 * hk), (cx - 3.6 * wk, cz + 3.0 * hk), (cx + 3.6 * wk, cz + 3.0 * hk)): put('bench', bx, bz)
for lx, lz in ((cx - 6.2 * wk * 1.4, PARK[1] + 0.7), (cx + 6.2 * wk * 1.4, PARK[1] + 0.7), (cx - 6.2 * wk * 1.4, PARK[3] - 0.7), (cx + 6.2 * wk * 1.4, PARK[3] - 0.7)): put('lamp', lx, lz)
put('vending', PARK[0] + 1.0, PARK[1] + 1.0); put('booth', PARK[0] + 1.0, PARK[3] - 1.0); put('bin', PARK[0] + 2.3, PARK[1] + 0.7)
bx = cx + 6.6 * wk * 1.15                                  # 버스킹: 들머리 반대쪽
put('amp', bx + 0.2, cz - 1.0); put('bin', PARK[2] - 0.7, PARK[1] + 0.7)
# 큰길: 순환도로와 만나는 두 곳에 신호등, 가로등
TL = [['tlight', ac + ahw + 0.3, T + r + 0.5], ['tlight', ac - ahw - 0.3, Bm - r - 0.5]]
for t in TL:
    if not any(math.hypot(t[1] - q[1], t[2] - q[2]) < 0.8 for q in props): props.append([t[0], round(t[1], 2), round(t[2], 2)])
S['props'] = props
spot = next(s for s in M['spots'] if s['k'] == 'site' and s['zone'] == ZI)
S['spots'] = [dict(spot, zone=0), dict(k='busker', zone=0, at=[round(bx + 0.9, 2), round(cz - 0.2, 2)], tool='guitar', mix=[['', 1, 1]]),
              dict(k='crowd', zone=0, ring=[round(bx + 0.9, 2), round(cz - 0.2, 2), 1.8, 3.2, -1], mix=[['', 3, 4], ['guard', 2, 3]])]
S['pr'] = {t: PR[t] for t in sorted(set(p[0] for p in props))}
json.dump(S, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print('wrote', OUT, 'buildings', len(B), [b['t'] for b in B], 'lots', len(S['lots']), 'props', len(props), 'mm', S['mm'])
