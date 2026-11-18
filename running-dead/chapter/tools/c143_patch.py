# c143: 길거리 빨강 20% 늘림 · 적의 모든 공격력 15% 올림 · 경찰차 출동: 수상함 15% 빠르게 → 데프콘은 그대로 (사이 단계는 고르게)
C143_R = [
 ("      if (t === 'vig' && Math.random() < 0.19) return;", "      if (t === 'vig' && Math.random() < 0.028) return;   /* c143: 길거리 빨강 20% 늘림 (안 나오던 19%를 2.8%로 — 남는 비율 0.81 → 0.972 = 1.2배) */"),
 ("    if (TEST_MAP && !CHAPTER && v === me) dmg = 0;   // v396", "    if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15;   // c143: 적(사람·경찰·군인·저격수·장갑차)의 공격력 15% 올림\n    if (TEST_MAP && !CHAPTER && v === me) dmg = 0;   // v396"),
 ("chDispT = (32 - 3 * (stars - 1)) * 0.8 / 0.85;", "const chCarK = 1 + 0.15 * (5 - stars) / 4; chDispT = (32 - 3 * (stars - 1)) * 0.8 / 0.85 * 2 / (1 + chCarK);   /* c143: 경찰차 출동만 빠르게 (수상함 15% · 난리남 11.25% · 개판 7.5% · 계엄 3.75% · 데프콘 그대로) — 걸어오는 출동 빈도는 그대로라, 전체 간격을 조금 줄이고 차가 뽑힐 확률을 그만큼 올린다 */"),
 ("    if (Math.random() < 0.5) addCar(p.x, p.z, Math.atan2(site.y - p.z, site.x - p.x), site, n);", "    if (Math.random() < chCarK / (1 + chCarK)) addCar(p.x, p.z, Math.atan2(site.y - p.z, site.x - p.x), site, n);"),
]
