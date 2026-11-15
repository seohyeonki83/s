# c88 패치 만들기 — 수비대 인원 새 표 · 바리케이트 한쪽 끝 한계를 종류별로 (바리케이트 6 · 경찰차 3)
import pprint
S = open('c87.mjs', encoding='utf8').read(); L = S.split('\n'); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
def line(prefix):
    m = [l for l in L if l.startswith(prefix)]; assert len(m) == 1, (len(m), prefix[:80]); return m[0]
rep(line("      const add = s === 1 ? { police: r2 < 0.2 ? 3 : r2 < 0.8 ? 4 : 5 } :"),
    "      const add = s === 1 ? { police: N(2, 4) } : s === 2 ? { police: N(2, 4) } : s === 3 ? { soldier: N(2, 3), sniper: N(1, 2) } : s === 4 ? { soldier: N(2, 3), sniper: N(2, 3) } : { soldier: N(3, 4), sniper: N(2, 3) };   // c88: 수상함 경찰 2~4 · 난리남 경찰 +2~4 · 개판 군인 2~3 저격수 1~2 · 계엄 군인 2~3 저격수 2~3 · 데프콘 군인 3~4 저격수 2~3 (절반으로 안 자른다)")
rep("n = chHalf(add[type] || 0); i < n; i++) {", "n = add[type] || 0; i < n; i++) {")
rep("          const live = () => X.rows[e].reduce((n, row) => n + (row || []).filter(chBarLive).length, 0);   /* c72 */",
    "          const live = (barr) => X.rows[e].reduce((n, row) => n + (row || []).filter((p) => chBarLive(p) && !!p.car.barr === barr).length, 0);   /* c72 · c88: 종류별로 센다 */")
rep("if (Math.random() < 2 / 3 && live() < CH_BAR_MAX) chBarAdd(X, e, true); if (Math.random() < 0.2 * 2 / 3 && live() < CH_BAR_MAX) chBarAdd(X, e, false); }",
    "if (Math.random() < 2 / 3 && live(true) < 6) chBarAdd(X, e, true); if (Math.random() < 0.2 * 2 / 3 && live(false) < 3) chBarAdd(X, e, false); }   /* c88: 한쪽 끝에 바리케이트 6개 · 경찰차 3대까지 */")
open('c88_patch.py', 'w', encoding='utf8').write('# c88: 수비대 인원 새 표 · 바리케이트 한계 종류별 (gen_c88.py가 만든다)\nC88_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
