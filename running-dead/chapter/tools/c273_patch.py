# c273: 충격 흡수복을 없애고 방탄복에 합친다 — 방탄복 = 총격 피해 감소 + 충격에 밀리지 않음 (흡수량은 예전 충격 흡수복과 같다: 2 + 2.5씩)
C273_R = [
 ("const absorbAmt = () => owned.absorb ? SNIPER_KD / 12 * (2 + 2.5 * lv('absorb'))", "const absorbAmt = () => (CHAPTER ? owned.vest : owned.absorb) ? SNIPER_KD / 12 * (2 + 2.5 * lv(CHAPTER ? 'vest' : 'absorb'))   /* c273: 방탄복에 합침 */"),
 ("'rage', 'crowbar', 'absorb', 'vest', 'shoes',", "'rage', 'crowbar', 'vest', 'shoes',   /* c273: 충격 흡수복 없음 */"),
 ("fire: { spec: ['crowbar', 'absorb'], p: CH_SPEC_2, rest: 90 - 2 * CH_SPEC_2 }", "fire: { spec: ['crowbar'], p: CH_SPEC_2, rest: 90 - CH_SPEC_2 }   /* c273 */"),
 ("'crowbar', 'absorb', 'vest', 'shoes', 'acidp']", "'crowbar', 'vest', 'shoes', 'acidp']   /* c273 */"),
 ("    vest: ['총격 피해를 줄여 줍니다.', '강화 시 더 많이 줄여 줍니다.'],", "    vest: ['원거리 공격, 총격 데미지 감소, 충격에 밀리지 않음', '강화 시 더 많이 줄이고 더 강한 충격도 버팁니다.'],   /* c273 */"),
 ("vest: (n) => `총격 피해 -${10 * (1 + n)}%`,", "vest: (n) => `원거리 공격 ${10 * (1 + n)}% 감소 · 밀림 ${2 + 2.5 * n} 감소`,   /* c273 */"),
 ("vest: ['총격', (n) => `-${10 * (1 + n)}%`]", "vest: ['총격', (n) => `-${10 * (1 + n)}% · 밀림 -${2 + 2.5 * n}`]"),
 ("vest: '총격 피해 감소'", "vest: '총격 피해 감소 · 충격에 밀리지 않음'"),
]
