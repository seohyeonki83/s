# 측정용: 큰 맵(map_m1.json)을 가로·세로 N장씩 이어 붙인 임시 월드 (회전·섞기 없음 — 크기와 내용물 수만 실제 9그룹 월드와 비슷하게)
import json, copy, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
m = json.load(open('map_m1.json'))
W = m['mm']['x1'] - m['mm']['x0']; H = m['mm']['z1'] - m['mm']['z0']
PX, PZ = W + 7, H + 7        # 그룹 사이 구역 간격 13
half = N // 2
offs = [(0, 0)] + [(i, j) for j in range(-half, N - half) for i in range(-half, N - half) if (i, j) != (0, 0)]
out = copy.deepcopy(m)
NB = len(m['b']); NZ = len(m['zones'])
def rect(r, dx, dz): return [r[0] + dx, r[1] + dz, r[2] + dx, r[3] + dz]
for k in ['zones', 'roads', 'rivers', 'bridges', 'lots', 'b', 'net', 'ave', 'areas', 'props', 'spots', 'fuel', 'passes2', 'passPts', 'passes']: out[k] = []
for ci, (i, j) in enumerate(offs):
    dx, dz = i * PX, j * PZ
    for k in ['zones', 'roads', 'rivers', 'bridges', 'lots']: out[k] += [rect(r, dx, dz) for r in m[k]]
    for b in m['b']:
        b = copy.deepcopy(b); b['x'] += dx; b['z'] += dz; b['local'] += ci * NB
        if b['zone'] >= 0: b['zone'] += ci * NZ
        if 'parent' in b: b['parent'] += ci * NB
        out['b'].append(b)
    for n in m['net']: out['net'].append({'nodes': [[x + dx, z + dz] for x, z in n['nodes']], 'edges': n['edges']})
    for a in m['ave']:
        a = copy.deepcopy(a)
        if a.get('V'): a['V']['c'] += dx; a['V']['a'] += dz; a['V']['b'] += dz
        if a.get('H'): a['H']['c'] += dz; a['H']['a'] += dx; a['H']['b'] += dx
        out['ave'].append(a)
    for a in m['areas']:
        a = copy.deepcopy(a); a['r'] = rect(a['r'], dx, dz); a['zone'] += ci * NZ
        if 'can' in a: a['can'] = rect(a['can'], dx, dz); a['isl'] = [x + dx for x in a['isl']]; a['iz'] += dz
        out['areas'].append(a)
    for p in m['props']: out['props'].append([p[0], p[1] + dx, p[2] + dz] + p[3:])
    for s in m['spots']:
        s = copy.deepcopy(s); s['zone'] += ci * NZ
        if 'at' in s: s['at'] = [s['at'][0] + dx, s['at'][1] + dz]
        if 'ring' in s: s['ring'] = [s['ring'][0] + dx, s['ring'][1] + dz] + s['ring'][2:]
        out['spots'].append(s)
    for f in m['fuel']: out['fuel'].append({'zone': f['zone'] + ci * NZ, 'slots': [[x + dx, z + dz, r] for x, z, r in f['slots']]})
    for P in m['passes2']:
        P = copy.deepcopy(P); v = P['axis'] == 'v'
        P['c'] += dz if v else dx; P['ax'] += dx; P['bx'] += dx; P['az'] += dz; P['bz'] += dz; P['za'] += ci * NZ; P['zb'] += ci * NZ
        P['mid'] = dx if v else m['zrMid'] + dz
        out['passes2'].append(P)
    for P in m['passPts']: out['passPts'].append({'x': P['x'] + dx, 'z': P['z'] + dz, 'dir': P['dir']})
    for a, c in m['passes']: out['passes'].append([a, c + (dz if a == 'v' else dx)])
xs = [z[0] for z in out['zones']] + [z[2] for z in out['zones']]; zs = [z[1] for z in out['zones']] + [z[3] for z in out['zones']]
out['mm'] = {'x0': min(xs) - 3, 'z0': min(zs) - 3, 'x1': max(xs) + 3, 'z1': max(zs) + 3}
json.dump(out, open('perf/map_w%d.json' % N, 'w'), separators=(',', ':'))
print('zones', len(out['zones']), 'b', len(out['b']), 'props', len(out['props']), 'mm', out['mm'], 'size', out['mm']['x1'] - out['mm']['x0'], out['mm']['z1'] - out['mm']['z0'])
