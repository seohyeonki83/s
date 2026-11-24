# c429: 현금 사거리 — ★0을 1로 두고 강화마다 1.4/12씩 (흰 ★6 = 1.7배). 다이아몬드는 빨간 별에서도 계속 (빨간 ★6 = 2.4배), 금은 1.7배에서 멈춘다
#        다이아몬드 빨간 별 = 공격할 수 있는 인간이 싸우는 쪽으로 바뀔 확률 (★1 17% … ★6 100%). 유혹 시간은 늘지 않는다
src = open('c428.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  const cashK = () => 1.2 + Math.min(6, lv('cash')) * 1.56 / 7.2;   /* c428: 흰 ★6에서 멈춘다 */",
    "  const chCashStep = (n) => 1 + 1.4 / 12 * n;   // c429: 현금 사거리 배율 (★0 = 1 · 흰 ★6 = 1.7 · 다이아몬드 빨간 ★6 = 2.4)\n  const cashK = () => CHAPTER ? 1.2 * chCashStep(chBr.cash === 'dia' ? lv('cash') : Math.min(6, lv('cash'))) : 1.2 + lv('cash') * 1.56 / 7.2;   /* c429 */")
rep("알아채는 거리 ${(8.64 + 1.56 * n).toFixed(1)}칸`", "알아채는 거리 ${(8.64 * chCashStep(Math.min(6, n))).toFixed(1)}칸`   /* c429 */")
rep("line: (r) => `유혹(싸우는) 시간 +${5 * r}%`, short: ['싸움', (r) => `+${5 * r}%`] },", "line: (r) => `서로 싸울 확률 ${Math.round(100 * r / 6)}% · 알아채는 거리 ${(8.64 * chCashStep(6 + r)).toFixed(1)}칸`, short: ['싸움', (r) => `${Math.round(100 * r / 6)}%`] },   /* c429 */")
rep("  const chDiaK = () => 1 + 0.05 * chBrR('cash', 'dia');", "  const chDiaK = () => 1;   // c429: 다이아몬드도 유혹 시간은 그대로")
rep("  function enterLured(c) { c.state = 'lured';", "  function enterLured(c) { c.diaF = CHAPTER && chBr.cash === 'dia' && c.maxHp > 0 && Math.random() < chBrR('cash', 'dia') / 6;   /* c429: 다이아몬드 — 싸우는 쪽으로 바뀔 확률 */ c.state = 'lured';")
rep("if (CHAPTER && chBr.cash === 'dia' && c.maxHp > 0 && c.hp > 0 && chDiaFight(c, dt)) return;", "if (CHAPTER && chBr.cash === 'dia' && c.diaF && c.maxHp > 0 && c.hp > 0 && chDiaFight(c, dt)) return;")
open('c429_patch.py', 'w').write("# c429: 현금 사거리 · 다이아몬드 싸울 확률\nC429_R = " + repr(R) + "\n")
