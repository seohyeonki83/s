# c224: 인게임 — 운동화 = 나·동료·변이 · 새 장비 틀니(감염 시간) · 산성 폭발(동료·변이가 죽으며 산성) · 무기 분해 · 레벨업 무기 강화 카드 25% 줄임
C224_R = [
 # ── 아이콘 · 이름 · 설명 ──
 ("    shoes: svgI('<path d=\"M2 17v-4c2 0 4-1 5-3l1.5-2 3 2.5c1.5 1 3 1.5 5 1.5h2.5a3 3 0 0 1 3 3V17z\" fill=\"#4fa3f0\"/><rect x=\"2\" y=\"17\" width=\"20\" height=\"3\" rx=\"1\" fill=\"#e9edf5\"/>'),",
  "    shoes: svgI('<path d=\"M2 17v-4c2 0 4-1 5-3l1.5-2 3 2.5c1.5 1 3 1.5 5 1.5h2.5a3 3 0 0 1 3 3V17z\" fill=\"#4fa3f0\"/><rect x=\"2\" y=\"17\" width=\"20\" height=\"3\" rx=\"1\" fill=\"#e9edf5\"/>'),\n"
  "    teeth: svgI('<path d=\"M3 8c0-2.5 4-4 9-4s9 1.5 9 4v3H3z\" fill=\"#e8768a\"/><path d=\"M3 13h18v3c0 2.5-4 4-9 4s-9-1.5-9-4z\" fill=\"#e8768a\"/><path d=\"M5 10.5h2.4v3H5zM8.2 10.5h2.4v3H8.2zM11.4 10.5h2.4v3h-2.4zM14.6 10.5H17v3h-2.4zM17.8 10.5h1.6v3h-1.6z\" fill=\"#fffdf2\"/>'),   /* c224 */\n"
  "    acid: svgI('<path d=\"M12 2C9 7 5 10.5 5 14.5a7 7 0 0 0 14 0C19 10.5 15 7 12 2z\" fill=\"#7ed321\"/><circle cx=\"9.5\" cy=\"14\" r=\"1.6\" fill=\"#d8ff9a\"/><circle cx=\"13.5\" cy=\"17\" r=\"1.1\" fill=\"#d8ff9a\"/><circle cx=\"20\" cy=\"6\" r=\"1.4\" fill=\"#7ed321\"/><circle cx=\"4\" cy=\"7\" r=\"1\" fill=\"#7ed321\"/>'),   /* c224 */"),
 ("    shoes: { icon: IC.shoes, name: '운동화', passive: true },",
  "    shoes: { icon: IC.shoes, name: '운동화', passive: true },\n    teeth: { icon: IC.teeth, name: '틀니', passive: true }, acid: { icon: IC.acid, name: '산성 폭발', passive: true },   // c224"),
 ("    shoes: ['나의 이동 속도가 빨라집니다.', '강화 시 더 빨라집니다.'],",
  "    shoes: ['나와 동료들의 이동 속도가 빨라집니다.', '강화 시 더 빨라집니다.'],   /* c224 */\n"
  "    teeth: ['인간을 더 빠르게 좀비로 만듭니다.', '강화 시 더 빨라집니다.', '한 명을 감염시킬 때 회복하는 체력은 같습니다.'],\n"
  "    acid: ['동료들이 산성피를 뿌리며 전사합니다.', '강화 시 산성이 더 넓게 퍼지고 더 오래 갑니다.', '겹쳐 맞으면 피해가 쌓입니다.'],"),
 ("    shoes: (n) => `이동 속도 +${7 * (1 + n)}%`,\n",
  "    shoes: (n) => `나·동료 이동 속도 +${7 * (1 + n)}%`,\n"
  "    teeth: (n) => `감염 시간 -${10 * (1 + n)}%`,   /* c224 */\n"
  "    acid: (n) => `범위 = 근접 거리 x${(1.2 * (1 + 0.15 * n)).toFixed(2)} · ${3 + n}초 · 0.5초마다 1 (겹치면 쌓임)`,\n"),
 ("    shoes: ['이동', (n) => `+${7 * (1 + n)}%`],", "    shoes: ['이동', (n) => `+${7 * (1 + n)}%`], teeth: ['감염', (n) => `-${10 * (1 + n)}%`], acid: ['산성', (n) => `${3 + n}초`],   /* c224 */"),
 ("shoes: '내 이동 속도 증가', catalyst", "shoes: '나·동료 이동 속도 증가', teeth: '감염 속도 증가', acid: '동료가 죽으며 산성', catalyst"),
 ("'shoes', 'catalyst', 'blood', 'revive'];   /* c100: 변이 줄기세포 */", "'shoes', 'catalyst', 'blood', 'revive', 'teeth', 'acid'];   /* c100: 변이 줄기세포 · c224: 틀니 · 산성 폭발 */"),
 ("ambul: ['mutate', 'awaken', 'catalyst', 'rage', 'blood', 'revive'],", "ambul: ['mutate', 'awaken', 'catalyst', 'rage', 'blood', 'revive', 'teeth', 'acid'],   /* c224 */"),
 # ── 운동화: 나·동료·변이 (기본 속도 기준 7%씩 더한다) ──
 ("  const legK = () => 1 + 0.07 * up.leg;", "  const legK = () => 1 + 0.07 * up.leg + (CHAPTER && owned.shoes ? 0.07 * (1 + lv('shoes')) : 0);   /* c224: 운동화 = 나·동료·변이 */"),
 ("  const meSpeed = () => MY_SPEED * (legK() + (owned.shoes ? 0.07 * (1 + lv('shoes')) : 0)", "  const meSpeed = () => MY_SPEED * (legK() + (!CHAPTER && owned.shoes ? 0.07 * (1 + lv('shoes')) : 0)"),
 ("    if (kind === 'shoes' && isZombie(me)) me.speed = meSpeed();\n    chSlots();",
  "    if (kind === 'shoes') for (const b of bodies) if (isZombie(b)) b.speed = b === me ? meSpeed() : SPEED * legK() * (b.mut ? MUT_SPEED : 1);   // c224: 나·동료·변이 다\n    chSlots();"),
 # ── 틀니: 감염 시간 (회복 총량은 그대로 — 회복 속도가 시간에 반비례) ──
 ("  const biteK = (n = up.bite) => Math.max(0, 1 - bitePct(n) / 100);", "  const biteK = (n = up.bite) => Math.max(0, 1 - bitePct(n) / 100) * (CHAPTER && owned.teeth ? 1 - 0.1 * (1 + lv('teeth')) : 1);   /* c224: 틀니 */"),
 # ── 산성 폭발 ──
 ("    if (z.dead) return;\n    z.dead = true;\n", "    if (z.dead) return;\n    z.dead = true;\n    if (CHAPTER && owned.acid && z !== me) chAcidBurst(z);   // c224\n"),
 ("  function gooTick(dt) {",
  """  const chAcidL = [], chAcBuf = [], chAcidMat = new THREE.SpriteMaterial({ map: flashTex, color: 0x9cff3a, transparent: true, depthTest: false, depthWrite: false });
  function chAcidOn(e, T) {                    // c224: 산성 한 겹 (겹마다 따로 시간이 간다)
    (e.acid || (e.acid = [])).push(T); if (e.acidT === undefined) e.acidT = 0;
    if (!chAcidL.includes(e)) chAcidL.push(e);
    if (!e.acidS && e.mesh) { const s = new THREE.Sprite(chAcidMat); s.position.set(-0.15, 0.18, 0.025); s.scale.setScalar(0.34); s.renderOrder = 1; e.mesh.add(s); e.acidS = s; }
  }
  function chAcidBurst(z) {                    // c224: 동료·변이가 죽으며 산성피 — 범위 = 그 몸의 근접 거리 × 1.2 (강화마다 +15%) · 3초 (강화마다 +1초)
    const n = lv('acid'), R = chReach(z) * 1.2 * (1 + 0.15 * n), T = 3 + n, x = z.foot.x, zz = z.foot.z;
    const f = puff(x, 0.5, zz, 0xd8ff9a, R * 0.8, R * 2.4, 0.22, 0, 0, 0, 0.9); f.s.renderOrder = UI - 0.6; f.peak = true;
    for (let i = 0; i < 12; i++) { const a = Math.random() * Math.PI * 2, sp = rand(1.5, 3.5) * R; const g = puff(x, 0.3, zz, i % 2 ? 0x3f8f2a : 0x7ed321, rand(0.25, 0.4), rand(0.3, 0.5), rand(0.35, 0.6), Math.cos(a) * sp, 0, Math.sin(a) * sp, 0.95); g.s.material.map = flashTex; }
    for (const c of nearIn(cCells, x, zz, R + 1, chAcBuf)) {
      if (c.kind !== 'citizen' || c.space !== z.space) continue;
      if (Math.hypot(c.foot.x - x, c.foot.z - zz) > R + (c.r || BODY) || blocked(x, zz, c.foot.x, c.foot.z)) continue;
      chAcidOn(c, T);
    }
    const tk = chTank; if (tk && !tk.wreck && !z.space && Math.hypot(tk.x - x, tk.z - zz) - CAR_L * CH_TK_KL / 2 <= R) chAcidOn(tk, T);   // 보스도
  }
  window.__kz = (z) => killZombie(z);   // 테스트용
  function chAcidTick(dt) {                    // c224: 겹마다 시간이 줄고, 0.5초마다 겹 수만큼 피해 (느려짐 없음)
    for (let i = chAcidL.length - 1; i >= 0; i--) {
      const e = chAcidL[i], car = e.tank;
      const gone = car ? e.wreck : (e.kind !== 'citizen' || !bodies.includes(e));
      for (let k = e.acid.length - 1; k >= 0; k--) if ((e.acid[k] -= dt) <= 0) e.acid.splice(k, 1);
      if (gone || !e.acid.length) { if (e.acidS) { e.mesh.remove(e.acidS); e.acidS = null; } e.acid.length = 0; e.acidT = 0; chAcidL.splice(i, 1); continue; }
      if ((e.acidT += dt) < 0.5) continue;
      e.acidT -= 0.5; const d = e.acid.length;
      if (car) { const o = e.obj; if (o && o.hp > d) o.hp -= d; continue; }
      if (e.hp <= 0) continue;
      e.hp = Math.max(0, e.hp - d);
      if (e.hp <= 0 && !e.police && e.state !== 'held') enterPanic(e, null, true);
    }
  }
  function gooTick(dt) {"""),
 ("    gooTick(dt);", "    gooTick(dt); if (CHAPTER) chAcidTick(dt);   // c224"),
 # ── 레벨업 무기 강화 카드 25% 줄임 (몫 1.5 → 1.125) ──
 ("Array(chWupN() * 1.5 | 0).fill('__w').concat(chWupN() % 2 && Math.random() < 0.5 ? ['__w'] : [])", "Array(chWupW()).fill('__w')   /* c224: 25% 더 줄임 */"),
 ("  function chWupCard() {", "  const chWupW = () => { const w = chWupN() * 1.5 * 0.75; return Math.floor(w) + (Math.random() < w - Math.floor(w) ? 1 : 0); };   // c224: 무기 강화 카드 몫 (소수는 확률로)\n  window.__lvup = () => { pendingLv++; };   // 테스트용\n  function chWupCard() {"),
 # ── 무기 분해 ──
 ("    tapOk(ov, '획득', () => {                 // v265", "    (CHAPTER && !d.passive && chCanDis(kind) ? chTwoOk : tapOk)(ov, '획득', () => {                 // v265 · c224: 다른 무기가 있으면 획득/분해"),
 ("  function tapOk(ov, label, done) {",
  """  const chCanDis = (kind) => chWeapons().some((k) => k !== kind && lv(k) < chLvMax(k));   // c224: 분해해서 강화할 무기가 있나
  function chTwoOk(ov, label, done) {          // c224: [획득] [분해] 두 갈래 — 각자 한 줄 설명
    const blockA = (e) => { e.stopPropagation(); e.preventDefault(); };
    for (const ev of ['pointerdown', 'pointermove', 'pointerup']) ov.addEventListener(ev, blockA);
    const kind = ov.dataset.kind, row = document.createElement('div');
    row.style.cssText = 'display:flex;gap:14px;margin-top:22px;justify-content:center';
    const mk = (lb, ds, bg, fn) => { const left = !row.children.length, col = document.createElement('div'); col.style.cssText = 'display:flex;flex-direction:column;align-items:center;width:146px';
      const b = document.createElement('button'); b.className = 'ok okBtn'; b.style.setProperty('margin', `0 0 0 ${left ? -140 : 16}px`, 'important'); b.style.background = bg; b.textContent = lb;   // 조이스틱 자리 양옆으로 동그라미 두 개
      const t = document.createElement('div'); t.style.cssText = 'margin-top:0;font:700 13px/1.35 var(--font);color:rgba(255,255,255,0.8);text-align:center;word-break:keep-all'; t.textContent = ds;
      b.addEventListener('pointerdown', (e) => { blockA(e); if (ov.dataset.done) return; row.style.visibility = 'hidden'; fn(); });
      col.append(b, t); row.appendChild(col); };
    mk(label, '무기를 사용할 수 있습니다', 'rgba(255,255,255,0.92)', done);
    mk('분해', '분해해서 다른 무기를 강화합니다', '#ffb26b', () => { ov.dataset.done = '1'; chDisasm(ov, kind); });
    ov.appendChild(row);
  }
  function chDisasm(ov, kind) {                // c224: 분해 — 짧게 부서지는 연출 → 강화할 무기를 고르는 창
    const big = ov.querySelector('.big'), sr = stage.getBoundingClientRect();
    if (big) {
      const br = big.getBoundingClientRect(), cx = br.left + br.width / 2 - sr.left, cy = br.top + br.height / 2 - sr.top;
      big.style.transition = 'transform 0.12s'; let k = 0; const sh = setInterval(() => { big.style.transform = `translate(${(k % 2 ? -1 : 1) * 7}px, ${(k % 3 - 1) * 4}px) rotate(${(k % 2 ? -1 : 1) * 6}deg)`; if (++k > 4) clearInterval(sh); }, 45);
      setTimeout(() => { big.style.visibility = 'hidden';
        for (let i = 0; i < 14; i++) { const p = document.createElement('div'), a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 90;
          p.style.cssText = `position:absolute;left:${cx}px;top:${cy}px;width:${8 + Math.random() * 10}px;height:${6 + Math.random() * 8}px;background:${i % 3 ? '#9aa4b5' : '#ffb26b'};border-radius:2px;z-index:23;pointer-events:none;transition:transform 0.38s ease-out, opacity 0.38s ease-out;transform:translate(-50%,-50%)`;
          stage.appendChild(p); p.getBoundingClientRect(); p.style.transform = `translate(calc(-50% + ${Math.cos(a) * d}px), calc(-50% + ${Math.sin(a) * d}px)) rotate(${Math.random() * 360}deg)`; p.style.opacity = '0'; setTimeout(() => p.remove(), 420); }
      }, 240);
    }
    setTimeout(() => { ov.remove(); chDisPick(); }, 620);
  }
  function chDisPick() {                       // c224: 분해한 부품으로 강화할 무기를 고른다 (끝까지 올린 것은 못 고른다)
    const ov = document.createElement('div'); ov.id = 'pick';
    ov.innerHTML = `<div class="hd">무기 강화</div><div class="sub">강화할 무기를 선택하세요</div><div class="cards" style="flex-wrap:wrap;justify-content:center">` +
      chWeapons().map((k) => { const n = lv(k), S = CH_SHORT[k], max = n >= chLvMax(k);
        return `<div class="card" data-k="${k}" style="min-height:158px;padding-top:8px${max ? ';opacity:0.4;pointer-events:none' : ''}"><div style="height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:#ffd34d">${max ? 'MAX' : chStars(n + 1)}</div>` +
          `<div class="ic" style="margin-top:4px">${ITEM[k].icon}</div><div class="nm" style="margin-top:8px">${ITEM[k].name}</div><div class="ds" style="margin-top:8px">${max ? '최대 강화' : '강화'}</div>` +
          `<div class="vl">${S[0]} ${max ? S[1](n) : S[1](n) + ' → ' + S[1](n + 1)}</div></div>`; }).join('') + `</div><button class="ok okBtn">확인</button>`;
    stage.appendChild(ov);
    let chosen = null; const block = (e) => { e.stopPropagation(); e.preventDefault(); };
    ov.addEventListener('pointermove', block); ov.addEventListener('pointerup', block);
    ov.addEventListener('pointerdown', (e) => {
      block(e); if (ov.dataset.done) return;
      const card = e.target.closest('.card'), ok = e.target.closest('.ok');
      if (card) { chosen = card.dataset.k; for (const c of ov.querySelectorAll('.card')) c.classList.toggle('on', c === card); ov.querySelector('.ok').classList.add('ready'); return; }
      if (!ok || !chosen) return;
      ov.dataset.done = '1';
      for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === chosen ? 'win' : 'gone'); }
      ov.querySelector('.ok').style.opacity = '0';
      ilv[chosen] = lv(chosen) + 1; chItemChanged(chosen);
      const el = (items.find((x) => x.kind === chosen) || {}).el; if (el) { el.classList.remove('pop'); el.getBoundingClientRect(); el.classList.add('pop'); }
      setTimeout(() => { ov.style.opacity = '0'; }, 550);
      setTimeout(() => { ov.remove(); acqOpen = false; paused = false; last = 0; }, 850);
    });
  }
  function tapOk(ov, label, done) {"""),
 ("    const d = ITEM[kind], ov = document.createElement('div');\n    ov.id = 'acq';\n    ov.innerHTML = (CHAPTER && !d.passive ? `<div style=\"font:900 54px",
  "    const d = ITEM[kind], ov = document.createElement('div');\n    ov.id = 'acq'; ov.dataset.kind = kind;   // c224\n    ov.innerHTML = (CHAPTER && !d.passive ? `<div style=\"font:900 54px"),
]
