# c221: 보스 돌진 피해 10% 줄임 · 보스 기관총 15% 줄임 · 처음 발견 빨강 5명·경찰 2명 확률 = 노랑 20% · 하양 20% · 그대로 60%
C221_R = [
 ("const dmg = CAR_HIT_DMG * ve / CAR_SPEED * (tkD ? 0.5 + Math.max(0, car.tkM) : 1);", "const dmg = CAR_HIT_DMG * ve / CAR_SPEED * (tkD ? (0.5 + Math.max(0, car.tkM)) * 0.9 : 1);   /* c221: 돌진 10% 줄임 */"),
 ("CH_SP_DMG = POLICE_DAMAGE * 1.2 / 4 * 0.9 * 0.9 / 10", "CH_SP_DMG = POLICE_DAMAGE * 1.2 / 4 * 0.9 * 0.9 / 10 * 0.85   /* c221: 15% 줄임 */"),
 ("const r = Math.random(); if (r < 0.3) chDemote(c, 'guard'); else if (r < 0.6) chDemote(c, '');", "const r = Math.random(); if (r < 0.2) chDemote(c, 'guard'); else if (r < 0.4) chDemote(c, '');   /* c221: 20% · 20% */"),
]
