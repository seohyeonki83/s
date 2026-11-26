import pathlib, re
s = pathlib.Path('c503.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
P = ['absorb', 'acid', 'acidp', 'blood', 'book', 'catalyst', 'crowbar', 'linger', 'parasite', 'rage', 'revive', 'shoes', 'teeth', 'vest', 'stim']
# 효과 계산은 lvE (장비 = 단계 ÷ 2 → 10단계가 예전 5단계와 같은 끝값)
lines = s.split('\n'); done = set()
for k in P:
    pat = "lv('%s')" % k
    for i, ln in enumerate(lines):
        if pat in ln and i not in done:
            done.add(i)
for i in sorted(done):
    ln = lines[i]; new = ln
    for k in P: new = new.replace("lv('%s')" % k, "lvE('%s')" % k)
    rep(ln, new)
rep("  const lv = (k) => CHAPTER ? (ilv[k] || 0) : up.brain;", "  const lv = (k) => CHAPTER ? (ilv[k] || 0) : up.brain;\n  const lvE = (k) => CHAPTER && k !== 'bag' && ITEM[k] && ITEM[k].passive ? lv(k) / 2 : lv(k);   // c504: 장비 효과 단계 — 장비는 10단계(흰 5 · 빨강 5)를 예전 5단계에 맞춰 반씩 쪼갠다")
import re as _re
_m = _re.search(r"const chLvMax = .*?\*/ : 5;", s); assert _m
rep(_m.group(0), _m.group(0)[:-2] + "10;   /* c504: 장비도 10단계 (가방은 3) */")
rep("  for (const k of Object.keys(CH_BRANCH)) { const S = CH_SHORT[k], f = S[1]; S[1] = (n) => { if (n <= 6) return f(n);", "  for (const k of Object.keys(CH_STAT)) if (k !== 'bag' && ITEM[k] && ITEM[k].passive) { const f = CH_STAT[k]; CH_STAT[k] = (n) => f(n / 2); }   // c504: 장비 설명 숫자도 반씩\n  for (const k of Object.keys(CH_SHORT)) if (k !== 'bag' && ITEM[k] && ITEM[k].passive) { const S = CH_SHORT[k], f = S[1]; S[1] = (n) => f(n / 2); }\n  for (const k of (false ? Object.keys(CH_BRANCH) : [])) { const S = CH_SHORT[k], f = S[1]; S[1] = (n) => { if (n <= 6) return f(n);   /* c504: 갈림길 표시 끔 (빨간 별 카드에 '갈림길'로 뜨던 것) */")
rep("      const d = MY_HP * (CHAPTER ? 0.12 : 0.10);   /* c198: 12%씩 */", "      const d = MY_HP * (CHAPTER ? 0.12 * (lv('blood') > 0 ? 0.5 : 1) : 0.10);   /* c504: 강화는 6%씩 (10단계) · c198: 12%씩 */")
pathlib.Path('c504_patch.py').write_text('C504_R = ' + repr(R) + '\n')
print(len(R))
