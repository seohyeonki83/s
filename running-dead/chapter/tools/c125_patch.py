# c125: 무기(쓰는 것)와 장비를 가른다 — 레벨업에는 장비만 + '무기 강화' 카드 · 무기 획득 연출 · 특공대 100초부터 5초씩 줄어듦 · 카운트다운이 가운데 크게 떴다가 제자리로
JS = r"""  // ── c125: 무기 강화 카드 · 특공대 시간표 · 카운트다운 연출 ──
  const chWeapons = () => items.map((x) => x.kind);                     // 가진 무기 (쓰는 것)
  const chWupN = () => chWeapons().filter((k) => lv(k) < chLvMax(k)).length;   // 강화할 수 있는 무기 수
  function chWupCard() {
    return `<div class="card" data-k="__w" style="min-height:158px;padding-top:8px;border-color:#ff7a4a"><div style="height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:#ff7a4a">무기</div>` +
      `<div class="ic" style="margin-top:4px">${IC.tool}</div><div class="nm" style="margin-top:8px">무기 강화</div><div class="ds" style="margin-top:8px">가진 무기 하나를 골라 강화</div><div class="vl"></div></div>`;
  }
  function chWupPick(ov) {                     // '무기 강화'를 골랐다 → 가진 무기가 다 뜬다 (끝까지 올린 것은 못 고른다)
    ov.querySelector('.hd').textContent = '무기 강화';
    ov.querySelector('.sub').textContent = '강화할 무기를 선택하세요';
    const box = ov.querySelector('.cards'); box.style.flexWrap = 'wrap'; box.style.justifyContent = 'center';
    box.innerHTML = chWeapons().map((k) => { const n = lv(k), S = CH_SHORT[k], max = n >= chLvMax(k);
      return `<div class="card" data-k="${k}" style="min-height:158px;padding-top:8px${max ? ';opacity:0.4;pointer-events:none' : ''}"><div style="height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:#ffd34d">${max ? 'MAX' : chStars(n + 1)}</div>` +
        `<div class="ic" style="margin-top:4px">${ITEM[k].icon}</div><div class="nm" style="margin-top:8px">${ITEM[k].name}</div><div class="ds" style="margin-top:8px">${max ? '최대 강화' : '강화'}</div>` +
        `<div class="vl">${S[0]} ${max ? S[1](n) : S[1](n) + ' → ' + S[1](n + 1)}</div></div>`; }).join('');
    ov.querySelector('.ok').classList.remove('ready');
  }
  const chSfAt = (n) => { let t = 0; for (let i = 0; i < n; i++) t += 100 - 5 * i; return t; };   // n번째 출동 시각: 100 · 195 · 285 · 370 · 450(보스)
  { const st = document.createElement('style'); st.textContent = '@keyframes sfpop { 0% { transform: translateY(30vh) scale(2.3); opacity: 0; } 10% { transform: translateY(30vh) scale(2.3); opacity: 1; } 60% { transform: translateY(30vh) scale(2.3); opacity: 1; } 100% { transform: none; opacity: 1; } }' +
      ' @keyframes wpnpop { 0% { transform: scale(3); opacity: 0; } 60% { transform: scale(0.92); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }'; document.head.appendChild(st); }
  function chSfPop(force) {                    // 카운트다운이 가운데 크게 떴다가 제자리에 박힌다
    if (!chSf.hide && !force) return;
    chSf.hide = false;
    if (!chSf.on || chSf.boss) return;
    chSfHud();
    chSfEl.style.animation = 'none'; chSfEl.offsetWidth; chSfEl.style.animation = 'sfpop 1.9s ease-in-out';
  }
"""
C125_R = [
 ("  function chLevelUp() {\n", JS + "  function chLevelUp() {\n"),
 # 레벨업: 무기는 안 나온다 (장비만) + 무기 강화 카드 (무기가 나오던 확률 = 강화할 수 있는 무기 수만큼)
 ("    return CH_ITEMS.filter((k) => !(chHas(k) && lv(k) >= chLvMax(k)) && (ITEM[k].passive || chHas(k)));   /* c124: 도구의 첫 등장은 레벨업에 없다 */",
  "    return CH_ITEMS.filter((k) => ITEM[k].passive && !(chHas(k) && lv(k) >= chLvMax(k)));   /* c125: 레벨업에는 장비만 (무기는 '무기 강화' 카드로) */"),
 ("    const pool = chUpPool(), keys = [];\n    while (keys.length < 3 && pool.length) keys.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);   // 그냥 랜덤 3장 (서로 다른 것)",
  "    let pool = chUpPool().concat(Array(chWupN()).fill('__w')); const keys = [];   // c125\n    while (keys.length < 3 && pool.length) { const k = pool.splice(Math.floor(Math.random() * pool.length), 1)[0]; keys.push(k); if (k === '__w') pool = pool.filter((q) => q !== '__w'); }   // 랜덤 3장 — 무기 강화 카드는 한 장만"),
 ("      keys.map((k) => { const has = chHas(k), n = lv(k), S = CH_SHORT[k];\n        return `<div class=\"card\" data-k=\"${k}\" style=\"min-height:158px;padding-top:8px\"><div style=\"height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:#ffd34d\">${has ? chStars(n + 1) : 'NEW'}</div>`",
  "      keys.map((k) => { if (k === '__w') return chWupCard(); const has = chHas(k), n = lv(k), S = CH_SHORT[k];\n        return `<div class=\"card\" data-k=\"${k}\" style=\"min-height:158px;padding-top:8px\"><div style=\"height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:#ffd34d\">${has ? chStars(n + 1) : 'NEW'}</div>`"),
 ("      if (!ok || !chosen) return;\n      ov.dataset.done = '1';\n      for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === chosen ? 'win' : 'gone'); }   // 고른 카드가 커지며 빛나고",
  "      if (!ok || !chosen) return;\n      if (chosen === '__w') { chWupPick(ov); chosen = null; return; }   // c125: 강화할 무기를 고르는 화면으로\n      ov.dataset.done = '1';\n      for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === chosen ? 'win' : 'gone'); }   // 고른 카드가 커지며 빛나고", 2),
 # 무기 획득 연출 (장비보다 훨씬 세게)
 ("    ov.innerHTML = `<div class=\"big\">${d.icon}</div><div class=\"t\">${d.name} 획득</div><div class=\"ds\">${itemDesc(kind)}<div class=\"up\">${lvText(kind)}</div></div>`;",
  "    ov.innerHTML = (CHAPTER && !d.passive ? `<div style=\"font:900 54px/1 var(--font);letter-spacing:3px;color:#ff4a3a;text-shadow:0 0 16px rgba(255,60,0,0.95),0 0 44px #ff2a00,0 4px 10px rgba(0,0,0,0.85);animation:wpnpop 0.45s ease-out both;margin-bottom:14px\">무기 획득</div><div class=\"big\">${d.icon}</div><div class=\"t\" style=\"font-size:30px;color:#ffd34d\">${d.name}</div>` : `<div class=\"big\">${d.icon}</div><div class=\"t\">${d.name} 획득</div>`) + `<div class=\"ds\">${itemDesc(kind)}<div class=\"up\">${lvText(kind)}</div></div>`;   /* c125 */"),
 ("    ov.innerHTML = `<div class=\"big\">${d.icon}</div><div class=\"t\">${d.name} ${max ? '(이미 최대 강화)' : '강화'}</div>` +",
  "    ov.innerHTML = (d.passive ? '' : `<div style=\"font:900 40px/1 var(--font);letter-spacing:2px;color:#ff7a4a;text-shadow:0 0 14px rgba(255,80,0,0.9),0 4px 10px rgba(0,0,0,0.85);animation:wpnpop 0.45s ease-out both;margin-bottom:12px\">무기 강화</div>`) + `<div class=\"big\">${d.icon}</div><div class=\"t\">${d.name} ${max ? '(이미 최대 강화)' : '강화'}</div>` +"),
 # 도구 → 무기
 ("'당신이 가진 모든 도구의 쿨타임이 감소합니다.'", "'당신이 가진 모든 무기의 쿨타임이 감소합니다.'"),
 ("'들 수 있는 도구가 하나 늘어납니다.'", "'들 수 있는 무기가 하나 늘어납니다.'"),
 ("bag: () => `도구 ${Math.min(5, 3 + n)}칸`", "bag: () => `무기 ${Math.min(5, 3 + n)}칸`"),
 ("book: (n) => `도구 쿨타임 -${5 * (1 + n)}%`", "book: (n) => `무기 쿨타임 -${5 * (1 + n)}%`"),
 ("bag: (n) => `도구 ${Math.min(5, 2 + n)}칸`", "bag: (n) => `무기 ${Math.min(5, 2 + n)}칸`"),
 ("'쓸 수 있는 도구가 하나 늘어납니다.'", "'쓸 수 있는 무기가 하나 늘어납니다.'"),
 ("bag: ['도구', (n)", "bag: ['무기', (n)"),
 ("book: '도구 쿨타임 단축', bag: '쓸 수 있는 도구 +1'", "book: '무기 쿨타임 단축', bag: '쓸 수 있는 무기 +1'"),
 ("toast('도구를 하나 채울 수 있습니다')", "toast('무기를 하나 채울 수 있습니다')"),
 # 특공대 시간표: 100초, 그 뒤로 5초씩 줄어든다
 ("const left = Math.max(0, Math.ceil(CH_SF_GAP * (chSf.n + 1) - chSf.T));", "const left = Math.max(0, Math.ceil(chSfAt(chSf.n + 1) - chSf.T));"),
 ("while (!chSf.boss && chSf.T >= CH_SF_GAP * (chSf.n + 1)) {\n        chSf.n++;", "while (!chSf.boss && chSf.T >= chSfAt(chSf.n + 1)) {\n        chSf.n++; chSf.hide = true; chSf.hideT = 8;   // c125: 다음 카운트다운은 출동 알림이 끝나면 크게 뜬다"),
 # 카운트다운 연출
 ("    if (chSf.on && !chSf.boss) {\n      const left", "    if (chSf.on && !chSf.boss && !chSf.hide) {\n      const left"),
 ("      if (stars >= 2) chSf.on = true;                                             // 난리남\n      else if (stars >= 1 && (chSf.susT += dt) >= CH_SF_FORCE) chSf.on = true;    // 수상함에서 3분 버팀 → 강제",
  "      if (stars >= 2) chSf.on = true;                                             // 난리남\n      else if (stars >= 1 && (chSf.susT += dt) >= CH_SF_FORCE) chSf.on = true;    // 수상함에서 3분 버팀 → 강제\n      if (chSf.on) chSfPop(true);"),
 ("    } else if (!chSf.boss) {\n      chSf.T += dt;", "    } else if (!chSf.boss) {\n      chSf.T += dt; if (chSf.hide && (chSf.hideT -= dt) <= 0) chSfPop();"),
 ("Object.assign(chSf, { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0 });", "Object.assign(chSf, { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0, hide: false, hideT: 0 });"),
 ("el.remove(); squadAnim = false; if (curFx === fx) curFx = null; for (const w of teamWait)", "el.remove(); squadAnim = false; if (curFx === fx) curFx = null; if (CHAPTER) chSfPop(); for (const w of teamWait)"),
]
