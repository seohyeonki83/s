# c120: 한 파일에 큰 맵·작은 맵 — 시작하면 맵 선택이 먼저 뜬다 · 테이저건 최우선 대상 = 변이 좀비가 될 사람(분홍)
import json, pprint
S = open('c119.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
old = [l for l in S.split('\n') if l.startswith('  const CH_MAP = ')]; assert len(old) == 1
i = old[0].index('{'); j = old[0].rindex('}'); big = old[0][i:j + 1]; tail = old[0][j + 1:]
small = json.dumps(json.load(open('map_s1.json', encoding='utf8')), ensure_ascii=False, separators=(',', ':'))
PICK = r'''  // ── c120: 맵 선택 — 시작하면 먼저 고른다 (큰 맵: 구역 4개 · 작은 맵: 구역 하나). 고른 뒤에 나머지가 만들어진다 ──
  const CH_SMALL = (window.__map || await new Promise((res) => {
    const ov = document.createElement('div');
    ov.style.cssText = 'position:fixed;inset:0;z-index:1000;background:#0e1014;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;font-family:system-ui,-apple-system,sans-serif;color:#fff;padding:24px;box-sizing:border-box';
    ov.innerHTML = '<div style="font-size:26px;font-weight:900;letter-spacing:1px">맵 선택</div>';
    for (const [k, name, sub] of [['b', '큰 맵', '구역 4개 · 다리와 산길 · 랜드마크 9'], ['s', '작은 맵', '구역 1개 · 사방이 산 · 랜드마크 2']]) {
      const bt = document.createElement('button');
      bt.style.cssText = 'width:min(300px,80vw);padding:18px 16px;border-radius:16px;border:2px solid #3a4250;background:#1b2028;color:#fff;font:inherit;text-align:center;touch-action:manipulation;-webkit-tap-highlight-color:transparent';
      bt.innerHTML = '<div style="font-size:22px;font-weight:900">' + name + '</div><div style="margin-top:6px;font-size:13px;color:#9aa6b8">' + sub + '</div>';
      bt.addEventListener('click', () => { ov.remove(); res(k); });
      ov.appendChild(bt);
    }
    document.body.appendChild(ov);
  })) === 's';
  { const v = document.getElementById('ver'); if (v) v.textContent = v.textContent.replace('챕터', CH_SMALL ? '작은 맵' : '큰 맵'); }
'''
R.append((old[0], PICK + '  const CH_MAP = CH_SMALL ? ' + small + ' : ' + big + tail))
rep("CH_GANG = 48, CH_COPS = 20, CH_ROOM = 45;", "CH_GANG = CH_SMALL ? 8 : 48, CH_COPS = CH_SMALL ? 3 : 20, CH_ROOM = 45;   /* c120: 작은 맵은 구역 하나 몫 */")
rep("  const CH_WHITE_OUT = 81, CH_YELLOW_OUT = 36;", "  const CH_WHITE_OUT = CH_SMALL ? 14 : 81, CH_YELLOW_OUT = CH_SMALL ? 6 : 36;")
rep("    for (let n = 24; n > 0; n--) { let r = Math.random() * ws", "    for (let n = CH_SMALL ? 4 : 24; n > 0; n--) { let r = Math.random() * ws")
rep("        cand.push({ c, k: DANGER(c), d });", "        cand.push({ c, k: CHAPTER && c.boss ? 99 : DANGER(c), d });   /* c120: 변이 좀비가 될 사람(분홍)이 맨 먼저 — 저격수보다 위 */")
open('c120_patch.py', 'w', encoding='utf8').write('# c120: 맵 선택(큰 맵·작은 맵) 한 파일 · 테이저건 최우선 = 분홍 (gen_c120.py가 만든다)\nC120_R = ' + pprint.pformat(R, width=10**7) + '\n')
print('replacements', len(R))
