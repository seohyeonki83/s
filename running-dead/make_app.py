"""러닝데드 — 폰 홈 화면에서 전체 화면으로 여는 앱 버전 만들기.

사용: python3 make_app.py v127.html
     python3 make_app.py chapter/c6.html chapter/app "러닝데드 챕터"   (나갈 폴더와 앱 이름을 따로 줄 수 있다)
  → app/index.html (전체 화면용 머리말을 붙인 게임), app/manifest.webmanifest, app/icon-*.png
app 폴더를 그대로 공개 주소(예: GitHub Pages)에 올리고, 아이폰 Safari에서 열어 '공유 → 홈 화면에 추가'.
"""
import json
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
src = here / sys.argv[1]
out = here / (sys.argv[2] if len(sys.argv) > 2 else 'app')
NAME = sys.argv[3] if len(sys.argv) > 3 else '러닝데드'
out.mkdir(exist_ok=True)

s = src.read_text(encoding='utf8')
rest = s[s.index('<body>') + len('<body>'):]                       # 아티팩트용 머리말은 버리고 본문만
rest = rest.replace('<title>러닝데드 이동 테스트</title>\n', '', 1)
head = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{NAME}">
<meta name="theme-color" content="#1f1f23">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
<title>{NAME}</title>
<style>html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; background: #1f1f23; -webkit-text-size-adjust: 100%; }</style>
</head>
<body>"""
(out / 'index.html').write_text(head.replace('{NAME}', NAME) + rest, encoding='utf8')

manifest = {
    'name': NAME, 'short_name': NAME, 'start_url': './', 'scope': './',
    'display': 'fullscreen', 'orientation': 'portrait',
    'background_color': '#1f1f23', 'theme_color': '#1f1f23',
    'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
}
(out / 'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')

try:                                                                 # 아이콘 — 짙은 바탕에 파란 나 + 연파랑 동료 셋
    from PIL import Image, ImageDraw
    def icon(n):
        k = 4; S = n * k
        im = Image.new('RGB', (S, S), (31, 31, 35) if NAME == '러닝데드' else (30, 52, 38)); d = ImageDraw.Draw(im)   # 챕터 앱은 바탕을 짙은 초록으로 (홈 화면에서 구분)
        def dot(cx, cy, r, c): d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=c)
        for cx, cy in ((0.27, 0.66), (0.5, 0.74), (0.73, 0.66)): dot(cx, cy, 0.105, (138, 164, 245))
        dot(0.5, 0.42, 0.2, (51, 102, 242))
        return im.resize((n, n), Image.LANCZOS)
    for n in (180, 192, 512): icon(n).save(out / f'icon-{n}.png')
except ImportError:
    print('PIL이 없어서 아이콘은 건너뜀')
print(str(out.relative_to(here)) + '/ 만듦:', sorted(p.name for p in out.iterdir()))
