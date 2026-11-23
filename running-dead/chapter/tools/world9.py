# 본 맵 미리보기 — 큰 맵(map_m1: 일자 건널목) 단락 4개를 재료로, 그룹(큰 2 + 작은 2)을 랜덤으로 돌리고 뒤집고 섞어 9개를 붙인다
import json, random, sys
from PIL import Image, ImageDraw, ImageFont
M = json.load(open('../map_m1.json'))
GAP = 13.0; RW = M['ring']
F = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 18); FS = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 13)
def inside(r, q): return q[0] <= (r[0] + r[2]) / 2 <= q[2] and q[1] <= (r[1] + r[3]) / 2 <= q[3]
# 단락 재료 (단락 기준 좌표 0..w, 0..h)
SRC = []
for zi, Z in enumerate(M['zones']):
    x0, z0, x1, z1 = Z; w, h = x1 - x0, z1 - z0
    loc = lambda r: [r[0] - x0, r[1] - z0, r[2] - x0, r[3] - z0]
    bl = [(b['t'], loc([b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2])) for b in M['b'] if b.get('zone') == zi and b['t'] not in ('hill',)]
    rd = [loc([max(r[0], x0), max(r[1], z0), min(r[2], x1), min(r[3], z1)]) for r in M['roads'] if r[0] < x1 and r[2] > x0 and r[1] < z1 and r[3] > z0]
    ar = [(a['k'], loc(a['r'])) for a in M['areas'] if inside(a['r'], Z)]
    lt = [loc(l) for l in M['lots'] if inside(l, Z)]
    SRC.append(dict(w=w, h=h, big=h > 60, b=bl, roads=rd, areas=ar, lots=lt))
def orient(rect, w, h, k, f):          # 단락 안 네모를 돌리고(k × 90°) 뒤집는다(f) — 돌린 뒤 크기도 돌려준다
    pts = [(rect[0], rect[1]), (rect[2], rect[3])]
    out = []
    for u, v in pts:
        if f: u = w - u
        W, H = w, h
        for _ in range(k): u, v, W, H = H - v, u, H, W
        out.append((u, v))
    return [min(out[0][0], out[1][0]), min(out[0][1], out[1][1]), max(out[0][0], out[1][0]), max(out[0][1], out[1][1])]
def odim(w, h, k): return (h, w) if k % 2 else (w, h)
def make_world(seed):
    rnd = random.Random(seed)
    groups = []
    for g in range(9):
        kinds = [0, 1, 2, 3]; rnd.shuffle(kinds)   # 2×2 칸에 단락을 섞어 놓는다
        zs = []
        for s, si in enumerate(kinds):
            k, f = rnd.randrange(4), rnd.randrange(2); W, H = odim(SRC[si]['w'], SRC[si]['h'], k)
            zs.append(dict(si=si, k=k, f=f, W=W, H=H, slot=(s // 2, s % 2)))
        cw = [max(z['W'] for z in zs if z['slot'][1] == c) for c in (0, 1)]; rh = [max(z['H'] for z in zs if z['slot'][0] == r) for r in (0, 1)]
        for z in zs:   # 칸 안에서 그룹 가운데 쪽으로 붙인다 (안쪽 틈이 13이 되게)
            r, c = z['slot']; z['ox'] = (cw[0] - z['W']) if c == 0 else cw[0] + GAP; z['oz'] = (rh[0] - z['H']) if r == 0 else rh[0] + GAP
        groups.append(dict(zs=zs, W=cw[0] + GAP + cw[1], H=rh[0] + GAP + rh[1]))
    CW = [max(groups[r * 3 + c]['W'] for r in range(3)) for c in range(3)]; RH = [max(groups[r * 3 + c]['H'] for c in range(3)) for r in range(3)]
    X = [0, CW[0] + GAP, CW[0] + CW[1] + 2 * GAP]; Zr = [0, RH[0] + GAP, RH[0] + RH[1] + 2 * GAP]
    zones = []
    for gi, G in enumerate(groups):
        r, c = gi // 3, gi % 3
        gx = X[c] + (CW[c] - G['W'] if c == 0 else 0 if c == 2 else (CW[c] - G['W']) / 2)   # 가운데 쪽으로 붙인다
        gz = Zr[r] + (RH[r] - G['H'] if r == 0 else 0 if r == 2 else (RH[r] - G['H']) / 2)
        G['x'], G['z'] = gx, gz
        for z in G['zs']: z['g'] = gi; z['x0'] = gx + z['ox']; z['z0'] = gz + z['oz']; z['x1'] = z['x0'] + z['W']; z['z1'] = z['z0'] + z['H']; zones.append(z)
    # 건널목: 마주 보는 단락 변 사이 (틈 13 ~ 45, 사이에 다른 단락 없음), 겹치는 길이 14 이상
    cap = {}
    for i, z in enumerate(zones):
        for s in 'NSWE': cap[(i, s)] = 1 if not SRC[z['si']]['big'] else rnd.choice((1, 2))
    used = {k: [] for k in cap}
    pairs = []
    for i, a in enumerate(zones):
        for j, b in enumerate(zones):
            if j <= i: continue
            for (p, q, sa, sb, ax) in ((a, b, 'E', 'W', 'x'), (b, a, 'E', 'W', 'x'), (a, b, 'S', 'N', 'z'), (b, a, 'S', 'N', 'z')):
                if ax == 'x': g = q['x0'] - p['x1']; lo, hi = max(p['z0'], q['z0']), min(p['z1'], q['z1'])
                else: g = q['z0'] - p['z1']; lo, hi = max(p['x0'], q['x0']), min(p['x1'], q['x1'])
                if not (GAP - 0.01 <= g <= 45) or hi - lo < 14: continue
                blk = False
                for o in zones:
                    if o is p or o is q: continue
                    if ax == 'x' and o['x0'] < q['x0'] and o['x1'] > p['x1'] and o['z0'] < hi and o['z1'] > lo: blk = True
                    if ax == 'z' and o['z0'] < q['z0'] and o['z1'] > p['z1'] and o['x0'] < hi and o['x1'] > lo: blk = True
                if blk: continue
                pi, qi = zones.index(p), zones.index(q)
                pairs.append((pi, qi, sa, sb, ax, g, lo, hi))
    rnd.shuffle(pairs)
    pairs.sort(key=lambda t: zones[t[0]]['g'] == zones[t[1]]['g'])   # 그룹끼리 잇는 것부터 (연결 보장)
    par = list(range(len(zones)))
    def fd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    cross = []
    for (pi, qi, sa, sb, ax, g, lo, hi) in pairs:
        n = min(cap[(pi, sa)] - len(used[(pi, sa)]), cap[(qi, sb)] - len(used[(qi, sb)]))
        if n <= 0: continue
        n = min(n, 2 if hi - lo >= 50 else 1)
        if fd(pi) == fd(qi) and rnd.random() < 0.35: n = 0   # 이미 이어진 곳은 가끔 비워 둔다
        for _ in range(n):
            for t in range(30):
                u = rnd.uniform(lo + 7, hi - 7)
                if all(abs(u - v) >= 24 for v in used[(pi, sa)] + used[(qi, sb)]): break
            else: continue
            used[(pi, sa)].append(u); used[(qi, sb)].append(u); par[fd(pi)] = fd(qi)
            p, q = zones[pi], zones[qi]
            cross.append(((p['x1'], u - 4, q['x0'], u + 4) if ax == 'x' else (u - 4, p['z1'], u + 4, q['z0']), g))
    ok = len({fd(i) for i in range(len(zones))}) == 1
    # 시작: 가운데 그룹의 단락 하나, 그 순환도로 위 아무 자리
    c4 = [z for z in zones if z['g'] == 4]; zs = rnd.choice(c4)
    t = rnd.random(); side = rnd.randrange(4); m = RW / 2
    sx = zs['x0'] + m + t * (zs['W'] - 2 * m) if side < 2 else (zs['x0'] + m if side == 2 else zs['x1'] - m)
    sz = (zs['z0'] + m if side == 0 else zs['z1'] - m) if side < 2 else zs['z0'] + m + t * (zs['H'] - 2 * m)
    Wt, Ht = X[2] + CW[2], Zr[2] + RH[2]
    return dict(zones=zones, groups=groups, cross=cross, ok=ok, start=(sx, sz), W=Wt, H=Ht)
COL = dict(police=(70, 110, 200), army=(110, 120, 70), fire=(200, 70, 60), hospital=(240, 240, 240), mart=(230, 140, 50), bank=(60, 160, 100), gym=(170, 80, 160), library=(120, 80, 40), conv=(230, 200, 60), store=(140, 120, 100), house=(200, 185, 160), room=(220, 210, 190), jail=(90, 90, 100))
ACOL = dict(park=(120, 180, 110), gas=(230, 210, 120), site=(170, 130, 90), court=(210, 120, 70))
def draw(Wd, path, seed):
    S = 2.4; P = 14; img = Image.new('RGB', (int(Wd['W'] * S) + 2 * P, int(Wd['H'] * S) + 2 * P + 30), (74, 110, 66)); d = ImageDraw.Draw(img)
    T = lambda x, z: (P + x * S, P + 30 + z * S)
    R = lambda r, **k: d.rectangle([T(r[0], r[1]), T(r[2], r[3])], **k)
    for (r, g) in Wd['cross']: R(r, fill=(150, 120, 80))
    for z in Wd['zones']:
        Z = SRC[z['si']]; ox, oz = z['x0'], z['z0']
        tr = lambda q: (lambda o: [o[0] + ox, o[1] + oz, o[2] + ox, o[3] + oz])(orient(q, Z['w'], Z['h'], z['k'], z['f']))
        R([z['x0'], z['z0'], z['x1'], z['z1']], fill=(175, 175, 170))
        for l in Z['lots']: R(tr(l), fill=(200, 192, 170))
        for (k, a) in Z['areas']: R(tr(a), fill=ACOL.get(k, (150, 150, 150)))
        for q in Z['roads']: R(tr(q), fill=(105, 105, 105))
        for (t, q) in Z['b']: R(tr(q), fill=COL.get(t, (180, 160, 140)), outline=(40, 40, 40))
        R([z['x0'], z['z0'], z['x1'], z['z1']], outline=(255, 255, 255) if Z['big'] else (255, 230, 120), width=2)
    for (r, g) in Wd['cross']: R(r, outline=(255, 220, 80), width=2)
    for gi, G in enumerate(Wd['groups']):
        x0, y0 = T(G['x'], G['z']); x1, y1 = T(G['x'] + G['W'], G['z'] + G['H'])
        for xx in range(int(x0), int(x1), 14): d.line([(xx, y0 - 4), (xx + 7, y0 - 4)], fill=(255, 255, 255), width=2); d.line([(xx, y1 + 4), (xx + 7, y1 + 4)], fill=(255, 255, 255), width=2)
        for yy in range(int(y0), int(y1), 14): d.line([(x0 - 4, yy), (x0 - 4, yy + 7)], fill=(255, 255, 255), width=2); d.line([(x1 + 4, yy), (x1 + 4, yy + 7)], fill=(255, 255, 255), width=2)
        d.text((x0 + 6, y0 + 4), f'그룹 {gi + 1}' + (' (시작)' if gi == 4 else ''), fill=(255, 255, 255), font=F, stroke_width=3, stroke_fill=(0, 0, 0))
    sx, sy = T(*Wd['start']); d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(255, 40, 40), outline=(255, 255, 255), width=3)
    d.text((P, 6), f'본 맵 미리보기 #{seed} · 단락 36 · 건널목 {len(Wd["cross"])} · 크기 {Wd["W"]:.0f}×{Wd["H"]:.0f} · ' + ('전부 이어짐' if Wd['ok'] else '끊긴 곳 있음') + ' · 흰 테두리 = 큰 단락, 노란 테두리 = 작은 단락, 빨간 점 = 시작', fill=(255, 255, 255), font=FS)
    img.save(path); return img.size
for i, seed in enumerate(range(int(sys.argv[1]), int(sys.argv[1]) + int(sys.argv[2]))):
    s = seed
    while True:
        W = make_world(s)
        if W['ok']: break
        s += 1000
    print(seed, '->', s, draw(W, f'/home/user/s/running-dead/chapter/shots/world9_{i + 1:02d}.png', s), len(W['cross']), round(W['W']), round(W['H']))
