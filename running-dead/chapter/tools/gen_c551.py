import pathlib, re
s = pathlib.Path('c550.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 단계: 챕터는 10단계 경보(chAL)까지 건널목이 자란다 (바리케이트·경찰차는 5단계까지)
rep("    if ((chBar.t -= dt) > 0 && stars <= chBar.stage) return;",
    "    const chBL = CHAPTER ? chAL : stars;   /* c551: 챕터는 10단계 경보까지 증원 */\n    if ((chBar.t -= dt) > 0 && chBL <= chBar.stage) return;")
old_late = [l for l in s.split('\n') if 'chBar.lateT' in l]
assert len(old_late) == 1
rep("    if (stars > chBar.stage) { for (let s = chBar.stage + 1; s <= stars; s++) chBarGrow(s); chBar.stage = stars; }\n" + old_late[0],
    "    if (chBL > chBar.stage) { for (let s = chBar.stage + 1; s <= chBL; s++) chBarGrow(s); chBar.stage = chBL; }")
rep("for (const e of [0, 1]) {", "for (const e of (s <= STAR_MAX ? [0, 1] : [])) {   /* c551: 바리케이트·경찰차는 5단계까지 */")
a = [l for l in s.split('\n') if l.startswith("      const add = s === 1 ? { police: N(2, 4) }")]
assert len(a) == 1
rep(a[0], "      const add = s <= 2 ? { police: N(2, 4) } : s < CH_MIXL ? { soldier: 1, sniper: 1 } : s === CH_MIXL ? {} : (() => { const o = { soldier: 1, sniper: 1, sg: 1 }; delete o[['soldier', 'sniper', 'sg'][Math.floor(Math.random() * 3)]]; return o; })();   /* c551: 1~2 경찰 2~4 · 터렛 전 군인 1 + 사각 1 · 터렛 단계는 터렛만 · 그 뒤 사각·군인·샷건 중 랜덤 둘 */")
rep("      for (const type of ['police', 'soldier', 'sniper']) for (let i = 0, n = add[type] || 0; i < n; i++) {   /* c72: 인원 절반 */ const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), type === 'sniper' ? 'robot' : type);",
    "      chNoMix = true;   /* c551: 건널목 증원은 정한 그대로 (섞임 없음) */\n      for (const type of ['police', 'soldier', 'sniper', 'sg']) for (let i = 0, n = add[type] || 0; i < n; i++) {   /* c72: 인원 절반 */ const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), type === 'sniper' ? 'robot' : type === 'sg' ? 'police' : type); if (type === 'sg') chMakeSg(c);")
rep("      if (CHAPTER && s === CH_MIXL) chBarTurret(X);", "      chNoMix = false;\n      if (CHAPTER && s === CH_MIXL) chBarTurret(X);")
rep("    for (let i = 0; i < 2; i++) { const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), 'police'); chMakeSg(c); c.gar = X; c.fresh = true; X.units.push(c); }\n",
    "    /* c551: 터렛 단계엔 샷건 경찰 없음 */\n")
pathlib.Path('c551_patch.py').write_text('C551_R = ' + repr(R) + '\n')
print(len(R))
