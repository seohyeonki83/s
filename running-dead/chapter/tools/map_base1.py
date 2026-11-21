# 거점 맵 1 (가장 작은 맵) — 큰 맵 가로 30% · 세로 80% · 구역 하나 · 8자 순환도로 (바깥 한 바퀴 + 가운데 가로 길) · 공원 · 주유소 · 집 · 랜드마크 5 · 맨 북쪽 경찰서(거점)
import json, math
M = json.load(open('../map_c107.json'))
W, H = 121.0 * 0.3, 141.4 * 0.8          # 36.3 × 113.12
MG, RW = 3.0, 4.5; r = RW / 2; HW = 2.5   # 산 띠 · 순환도로 폭 · 가운데 길 반폭
X0, X1, Z0, Z1 = -W / 2 + MG, W / 2 - MG, -H / 2 + MG, H / 2 - MG   # 구역
S = dict(seed=11, mm=dict(x0=-W / 2, z0=-H / 2, x1=W / 2, z1=H / 2), zones=[[X0, Z0, X1, Z1]], ring=RW, gap=M['gap'], passW=M['passW'], zrMid=-9999,
         passes=[], passes2=[], passPts=[], rivers=[], bridges=[], paths=[], curves=[], cross=dict(M['cross'], ends=[]), popK=1 / 6)
S['roads'] = [[X0, Z0, X1, Z0 + RW], [X0, Z1 - RW, X1, Z1], [X0, Z0, X0 + RW, Z1], [X1 - RW, Z0, X1, Z1], [X0, -HW, X1, HW]]   # 바깥 한 바퀴 + 가운데 가로 길 = 8자
L, R, T, Bm = X0 + r, X1 - r, Z0 + r, Z1 - r
S['ave'] = [dict(V=None, H=dict(c=0.0, hw=HW, a=L, b=R))]
S['net'] = [dict(nodes=[[L, T], [R, T], [R, 0.0], [R, Bm], [L, Bm], [L, 0.0]], edges=[[0, 1, r, r / 2], [1, 2, r, r / 2], [2, 3, r, r / 2], [3, 4, r, r / 2], [4, 5, r, r / 2], [5, 0, r, r / 2], [5, 2, HW, 1.3]])]
S['start'] = [0.0, round(Z1 - r, 2)]   # 맨 남쪽 길 가운데에서 시작 — 북쪽 거점으로 올라간다
B = []
def bld(t, x, z, w, d, door, **kw):
    b = dict(x=round(x, 3), z=round(z, 3), w=w, d=d, doors=[door], kinds={}, local=len(B), block=-1, t=t, zone=0, sideK=1); b.update(kw); B.append(b); return len(B) - 1
IX0, IX1 = X0 + RW + 0.9, X1 - RW - 0.9          # 건물 놓는 안쪽 (길에서 0.9칸)
NZ0, NZ1, SZ0, SZ1 = Z0 + RW + 0.9, -HW - 0.9, HW + 0.9, Z1 - RW - 0.9
LC, RC = (IX0 - 0.4) / 2 + IX0 / 2 * 0, 0         # (아래에서 칸마다 직접 잡는다)
# ── 북쪽 칸 (위에서 아래로) ──
pol = bld('police', 0.0, NZ0 + 6.87 / 2, 9.58, 6.87, 's')                                     # 거점 — 맨 북쪽 가운데
B.append(dict(x=round(-3.13, 3), z=round(NZ0 + 6.87 / 2 - 1.96, 3), w=3.32, d=2.95, doors=['s'], locks=[], kinds={}, local=len(B), block=-1, t='jail', zone=0, parent=pol, room=dict(doors=[dict(s='s', w=2.0, ext=False)])))   # 경찰서 철창 (큰 맵과 같은 자리)
z = NZ0 + 6.87 + 2.2
bld('bank', IX0 + 9.58 / 2, z + 6.87 / 2, 9.58, 6.87, 'w')                                    # 은행 (왼쪽)
for k, x in enumerate((IX1 - 2.05 - 5.0, IX1 - 2.05)): bld('house', x, z + 2.5, 4.1, 4.95, 'e')   # 집 둘 (오른쪽)
z += 6.87 + 2.2
PARK = [IX0 + 1.0, z, IX1 - 1.0, z + 7.4]                                                     # 공원 (가로 한 줄)
z += 7.4 + 2.2
bld('gym', IX1 - 9.58 / 2, z + 6.87 / 2, 9.58, 6.87, 'e')                                     # 헬스장 (오른쪽)
for x in (IX0 + 2.05, IX0 + 2.05 + 5.0): bld('house', x, z + 2.5, 4.1, 4.95, 'w')             # 집 둘 (왼쪽)
z += 6.87 + 2.2
for x in (IX0 + 2.05, IX0 + 2.05 + 5.0): bld('house', x, z + 2.5, 4.1, 4.95, 'w')             # 집 둘 (왼쪽)
for x in (IX1 - 2.05, IX1 - 2.05 - 5.0): bld('house', x, z + 2.5, 4.1, 4.95, 'e')             # 집 둘 (오른쪽)
nz_end = z + 4.95
# ── 남쪽 칸 (위에서 아래로) ──
z = SZ0
bld('mart', IX0 + 11.9 / 2, z + 8.3 / 2, 11.9, 8.3, 'w')                                      # 마트 (왼쪽)
bld('house', IX1 - 2.05, z + 2.5, 4.1, 4.95, 'e')                                             # 집 (오른쪽)
z += 8.3 + 2.2
GAS = [IX0, z, IX0 + 10.5, z + 10.5]                                                          # 주유소 (왼쪽)
for x in (IX1 - 2.05, IX1 - 2.05 - 5.0): bld('house', x, z + 2.5, 4.1, 4.95, 'e')             # 집 둘 (오른쪽)
bld('house', IX1 - 2.5, z + 8.0, 5.0, 4.0, 'e')                                               # 집 (오른쪽 아래)
z += 10.5 + 2.2
for x in (IX0 + 2.05, IX0 + 2.05 + 5.0): bld('house', x, z + 2.5, 4.1, 4.95, 'w')             # 집 둘 (왼쪽)
bld('library', IX1 - 9.1 / 2, z + 6.51 / 2, 9.1, 6.51, 'e')                                   # 도서관 (오른쪽)
z += 6.87 + 2.2
bld('store', IX0 + 8.67 / 2, z + 6.27 / 2, 8.67, 6.27, 'w')                                   # 창고 (왼쪽)
bld('hospital', IX1 - 9.58 / 2, z + 6.87 / 2, 9.58, 6.87, 'e')                                # 병원 (오른쪽)
sz_end = z + 6.87
assert nz_end <= NZ1 + 0.01, (nz_end, NZ1); assert sz_end <= SZ1 + 0.01, (sz_end, SZ1)
def hill(a, b2, c, d): B.append(dict(x=round((a + c) / 2, 3), z=round((b2 + d) / 2, 3), w=round(c - a, 3), d=round(d - b2, 3), doors=[], locks=[], kinds={}, local=len(B), block=-1, t='hill', zone=-1))
mx0, mz0, mx1, mz1 = S['mm']['x0'], S['mm']['z0'], S['mm']['x1'], S['mm']['z1']
hill(mx0, mz0, mx1, Z0); hill(mx0, Z1, mx1, mz1); hill(mx0, Z0, X0, Z1); hill(X1, Z0, mx1, Z1)   # 사방의 산
S['b'] = B
# ── 공원 · 주유소: 큰 맵 것을 옮겨 온다 (사물째) ──
pk = next(a for a in M['areas'] if a['k'] == 'park' and a['zone'] == 0); gs = next(a for a in M['areas'] if a['k'] == 'gas' and a['zone'] == 0)
inr = lambda p, q: q[0] <= p[1] <= q[2] and q[1] <= p[2] <= q[3]
pw, ph = pk['r'][2] - pk['r'][0], pk['r'][3] - pk['r'][1]; PARK = [(IX0 + IX1) / 2 - pw / 2, PARK[1], (IX0 + IX1) / 2 + pw / 2, PARK[1] + ph]
pdx, pdz = PARK[0] - pk['r'][0], PARK[1] - pk['r'][1]; gdx, gdz = GAS[0] - gs['r'][0], GAS[1] - gs['r'][1]
mv = lambda q, dx, dz: [round(q[0] + dx, 3), round(q[1] + dz, 3), round(q[2] + dx, 3), round(q[3] + dz, 3)]
props = [[p[0], round(p[1] + pdx, 2), round(p[2] + pdz, 2)] + p[3:] for p in M['props'] if inr(p, pk['r'])]
props += [[p[0], round(p[1] + gdx, 2), round(p[2] + gdz, 2)] + p[3:] for p in M['props'] if inr(p, gs['r'])]
for x, zz in ((L + r + 0.4, -HW - 0.5), (R - r - 0.4, HW + 0.5)): props.append(['tlight', round(x, 2), round(zz, 2)])   # 가운데 길 양 끝 신호등
S['areas'] = [dict(k='park', r=mv(pk['r'], pdx, pdz), zone=0, v=pk['v'], gate=pk['gate']), dict(gs, r=mv(gs['r'], gdx, gdz), zone=0, can=mv(gs['can'], gdx, gdz), isl=[round(v + gdx, 3) for v in gs['isl']], iz=round(gs['iz'] + gdz, 3))]
F = next(f for f in M['fuel'] if f['zone'] == 0); S['fuel'] = [dict(zone=0, slots=[[round(a + gdx, 2), round(b + gdz, 2), c] for a, b, c in F['slots']])]
sp = next(s for s in M['spots'] if s['k'] == 'gas' and s['zone'] == 0); S['spots'] = [dict(sp, zone=0, at=[round(sp['at'][0] + gdx, 2), round(sp['at'][1] + gdz, 2)])]
S['lots'] = []; S['props'] = props; S['pr'] = {t: M['pr'][t] for t in sorted(set(p[0] for p in props))}
DX = -(W / 2) - 1.0   # 게임은 x > 0 을 다른 구역(큰 맵 오른쪽)으로 본다 — 맵 전체를 x < 0 쪽으로 옮긴다 (작은 맵 s1처럼)
S['mm'] = dict(x0=S['mm']['x0'] + DX, z0=S['mm']['z0'], x1=S['mm']['x1'] + DX, z1=S['mm']['z1'])
S['zones'] = [[q[0] + DX, q[1], q[2] + DX, q[3]] for q in S['zones']]
S['roads'] = [[q[0] + DX, q[1], q[2] + DX, q[3]] for q in S['roads']]
for A in S['ave']:
    if A['H']: A['H']['a'] += DX; A['H']['b'] += DX
for N in S['net']: N['nodes'] = [[x + DX, z] for x, z in N['nodes']]
S['start'][0] += DX
for b in S['b']: b['x'] = round(b['x'] + DX, 3)
for A in S['areas']:
    A['r'] = [A['r'][0] + DX, A['r'][1], A['r'][2] + DX, A['r'][3]]
    if 'can' in A: A['can'] = [A['can'][0] + DX, A['can'][1], A['can'][2] + DX, A['can'][3]]; A['isl'] = [v + DX for v in A['isl']]
for F in S['fuel']: F['slots'] = [[a + DX, b, c] for a, b, c in F['slots']]
for p in S['spots']: p['at'] = [p['at'][0] + DX, p['at'][1]]
for p in S['props']: p[1] = round(p[1] + DX, 2)
json.dump(S, open('../map_p1.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('mm', S['mm'], 'zone', S['zones'][0], 'buildings', [(b['t'], b['x'], b['z']) for b in B if b['t'] != 'hill'])
print('north rows end', round(nz_end, 2), '<=', round(NZ1, 2), ' south end', round(sz_end, 2), '<=', round(SZ1, 2))
