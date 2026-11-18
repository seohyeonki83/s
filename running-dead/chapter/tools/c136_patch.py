# c136: 나와 동료(얻은 변이 좀비 포함) 최대 체력 10% 깎음 · 길거리 하양 20% 줄임
C136_R = [
 ("const MY_HP = HP_MAX * 2 * 1.5 * 1.3 * 0.7 * 0.75 * 0.85 * 1.3 * 0.7 * 1.2 * 1.2 * 1.2;", "const MY_HP = HP_MAX * 2 * 1.5 * 1.3 * 0.7 * 0.75 * 0.85 * 1.3 * 0.7 * 1.2 * 1.2 * 1.2 * 0.9;   /* c136: 10% 깎음 (273.6 → 246.2) */"),
 ("const allyMaxHp = () => ALLY_HP * (1 + 0.07 * up.skin);", "const allyMaxHp = () => ALLY_HP * 0.9 * (1 + 0.07 * up.skin);   /* c136: 동료 10% 깎음 (94.5 → 85.05) — 체력바 한 겹 기준(ALLY_HP)은 그대로 */"),
 ("if (t === 'armor') b.maxHp = 380; else b.maxHp *= 1.0;", "if (t === 'armor') b.maxHp = 380 * 0.9; else b.maxHp *= 1.0;   /* c136: 얻은 덩치 342 (히드라는 동료 체력에서 따라 내려간다) */"),
 ("const whiteOut = Math.round((CH_WHITE_OUT + houseOut) * 1.15 * CH_ONE_K * 1.2);", "const whiteOut = chRoundP((CH_WHITE_OUT + houseOut) * 1.15 * CH_ONE_K * 1.2 * 0.775);   /* c136: 길거리 하양 전체가 20% 줄게 (다른 색에서 하양으로 바뀌어 오는 몫은 그대로라 여기서 조금 더 뺀다) */"),
 ("if (!((type === 'guard' || type === 'attacker') && Math.random() < 0.2)) list.push(type); }", "if (!((type === 'guard' || type === 'attacker' || type === '') && Math.random() < 0.2)) list.push(type); }"),
 ("if (!(q === 'guard' && Math.random() < 0.2)) ex[i].push(q); }", "if (Math.random() >= 0.2) ex[i].push(q); }"),
]
