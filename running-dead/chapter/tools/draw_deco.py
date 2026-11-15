# 꾸민 맵 그림 — map_c85.json → png (자리·사물 포함). 인자: json png [x0 z0 x1 z1 배율]
import json, sys, math
from PIL import Image, ImageDraw
sys.argv = sys.argv[:1] + sys.argv[1:]
M = json.load(open(sys.argv[1])); out = sys.argv[2]
mm = M['mm']; x0, z0, x1, z1 = (float(v) for v in sys.argv[3:7]) if len(sys.argv) > 6 else (mm['x0'], mm['z0'], mm['x1'], mm['z1'])
S = float(sys.argv[7]) if len(sys.argv) > 7 else 6
im = Image.new('RGB', (int((x1 - x0) * S), int((z1 - z0) * S)), (150, 150, 150)); dr = ImageDraw.Draw(im)
P = lambda x, z: ((x - x0) * S, (z - z0) * S)
R = lambda r, **k: dr.rectangle([P(r[0], r[1]), P(r[2], r[3])], **k)
for l in M.get('lots', []): R(l, fill=(172, 166, 150))
AC = dict(park=(96, 150, 84), gas=(190, 190, 186), court=(196, 120, 80), site=(150, 120, 86))
for a in M.get('areas', []):
    R(a['r'], fill=AC[a['k']])
    if 'can' in a: R(a['can'], outline=(200, 40, 40), width=2)
for r in M['roads']: R(r, fill=(120, 120, 120))
for p in M.get('paths', []):
    for i in range(len(p['pts']) - 1):
        a, b = p['pts'][i], p['pts'][i + 1]; dr.line([P(*a), P(*b)], fill=(120, 120, 120), width=int(p['hw'] * 2 * S))
        for (cx, cz) in (a, b): dr.ellipse([P(cx - p['hw'], cz - p['hw']), P(cx + p['hw'], cz + p['hw'])], fill=(120, 120, 120))
for h in M['rivers']: R(h, fill=(60, 120, 170))
for h in M['bridges']: R(h, fill=(150, 130, 105))
COL = {'house': (45, 42, 40), 'store': (125, 110, 90), 'bank': (46, 158, 91), 'police': (59, 111, 212), 'fire': (226, 69, 44), 'mart': (240, 138, 36), 'hospital': (244, 244, 246),
       'army': (91, 107, 47), 'library': (139, 90, 43), 'conv': (24, 166, 166), 'gym': (176, 64, 143), 'hill': (70, 100, 62), 'room': None, 'jail': None}
for b in M['b']:
    c = COL.get(b['t'], (200, 0, 200)); r = (b['x'] - b['w'] / 2, b['z'] - b['d'] / 2, b['x'] + b['w'] / 2, b['z'] + b['d'] / 2)
    if c is None: R(r, outline=(255, 255, 255)); continue
    if b.get('gas'): c = (150, 40, 34)
    R(r, fill=c, outline=None if b['t'] == 'hill' else (0, 0, 0))
    if b['t'] not in ('hill',) and b.get('doors'):
        nx, nz = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}[b['doors'][0]]; cx, cz = b['x'] + nx * b['w'] / 2, b['z'] + nz * b['d'] / 2
        dr.line([P(cx - abs(nz) * 1.3, cz - abs(nx) * 1.3), P(cx + abs(nz) * 1.3, cz + abs(nx) * 1.3)], fill=(255, 220, 60), width=3)
from map_radii import PR
PC = dict(lamp=(255, 240, 150), tlight=(60, 220, 90), bench=(150, 90, 40), cone=(255, 120, 20), pump=(230, 40, 40), pillar=(90, 90, 90), fountain=(120, 200, 255), statue=(200, 200, 210), hoop=(255, 90, 30))
for t, x, z in (q[:3] for q in M.get('props', [])):
    r = PR.get(t, .3); dr.ellipse([P(x - r, z - r), P(x + r, z + r)], fill=PC.get(t, (240, 60, 200)), outline=(0, 0, 0))
    if S >= 14: dr.text((P(x, z)[0] + r * S + 1, P(x, z)[1] - 5), t[:5], fill=(255, 255, 255))
for sp in M.get('spots', []):
    if 'at' in sp: x, z = sp['at']; rr = sp.get('rad', 0.5)
    else: x, z, rr = sp['ring'][0], sp['ring'][1], sp['ring'][3]
    dr.ellipse([P(x - rr, z - rr), P(x + rr, z + rr)], outline=(255, 255, 0), width=2)
for f in M.get('fuel', []):
    for x, z, h in f['slots']: R([x - .55, z - 1.0, x + .55, z + 1.0], outline=(0, 0, 255), width=1)
g = 10
for x in range(int(math.ceil(x0 / g) * g), int(x1) + 1, g): dr.line([P(x, z0), P(x, z1)], fill=(90, 90, 90), width=1); dr.text((P(x, z0)[0] + 2, 2), str(x), fill=(255, 255, 0))
for z in range(int(math.ceil(z0 / g) * g), int(z1) + 1, g): dr.line([P(x0, z), P(x1, z)], fill=(90, 90, 90), width=1); dr.text((2, P(x0, z)[1] + 2), str(z), fill=(255, 255, 0))
im.save(out); print(out, im.size)
