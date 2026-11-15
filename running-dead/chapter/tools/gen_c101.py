# c101: 현금 수송차에서는 경찰 1명 + 빨강 또는 주황 1명이 내린다
import pprint
S = open('c100.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("if (loot === 'cash') { who.length = 0; who.push('guard', 'guard'); }", "if (loot === 'cash') { who.length = 0; who.push('police', Math.random() < 0.5 ? 'vig' : 'attacker'); }   /* c101: 현금 수송차 = 경찰 1 + 빨강 또는 주황 1 (전엔 노랑 둘) */")
rep("  function chPut(x, z, area, type, B) {\n    if (Math.random() < 0.1) type =", "  let chExact = false;                        // c101: 색을 한 단계 낮추지 않고 말한 그대로 만든다 (현금 수송차에서 내리는 사람)\n  function chPut(x, z, area, type, B) {\n    if (!chExact && Math.random() < 0.1) type =")
rep("      const c = chPut(x, z, chSideArea(x, z), w, null); c.sleep = false; c.met = true; c.tick = 0; c.fromCar = true;", "      chExact = car.loot === 'cash'; const c = chPut(x, z, chSideArea(x, z), w, null); chExact = false; c.sleep = false; c.met = true; c.tick = 0; c.fromCar = true;")
open('c101_patch.py', 'w', encoding='utf8').write('# c101: 현금 수송차에서는 경찰 1명 + 빨강 또는 주황 1명이 내린다 (gen_c101.py가 만든다)\nC101_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
