# c19: 금고와 아이템 (챕터) — build.py가 불러다 R 뒤에 붙인다. (찾을 글, 바꿀 글[, 나와야 하는 횟수])
LOOT = r'''  // ── c19: 금고와 아이템 (챕터) ──
  //   건물마다 금고: 집 말고는 전부 하나씩, 집은 5%만 (지붕 표시 없음 — 문을 열고 들어가 봐야 안다. 집 금고에는 꽝이 없다)
  //   금고를 깨면 건물 종류에 따라 아이템 하나 또는 꽝. 아이템은 그 자리에 떨어지고 내가 가서 닿아야 얻는다 (테스트맵과 같다)
  //   아이템 14종 = 도구 5 (자폭 스위치 · 변이 주사 · 테이저건 · 각성 주사 · 현금) + 장비 9 (백과사전 · 가방 · 분노 바이러스 · 빠루 · 충격 흡수복 · 방탄복 · 운동화 · 촉매제 · 혈액팩)
  //   같은 아이템을 또 얻으면 그 아이템만 강화 +1 (최대 5단계, 가방은 2단계)
  const CH_ITEMS = ['bomb', 'mutate', 'taser', 'awaken', 'cash', 'book', 'bag', 'rage', 'crowbar', 'absorb', 'vest', 'shoes', 'catalyst', 'blood'];
  const CH_RARE = ['cash', 'book', 'bomb'];   // '나머지' 안에서 다른 아이템의 10분의 1 확률 (집·창고는 균등)
  const CH_SPEC_1 = 46.1893, CH_SPEC_2 = 19.8265;   // 지정 아이템 하나의 확률(%) — 랜드마크를 하나씩 다 털면 14종이 똑같이 나오게 맞춘 값 (표의 46.2 · 19.8)
  const CH_DROP = {                           // spec = 지정 아이템, p = 지정 하나의 확률(%), rest = 나머지 전체(%), 남는 것 = 꽝
    bank: { spec: ['cash'], p: CH_SPEC_1, rest: 90 - CH_SPEC_1 }, library: { spec: ['book'], p: CH_SPEC_1, rest: 90 - CH_SPEC_1 }, army: { spec: ['bomb'], p: CH_SPEC_1, rest: 90 - CH_SPEC_1 },
    police: { spec: ['taser', 'vest'], p: CH_SPEC_2, rest: 90 - 2 * CH_SPEC_2 }, fire: { spec: ['crowbar', 'absorb'], p: CH_SPEC_2, rest: 90 - 2 * CH_SPEC_2 }, mart: { spec: ['shoes', 'bag'], p: CH_SPEC_2, rest: 90 - 2 * CH_SPEC_2 },
    hospital: { spec: ['mutate', 'awaken', 'catalyst', 'rage', 'blood'], p: 16, rest: 10 },
    store: { spec: [], p: 0, rest: 90, flat: true }, conv: { spec: [], p: 0, rest: 30 }, gym: { spec: [], p: 0, rest: 30 },
    house: { spec: [], p: 0, rest: 100, flat: true },   // 집: 금고가 있는 집(5%)이면 꽝 없이 14종 균등
  };
  const CH_HOUSE_SAFE = 0.05;
  function chLoot(type) {                     // 그 건물 금고에서 나올 것 — 아이템 이름, 꽝이면 null
    const T = CH_DROP[type]; let r = Math.random() * 100;
    for (const k of T.spec) if ((r -= T.p) < 0) return k;
    if (r >= T.rest) return null;
    const pool = CH_ITEMS.filter((k) => !T.spec.includes(k)), w = pool.map((k) => T.flat || !CH_RARE.includes(k) ? 1 : 0.1);
    let q = Math.random() * w.reduce((a, c) => a + c, 0);
    for (let i = 0; i < pool.length; i++) if ((q -= w[i]) < 0) return pool[i];
    return pool[pool.length - 1];
  }
  function chSafes() {
    for (const B of buildings) {
      B.safe = null;
      if (B.type === 'hill' || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;
      addSafe(B);
      const s = B.safe; s.B = B; s.loot = chLoot(B.type); s.dud = !s.loot;
      for (const c of bodies) {               // 금고 자리에 겹친 사람은 옆으로 (자는 사람은 부딪힘 계산을 안 해서 겹친 채 남는다)
        if (c.kind !== 'citizen' || c.space !== B) continue;
        const dx = c.foot.x - s.foot.x, dz = c.foot.z - s.foot.z, d = Math.hypot(dx, dz), R = s.r + BODY + 0.1;
        if (d >= R) continue;
        const ux = d > 1e-6 ? dx / d : 1, uz = d > 1e-6 ? dz / d : 0;
        c.foot.x = Math.max(B.x0 + 0.6, Math.min(B.x1 - 0.6, s.foot.x + ux * R)); c.foot.z = Math.max(B.z0 + 0.6, Math.min(B.z1 - 0.6, s.foot.z + uz * R));
      }
    }
  }
  const chLvMax = (k) => k === 'bag' ? 2 : 5;
  const chHas = (k) => ITEM[k].passive ? !!owned[k] : items.some((x) => x.kind === k);
  const chToolCap = () => Math.min(SLOT_A.length, 2 + (owned.bag ? 1 + lv('bag') : 0));   // 도구는 2개까지 (테스트맵과 같다) — 가방 하나마다 +1, 최대 5
  function chCanTake(kind) {                  // 바닥의 아이템을 지금 주울 수 있나 — 새 도구는 칸이 남아야 한다 (장비와, 이미 가진 것의 강화는 늘 된다)
    if (ITEM[kind].passive || chHas(kind)) return true;
    const waiting = pendingAward.concat(fxQueue.filter((e) => e.t === 'award').map((e) => e.k)).filter((k, i, a) => ITEM[k] && !ITEM[k].passive && !chHas(k) && a.indexOf(k) === i);
    return waiting.includes(kind) || items.length + waiting.length < chToolCap();
  }
  function chItemChanged(kind) {              // 얻었거나 강화한 바로 그때 적용할 것
    if (kind === 'blood' && isZombie(me)) {   // 혈액팩: 나만 최대 체력 +10% (기본 체력 기준 — 얻을 때, 그리고 강화할 때마다)
      const d = MY_HP * 0.10;
      if (me.baseMaxHp) { me.baseMaxHp += d; me.maxHp += d * 3; me.hp = Math.min(me.maxHp, me.hp + d * 3); } else { me.maxHp += d; me.hp = Math.min(me.maxHp, me.hp + d); }
    }
    if (kind === 'shoes' && isZombie(me)) me.speed = meSpeed();
    refreshBadges(); refreshItems();
  }
  function chUpgrade(kind) {                  // 가진 아이템을 또 얻었다 → 그 아이템만 강화 +1 (획득창과 같은 모양)
    acqOpen = true; paused = true; stopInput();
    const d = ITEM[kind], n = lv(kind), max = n >= chLvMax(kind), ov = document.createElement('div');
    ov.id = 'acq';
    ov.innerHTML = `<div class="big">${d.icon}</div><div class="t">${d.name} ${max ? '(이미 최대 강화)' : '강화'}</div><div class="ds">${itemDesc(kind)}<div class="up">` +
      (max ? `지금 (강화 ${n}단계 · 최대): ${statLine(kind, n)}` : `지금 (강화 ${n}단계): ${statLine(kind, n)}<br>강화 뒤 (${n + 1}단계): ${statLine(kind, n + 1)}`) + `</div></div>`;
    stage.appendChild(ov);
    tapOk(ov, max ? '확인' : '강화', () => {
      if (ov.dataset.done) return;
      ov.dataset.done = '1';
      if (!max) {
        ilv[kind] = n + 1; chItemChanged(kind);
        const el = ITEM[kind].passive ? pBadges[kind] : (items.find((x) => x.kind === kind) || {}).el;
        if (el) { el.classList.remove('pop'); el.getBoundingClientRect(); el.classList.add('pop'); }
      }
      ov.remove(); acqOpen = false; paused = false; last = 0;
    });
  }
  function chBadgeGrid() {                    // 장비 배지 = 왼쪽 아래에 3칸씩 위로 쌓는다 (최대 9개 — 한 줄로 늘어놓으면 조이스틱과 능력치 버튼에 닿는다)
    Object.values(pBadges).forEach((el, i) => {
      el.style.left = `calc(max(16px, env(safe-area-inset-left, 0px)) + ${(i % 3) * 40}px)`;
      el.style.bottom = `calc(6px + env(safe-area-inset-bottom, 0px) + ${Math.floor(i / 3) * 48}px)`;
      el.style.width = el.style.height = '36px';
      const m = el.querySelector('.mag'); if (m) m.style.display = 'none';
    });
  }
  let rageT = 0;
  function rageTick(dt) {                     // 분노 바이러스: 일정 시간마다 아직 안 걸린 동료 한 명 — 공격 속도·이동 속도 +5% (그 동료가 살아 있는 동안 계속)
    if (!owned.rage || !isZombie(me)) return;
    const cand = zombies.filter((z) => z !== me && isZombie(z) && !z.rage);
    if (!cand.length) return;                 // 걸 동료가 없으면 시간도 멈춘다
    if ((rageT += dt) < 25 - lv('rage')) return;
    rageT = 0;
    const z = cand[Math.floor(Math.random() * cand.length)];
    z.rage = true;
    z.flame = new THREE.Sprite(flameMat); z.flame.scale.set(0.6, 0.6, 1); z.flame.renderOrder = UI; scene.add(z.flame); stimmed.push(z);   // 머리 위 작은 불꽃 (따라다니기·지우기는 스팀팩 코드가 한다)
    for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; puff(z.foot.x, 0.4, z.foot.z, 0xff5a3c, 0.4, 1.1, 0.4, Math.cos(a) * 2.2, 0.4, Math.sin(a) * 2.2, 0.85); }
  }
'''
ICONS4 = r'''  IC.bag = svgI('<path d="M8 7V5.5A2.5 2.5 0 0 1 10.5 3h3A2.5 2.5 0 0 1 16 5.5V7" fill="none" stroke="#c9a06a" stroke-width="2"/><rect x="4" y="7" width="16" height="14" rx="3" fill="#a9763f"/><rect x="7" y="12" width="10" height="5" rx="1.5" fill="#c9965a"/><rect x="11" y="11" width="2" height="3" rx="0.6" fill="#f2d9a8"/>');   // c19: 가방
  IC.rage = svgI('<circle cx="12" cy="12" r="6" fill="#d8342c"/><g stroke="#d8342c" stroke-width="2.2" stroke-linecap="round"><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/></g><circle cx="10" cy="11" r="1.5" fill="#ffd9d4"/><circle cx="14.2" cy="13.4" r="1.1" fill="#ffd9d4"/>');   // c19: 분노 바이러스
  IC.catalyst = svgI('<path d="M9.5 3h5v2h-1v5l5 8.5a1.7 1.7 0 0 1-1.5 2.5H7a1.7 1.7 0 0 1-1.5-2.5l5-8.5V5h-1z" fill="#dfe7f2"/><path d="M8.2 15h7.6l2 3.5a1 1 0 0 1-.9 1.5H7.1a1 1 0 0 1-.9-1.5z" fill="#4fd08a"/><circle cx="11" cy="17.5" r="0.9" fill="#d9ffe9"/><circle cx="14" cy="16.3" r="0.6" fill="#d9ffe9"/>');   // c19: 촉매제
  IC.blood = svgI('<rect x="10" y="2" width="4" height="3" rx="1" fill="#cfd6e3"/><path d="M7 5h10a2 2 0 0 1 2 2v10a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V7a2 2 0 0 1 2-2z" fill="#f4e9e9"/><path d="M6.5 11h11v6a3 3 0 0 1-3 3h-5a3 3 0 0 1-3-3z" fill="#d8342c"/><rect x="11" y="12.5" width="2" height="5.5" fill="#fff"/><rect x="9.25" y="14.25" width="5.5" height="2" fill="#fff"/>');   // c19: 혈액팩
'''
LV_OLD = '<div class="up">지금 (강화 ${up.brain}단계): ${statLine(kind, up.brain)}<br>다음 강화: ${statLine(kind, up.brain + 1)}</div>'
LOOT_R = [
  # ── 아이템마다 강화 단계 ──
  ("const up = { brain: 0, meat: 0, arm: 0, bite: 0, skin: 0, leg: 0, life: 0 };",
   "const up = { brain: 0, meat: 0, arm: 0, bite: 0, skin: 0, leg: 0, life: 0 };\n"
   "  const ilv = {};                             // c19: 아이템마다 강화 단계 (챕터) — 같은 걸 또 얻으면 그것만 +1. 테스트맵은 지금까지처럼 '장비/도구 강화' 한 값을 다 같이 쓴다\n"
   "  const lv = (k) => CHAPTER ? (ilv[k] || 0) : up.brain;\n"
   "  const lvText = (kind) => { const n = lv(kind), max = CHAPTER && n >= chLvMax(kind); return `지금 (강화 ${n}단계${max ? ' · 최대' : ''}): ${statLine(kind, n)}` + (max ? '' : `<br>다음 강화: ${statLine(kind, n + 1)}`); };"),
  (LV_OLD, '<div class="up">${lvText(kind)}</div>', 2),
  ("owned.absorb ? SNIPER_KD / 4 * (1 + up.brain) : 0;", "owned.absorb ? SNIPER_KD / 4 * (1 + lv('absorb')) : 0;"),
  ("base * vestK(up.brain) : base", "base * vestK(lv('vest')) : base"),
  ("dmg *= 1.4 + 0.1 * up.brain;", "dmg *= 1.4 + 0.1 * lv('crowbar');"),
  ("(owned.shoes ? 0.10 + 0.03 * up.brain : 0)", "(owned.shoes ? 0.10 + 0.03 * lv('shoes') : 0)"),
  ("const cashK = () => 1.2 + 0.2 * up.brain;", "const cashK = () => 1.2 + 0.2 * lv('cash');"),
  ("const lureHits = () => 2 + 2 * up.brain;", "const lureHits = () => 2 + 2 * lv('cash');"),
  ("cand.slice(0, taserN(up.brain));", "cand.slice(0, taserN(lv('taser')));"),
  ("c.stunT = taserT(up.brain);", "c.stunT = taserT(lv('taser'));"),
  ("const MUT_T = () => 23 + 4 * up.brain;", "const MUT_T = () => 23 + 4 * lv('mutate');"),
  ("k === 'mutate' ? 1 + up.brain : ITEM[k].max;", "k === 'mutate' ? 1 + lv('mutate') : ITEM[k].max;"),
  ("1 - Math.pow(0.93, up.brain + 1) : 0;", "1 - Math.pow(0.93, lv('book') + 1) : 0;"),
  ("Math.max(10, 40 - 3 * up.brain) * 1.15 * 1.1", "Math.max(10, 40 - 3 * lv('bomb')) * 1.15 * 1.1"),
  ("      vest: () => '-' + vestPct(up.brain) + '%',", "      vest: () => '-' + vestPct(lv('vest')) + '%',"),
  ("      absorb: () => Math.min(100, 25 * (1 + up.brain)) + '%',", "      absorb: () => Math.min(100, 25 * (1 + lv('absorb'))) + '%',"),
  ("      crowbar: () => '+' + Math.round(40 + 10 * up.brain) + '%',", "      crowbar: () => '+' + Math.round(40 + 10 * lv('crowbar')) + '%',"),
  ("      shoes: () => '+' + Math.round(10 + 3 * up.brain) + '%',",
   "      shoes: () => '+' + Math.round(10 + 3 * lv('shoes')) + '%',\n"
   "      bag: () => chToolCap() + '칸', rage: () => (25 - lv('rage')) + '초', catalyst: () => '+' + 5 * (1 + lv('catalyst')) + '%', blood: () => '+' + 10 * (1 + lv('blood')) + '%',   // c19"),
  ("me.mutT = 15 + 1.5 * up.brain;", "me.mutT = 15 + 1.5 * lv('awaken');"),
  # 강화 별: 아이템마다 자기 단계
  ("    const n = up.brain, els = [...items.map((it) => it.el), ...Object.values(pBadges), ...Object.values(aBadges)];",
   "    let n = up.brain; const els = [...items.map((it) => it.el), ...Object.values(pBadges), ...Object.values(aBadges)], kd = [...items.map((it) => it.kind), ...Object.keys(pBadges), ...Object.keys(aBadges)];"),
  ("      let t = el.querySelector(':scope > .upn');\n      if (!n) { if (t) t.remove(); continue; }",
   "      if (CHAPTER) n = lv(kd[els.indexOf(el)]);   // c19: 아이템마다 자기 강화 단계\n      let t = el.querySelector(':scope > .upn');\n      if (!n) { if (t) t.remove(); continue; }"),
  ("const st = Array.from({ length: Math.ceil(n / 3) }, (_, i) => '★'.repeat(Math.min(3, n - i * 3))).reverse().join('<br>');",
   "const st = CHAPTER ? '★' + n : Array.from({ length: Math.ceil(n / 3) }, (_, i) => '★'.repeat(Math.min(3, n - i * 3))).reverse().join('<br>');   /* c19: 배지가 촘촘해서 별 하나 + 숫자 */"),
  # 레벨업 카드에서 '장비/도구 강화'는 뺀다 (강화는 같은 아이템을 또 얻을 때)
  ("const pool = Object.keys(ABIL).map((k) => [k, k === 'brain' ? 0.25 : 1]), keys = [];",
   "const pool = Object.keys(ABIL).filter((k) => !(CHAPTER && k === 'brain')).map((k) => [k, k === 'brain' ? 0.25 : 1]), keys = [];   /* c19: 챕터는 '장비/도구 강화' 카드 없음 */"),
  # ── 새 아이템 4종 ──
  ("  const ITEM = {\n", ICONS4 + "  const ITEM = {\n"),
  ("    shoes: { icon: IC.shoes, name: '운동화', passive: true },",
   "    bag: { icon: IC.bag, name: '가방', passive: true }, rage: { icon: IC.rage, name: '분노 바이러스', passive: true }, catalyst: { icon: IC.catalyst, name: '촉매제', passive: true }, blood: { icon: IC.blood, name: '혈액팩', passive: true },   // c19: 챕터 장비 4종\n"
   "    shoes: { icon: IC.shoes, name: '운동화', passive: true },"),
  ("    shoes: ['나의 이동 속도가 빨라집니다.', '강화 시 더 빨라집니다.'],",
   "    shoes: ['나의 이동 속도가 빨라집니다.', '강화 시 더 빨라집니다.'],\n"
   "    bag: ['들 수 있는 도구가 하나 늘어납니다.', '강화 시 하나 더 늘어납니다.'],\n"
   "    rage: ['일정 시간마다 동료 한 명의 공격 속도와 이동 속도가 오릅니다.', '강화 시 더 자주 퍼집니다.'],\n"
   "    catalyst: ['변이한 좀비의 공격력이 오릅니다.', '강화 시 더 오릅니다.'],\n"
   "    blood: ['나의 최대 체력이 늘어납니다.', '강화 시 더 늘어납니다.'],"),
  ("shoes: () => `이동 속도 +${10 + 3 * n}%`,",
   "shoes: () => `이동 속도 +${10 + 3 * n}%`,\n"
   "      bag: () => `도구 ${Math.min(5, 3 + n)}칸`, rage: () => `${25 - n}초마다 동료 1명 · 공격 속도·이동 속도 +5%`, catalyst: () => `변이 좀비 공격력 +${5 * (1 + n)}%`, blood: () => `내 최대 체력 +${10 * (1 + n)}%`,   // c19"),
  ("(z.mut === 'armor' && z !== me ? 1.3 * 1.3 * 2 : 1);", "(z.mut === 'armor' && z !== me ? 1.3 * 1.3 * 2 : 1) * (CHAPTER && z.mut && owned.catalyst ? 1 + 0.05 * (1 + lv('catalyst')) : 1);   /* c19: 촉매제 */"),
  ("if (z.atkT > 0) z.atkT -= dt;", "if (z.atkT > 0) z.atkT -= dt * (z.rage ? 1.05 : 1);   /* c19: 분노 바이러스 — 공격 속도 +5% */"),
  ("const gk = b.goo ? 0.56 : 1;", "const gk = (b.goo ? 0.56 : 1) * (b.rage ? 1.05 : 1);   /* c19: 분노 바이러스 — 이동 속도 +5% */"),
  ("    stimTick(dt);", "    stimTick(dt);\n    if (CHAPTER) rageTick(dt);"),
  ("trickleT = TRICKLE_T; stimT = 0; reviveT = 0;", "trickleT = TRICKLE_T; stimT = 0; reviveT = 0; rageT = 0;"),
  # ── 도구 칸 · 배지 ──
  ("const SLOT_A = [45, 15, 75], SLOT_R = 125;", "const SLOT_A = CHAPTER ? [45, 15, 75, 105, 135] : [45, 15, 75], SLOT_R = 125;   /* c19: 가방을 얻으면 도구 칸이 5개까지 */"),
  ("stage.appendChild(el); pBadges[kind] = el;", "stage.appendChild(el); pBadges[kind] = el; if (CHAPTER) chBadgeGrid();"),
  ("    }\n  }\n  function toast(text) {", "    }\n    if (CHAPTER) chBadgeGrid();\n  }\n  function toast(text) {"),
  # ── 금고 ──
  ("    if (!S.station && !S.qm) {", "    if (!CHAPTER && !S.station && !S.qm) {   // c19: 챕터는 지붕 물음표 없음 (건물 아이콘이 이미 있고, 집은 열어 봐야 안다)"),
  ("    if (b.dud) { dust(b.foot.x, b.foot.z, 16, 1.4);", "    if (CHAPTER && b.B) b.B.done = true;       // c19: 금고를 깬 건물 = 잠식 (지붕·미니맵 아이콘이 X로)\n    if (b.dud) { dust(b.foot.x, b.foot.z, 16, 1.4);"),
  ("    if (b.hidden) {", "    if (CHAPTER) { dropPickup(b.loot, b.foot.x, b.foot.z, b.space); return; }   // c19: 그 금고에 든 아이템이 떨어진다\n    if (b.hidden) {"),
  ("      if (isZombie(me) && me.space === p.space && Math.hypot(me.foot.x - p.x, me.foot.z - p.z) <= PICK_R) {",
   "      if (isZombie(me) && me.space === p.space && Math.hypot(me.foot.x - p.x, me.foot.z - p.z) <= PICK_R) {\n"
   "        if (CHAPTER && !chCanTake(p.kind)) { if (!(p.warn > clock)) { p.warn = clock + 4; toast('도구 칸이 꽉 찼습니다 — 가방이 있어야 더 들 수 있습니다'); } continue; }   // c19: 새 도구는 칸이 남아야 줍는다 (바닥에 그대로 남는다)"),
  ("if (e.k === 'dud') showDud(); else showAward(e.k);", "if (e.k === 'dud') showDud(); else if (CHAPTER && chHas(e.k)) chUpgrade(e.k); else showAward(e.k);", 2),
  ("if (it.passive) { owned[kind] = true; if (kind === 'vest') hasVest = true; if (kind === 'shoes' && isZombie(me)) me.speed = meSpeed(); refreshBadges(); } else { items.push(it); addActiveBadge(kind); }",
   "if (it.passive) { owned[kind] = true; if (kind === 'vest') hasVest = true; if (kind === 'shoes' && isZombie(me)) me.speed = meSpeed(); refreshBadges(); } else { items.push(it); addActiveBadge(kind); }\n        if (CHAPTER) chItemChanged(kind);"),
  ("    for (const k of Object.keys(owned)) delete owned[k];", "    for (const k of Object.keys(owned)) delete owned[k];\n    for (const k of Object.keys(ilv)) delete ilv[k];   // c19"),
  ("  function showDud() {", LOOT + "  function showDud() {"),
  ("chPopulate(); return; }", "chPopulate(); chSafes(); return; }"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, loot: CHAPTER ? chLoot : null, breakSafe, give: (k) => pendingAward.push(k), inv: () => ({ tools: items.map((x) => x.kind + ':' + x.ammo), owned: Object.keys(owned), lv: Object.assign({}, ilv), cap: chToolCap(), pickups: pickups.map((p) => [p.kind, +p.x.toFixed(1), +p.z.toFixed(1)]), acq: acqOpen }), zDamage,"),
]
