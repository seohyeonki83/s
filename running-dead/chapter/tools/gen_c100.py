# c100 패치 만들기 — 수송차 종류 비율 고정(주머니 뽑기) · 경보단계 5% 더 · 얻은 덩치 체력 2배 · 변이 줄기세포(부활 장비)
import pprint
S = open('c99.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
# 1. 수송차: 종류를 주머니에서 뽑는다 (14 → 15칸: 현금 1 · 구급 6 · 택배 8). 차가 실제로 생겼을 때만 주머니에서 뺀다 — 큰 차가 자리 검사에서 떨어져도 비율이 안 틀어진다
rep("  const chLootRoll = () => { let r = Math.random() * CH_LOOT_N / CH_LOOT_P; if (r >= CH_LOOT_N) return null; for (const k in CH_LOOT_CAR) if ((r -= CH_LOOT_CAR[k].length) < 0) return k; return 'parcel'; };",
    "  const chLootBag = [];                        // c100: 다음에 나올 수송차 종류들 (실은 가짓수만큼 들어 있고 섞여 있다)\n"
    "  const chLootRoll = () => { if (Math.random() >= CH_LOOT_P) return null; if (!chLootBag.length) { for (const k in CH_LOOT_CAR) for (const _ of CH_LOOT_CAR[k]) chLootBag.push(k); chLootBag.sort(() => Math.random() - 0.5); } return chLootBag[chLootBag.length - 1]; };")
rep("      car.loot = loot;\n", "      car.loot = loot; if (chLootBag[chLootBag.length - 1] === loot) chLootBag.pop();   // c100\n")
rep("ambul: ['mutate', 'awaken', 'catalyst', 'rage', 'blood'], parcel:", "ambul: ['mutate', 'awaken', 'catalyst', 'rage', 'blood', 'revive'], parcel:")
# 2. 경보단계 5% 더
rep("STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3);", "STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3 * 1.05);   /* c100: 5% 더 → [10, 85, 205, 459, 988] */")
# 3. 얻은 덩치(철창 수감자·관장) 체력 2배 — 변이 주사로 만든 덩치는 그대로
rep("    mutate(b, t);   // c56: 검은 테두리는 뺐다 (테두리는 변이한 나만)", "    mutate(b, t);   // c56: 검은 테두리는 뺐다 (테두리는 변이한 나만)\n    if (t === 'armor') { b.maxHp *= 2; b.hp = b.maxHp; }   // c100: 얻은 덩치는 체력 2배")
# 4. 변이 줄기세포 = 부활 장비 (죽으면 되살아난다 · 쿨타임 120초, 강화마다 남은 시간의 10%씩 줄어든다)
rep("    revive: { icon: IC.revive, name: '부활', passive: true },", "    revive: { icon: IC.revive, name: '변이 줄기세포', passive: true },")
rep("    revive: ['죽으면 되살아납니다. 다시 쓰려면 시간이 지나야 합니다.', '강화 시 더 많은 체력으로 되살아납니다.'],", "    revive: ['죽으면 되살아납니다. 다시 쓰려면 2분이 지나야 합니다.', '강화 시 기다리는 시간이 10%씩 줄어듭니다.'],")
rep("'shoes', 'catalyst', 'blood'];\n  const CH_RARE", "'shoes', 'catalyst', 'blood', 'revive'];   /* c100: 변이 줄기세포 */\n  const CH_RARE")
rep("hospital: { spec: ['mutate', 'awaken', 'catalyst', 'rage', 'blood'], p: 16, rest: 10 },", "hospital: { spec: ['mutate', 'awaken', 'catalyst', 'rage', 'blood', 'revive'], p: 14, rest: 6 },")
rep("    shoes: (n) => `이동 속도 +${5 * (1 + n)}%`,\n", "    shoes: (n) => `이동 속도 +${5 * (1 + n)}%`,\n    revive: (n) => `체력 30%로 부활 · 쿨타임 ${Math.round(120 * Math.pow(0.9, n))}초`,\n")
rep("blood: ['체력', (n) => `+${10 * (1 + n)}%`],", "blood: ['체력', (n) => `+${10 * (1 + n)}%`], revive: ['쿨타임', (n) => `${Math.round(120 * Math.pow(0.9, n))}초`],")
rep("blood: '내 최대 체력 증가',", "blood: '내 최대 체력 증가', revive: '죽으면 되살아남',")
rep("  const reviveCd = () => 120;", "  const reviveCd = () => CHAPTER ? 120 * Math.pow(0.9, lv('revive')) : 120;   /* c100: 강화마다 남은 시간의 10%씩 줄어든다 (120 → 108 → 97 → 87 → 79 → 71초) */")
rep("  const reviveHp = (n = up.brain) =>", "  const reviveHp = (n = CHAPTER ? 0 : up.brain) =>")
open('c100_patch.py', 'w', encoding='utf8').write('# c100: 수송차 종류 비율 고정 · 경보단계 5% 더 · 얻은 덩치 체력 2배 · 변이 줄기세포 (gen_c100.py가 만든다)\nC100_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
