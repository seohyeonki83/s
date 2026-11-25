import pathlib
s = pathlib.Path('c465.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
# 맵 선택 — 버튼 높이 약 3분의 1 줄이고 간격도 줄임 · 넘치면 스크롤
rep("justify-content:center;gap:18px;font-family:system-ui,-apple-system,sans-serif;color:#fff;padding:24px;box-sizing:border-box'",
    "justify-content:flex-start;gap:8px;font-family:system-ui,-apple-system,sans-serif;color:#fff;padding:16px 24px;box-sizing:border-box;overflow-y:auto;-webkit-overflow-scrolling:touch'   /* c466: 간격 18 → 8 · 넘치면 스크롤 */")
rep("bt.style.cssText = 'width:min(300px,80vw);padding:18px 16px;", "bt.style.cssText = 'flex:none;width:min(300px,80vw);padding:9px 16px;")
rep("'<div style=\"font-size:22px;font-weight:900\">' + name + '</div><div style=\"margin-top:6px;font-size:13px;color:#9aa6b8\">' + sub + '</div>'",
    "'<div style=\"font-size:19px;font-weight:900\">' + name + '</div><div style=\"margin-top:3px;font-size:12px;color:#9aa6b8\">' + sub + '</div>'")
rep("    document.body.appendChild(ov);\n  }));", "    ov.firstChild.style.marginTop = 'auto'; ov.lastChild.style.marginBottom = 'auto';   // c466: 가운데 정렬하되 넘치면 위부터\n    document.body.appendChild(ov);\n  }));")
# 적 테스트 — 경찰 · 군인이 나를 쫓아오던 것 끔
rep("    } else if (c.police && !c.station && !c.post && isZombie(me)) {", "    } else if (c.police && !c.station && !c.post && isZombie(me) && !CH_ET) {   /* c466: 적 테스트는 안 쫓는다 */")
pathlib.Path('c466_patch.py').write_text('C466_R = ' + repr(R) + '\n')
