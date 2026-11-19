# c199: 충격 흡수복 2에서 강화마다 +2.5 (4번 강화에 12 = 저격수 완전히 막음) · 촉매 7%씩
C199_R = [
 ("SNIPER_KD / 12 * (2 + 2 * lv('absorb'))", "SNIPER_KD / 12 * (2 + 2.5 * lv('absorb'))"),
 ("absorb: (n) => `충격 흡수 ${2 + 2 * n} (근접", "absorb: (n) => `충격 흡수 ${2 + 2.5 * n} (근접"),
 ("absorb: () => '흡수 ' + (2 + 2 * lv('absorb'))", "absorb: () => '흡수 ' + (2 + 2.5 * lv('absorb'))"),
 ("absorb: ['흡수', (n) => `${2 + 2 * n}`]", "absorb: ['흡수', (n) => `${2 + 2.5 * n}`]"),
 ("owned.catalyst ? 1 + 0.05 * (1 + lv('catalyst')) : 1", "owned.catalyst ? 1 + 0.07 * (1 + lv('catalyst')) : 1"),
 ("catalyst: (n) => `변이 좀비 공격력 +${5 * (1 + n)}%`,\n    blood:", "catalyst: (n) => `변이 좀비 공격력 +${7 * (1 + n)}%`,\n    blood:"),
 ("catalyst: ['변이', (n) => `+${5 * (1 + n)}%`]", "catalyst: ['변이', (n) => `+${7 * (1 + n)}%`]"),
]
