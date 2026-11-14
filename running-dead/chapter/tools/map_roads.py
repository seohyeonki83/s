# c69: 구역마다 순환도로(링)를 더하고, 길에 걸리는 건물만 조금씩 안쪽으로 옮긴다.  map_base.json (gen.py 출력) → map.json
#   링 = 구역 테두리 안쪽으로 폭 4.5칸. 다리·산 길목·대로 자리는 그대로. 방·철창은 딸린 건물과 같이 움직인다.
import json, sys
RW, CL, GAP_MIN = 4.5, 0.5, 1.6
M = json.load(open('map_base.json'))
assert 'ring' not in M
B = M['b']
top = [i for i, b in enumerate(B) if b['t'] != 'hill' and b.get('parent') is None]
rect = lambda b: (b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)
def gap(a, b):
    ax0, az0, ax1, az1 = rect(a); bx0, bz0, bx1, bz1 = rect(b)
    dx = max(bx0 - ax1, ax0 - bx1, 0); dz = max(bz0 - az1, az0 - bz1, 0)
    return (dx * dx + dz * dz) ** 0.5 if (dx > 0 or dz > 0) else -min(min(ax1, bx1) - max(ax0, bx0), min(az1, bz1) - max(az0, bz0))
gap0 = {(i, j): gap(B[i], B[j]) for i in top for j in top if i < j}
rings = []
for zi, (x0, z0, x1, z1) in enumerate(M['zones']):
    rings += [(zi, 'W', [x0, z0, x0 + RW, z1]), (zi, 'E', [x1 - RW, z0, x1, z1]), (zi, 'N', [x0, z0, x1, z0 + RW]), (zi, 'S', [x0, z1 - RW, x1, z1])]
moved = []
# 옮긴 건물에 밀려 이웃과의 골목이 좁아졌으면(원래 간격과 2칸 중 작은 쪽보다) 그 이웃도 같은 쪽으로 밀어 준다 — 길에 닿지 않는 한에서 차례로
def shift(i, dx, dz):
    for j, c in enumerate(B):
        if j == i or c.get('parent') == i: c['x'] = round(c['x'] + dx, 2); c['z'] = round(c['z'] + dz, 2)
dirs = {}
for i in top:
    b = B[i]; dx = dz = 0.0
    for zi, side, r in rings:
        if b['zone'] != zi: continue
        bx0, bz0, bx1, bz1 = rect(b)
        if min(bx1, r[2] + CL) - max(bx0, r[0] - CL) <= 0 or min(bz1, r[3] + CL) - max(bz0, r[1] - CL) <= 0: continue
        if side == 'W': dx = max(dx, r[2] + CL - bx0)
        if side == 'E': dx = min(dx, r[0] - CL - bx1)
        if side == 'N': dz = max(dz, r[3] + CL - bz0)
        if side == 'S': dz = min(dz, r[1] - CL - bz1)
    if dx or dz:
        dx, dz = round(dx + (0.01 if dx > 0 else -0.01 if dx < 0 else 0), 2), round(dz + (0.01 if dz > 0 else -0.01 if dz < 0 else 0), 2)
        shift(i, dx, dz); moved.append([b['t'], b['zone'], dx, dz, i]); dirs[i] = (dx, dz)
queue = list(dirs.items()); pushed = []
while queue:
    i, (dx, dz) = queue.pop(0)
    for j in top:
        if j == i or B[j]['zone'] != B[i]['zone']: continue
        key = (min(i, j), max(i, j)); T = min(gap0[key], 2.0); g = gap(B[i], B[j])
        if g >= T - 1e-6: continue
        ax0, az0, ax1, az1 = rect(B[i]); bx0, bz0, bx1, bz1 = rect(B[j])
        gx = max(bx0 - ax1, ax0 - bx1, 0); gz = max(bz0 - az1, az0 - bz1, 0)
        if gz == 0 and gx > 0 or (gx > 0 and gz > 0 and gx >= gz) or (gx == 0 and gz == 0 and abs(dx) >= abs(dz)):   # 옆으로 나란한 사이 → x로, 위아래 사이 → z로
            need = (max(T * T - gz * gz, 0) ** 0.5) - gx; sx = (1 if B[j]['x'] > B[i]['x'] else -1) * round(need + 0.01, 2); sz = 0.0
        else:
            need = (max(T * T - gx * gx, 0) ** 0.5) - gz; sz = (1 if B[j]['z'] > B[i]['z'] else -1) * round(need + 0.01, 2); sx = 0.0
        if need <= 0: continue
        shift(j, sx, sz); pushed.append((B[j]['t'], B[j]['zone'], sx, sz, '←', B[i]['t'])); queue.append((j, (sx, sz)))
        assert len(pushed) < 200
print('길에 걸려 옮긴 건물', len(moved)); [print('  ', m[:4]) for m in moved]
print('이웃에 밀려 옮긴 건물', len(pushed)); [print('  ', m) for m in pushed]
bad = 0
for (i, j), g0 in gap0.items():
    g1 = gap(B[i], B[j])
    if g1 < GAP_MIN and g1 < g0 - 1e-6: bad += 1; print('  간격 좁아짐', B[i]['t'], B[j]['t'], (B[i]['x'], B[i]['z']), (B[j]['x'], B[j]['z']), round(g0, 2), '→', round(g1, 2))
roads0 = [list(r) for r in M['roads']]
for i in top:
    for r in roads0 + [x[2] for x in rings]:
        bx0, bz0, bx1, bz1 = rect(B[i])
        ox, oz = min(bx1, r[2]) - max(bx0, r[0]), min(bz1, r[3]) - max(bz0, r[1])
        if ox > 0.01 and oz > 0.01: bad += 1; print('  길 위 건물', B[i]['t'], (B[i]['x'], B[i]['z']), r, round(min(ox, oz), 2))
print('문제', bad, ' 가장 좁은 건물 사이', round(min(gap(B[i], B[j]) for i in top for j in top if i < j), 2), '(전', round(min(gap0.values()), 2), ')')
M['roads'] = roads0 + [[round(v, 2) for v in r] for _, _, r in rings]
M['ring'] = RW
json.dump(M, open('map.json', 'w'), ensure_ascii=False, separators=(',', ':'))
