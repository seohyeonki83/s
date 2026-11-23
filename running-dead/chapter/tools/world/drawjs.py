# gen9.js가 만든 맵 데이터(json)를 그림으로 — 게임이 읽는 데이터 그대로 그린다
import json, sys
from PIL import Image, ImageDraw
W = json.load(open(sys.argv[1])); mm = W['mm']; S = float(sys.argv[3]) if len(sys.argv) > 3 else 2.2; P = 8
img = Image.new('RGB', (int((mm['x1'] - mm['x0']) * S) + 2 * P, int((mm['z1'] - mm['z0']) * S) + 2 * P), (20, 20, 24)); d = ImageDraw.Draw(img)
T = lambda x, z: (P + (x - mm['x0']) * S, P + (z - mm['z0']) * S)
R = lambda r, **k: d.rectangle([T(r[0], r[1]), T(r[2], r[3])], **k)
COL = dict(police=(70, 110, 200), army=(110, 120, 70), fire=(200, 70, 60), hospital=(240, 240, 240), mart=(230, 140, 50), bank=(60, 160, 100), gym=(170, 80, 160), library=(120, 80, 40), conv=(230, 200, 60), store=(140, 120, 100), house=(200, 185, 160), room=(235, 225, 205), jail=(90, 90, 100))
ACOL = dict(park=(120, 180, 110), gas=(230, 210, 120), site=(170, 130, 90), court=(210, 120, 70))
for r in W['rivers']: R(r, fill=(52, 110, 160), outline=(40, 90, 135))
for b in W['b']:
    if b['t'] == 'hill': R([b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2], fill=(62, 90, 54), outline=(50, 74, 44))
for z in W['zones']: R(z, fill=(175, 175, 170))
for l in W['lots']: R(l, fill=(200, 192, 170))
for a in W['areas']: R(a['r'], fill=ACOL.get(a['k'], (150, 150, 150)))
for q in W['roads']: R(q, fill=(105, 105, 105))
for br in W['bridges']: R(br[:4], fill=(141, 124, 102), outline=(255, 220, 80))
for b in W['b']:
    if b['t'] == 'hill': continue
    r = [b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2]; R(r, fill=COL.get(b['t'], (180, 160, 140)), outline=(40, 40, 40))
    for sd in b['doors'] + b.get('open', []):
        cx, cz = b['x'], b['z']
        if sd == 'n': cz -= b['d'] / 2
        if sd == 's': cz += b['d'] / 2
        if sd == 'w': cx -= b['w'] / 2
        if sd == 'e': cx += b['w'] / 2
        x, y = T(cx, cz); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 60, 60))
for p in W['props']: x, y = T(p[1], p[2]); d.point((x, y), fill=(30, 30, 30))
for n in W['net']:
    for e in n['edges']: a, b = n['nodes'][e[0]], n['nodes'][e[1]]; d.line([T(*a), T(*b)], fill=(255, 255, 255), width=1)
for i in W['startZ']: R(W['zones'][i], outline=(255, 60, 60), width=3)
img.save(sys.argv[2]); print(img.size)
