# c106: 덩치 무게 11 · 덩치가 차·바리케이트를 밀 때 3분의 2만 들어가던 것 없앰 · 감염시켜 얻은 덩치 체력 570
import pprint
S = open('c105.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("z.force = MY_FORCE * 1.3 + (CHAPTER ? 2 : 0);", "z.force = CHAPTER ? 11 : MY_FORCE * 1.3;   /* c106: 덩치 무게 11 */")
rep("me.force = MY_FORCE * 1.3 + (CHAPTER ? 2 : 0); }", "me.force = CHAPTER ? 11 : MY_FORCE * 1.3; }")
rep("          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) && !car.wreck", "          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' && !CHAPTER ? 2 / 3 : 1), sh = isZombie(b) && !car.wreck")
rep("          const f = b === me || b.sniper ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1),", "          const f = b === me || b.sniper ? 1 : (b.force || 1) * (b.mut === 'armor' && !CHAPTER ? 2 / 3 : 1),   /* c106: 덩치도 제 무게 그대로 차를 민다 */")
rep("    b.maxHp *= t === 'armor' ? 2 * 1.2 : 1.5; b.hp = b.maxHp;", "    if (t === 'armor') b.maxHp = 570; else b.maxHp *= 1.5;   /* c106: 얻은 덩치 체력 570 */ b.hp = b.maxHp;")
open('c106_patch.py', 'w', encoding='utf8').write('# c106: 덩치 무게 11 · 차 미는 힘 깎기 없앰 · 얻은 덩치 체력 570 (gen_c106.py가 만든다)\nC106_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
