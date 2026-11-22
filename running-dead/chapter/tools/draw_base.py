import json, sys
from PIL import Image, ImageDraw, ImageFont
S = json.load(open(sys.argv[1])); OUT = sys.argv[2]
K = 16; PAD = 10; mm = S['mm']; W = int((mm['x1'] - mm['x0']) * K) + 2 * PAD + 150; H = int((mm['z1'] - mm['z0']) * K) + 2 * PAD + 40
img = Image.new('RGB', (W, H), (250, 250, 247)); d = ImageDraw.Draw(img)
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'; f = ImageFont.truetype(F, 15); fs = ImageFont.truetype(F, 11); fb = ImageFont.truetype(F, 18)
P = lambda x, z: (PAD + (x - mm['x0']) * K, PAD + 30 + (z - mm['z0']) * K)
R = lambda r, **k: d.rectangle([P(r[0], r[1]), P(r[2], r[3])], **k)
d.text((PAD, 6), '거점 맵 배치도 (c358) · 위 = 북쪽', fill=(30, 30, 30), font=fb)
NAME = dict(police='경찰서 (거점)', bank='은행', gym='헬스장', mart='마트', hospital='병원', store='창고', house='집', jail='유치장', room='방')
for b in S['b']:
    if b['t'] == 'hill': R([b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2], fill=(150, 175, 130))
for r in S['roads']: R(r, fill=(120, 120, 120))
for l in S['lots']: R(l, fill=(205, 200, 185), outline=(140, 135, 120)); d.text(P(l[0] + 0.4, l[1] + 0.3), '주차장', fill=(70, 70, 60), font=f)
AC = dict(park=((150, 205, 140), '공원'), gas=((235, 215, 160), '주유소'), site=((190, 150, 105), '공사 현장'))
for A in S['areas']:
    c, n = AC[A['k']]; R(A['r'], fill=c, outline=(90, 90, 90)); d.text(P(A['r'][0] + 0.4, A['r'][1] + 0.3), n, fill=(40, 40, 40), font=f)
LC = dict(police=(70, 110, 200), house=(225, 215, 195))
for b in S['b']:
    if b['t'] == 'hill': continue
    r = [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]
    inner = b['t'] in ('room', 'jail')
    R(r, fill=(250, 235, 210) if inner else LC.get(b['t'], (240, 190, 140)), outline=(60, 60, 60), width=1 if inner else 2)
    # 정문 표시
    for s in b['doors'][:1] if not inner else []:
        x0, y0 = P(r[0], r[1]); x1, y1 = P(r[2], r[3]); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        q = dict(n=[cx - 12, y0 - 2, cx + 12, y0 + 2], s=[cx - 12, y1 - 2, cx + 12, y1 + 2], w=[x0 - 2, cy - 12, x0 + 2, cy + 12], e=[x1 - 2, cy - 12, x1 + 2, cy + 12])[s]
        d.rectangle(q, fill=(220, 40, 40))
    t = NAME.get(b['t'], b['t']); fn = fs if inner or b['t'] == 'house' else f
    tw = d.textlength(t, font=fn); cx, cy = P(b['x'], b['z']); d.text((cx - tw / 2, cy - 8), t, fill=(255, 255, 255) if b['t'] == 'police' else (30, 30, 30), font=fn)
for p in S['props']:
    x, y = P(p[1], p[2]); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(90, 90, 160))
for sp in S['spots']:
    a = sp.get('at') or sp['ring'][:2]; x, y = P(*a); d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(200, 0, 160), width=2)
x, y = P(*S['start']); d.polygon([(x, y - 9), (x - 8, y + 6), (x + 8, y + 6)], fill=(20, 120, 255)); d.text((x + 10, y - 8), '시작', fill=(20, 80, 200), font=f)
# 가운데 세로 골목
zs = S['zones'][0]; cxm = (zs[0] + zs[2]) / 2; d.line([P(cxm, zs[1] + 6), P(cxm, zs[3] - 6)], fill=(255, 140, 0), width=2)
# 범례
lx = W - 145; ly = 50
for c, t in [((70, 110, 200), '거점 (경찰서)'), ((240, 190, 140), '랜드마크'), ((225, 215, 195), '집'), ((250, 235, 210), '방 · 유치장'), ((120, 120, 120), '8자 순환도로'), ((150, 175, 130), '산'), ((220, 40, 40), '정문')]:
    d.rectangle([lx, ly, lx + 16, ly + 14], fill=c, outline=(60, 60, 60)); d.text((lx + 22, ly - 1), t, fill=(30, 30, 30), font=fs); ly += 22
d.ellipse([lx + 4, ly + 3, lx + 10, ly + 9], fill=(90, 90, 160)); d.text((lx + 22, ly - 1), '길거리 사물', fill=(30, 30, 30), font=fs); ly += 22
d.ellipse([lx + 2, ly + 1, lx + 14, ly + 13], outline=(200, 0, 160), width=2); d.text((lx + 22, ly - 1), '사람 모이는 곳', fill=(30, 30, 30), font=fs); ly += 22
d.line([lx, ly + 7, lx + 16, ly + 7], fill=(255, 140, 0), width=2); d.text((lx + 22, ly - 1), '세로 골목', fill=(30, 30, 30), font=fs)
img.save(OUT); print(OUT, img.size)
