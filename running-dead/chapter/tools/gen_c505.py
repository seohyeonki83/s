import pathlib, re
s = pathlib.Path('c504.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
def between(a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

# ───────── 1. 부팅 · 저장 · 아웃게임 (맵 선택 화면을 대신한다) ─────────
old_pick = between("  const CH_PICK = (window.__map ||", "  const CH_TOUR = CH_PICK === 'w'")
rep(old_pick, r"""  // ── c505: 본편 — 저장 · 아웃게임 (스테이지 · 난이도 · 성장). 처음엔 튜토리얼부터 ──
  const CH_SV = (() => { let o = null; try { o = JSON.parse(localStorage.getItem('rd_save_v1') || 'null'); } catch (e) {} o = o || {}; o.genes = o.genes || 0; o.clr = o.clr || {}; o.sub = o.sub || {}; o.up = Object.assign({ hp: 0, ahp: 0, atk: 0 }, o.up || {}); o.tut = !!o.tut;
    if (!o.mig) { o.mig = 1; try { o.genes += +localStorage.getItem('rd_genes') || 0; localStorage.removeItem('rd_genes'); } catch (e) {} } return o; })();
  function chSave() { try { localStorage.setItem('rd_save_v1', JSON.stringify(CH_SV)); } catch (e) {} }
  chSave();
  const CH_UP_COST = 100;   // 성장 1포인트 = 유전자 100 · 기본값의 1%
  const CH_UPK = { hp: 1 + 0.01 * CH_SV.up.hp, ahp: 1 + 0.01 * CH_SV.up.ahp, atk: 1 + 0.01 * CH_SV.up.atk };
  const CH_DIF_NM = { e: '쉬움', n: '보통', h: '어려움' };
  let CH_STG = +window.__stg || 2, CH_DIF = window.__dif || 'h';   // 테스트 맵 기본값 (불도저 · 어려움)
  const chUnlocked = (st, d) => (st === 1 || ['e', 'n', 'h'].some((q) => CH_SV.clr[(st - 1) + q])) && (d === 'e' || CH_SV.clr[st + (d === 'n' ? 'e' : 'n')]);
  function chOutgame(go, tut) {
    const ov = document.createElement('div'); ov.id = 'outg';
    ov.style.cssText = 'position:fixed;inset:0;z-index:1000;background:#0e1014;color:#fff;font-family:system-ui,-apple-system,sans-serif;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:calc(16px + env(safe-area-inset-top, 0px)) 16px calc(24px + env(safe-area-inset-bottom, 0px));box-sizing:border-box';
    const draw = () => {
      const g = CH_SV.genes, row = (k, nm) => { const n = CH_SV.up[k]; return `<div class="og-up"><div><div class="og-n">${nm}</div><div class="og-s">+${n}% · ${n}포인트</div></div><div class="og-bar"><i style="height:${(n % 10) * 10 + 10}%"></i></div><button data-up="${k}" ${g < CH_UP_COST ? 'disabled' : ''}>+1% <small>🧬${CH_UP_COST}</small></button></div>`; };
      let h = `<div class="og-t">러닝데드</div><div class="og-g">🧬 유전자 <b>${g}</b></div><div class="og-h">성장</div>` + row('hp', '내 체력') + row('ahp', '동료 체력') + row('atk', '나 · 동료 공격력') + '<div class="og-h">스테이지</div>';
      for (const st of [1, 2, 3]) {
        h += `<div class="og-st"><div class="og-n">스테이지 ${st} <span class="og-s">${['', '보스: 군인차 부대', '보스: 불도저 2대', '보스: 장갑차'][st]}</span></div><div class="og-d">`;
        for (const d of ['e', 'n', 'h']) { const ok = chUnlocked(st, d), cl = CH_SV.clr[st + d]; h += `<button data-st="${st}" data-d="${d}" ${ok ? '' : 'disabled'}>${ok ? '' : '🔒 '}${CH_DIF_NM[d]}${cl ? ' ✓' : ''}</button>`; }
        h += '</div></div>';
      }
      h += `<button class="og-tut" data-tut="1">튜토리얼 다시 하기</button>`;
      ov.innerHTML = h;
    };
    const st = document.createElement('style');
    st.textContent = '#outg .og-t{font-size:28px;font-weight:900;text-align:center;margin:6px 0 4px}#outg .og-g{text-align:center;font-size:15px;color:#bfefff;margin-bottom:14px}#outg .og-g b{font-size:20px;color:#fff}' +
      '#outg .og-h{font-size:13px;font-weight:900;color:#9aa6b8;margin:16px 2px 8px;letter-spacing:1px}#outg .og-up,#outg .og-st{background:#1b2028;border:2px solid #2c3340;border-radius:14px;padding:10px 12px;margin-bottom:8px}' +
      '#outg .og-up{display:flex;align-items:center;gap:10px}#outg .og-up>div:first-child{flex:1}#outg .og-n{font-size:16px;font-weight:900}#outg .og-s{font-size:12px;color:#9aa6b8;font-weight:700}' +
      '#outg .og-bar{width:12px;height:40px;border-radius:6px;background:#2c3340;position:relative;overflow:hidden}#outg .og-bar i{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(#7fe3ff,#c78bff)}' +
      '#outg button{font:inherit;font-weight:900;color:#fff;background:#2f6fe0;border:none;border-radius:12px;padding:10px 12px;touch-action:manipulation}#outg button:disabled{background:#3a4250;color:#8a93a3}#outg button small{font-weight:700;opacity:0.85}' +
      '#outg .og-d{display:flex;gap:8px;margin-top:8px}#outg .og-d button{flex:1;padding:12px 0}#outg .og-tut{width:100%;margin-top:14px;background:#3a4250}';
    document.head.appendChild(st);
    ov.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b || b.disabled) return;
      if (b.dataset.up) { if (CH_SV.genes < CH_UP_COST) return; CH_SV.genes -= CH_UP_COST; CH_SV.up[b.dataset.up]++; chSave(); draw(); return; }
      if (b.dataset.tut) { ov.remove(); tut(); return; }
      if (b.dataset.st) { CH_UPK.hp = 1 + 0.01 * CH_SV.up.hp; CH_UPK.ahp = 1 + 0.01 * CH_SV.up.ahp; CH_UPK.atk = 1 + 0.01 * CH_SV.up.atk; ov.remove(); go(+b.dataset.st, b.dataset.d); }
    });
    draw(); document.body.appendChild(ov);
  }
  const CH_PICK = window.__map || await new Promise((res) => {
    try { window.name = ''; } catch (e) {}
    if (!CH_SV.tut) { res('t'); return; }
    chOutgame((st, d) => { CH_STG = st; CH_DIF = d; res('m'); }, () => res('t'));
  });
  const CH_RUN = CH_PICK === 'm' && !window.__noRun;   // c505: 본편 판 (스테이지 · 난이도 규칙)
  const CH_SK = CH_RUN ? 1 + 0.2 * (CH_STG - 1) : 1;   // 스테이지 강화 — 적 체력 · 공격력 · 벽 · 사물 (보스 체력 제외)
  const CH_MIXL = CH_RUN ? { e: 5, n: 4, h: 3 }[CH_DIF] : 5;   // 샷건 · 로봇 섞임 + 건널목 터렛 — 쉬움 총동원령 · 보통 팬데믹 · 어려움 비상
  const CH_MIS = (CH_RUN ? { e: [[3, 6], 30], n: [[4, 7], 50], h: [[5, 8], 70] }[CH_DIF] : [[3, 6], 30]);   // 서브 미션 (임시) — [경보 단계, 분] · 동료 수
  const chMis = [{ done: false }, { done: false }];
  let chRunT = 0, chRunGenes = 0, chRunOver = false;
""")
rep("  { const v = document.getElementById('ver'); if (v) v.textContent = v.textContent.replace('챕터',", "  { const v = document.getElementById('ver'); if (v && CH_RUN) v.textContent = '스테이지 ' + CH_STG + ' · ' + CH_DIF_NM[CH_DIF]; else if (v) v.textContent = v.textContent.replace('챕터',")

# ───────── 2. 경보 단계 (경계 뒤 130부터 40씩) ─────────
rep("  const CH_AL_AT = [5, 30, 164, 432, 711, 1021, 1384, 1821, 2353, 3000];", "  const CH_AL_AT = [5, 30, 160, 330, 540, 790, 1080, 1410, 1780, 2190];   // c505: 경계 뒤로 130 · 170 · 210 … (40씩)")
rep("STAR_AT[0] = 5; STAR_AT[1] = 30;", "STAR_AT[0] = 5; STAR_AT[1] = 30; STAR_AT[2] = 160; STAR_AT[3] = 330; STAR_AT[4] = 540;   /* c505 */")

# ───────── 3. 사람 만들기 — 로봇 종류 · 특공대 표시 · 스테이지 강화 ─────────
rep("  function addCitizen(x, z, area, type) {\n", "  function addCitizen(x, z, area, type) {\n    const robo = type === 'robot'; if (robo) type = 'soldier';   // c505: 'robot' = 사각 로봇\n")
rep("scene.add(c.gauge);\n    enterNormal(c);\n    return c;", "scene.add(c.gauge);\n    enterNormal(c);\n    if (robo) chMakeRobot(c); if (chSfTag) c.sfw = chSfTag;   // c505\n    if (CHAPTER && CH_SK !== 1 && c.maxHp > 0) { c.maxHp *= CH_SK; c.hp *= CH_SK; }   // c505: 스테이지 강화\n    return c;")
rep("  function chMakeRobot(c) {", "  function chMakeRobot(c) { if (c.robot) return;   // c505: 두 번 안 바뀐다")
rep("if (CHAPTER && chAL >= 5 && !chNoMix)", "if (CHAPTER && chAL >= CH_MIXL && !chNoMix)   /* c505: 난이도별 */")
rep("if (CHAPTER && s === 5) chBarTurret(X);", "if (CHAPTER && s === CH_MIXL) chBarTurret(X);   /* c505: 난이도별 */")
rep("    army: [['sniper', 1, 1],", "    army: [['robot', 1, 1],   /* c505: 저격수 → 사각 로봇 */")
rep("const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), type);", "const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), type === 'sniper' ? 'robot' : type);   /* c505: 건널목 저격수 → 로봇 */")
rep("c.hp = c.maxHp = GUARD_HP * 0.95 * 0.9 * 0.95 * 0.9 * 1.1 * 0.95;", "c.hp = c.maxHp = CH_SK * GUARD_HP * 0.95 * 0.9 * 0.95 * 0.9 * 1.1 * 0.95;   /* c505 */")
rep("hp: CH_DRONE_HP, maxHp: CH_DRONE_HP", "hp: CH_DRONE_HP * CH_SK, maxHp: CH_DRONE_HP * CH_SK")
rep("    while (S.hurt >= CALL_HP) {", "    while (S.hurt >= CALL_HP * CH_SK) {   /* c505 */")
rep("      S.hurt -= CALL_HP;", "      S.hurt -= CALL_HP * CH_SK;")

# 군인차에서 내릴 때 — 로봇 · 특공대 차례 · 보스 표시
rep("      const c = addCitizen(p.x, p.z, square(p.x, p.z), t);", "      const c = addCitizen(p.x, p.z, square(p.x, p.z), t); if (car.sfw) c.sfw = car.sfw; if (car.cvy) c.cvy = true;   /* c505 */")
rep("      c.tick = 0;\n    }\n  }\n  function unload(car) {", "      c.tick = 0;\n    }\n    car.crewOut = true;   // c505\n  }\n  function unload(car) {")

# ───────── 4. 피해 — 적 공격력 · 사물 · 차 ─────────
rep("if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15 * 1.2 * 0.95 * 0.93 * 0.93;", "if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15 * 1.2 * 0.95 * 0.93 * 0.93;\n    if (CHAPTER && CH_SK !== 1 && a && (a.kind === 'citizen' || a.kind === 'drone')) dmg *= CH_SK;   // c505: 스테이지 강화 — 적 공격력\n    if (CHAPTER && CH_SK !== 1 && (v.kind === 'obj' || v.kind === 'safe') && !(v.car && v.car.tank)) dmg /= CH_SK;   // c505: 벽 · 사물 체력")
rep("const dmg = CAR_HIT_DMG * se / CAR_SPEED;", "const dmg = CAR_HIT_DMG * se / CAR_SPEED * (CHAPTER && isZombie(b) ? CH_SK : 1);   /* c505 */")
rep("(CHAPTER && car.tank ? 0.85 : 1)   /* c494: 장갑차도 불도저와 같다 */", "(CHAPTER && car.tank ? (car.dozer ? 0.85 : 0.85 * 1.5) : 1) * (CHAPTER && isZombie(b) ? CH_SK : 1)   /* c505: 장갑차 밀기 = 불도저 1.5배 · 스테이지 강화 */")

# ───────── 5. 성장 (아웃게임) ─────────
rep("    me.maxHp = MY_HP;", "    me.maxHp = MY_HP * CH_UPK.hp;   // c505: 성장")
rep("const allyMaxHp = () => ALLY_HP * 0.9 * 0.9 * (1 + 0.07 * up.skin);", "const allyMaxHp = () => ALLY_HP * 0.9 * 0.9 * (1 + 0.07 * up.skin) * CH_UPK.ahp;   /* c505 */")
rep("const zDamage = (z) => (z === me ? MY_DAMAGE : ALLY_DAMAGE)", "const zDamage = (z) => CH_UPK.atk * (z === me ? MY_DAMAGE : ALLY_DAMAGE)")
rep("a === me ? ALLY_DAMAGE * (1 + 0.07 * up.arm) * (CHAPTER ? 3 : 1.3 * 1.3 * 2)", "a === me ? CH_UPK.atk * ALLY_DAMAGE * (1 + 0.07 * up.arm) * (CHAPTER ? 3 : 1.3 * 1.3 * 2)")
rep("const d = MY_HP * (CHAPTER ? 0.12 * (lv('blood') > 0 ? 0.5 : 1) : 0.10);", "const d = MY_HP * CH_UPK.hp * (CHAPTER ? 0.12 * (lv('blood') > 0 ? 0.5 : 1) : 0.10);   /* c505: 성장한 체력 기준 */")
# 도트 · 산성 — 공격력 성장을 따라간다 (정확히 · 보이는 숫자만 정수)
rep("c.hp = Math.max(0, c.hp - CH_GOO_DOT - chAcidB());", "c.hp = Math.max(0, c.hp - (CH_GOO_DOT + chAcidB()) * CH_UPK.atk);   /* c505 */")
rep("chDotPop(c.foot.x + 0.6, c.foot.z, CH_GOO_DOT + chAcidB());", "chDotPop(c.foot.x + 0.6, c.foot.z, (CH_GOO_DOT + chAcidB()) * CH_UPK.atk);")
rep("d.gooT -= CH_DOT_T; const n = CH_GOO_DOT + chAcidB();", "d.gooT -= CH_DOT_T; const n = (CH_GOO_DOT + chAcidB()) * CH_UPK.atk;")
rep("car.gooT -= CH_DOT_T; const gd = CH_GOO_DOT + chAcidB();", "car.gooT -= CH_DOT_T; const gd = (CH_GOO_DOT + chAcidB()) * CH_UPK.atk;")
rep("e.acidT -= CH_DOT_T; const d = 1 * HPK + chAcidB();", "e.acidT -= CH_DOT_T; const d = (1 * HPK + chAcidB()) * CH_UPK.atk;")
rep("d.acidT -= CH_DOT_T; const n = 1 * HPK + chAcidB();", "d.acidT -= CH_DOT_T; const n = (1 * HPK + chAcidB()) * CH_UPK.atk;")
rep("const chAcidHit = () => Math.round(3 + 7 * lvE('acid') / 5) * HPK;", "const chAcidHit = () => Math.round(3 + 7 * lvE('acid') / 5) * HPK * CH_UPK.atk;   /* c505 */")
rep("  function chDotPop(x, z, n, y = 1.3) {", "  function chDotPop(x, z, n, y = 1.3) { n = Math.round(n);   // c505: 보이는 숫자는 정수")
# 변이 주사 장탄 — ★5에서 멈춘다
rep("const itemMax = (k) => k === 'mutate' ? CH_WV('mutN', lv('mutate'))", "const itemMax = (k) => k === 'mutate' ? CH_WV('mutN', chLvB('mutate'))   /* c505: 빨간 별에서 4발 되던 것 */")

# ───────── 6. 유전자 — 적이 사라질 때마다 1 ─────────
rep("  let chGenes = 0; try { chGenes = +localStorage.getItem('rd_genes') || 0; } catch (e) {}", "  let chGenes = CH_SV.genes;   // c505: 저장된 유전자")
rep("  function chGeneAdd(n) { chGenes += n; chGeneEl.lastChild.textContent = chGenes; try { localStorage.setItem('rd_genes', String(chGenes)); } catch (e) {} }", "  function chGeneAdd(n) { if (chRunOver) return; chGenes += n; chRunGenes += n; CH_SV.genes += n; chSave(); chGeneEl.lastChild.textContent = chGenes; }   // c505")
rep("    chBTgone(c); if (isZombie(me)) gainXp();\n  }", "    chBTgone(c); if (isZombie(me)) gainXp(); if (CHAPTER && !c.mad) chGeneAdd(1);   /* c505 */\n  }")
rep("    if (d.dead) return; d.dead = true;", "    if (d.dead) return; d.dead = true; if (CHAPTER && !d.mad) chGeneAdd(1);   /* c505 */")
rep("  function chMadRoll(c) {", "  function chMadRoll(c) { const ok = chMadRoll0(c); if (ok) chGeneAdd(1); return ok; }   // c505: 오작동 = 적에서 사라짐\n  function chMadRoll0(c) {")
# 저격수 — 사라질 때 장비 하나
rep("  function makeZombie(b) {", "  function makeZombie(b) {\n    if (CHAPTER && b.sniper && b.kind === 'citizen') { const pool = CH_ITEMS.filter((k) => ITEM[k] && ITEM[k].passive && !chFull(k)); if (pool.length) dropPickup(pool[Math.floor(Math.random() * pool.length)], b.foot.x, b.foot.z, b.space || null); }   // c505: 저격수 → 장비 하나")

# ───────── 7. 특공대 · 보스 · 클리어 ─────────
rep("P.forEach(([m, c], k) => teamWait.push(m === 'W' ? { comp: c, t: k * 3, first: false, seg, hold: true } : { car: c, t: k * 3, seg: k ? chTeamSeg2(seg) : seg, hold: true }));", "P.forEach(([m, c], k) => teamWait.push(m === 'W' ? { comp: c, t: k * 3, first: false, seg, hold: true, sfw: i + 1 } : { car: c, t: k * 3, seg: k ? chTeamSeg2(seg) : seg, hold: true, sfw: i + 1 }));   /* c505: 몇 번째 특공대 */")
rep("const CR = [null, [S_, G_, G_], [S_, G_, G_, G_, G_], [S_, G_, G_, G_, G_]][i];", "const CR = [null, [S_, G_, G_], [S_, G_, G_, G_, G_], [S_, S_, G_, G_, G_, G_, G_, G_]][i];   /* c505: 4번째 = 보통의 네 번째 (3팀 + 군2 · 저1) */")
rep("if (w.boss) { if (w.tank) chBossSpawn(w.seg, 'tank'); else { chBossSpawn(w.seg); chBossSpawn(w.seg); } }", "if (w.boss) { chSf.bossOut = true; if (w.kind === 'tank' || w.tank) chBossSpawn(w.seg, 'tank'); else { chBossSpawn(w.seg); chBossSpawn(w.seg); } }   /* c505 */")
rep("else if (w.car) { const p = teamSpot(w.seg); addCar(p.x, p.z, Math.atan2(me.foot.z - p.z, me.foot.x - p.x), null, 0, w.car); if (w.tk) cars[cars.length - 1].tkWave = true; }",
    "else if (w.car) { const p = teamSpot(w.seg); addCar(p.x, p.z, Math.atan2(me.foot.z - p.z, me.foot.x - p.x), null, 0, w.car); const cc = cars[cars.length - 1]; if (w.tk) cc.tkWave = true; if (w.sfw) cc.sfw = w.sfw;\n      if (w.cvy) { chSf.bossOut = true; cc.tkWave = true; cc.cvy = true; chCvy.push(cc); for (let k = 0; k < w.nd; k++) { const d = chDroneAdd(cc.x, cc.z); d.cvy = true; d.ride = cc; d.rideK = k; } } }   /* c505: 군인차 부대 — 드론이 붙어 온다 */")
rep("else { chTkMark = !!w.tk; spawnTeam(w.comp, w.first, w.seg); chTkMark = false; }", "else { chTkMark = !!w.tk; chSfTag = w.sfw || 0; spawnTeam(w.comp, w.first, w.seg); chTkMark = false; chSfTag = 0; }   /* c505 */")
# 드론 — 차에 붙어 있다가 차가 서면 날아오른다
rep("      dt = dt0 * Math.min(d.statT > 0 ? CH_STAT_SLOW : 1, d.goo > 0 ? chStickyK() : 1);   // c479 · c468",
    "      dt = dt0 * Math.min(d.statT > 0 ? CH_STAT_SLOW : 1, d.goo > 0 ? chStickyK() : 1);   // c479 · c468\n      if (d.ride) { const c = d.ride; if (c.wreck || c.crewOut || !cars.includes(c)) d.ride = null; else { const a = d.rideK * 2.1 + clock * 0.6; d.x = c.x + Math.cos(a) * 0.8; d.z = c.z + Math.sin(a) * 0.8; d.foot.set(d.x, 0, d.z); chDroneDraw(d, dt); continue; } }   // c505: 차에 붙어 온다")
# 장갑차 — 패턴은 불도저와 같다 · 판이 끝나는 보스라 부서져도 증원 없음
rep("if (CHAPTER && kind === 'tank') { car.massK = 2 * 1.2;", "if (CHAPTER && kind === 'tank') { car.dzl = true; car.massK = 2 * 1.2;")
rep("if (car.dozer) car.dashAt /= 1.5;", "if (car.dozer || car.dzl) car.dashAt /= 1.5;   /* c505 */")
rep("* (car.dozer ? 1.5 : 1); car.tkPhT -= dt;", "* (car.dozer || car.dzl ? 1.5 : 1); car.tkPhT -= dt;")
rep("car.tkPhT = car.dozer ? 2 / 1.5 : 2;", "car.tkPhT = car.dozer || car.dzl ? 2 / 1.5 : 2;")
rep("    if (car.dozer) { const pool = CH_ITEMS.filter((k) => !chFull(k));", "    if (CHAPTER) chGeneAdd(1);   // c505\n    if (CH_RUN && !car.dozer) { chSf.chk = 1; return; }   // c505: 본편 — 장갑차가 부서져도 증원 없음\n    if (car.dozer) { const pool = CH_ITEMS.filter((k) => !chFull(k));")
rep("    chTank = null; chTanks.length = 0;   // c454", "    chTank = null; chTanks.length = 0;   // c454\n    chCvy.length = 0;   // c505")
rep("hide: false, hideT: 0, c2: null, repNext: 650 })", "hide: false, hideT: 0, c2: null, repNext: 650, bossOut: false })")

# chSfTick · chSfHud — 난이도별
old_tick = between("  function chSfTick(dt) {", "  function chTankMaster(c) {")
new_tick = r"""  const chCvy = [];                            // c505: 스테이지 1 보스 — 군인차 부대
  let chSfTag = 0;
  const chSfLast = () => CH_DIF === 'e' ? 3 : 4;
  const chSfLeft = (w) => teamWait.some((x) => x.sfw === w) || cars.some((c) => c.sfw === w && !c.wreck && !c.crewOut) || bodies.some((b) => b.kind === 'citizen' && b.sfw === w);
  const chSfDone = () => { let k = 0; for (let w = 1; w <= chSfLast(); w++) if (chSf.n >= w && !chSfLeft(w)) k++; return k; };
  function chBossAlive() {
    if (CH_STG === 1 && CH_RUN) return chCvy.some((c) => !c.wreck && !c.crewOut) || bodies.some((b) => b.kind === 'citizen' && b.cvy) || chDrones.some((d) => d.cvy && !d.dead) || teamWait.some((w) => w.cvy);
    return chTanks.some((t) => !t.wreck);
  }
  function chRunTick(dt) {                     // c505: 판 시간 · 서브 미션 · 끼인 특공대 풀기
    chRunT += dt;
    if (!chMis[0].done && chAL >= CH_MIS[0][0] && chRunT <= CH_MIS[0][1] * 60) chMis[0].done = true;
    if (!chMis[1].done && zombies.length - 1 >= CH_MIS[1]) chMis[1].done = true;
    if ((chSf.stkT = (chSf.stkT || 0) - dt) > 0) return; chSf.stkT = 1;
    for (const b of bodies) {
      if (b.kind !== 'citizen' || !(b.sfw || b.tkU || b.cvy) || b.fixed || b.state === 'held') continue;
      const dm = Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z);
      if (b.stkX === undefined || Math.hypot(b.foot.x - b.stkX, b.foot.z - b.stkZ) > 0.6 || dm < 9) { b.stkX = b.foot.x; b.stkZ = b.foot.z; b.stkN = 0; continue; }
      if (++b.stkN < 4) continue;
      const ux = (me.foot.x - b.foot.x) / dm, uz = (me.foot.z - b.foot.z) / dm;   // 4초 동안 못 움직였다 — 나 쪽으로 순간이동 (차 풀리듯)
      for (let k = Math.min(8, dm - 5); k > 1; k -= 0.5) { const x = b.foot.x + ux * k, z = b.foot.z + uz * k; if (!spaceOf(x, z) && freeSpot(x, z, null)) { b.foot.x = x; b.foot.z = z; b.space = null; break; } }
      b.stkX = b.foot.x; b.stkZ = b.foot.z; b.stkN = 0;
    }
  }
  function chSfTick(dt) {
    if (CH_TUT) return;   // c293: 튜토리얼은 특공대·보스 없음
    chDiscTick(dt);   // c220
    if (CH_RUN) chRunTick(dt);
    if (!chSf.on) {
      if (stars >= 2) chSf.on = true;                                             // 난리남
      else if (stars >= 1 && (chSf.susT += dt) >= CH_SF_FORCE) chSf.on = true;    // 수상함에서 3분 버팀 → 강제
      if (chSf.on) chSfPop(true);
    } else if (!chSf.boss) {
      chSf.T += dt; if (chSf.hide && (chSf.hideT -= dt) <= 0) chSfPop();
      while (!chSf.boss && chSf.T >= chSfAt(chSf.n + 1)) {
        chSf.n++; chSf.hide = true; chSf.hideT = 8;   // c125
        if (chSf.n <= 3) chQueueTeam(chSf.n - 1);
        else if (CH_RUN && CH_DIF === 'n') chQueueTeam(3);   // c505: 보통 — 네 번째 특공대
        else {   // 어려움 — 보스 (스테이지 1 군인차 부대 · 2 불도저 2대 · 3 장갑차)
          teamsSpawned++; chBanner.push('boss'); const seg = teamSeg();
          if (CH_RUN && CH_STG === 1) [[0, 3], [1.2, 3], [2.4, 2]].forEach(([t, nd]) => teamWait.push({ car: ['robot', 'robot', G_, G_, G_], t, seg, hold: true, cvy: true, nd }));
          else teamWait.push({ boss: true, kind: CH_RUN && CH_STG === 3 ? 'tank' : 'dozer', t: 0, seg, hold: true });
        }
        if (!CH_RUN ? chSf.n >= 4 : chSf.n >= (CH_DIF === 'e' ? 3 : 4)) chSf.boss = true;   // 마지막 차례 — 시계는 여기까지
      }
    } else if (!CH_RUN || CH_DIF === 'h') {
      chSf.T += dt;
      const alive = chBossAlive();
      if (chSf.bossOut && alive && (chSf.waveT += dt) >= CH_SF_WAVE) { chSf.waveT -= CH_SF_WAVE; chSf.wn = (chSf.wn || 0) + 1; teamWait.push({ comp: [G_, G_], t: 0, first: false, seg: teamSeg(), tk: true }); }   // 보스가 살아 있는 동안 15초마다 군인 2
      if (chSf.bossOut && !alive && !chSf.won && (chSf.chk -= dt) <= 0) {
        chSf.chk = 0.5;
        if (!teamWait.some((w) => w.tk || w.boss || w.cvy) && !cars.some((c) => c.tkWave && !c.wreck && !c.crewOut && c.state !== 'parked') && !bodies.some((b) => b.kind === 'citizen' && (b.tkU || b.cvy))) chSf.won = true;
      }
    }
    if (CH_RUN && CH_DIF !== 'h' && chSf.boss && !chSf.won && (chSf.chk -= dt) <= 0) { chSf.chk = 0.5; if (chSfDone() >= chSfLast()) chSf.won = true; }   // c505: 쉬움 · 보통 — 특공대를 다 물리쳤다
    chSfHud();
  }
  function chSfHud() {
    let s = '';
    if (chSf.on && !chSf.boss && !chSf.hide) {
      const left = Math.max(0, Math.ceil(chSfAt(chSf.n + 1) - chSf.T)), bossNext = chSf.n >= 3 && (!CH_RUN || CH_DIF === 'h');
      s = !bossNext ? (chSf.n === 0 ? '특공대 도착까지 ' : '다음 특공대 출동까지 ') + left + '초' : '<span class="bosscd"><i>!</i>보스 출동까지 ' + left + '초<i>!</i></span>';   /* c126 · c505 */
    }
    if (s !== chSf.shown) { chSf.shown = s; chSfEl.innerHTML = s; chSfEl.style.display = s ? 'block' : 'none'; }
    if (CH_RUN) chObjHud();
  }
"""
rep(old_tick, new_tick)

# ───────── 8. 경보 게이지 · 목표 · 펼치기 ─────────
rep("    starsEl.querySelector('.lv').textContent = shownStars ? LEVEL_NAME[shownStars - 1] : '';", "    starsEl.querySelector('.lv').textContent = shownStars ? LEVEL_NAME[shownStars - 1] : '';\n    if (CHAPTER && !starsEl.querySelector('.ag')) { const g = document.createElement('div'); g.className = 'ag'; g.innerHTML = '<i></i>'; starsEl.appendChild(g); const o = document.createElement('div'); o.className = 'obj'; starsEl.appendChild(o); }   // c505: 경보 게이지 · 목표")
rep("  const starsEl = document.getElementById('stars');", r"""  const starsEl = document.getElementById('stars');
  if (CHAPTER) {   // c505: 경보 게이지 — 느낌표(또는 해골) 5개 사이를 채운다 · 누르면 10단계 전체
    const st = document.createElement('style');
    st.textContent = '#stars{pointer-events:auto!important;cursor:pointer}#stars .ag{width:150px;height:6px;margin:3px auto 0;border-radius:3px;background:rgba(255,255,255,0.18);overflow:hidden}#stars .ag i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffb84d,#ff4a3a)}#stars .obj{margin-top:26px;font:800 11px/1.2 system-ui,sans-serif;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,0.9);white-space:nowrap}' +
      '#alp{position:absolute;inset:0;z-index:60;background:rgba(0,0,0,0.82);color:#fff;font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;box-sizing:border-box}#alp .r{width:min(340px,90vw);display:flex;align-items:center;gap:8px;margin:3px 0;font:800 13px system-ui}#alp .r b{width:64px}#alp .r .g{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,0.15);overflow:hidden}#alp .r .g i{display:block;height:100%;background:linear-gradient(90deg,#ffb84d,#ff4a3a)}#alp .r span{width:44px;text-align:right;color:#9aa6b8}#alp .m{width:min(340px,90vw);margin-top:12px;font:700 13px/1.5 system-ui}';
    document.head.appendChild(st);
    starsEl.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); chAlPanel(); });
  }
  function chAlFill(L) { const lo = L ? CH_AL_AT[L - 1] : 0, hi = CH_AL_AT[L]; return Math.max(0, Math.min(1, (deaths - lo) / (hi - lo))); }
  function chAlPanel() {
    if (document.getElementById('alp')) return;
    const ov = document.createElement('div'); ov.id = 'alp'; const wasP = paused; paused = true; stopInput();
    let h = '<div style="font:900 18px system-ui;margin-bottom:10px">경보 단계</div>';
    for (let L = 0; L < 10; L++) h += `<div class="r"><b style="color:${L < 5 ? '#ffd34d' : '#ff5a5a'}">${L < 5 ? '!' : '☠'} ${LEVEL_NAME[L]}</b><div class="g"><i style="width:${Math.round(chAlFill(L) * 100)}%"></i></div><span>${CH_AL_AT[L]}</span></div>`;
    h += `<div class="m">지금 감염 ${deaths}</div>`;
    if (CH_RUN) h += `<div class="m">목표: ${chObjText()}<br>서브 미션<br>${chMisText(0)}<br>${chMisText(1)}</div>`;
    h += '<div style="margin-top:14px;font:700 12px system-ui;color:#9aa6b8">눌러서 닫기</div>';
    ov.innerHTML = h; stage.appendChild(ov);
    ov.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); ov.remove(); if (!wasP) { paused = false; last = 0; } });
  }
  function chMisText(i) { const m = i ? `동료 ${CH_MIS[1]}마리 모으기 (${Math.max(0, zombies.length - 1)}/${CH_MIS[1]})` : `${CH_MIS[0][1]}분 안에 ${LEVEL_NAME[CH_MIS[0][0] - 1]} 도달`; return (chMis[i].done ? '✓ ' : '· ') + m; }
  function chObjText() {
    if (CH_DIF !== 'h') return `특공대 ${chSfLast()}번 물리치기 (${chSfDone()}/${chSfLast()})`;
    if (!chSf.bossOut) return '보스 물리치기';
    const n = bodies.filter((b) => b.kind === 'citizen' && (b.tkU || b.cvy)).length + chDrones.filter((d) => d.cvy && !d.dead).length + chTanks.filter((t) => !t.wreck).length + chCvy.filter((c) => !c.wreck && !c.crewOut).length;
    return `보스 물리치기 · 남은 적 ${n}`;
  }
  function chObjHud() {
    const g = starsEl.querySelector('.ag i'), o = starsEl.querySelector('.obj'); if (!g || !o) return;
    const b0 = chAL >= 5 ? 5 : 0; let f = 0; for (let L = b0; L < b0 + 5; L++) f += chAlFill(L); const w = Math.round(f / 5 * 1000) / 10 + '%';
    if (g.style.width !== w) g.style.width = w;
    const t = chObjText(); if (o.textContent !== t) o.textContent = t;
  }""")

# ───────── 9. 판 끝 — 결과 창 → 아웃게임 ─────────
rep("    if ((((stationDown || (CHAPTER && chSf.won))", "    if ((CH_RUN || CH_TUT) && !chRunOver && ((CH_RUN && chSf.won) || (CH_TUT && chTutGate && chTutGate.dead && me.foot.z < chTutGateZ - 0.5))) { chRunResult(true); return; }   // c505: 클리어 → 결과 창\n    if ((((stationDown || (CHAPTER && chSf.won))")
rep("      retryEl.hidden = false;                 // 화면 아래 '다시 하기' (v225) — 그 자리 조이스틱은 숨긴다", "      retryEl.hidden = !!(CH_RUN || CH_TUT);   // c505: 본편은 결과 창으로\n      if ((CH_RUN || CH_TUT) && !chRunOver) setTimeout(() => chRunResult(!!(CH_RUN && chSf.won)), 1800);   /* 클리어가 정해진 뒤면 클리어 */   // 화면 아래 '다시 하기' (v225) — 그 자리 조이스틱은 숨긴다")
RES = (r"""  function chRunResult(win) {                 // c505: 클리어 · 실패 — 보상 정산 → 아웃게임
    if (chRunOver) return; chRunOver = true; paused = true; stopInput();
    const R = []; let add = 0;
    if (CH_TUT) { if (win && !CH_SV.tut) { add += 100; R.push(['튜토리얼 클리어', 100]); } if (win) CH_SV.tut = true; }
    else if (CH_RUN && win) {
      const key = CH_STG + CH_DIF;
      if (!CH_SV.clr[key]) { const g = CH_DIF === 'h' ? 1000 : 300; add += g; R.push([CH_DIF_NM[CH_DIF] + ' 클리어', g]); CH_SV.clr[key] = 1; }
      chMis.forEach((m, i) => { const k = key + i; if (m.done && !CH_SV.sub[k]) { add += 100; R.push(['서브 미션 ' + (i + 1), 100]); CH_SV.sub[k] = 1; } });
    }
    CH_SV.genes += add; chSave();
    const ov = document.createElement('div'); ov.id = 'rres';
    ov.style.cssText = 'position:absolute;inset:0;z-index:70;background:rgba(8,10,14,0.92);color:#fff;font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;padding:20px;box-sizing:border-box';
    let h = `<div style="font:900 34px system-ui;color:${win ? '#ffd34d' : '#ff5a5a'}">${win ? '클리어!' : '실패'}</div><div style="font:800 14px system-ui;color:#9aa6b8">${CH_TUT ? '튜토리얼' : '스테이지 ' + CH_STG + ' · ' + CH_DIF_NM[CH_DIF]}</div>`;
    h += `<div style="width:min(320px,86vw);margin-top:10px;font:800 15px/1.9 system-ui"><div style="display:flex;justify-content:space-between"><span>감염 · 처치</span><span>🧬 ${chRunGenes}</span></div>`;
    for (const [n, g] of R) h += `<div style="display:flex;justify-content:space-between"><span>${n}</span><span>🧬 ${g}</span></div>`;
    if (CH_RUN) for (let i = 0; i < 2; i++) h += `<div style="font:700 12px/1.6 system-ui;color:#9aa6b8">${chMisText(i)}${chMis[i].done && !win ? ' (클리어해야 보상)' : ''}</div>`;
    h += `<div style="display:flex;justify-content:space-between;border-top:1px solid #3a4250;margin-top:6px;padding-top:6px"><span>보유 유전자</span><span>🧬 ${CH_SV.genes}</span></div></div><button style="margin-top:14px;font:900 18px system-ui;color:#fff;background:#2f6fe0;border:none;border-radius:14px;padding:12px 44px">확인</button>`;
    ov.innerHTML = h; stage.appendChild(ov);
    ov.querySelector('button').addEventListener('click', () => { try { window.name = ''; } catch (e) {} location.reload(); });
  }
""")
R = [(a, (RES + b) if a == "  function chMadRoll(c) {" else b) for a, b in R]
rep(between('  function chSfHud() {', '  function chSfReset() {'), '')   # c505: 옛 HUD (아래 새것으로)
pathlib.Path('c505_patch.py').write_text('C505_R = ' + repr(R) + '\n')
print(len(R))
