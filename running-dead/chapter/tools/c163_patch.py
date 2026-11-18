# c163: 동료만 최대 체력 7% 올림 (얻은 변이 좀비 포함) · 빠루 = 사물 피해 +15%, 강화마다 +15% · 충격 흡수복 = 처음부터 흡수 2 (강화마다 +1)
C163_R = [
 ("const allyMaxHp = () => ALLY_HP * 0.9 * (1 + 0.07 * up.skin);", "const allyMaxHp = () => ALLY_HP * 0.9 * 1.07 * (1 + 0.07 * up.skin);   /* c163: 동료 7% 올림 (85.05 → 91.0) */"),
 ("if (t === 'armor') b.maxHp = 380 * 0.9; else b.maxHp *= 1.0;", "if (t === 'armor') b.maxHp = 380 * 0.9 * 1.07; else b.maxHp *= 1.0;   /* c163: 얻은 덩치 365.9 */"),
 ("dmg *= 1 + 0.1 * (1 + lv('crowbar'));", "dmg *= 1 + 0.15 * (1 + lv('crowbar'));   /* c163: 빠루 +15%, 강화마다 +15%p */"),
 ("crowbar: (n) => `사물 피해 +${10 * (1 + n)}%`,", "crowbar: (n) => `사물 피해 +${15 * (1 + n)}%`,"),
 ("crowbar: () => '+' + 10 * (1 + lv('crowbar')) + '%'", "crowbar: () => '+' + 15 * (1 + lv('crowbar')) + '%'"),
 ("crowbar: ['사물', (n) => `+${10 * (1 + n)}%`]", "crowbar: ['사물', (n) => `+${15 * (1 + n)}%`]"),
 ("const absorbAmt = () => owned.absorb ? SNIPER_KD / 12 * (1 + lv('absorb')) : 0;", "const absorbAmt = () => owned.absorb ? SNIPER_KD / 12 * (2 + lv('absorb')) : 0;   /* c163: 처음부터 흡수 2 */"),
 ("absorb: (n) => `충격 흡수 ${1 + n} (근접 무기 1 · 권총 2 · 군인 3 · 저격수 12)`,", "absorb: (n) => `충격 흡수 ${2 + n} (근접 무기 1 · 권총 2 · 군인 3 · 저격수 12)`,"),
 ("absorb: () => '흡수 ' + (1 + lv('absorb'))", "absorb: () => '흡수 ' + (2 + lv('absorb'))"),
 ("absorb: ['흡수', (n) => `${1 + n}`]", "absorb: ['흡수', (n) => `${2 + n}`]"),
]
