# c109: 미는 힘이 깎이는 데를 전부 없앤다 — 나(8 · 덩치일 땐 11)·덩치(11)·히드라(4) 모두 제 힘 그대로 차·바리케이트·건물 안 네모 사물·달리는 차에 들어간다
import pprint
S = open('c108.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' && !CHAPTER ? 2 / 3 : 1), sh = isZombie(b) && !car.wreck", "          const f = CHAPTER ? (b.force || 1) : b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) && !car.wreck   /* c109: 바리케이트 — 제 힘 그대로 */")
rep("          const f = b === me || b.sniper ? 1 : (b.force || 1) * (b.mut === 'armor' && !CHAPTER ? 2 / 3 : 1),", "          const f = CHAPTER ? (isZombie(b) ? (b.force || 1) : 1) : b === me || b.sniper ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1),   /* c109: 서 있는 차 — 좀비는 제 힘 그대로 (나 8 · 덩치 11), 사람은 1 */")
rep("          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) ? f / (f + t.mass) : 0;", "          const f = CHAPTER ? (b.force || 1) : b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) ? f / (f + t.mass) : 0;   /* c109: 건물 안 네모 사물 */")
rep("  const chCarW = (b) => b.mut === 'armor' ? MY_FORCE * 1.3 * 2 / 3 : b.mut === 'hydra' ? 2 : 1;", "  const chCarW = (b) => isZombie(b) ? (b.force || 1) : 1;   /* c109: 달리는 차를 막는 무게 = 제 힘 그대로 (나 8 · 덩치 11 · 히드라 4 · 동료 1). 사람은 1 */")
open('c109_patch.py', 'w', encoding='utf8').write('# c109: 미는 힘 깎이는 곳 전부 없앰 (gen_c109.py가 만든다)\nC109_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
