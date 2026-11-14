# c19: 금고와 아이템 (챕터) — build.py가 불러다 R 뒤에 붙인다. (찾을 글, 바꿀 글[, 나와야 하는 횟수])
LOOT = r'''  // ── c19: 금고와 아이템 (챕터) ──
  //   건물마다 금고: 집 말고는 전부 하나씩, 집은 5%만 (지붕 표시 없음 — 문을 열고 들어가 봐야 안다. 집 금고에는 꽝이 없다)
  //   금고를 깨면 건물 종류에 따라 아이템 하나 또는 꽝. 아이템은 그 자리에 떨어지고 내가 가서 닿아야 얻는다 (테스트맵과 같다)
  //   아이템 14종 = 도구 5 (자폭 스위치 · 변이 주사 · 테이저건 · 각성 주사 · 현금) + 장비 9 (백과사전 · 가방 · 분노 바이러스 · 빠루 · 충격 흡수복 · 방탄복 · 운동화 · 촉매제 · 혈액팩)
  //   같은 아이템을 또 얻으면 그 아이템만 강화 +1 (최대 5단계). 가방은 4개까지 (도구 칸 1 → 5). 끝까지 올린 아이템은 더 안 나온다 (c21)
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
        for (let t = 0; t < 40 && (Math.hypot(c.foot.x - s.foot.x, c.foot.z - s.foot.z) < R || bodies.some((o) => o !== c && o.kind === 'citizen' && Math.hypot(o.foot.x - c.foot.x, o.foot.z - c.foot.z) < 1.0)); t++) {   // c30: 벽 쪽에 막혀 아직 겹치면 그 건물 안 다른 빈 자리로
          c.foot.x = rand(B.x0 + 0.6, B.x1 - 0.6); c.foot.z = rand(B.z0 + 0.6, B.z1 - 0.6);
        }
      }
    }
  }
  const chLvMax = (k) => k === 'bag' ? 3 : 5;   // c21: 가방은 4개가 끝 (도구 칸 5개가 다 열린다)
  const chHas = (k) => ITEM[k].passive ? !!owned[k] : items.some((x) => x.kind === k);
  const chToolCap = () => Math.min(SLOT_A.length, 1 + (owned.bag ? 1 + lv('bag') : 0));   // c21: 쓸 수 있는 도구는 처음 1개 — 가방 하나마다 +1, 최대 5
  const chAccMax = () => 10 + 3 * lv('awaken');   // c21: 각성 주사 — 모을 수 있는 시간(초). 가득 차는 데는 늘 40초
  function chSlots() {                        // c21: 도구는 얻은 순서대로 칸 수만큼만 켜진다 — 칸이 없으면 회색으로 붙어만 있다가, 가방을 얻으면 먼저 얻은 것부터 켜진다
    items.forEach((it, i) => {
      const off = i >= chToolCap();
      if (it.off && !off) { it.ammo = itemMax(it.kind); it.t = 0; if (it.kind === 'awaken') it.acc = chAccMax(); it.el.classList.remove('pop'); it.el.getBoundingClientRect(); it.el.classList.add('pop'); }
      it.off = off;
    });
  }
  const chCopies = (k) => (chHas(k) ? 1 + lv(k) : 0) + pickups.filter((p) => p.kind === k).length + pendingAward.filter((x) => x === k).length + fxQueue.filter((e) => e.t === 'award' && e.k === k).length;
  const chFull = (k) => chCopies(k) >= 1 + chLvMax(k);   // 가진 것 + 바닥에 떨어진 것 + 획득창을 기다리는 것까지 쳐서 끝까지 찼나
  function chFinal(b) {                       // c21: 금고를 깨는 순간 — 끝까지 올린 아이템(가방 4개 등)이 들어 있었으면 그 건물에서 나올 수 있는 다른 아이템으로 바꾼다
    if (!chFull(b.loot)) return b.loot;
    const T = CH_DROP[b.B.type], pool = CH_ITEMS.filter((k) => !chFull(k)), w = pool.map((k) => T.flat || T.spec.includes(k) || !CH_RARE.includes(k) ? 1 : 0.1);
    let q = Math.random() * w.reduce((a, c) => a + c, 0);
    for (let i = 0; i < pool.length; i++) if ((q -= w[i]) < 0) return pool[i];
    return null;
  }
  const CH_STAT = {                           // c21: 획득창·설명창에 나오는 수치 (n = 강화 단계)
    bomb: (n) => `터지는 범위 ${(ATTACK * (1 + 0.2 * n)).toFixed(1)}칸 (${n ? '+' + 20 * n + '%' : '덮치는 거리와 같음'})`,
    mutate: (n) => `주사 ${1 + n}개 · 변이 ${10 + 3 * n}초`,
    taser: (n) => `한 번에 ${1 + n}명 · 3초 감전`,
    awaken: (n) => `최대 ${10 + 3 * n}초 변이 · 가득 모이는 데 40초`,
    cash: (n) => n ? `유혹 강도와 범위 +${n}` : '유혹 강도와 범위 기본',
    book: (n) => `도구 쿨타임 -${5 * (1 + n)}%`,
    bag: (n) => `도구 ${Math.min(5, 2 + n)}칸`,
    rage: (n) => `30초마다 동료 1명 · 공격 속도·이동 속도 +${5 + 2 * n}%`,
    crowbar: (n) => `사물 피해 +${10 * (1 + n)}%`,
    absorb: (n) => `충격 흡수 ${1 + n} (근접 무기 1 · 권총 2 · 군인 3 · 저격수 12)`,
    vest: (n) => `총격 피해 -${10 * (1 + n)}%`,
    shoes: (n) => `이동 속도 +${5 * (1 + n)}%`,
    catalyst: (n) => `변이 좀비 공격력 +${5 * (1 + n)}%`,
    blood: (n) => `내 최대 체력 +${10 * (1 + n)}%`,
  };
  const CH_BADGE = { rage: () => '+' + (5 + 2 * lv('rage')) + '%', absorb: () => '흡수 ' + (1 + lv('absorb')), crowbar: () => '+' + 10 * (1 + lv('crowbar')) + '%', shoes: () => '+' + 5 * (1 + lv('shoes')) + '%' };   // 배지 아래 짧은 수치
  Object.assign(ITEM_TEXT, {                  // c21: 바뀐 규칙에 맞춘 설명
    taser: ['대상을 3초 동안 감전시킵니다.', '강화 시 감전 대상이 늘어납니다.'],
    awaken: ['모아 둔 시간만큼 내가 변이 좀비로 변합니다. 쓰지 않는 동안 시간이 모입니다.', '강화 시 모을 수 있는 시간이 늘어납니다.'],
    bomb: ['가장 위험한 적 곁의 동료 하나가 터지며 산성 덩어리를 뿌립니다.', '강화 시 터지는 범위가 넓어집니다.'],
    bag: ['쓸 수 있는 도구가 하나 늘어납니다.', '하나 더 얻을 때마다 한 칸씩 더 늘어납니다.'],
    absorb: ['총격과 충격에 덜 밀려납니다. 약한 충격은 아예 받지 않습니다.', '강화 시 더 강한 충격도 흡수합니다.'],
    vest: ['총격 피해를 줄여 줍니다.', '강화 시 더 많이 줄여 줍니다.'],
    crowbar: ['사물에 입히는 피해가 늘어납니다.', '강화 시 피해가 더 늘어납니다.'],
    rage: ['30초마다 동료 한 명을 감염시켜 공격 속도와 이동 속도를 올립니다. 변이한 동료가 먼저입니다.', '강화 시 오르는 폭이 커집니다.'],   // c22
  });
  function chItemChanged(kind) {              // 얻었거나 강화한 바로 그때 적용할 것
    if (kind === 'blood' && isZombie(me)) {   // 혈액팩: 나만 최대 체력 +10% (기본 체력 기준 — 얻을 때, 그리고 강화할 때마다)
      const d = MY_HP * 0.10;
      if (me.baseMaxHp) { me.baseMaxHp += d; me.maxHp += d * 3; me.hp = Math.min(me.maxHp, me.hp + d * 3); } else { me.maxHp += d; me.hp = Math.min(me.maxHp, me.hp + d); }
    }
    if (kind === 'shoes' && isZombie(me)) me.speed = meSpeed();
    chSlots(); refreshBadges(); refreshItems();
  }
  function chUpgrade(kind) {                  // 가진 아이템을 또 얻었다 → 그 아이템만 강화 +1 (획득창과 같은 모양)
    acqOpen = true; paused = true; stopInput();
    const d = ITEM[kind], n = lv(kind), max = n >= chLvMax(kind), ov = document.createElement('div');
    ov.id = 'acq';
    ov.innerHTML = `<div class="big">${d.icon}</div><div class="t">${d.name} ${max ? '(이미 최대 강화)' : '강화'}</div>` +
      `<div style="margin-top:6px;font:900 22px/1 var(--font);color:#ffd34d;letter-spacing:1px;text-shadow:0 2px 6px rgba(0, 0, 0, 0.7)">${chStars(max ? n : n + 1)}</div><div class="ds">${itemDesc(kind)}<div class="up">` +   // c26: 강화 단계는 별로
      (max ? `지금${starTag(n)} (최대): ${statLine(kind, n)}` : `지금${starTag(n)}: ${statLine(kind, n)}<br>강화 뒤${starTag(n + 1)}: ${statLine(kind, n + 1)}`) + `</div></div>`;
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
  function chBadgeGrid() {                    // c26: 장비 배지 — 왼쪽 아래 두 줄(3개씩)이 차면 오른쪽 아래에 이어서 (유전자 버튼이 있던 자리)
    Object.values(pBadges).forEach((el, i) => {
      const right = i >= 6, j = right ? i - 6 : i, side = right ? 'right' : 'left';
      el.style.left = 'auto'; el.style.right = 'auto';
      el.style[side] = `calc(max(16px, env(safe-area-inset-${side}, 0px)) + ${(j % 3) * 40}px)`;
      el.style.bottom = `calc(6px + env(safe-area-inset-bottom, 0px) + ${Math.floor(j / 3) * 48}px)`;
      el.style.width = el.style.height = '36px';
      const m = el.querySelector('.mag'); if (m) m.style.display = 'none';
    });
  }
  // ── c25 · c27: 레벨업 = 도구·장비 14종 가운데 랜덤 3장 중 하나를 고른다 — 없는 것이면 새로 얻고, 가진 것이면 강화 +1 ──
  const CH_SHORT = {                          // 카드 한 줄에 쓰는 짧은 수치 — [이름표, n단계 값]
    bomb: ['범위', (n) => n ? `+${20 * n}%` : '기본'], mutate: ['', (n) => `${1 + n}개·${10 + 3 * n}초`], taser: ['대상', (n) => `${1 + n}명`], awaken: ['최대', (n) => `${10 + 3 * n}초`], cash: ['유혹', (n) => n ? `+${n}` : '기본'],
    book: ['쿨타임', (n) => `-${5 * (1 + n)}%`], bag: ['도구', (n) => `${Math.min(5, 2 + n)}칸`], rage: ['속도', (n) => `+${5 + 2 * n}%`], crowbar: ['사물', (n) => `+${10 * (1 + n)}%`], absorb: ['흡수', (n) => `${1 + n}`], vest: ['총격', (n) => `-${10 * (1 + n)}%`],
    shoes: ['이동', (n) => `+${5 * (1 + n)}%`], catalyst: ['변이', (n) => `+${5 * (1 + n)}%`], blood: ['체력', (n) => `+${10 * (1 + n)}%`],
  };
  const CH_BRIEF = {                          // 카드에 쓰는 한 줄 설명
    bomb: '동료 하나가 자폭', mutate: '동료 하나를 변이', taser: '적을 감전', awaken: '내가 변이', cash: '적을 유혹',
    book: '도구 쿨타임 단축', bag: '쓸 수 있는 도구 +1', rage: '동료 속도 강화', crowbar: '사물 피해 증가', absorb: '충격 흡수', vest: '총격 피해 감소', shoes: '내 이동 속도 증가', catalyst: '변이 좀비 공격력 증가', blood: '내 최대 체력 증가',
  };
  function chUpPool() {                       // 레벨업에 나올 수 있는 것 — 14종 전부, 끝까지 올린 것만 뺀다
    return CH_ITEMS.filter((k) => !(chHas(k) && lv(k) >= chLvMax(k)));
  }
  function chGain(kind) {                     // c27: 획득창 없이 바로 얻는다 (레벨업에서 고른 새 아이템) — 금고에서 얻을 때와 같은 자리에 붙는다
    const d = ITEM[kind]; let el;
    if (d.passive) {
      el = document.createElement('div'); el.className = 'pbadge';
      el.innerHTML = `<span class="ic">${d.icon}</span><span class="pc"></span><span class="mag"><svg viewBox="0 0 24 24"><circle cx="10" cy="10" r="6" fill="none" stroke="#e8eef5" stroke-width="3"/><path d="M14.5 14.5 20 20" stroke="#e8eef5" stroke-width="3.4" stroke-linecap="round"/></svg></span>`;
      el.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); showInfo(kind); });
      stage.appendChild(el); pBadges[kind] = el; if (kind === 'vest') { vestEl = el; hasVest = true; }
      owned[kind] = true;
    } else {
      const it = { kind, ammo: itemMax(kind), t: 0, el: makeItemButton(kind, items.length), acc: kind === 'awaken' ? chAccMax() : 0, off: items.length >= chToolCap() };
      items.push(it); addActiveBadge(kind); el = it.el;
    }
    chItemChanged(kind); el.classList.add('pop');
  }
  function chLevelUp() {
    const pool = chUpPool(), keys = [];
    while (keys.length < 3 && pool.length) keys.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);   // 그냥 랜덤 3장 (서로 다른 것)
    if (!keys.length) { lvQueued = Math.max(0, lvQueued - 1); return; }   // 전부 끝까지 올렸으면 뜰 게 없다
    lvOpen = true; paused = true; stopInput();
    const ov = document.createElement('div');
    ov.id = 'pick';
    ov.innerHTML = `<div class="hd">LEVEL UP!</div><div class="sub">Lv ${level} → Lv ${level + 1} · 하나를 고르세요</div><div class="cards">` +
      keys.map((k) => { const has = chHas(k), n = lv(k), S = CH_SHORT[k];
        return `<div class="card" data-k="${k}" style="min-height:158px;padding-top:8px"><div style="height:14px;font:900 12px/14px var(--font);letter-spacing:-0.5px;color:${has ? '#ffd34d' : '#7dffa0'}">${has ? chStars(n) : 'NEW'}</div>` +
          `<div class="ic" style="margin-top:4px">${ITEM[k].icon}</div><div class="nm" style="margin-top:8px">${ITEM[k].name}</div><div class="ds" style="margin-top:8px">${has ? '강화' : CH_BRIEF[k]}</div>` +
          `<div class="vl">${S[0]} ${has ? S[1](n) + ' → ' + S[1](n + 1) : S[1](0)}</div></div>`; }).join('') +
      `</div><button class="ok okBtn">확인</button>`;
    stage.appendChild(ov);
    let chosen = null;
    const block = (e) => { e.stopPropagation(); e.preventDefault(); };
    ov.addEventListener('pointermove', block); ov.addEventListener('pointerup', block);
    ov.addEventListener('pointerdown', (e) => {
      block(e);
      if (ov.dataset.done) return;
      const card = e.target.closest('.card'), ok = e.target.closest('.ok');
      if (card) { chosen = card.dataset.k; for (const c of ov.querySelectorAll('.card')) c.classList.toggle('on', c === card); ov.querySelector('.ok').classList.add('ready'); return; }
      if (!ok || !chosen) return;
      ov.dataset.done = '1';
      for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === chosen ? 'win' : 'gone'); }   // 고른 카드가 커지며 빛나고 나머지는 사라진다
      ov.querySelector('.ok').style.opacity = '0';
      if (chHas(chosen)) { ilv[chosen] = lv(chosen) + 1; chItemChanged(chosen); } else chGain(chosen);   // 가진 것이면 강화, 없는 것이면 새로 얻는다
      pendingLv--; lvQueued = Math.max(0, lvQueued - 1); level++;
      drawLv();
      setTimeout(() => { ov.style.opacity = '0'; }, 550);
      setTimeout(() => { ov.remove(); lvOpen = false; paused = false; last = 0; }, 850);
    });
  }
  let rageT = 0;
  const RAGE_CD = 30, rageK = () => 0.05 + 0.02 * lv('rage');   // c22: 30초 고정 · 효과 5%에서 강화마다 +2%p (15%까지) — 걸린 동료 전원에게 지금 단계가 적용된다
  function rageTick(dt) {                     // 분노 바이러스: 30초마다 아직 안 걸린 동료 한 명 — 공격 속도·이동 속도가 오른다 (그 동료가 살아 있는 동안 계속)
    if (!owned.rage || !isZombie(me)) return;
    rageT = Math.min(RAGE_CD, rageT + dt);    // c22: 30초 고정 — 시간은 늘 흐른다 (백과사전의 영향은 안 받는다 — 장비라서). 다 찼는데 걸 동료가 없으면 생길 때까지 기다렸다가 바로 건다
    if (rageT < RAGE_CD) return;
    const free = zombies.filter((z) => z !== me && isZombie(z) && !z.rage);
    let cand = free.filter((z) => z.mut);     // 1순위 = 변이한 동료 (거리 상관없이. 나는 대상이 아니다 — 내가 각성해 있어도), 없으면 내 근접 거리 안 동료
    if (!cand.length) { const R = NEAR * armyK; cand = free.filter((z) => Math.hypot(z.foot.x - me.foot.x, z.foot.z - me.foot.z) <= R); }
    if (!cand.length && free.length) cand = [free.reduce((a, z) => Math.hypot(z.foot.x - me.foot.x, z.foot.z - me.foot.z) < Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) ? z : a)];   // c23: 곁에 없으면 안 걸린 동료 중 나와 가장 가까운 하나 — 걸 동료가 하나라도 있으면 기다리지 않는다
    if (!cand.length) return;                 // 걸 동료가 아무도 없다 (전부 걸렸거나 동료가 없다) → 쓰지 않고 기다렸다가, 동료가 생기면 바로 건다. 한 번 걸린 동료는 다시 안 걸린다
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
   "  const chStars = (n) => '★'.repeat(Math.max(0, Math.min(5, n)));   // c26: 강화 단계 = 별 (최대 5개)\n"
   "  const starTag = (n) => n ? ` <span style=\"color:#ffd34d;letter-spacing:-1px\">${chStars(n)}</span>` : '';\n"
   "  const lvText = (kind) => { const n = lv(kind); if (!CHAPTER) return `지금 (강화 ${n}단계): ${statLine(kind, n)}<br>다음 강화: ${statLine(kind, n + 1)}`; const max = n >= chLvMax(kind); return `지금${starTag(n)}${max ? ' (최대)' : ''}: ${statLine(kind, n)}` + (max ? '' : `<br>다음 강화${starTag(n + 1)}: ${statLine(kind, n + 1)}`); };"),
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
   "if (CHAPTER) t.style.fontSize = el.classList.contains('pbadge') ? '9px' : '';   /* c26: 배지는 작아서 별도 작게 (5개가 한 줄에 들어가게) */ const st = CHAPTER ? chStars(n) : Array.from({ length: Math.ceil(n / 3) }, (_, i) => '★'.repeat(Math.min(3, n - i * 3))).reverse().join('<br>');   /* c26: 강화 단계만큼 별 (최대 5개, 한 줄) */"),
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
  ("if (z.atkT > 0) z.atkT -= dt;", "if (z.atkT > 0) z.atkT -= dt * (z.rage ? 1 + rageK() : 1);   /* c19 · c22: 분노 바이러스 — 공격 속도 +5~15% */"),
  ("const gk = b.goo ? 0.56 : 1;", "const gk = (b.goo ? 0.56 : 1) * (b.rage ? 1 + rageK() : 1);   /* c19 · c22: 분노 바이러스 — 이동 속도 +5~15% */"),
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
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, rageK: CHAPTER ? rageK : null, loot: CHAPTER ? chLoot : null, breakSafe, give: (k) => pendingAward.push(k), inv: () => ({ tools: items.map((x) => x.kind + ':' + x.ammo), owned: Object.keys(owned), lv: Object.assign({}, ilv), cap: chToolCap(), pickups: pickups.map((p) => [p.kind, +p.x.toFixed(1), +p.z.toFixed(1)]), acq: acqOpen }), zDamage,"),
]

ITEM_R = [   # c21: 도구·장비 수치를 정한 대로 (c19의 결과물 위에 다시 바꾼다)
  ("dmg *= 1.4 + 0.1 * lv('crowbar');", "dmg *= 1 + 0.1 * (1 + lv('crowbar'));   /* c21: 빠루 +10%, 강화마다 +10%p (60%까지) */"),
  ("(owned.shoes ? 0.10 + 0.03 * lv('shoes') : 0)", "(owned.shoes ? 0.05 * (1 + lv('shoes')) : 0)"),
  ("const vestK = (n) => Math.pow(0.8, n + 1);", "const vestK = (n) => CHAPTER ? 1 - 0.1 * (n + 1) : Math.pow(0.8, n + 1);   /* c21: 방탄복 10%, 강화마다 +10%p (60%까지) */"),
  ("owned.absorb ? SNIPER_KD / 4 * (1 + lv('absorb')) : 0;", "owned.absorb ? SNIPER_KD / 12 * (1 + lv('absorb')) : 0;   /* c21: 충격 흡수 1 = 저격수 넉백의 12분의 1 (근접 무기 1 · 권총 2 · 군인 3 · 저격수 12). 강화마다 +1, 6까지 */"),
  ("cand.slice(0, taserN(lv('taser')));", "cand.slice(0, 1 + lv('taser'));   /* c21: 대상만 늘어난다 (1 → 6명) */"),
  ("c.stunT = taserT(lv('taser'));", "c.stunT = STUN_T;   /* c21: 감전은 늘 3초 */"),
  ("const MUT_T = () => 23 + 4 * lv('mutate');", "const MUT_T = () => 10 + 3 * lv('mutate');   /* c21: 변이 10초, 강화마다 +3초 (주사 개수 +1은 테스트맵 그대로) */"),
  ("1 - Math.pow(0.93, lv('book') + 1) : 0;", "0.05 * (1 + lv('book')) : 0;   /* c21: 백과사전 5%, 강화마다 +5%p (30%까지) */"),
  ("Math.max(10, 40 - 3 * lv('bomb')) * 1.15 * 1.1", "40 * 1.15 * 1.1   /* c21: 자폭 쿨타임은 고정 — 강화는 범위로 간다 */"),
  ("    const R = me.sense / 3 * 1.5 * 1.5 * 0.8;", "    const R = ATTACK * (1 + 0.2 * lv('bomb'));   // c21: 자폭 범위 = 내 덮치는 거리(3.24칸), 강화마다 +20% (2배까지)"),
  # 각성 주사: 모아 둔 시간만큼 변이 (회복 없음)
  ("  function awakenMe() {", "  function awakenMe(sec) {"),
  ("me.mutT = 15 + 1.5 * lv('awaken');", "me.mutT = sec;   /* c21: 모아 둔 시간만큼 */"),
  ("    me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.2);\n", "    // c21: 체력 회복 없음\n"),
  ("      it.ammo--; awakenMe(); refreshItems(); return;", "      if (it.acc < 1) { toast('아직 모인 시간이 없습니다'); return; }\n      awakenMe(it.acc); it.acc = 0; refreshItems(); return;   // c21: 모인 시간을 한 번에 다 쓴다 (다 안 찼어도 된다)"),
  ("    if (!it || it.ammo <= 0 || !isZombie(me)) return;", "    if (it && it.off) { toast('가방이 있어야 쓸 수 있습니다'); return; }   // c21: 칸이 없어 꺼져 있는 도구\n    if (!it || it.ammo <= 0 || !isZombie(me)) return;"),
  ("      if (it.ammo >= itemMax(it.kind)) { it.t = 0; continue; }",
   "      if (it.off) continue;                   // c21: 꺼진 도구는 멈춰 있다\n"
   "      if (it.kind === 'awaken') { const m = chAccMax(); it.acc = Math.min(m, (it.acc || 0) + dt * m / (40 * (1 - bookCut()))); continue; }   // c21: 각성 주사 — 가득 차는 데 늘 40초 (백과사전이 줄여 준다)\n"
   "      if (it.ammo >= itemMax(it.kind)) { it.t = 0; continue; }"),
  ("      it.el.classList.toggle('empty', it.ammo <= 0);",
   "      it.el.classList.toggle('empty', it.ammo <= 0);\n"
   "      it.el.style.filter = it.off ? 'grayscale(1)' : ''; it.el.style.opacity = it.off ? '0.45' : '';   // c21: 꺼진 도구는 회색\n"
   "      if (it.off) { it.el.style.setProperty('--p', 0); it.el.querySelector('.n').textContent = ''; it.el.classList.remove('empty'); }\n"
   "      else if (it.kind === 'awaken') { it.el.style.setProperty('--p', Math.round(it.acc / chAccMax() * 100)); it.el.querySelector('.n').textContent = Math.floor(it.acc); it.el.classList.toggle('empty', it.acc < 1); }   // 각성 주사는 모인 시간(초)"),
  ("      } else it = { kind, ammo: itemMax(kind), t: 0, el: makeItemButton(kind, items.length) };",
   "      } else it = { kind, ammo: itemMax(kind), t: 0, el: makeItemButton(kind, items.length), acc: kind === 'awaken' ? chAccMax() : 0, off: items.length >= chToolCap() };   // c21: 칸이 없으면 꺼진 채로 붙는다"),
  # 칸이 없어도 줍는다 (c19의 '못 줍는다'는 없앤다)
  ("        if (CHAPTER && !chCanTake(p.kind)) { if (!(p.warn > clock)) { p.warn = clock + 4; toast('도구 칸이 꽉 찼습니다 — 가방이 있어야 더 들 수 있습니다'); } continue; }   // c19: 새 도구는 칸이 남아야 줍는다 (바닥에 그대로 남는다)", ""),
  ("    if (CHAPTER) { dropPickup(b.loot, b.foot.x, b.foot.z, b.space); return; }   // c19: 그 금고에 든 아이템이 떨어진다",
   "    if (CHAPTER) { const k = chFinal(b); if (k) dropPickup(k, b.foot.x, b.foot.z, b.space); else dust(b.foot.x, b.foot.z, 16, 1.4); return; }   // c19: 그 금고에 든 아이템이 떨어진다 · c21: 끝까지 올린 아이템이면 다른 것으로"),
  ("  function statLine(kind, n) {                // v344: 장비 강화 n단계일 때 수치\n    return {", "  function statLine(kind, n) {                // v344: 장비 강화 n단계일 때 수치\n    if (CHAPTER && CH_STAT[kind]) return CH_STAT[kind](n);   // c21\n    return {"),
  ("    for (const [k, el] of Object.entries(pBadges)) if (t[k]) el.querySelector('.pc').textContent = t[k]();", "    for (const [k, el] of Object.entries(pBadges)) if (t[k]) el.querySelector('.pc').textContent = (CHAPTER && CH_BADGE[k] ? CH_BADGE[k] : t[k])();"),
  ("tools: items.map((x) => x.kind + ':' + x.ammo),", "tools: items.map((x) => x.kind + ':' + (x.off ? 'off' : x.kind === 'awaken' ? (+x.acc.toFixed(1)) + 's' : x.ammo)),"),
]

CHIPS = r"""  // c24: 잔해 — 본편(f23 · f24)에서 가져왔다. 부서질 때 작은 조각들이 팍 튀어 올랐다가 떨어져 한 번 튕기고, 바닥에서 잠깐 있다 사라진다
  const chips = [], chipGeo = new THREE.PlaneGeometry(1, 1);
  const DOOR_BITS = [0xc4c4c4, 0x6a6a6a, 0x2b2b2b, 0xe0e0e0], CHEST_BITS = [0x9c5b2e, 0xb8743a, 0xf2c14e, 0x3a2410];   // 문짝 조각 · 금고(상자) 조각
  function debris(x, z, n, colors, size, spd) {
    for (let i = 0; i < n; i++) {
      const a = Math.random() * Math.PI * 2, sp = rand(spd * 0.45, spd);
      const m = new THREE.Mesh(chipGeo, new THREE.MeshBasicMaterial({ color: colors[i % colors.length], transparent: true, depthTest: false, depthWrite: false }));
      m.scale.set(rand(size * 0.5, size), rand(size * 0.22, size * 0.55), 1);
      m.quaternion.copy(camera.quaternion); m.rotateZ(Math.random() * Math.PI); m.renderOrder = 6;   // 먼지 위로
      m.position.set(x + Math.cos(a) * 0.25, 0.4, z + Math.sin(a) * 0.25);
      scene.add(m);
      chips.push({ m, vx: Math.cos(a) * sp, vz: Math.sin(a) * sp, vy: rand(3.5, 7), y: 0.4, spin: rand(-14, 14), t: 0, life: rand(1.3, 2.0) });
    }
  }
  function stepChips(dt) {
    for (let i = chips.length - 1; i >= 0; i--) {
      const c = chips[i]; c.t += dt;
      c.vy -= 20 * dt; c.y += c.vy * dt;
      if (c.y < 0.06) { c.y = 0.06; if (c.vy < -2.5) c.vy = -c.vy * 0.3; else c.vy = 0; c.vx *= 0.45; c.vz *= 0.45; c.spin *= 0.4; }   // 바닥에 떨어지면 한 번 통 튀고 멈춘다
      c.m.position.x += c.vx * dt; c.m.position.z += c.vz * dt; c.m.position.y = c.y;
      if (c.y > 0.06) { c.vx *= 1 - Math.min(1, dt * 0.8); c.vz *= 1 - Math.min(1, dt * 0.8); }
      c.m.rotateZ(c.spin * dt);
      c.m.material.opacity = c.t > c.life - 0.4 ? Math.max(0, (c.life - c.t) / 0.4) : 1;
      if (c.t >= c.life) { scene.remove(c.m); c.m.material.dispose(); chips.splice(i, 1); }
    }
  }
"""
FX_R = [   # c24: 문·금고가 부서질 때 파편 (본편과 같은 수치)
  ("  function stepFx(dt) {\n", CHIPS + "  function stepFx(dt) {\n"),
  ("    stepFx(dt); drawObjBars(dt);", "    stepFx(dt); stepChips(dt); drawObjBars(dt);"),
  ("      dust(o.L.cx, o.L.cz, 18, 1.4);", "      dust(o.L.cx, o.L.cz, 18, 1.4); debris(o.L.cx, o.L.cz, 18, DOOR_BITS, 0.4, 6.5);   // c24: 문짝 조각"),
  ("    if (CHAPTER && b.B) b.B.done = true;       // c19: 금고를 깬 건물 = 잠식 (지붕·미니맵 아이콘이 X로)\n",
   "    if (CHAPTER && b.B) b.B.done = true;       // c19: 금고를 깬 건물 = 잠식 (지붕·미니맵 아이콘이 X로)\n"
   "    debris(b.foot.x, b.foot.z, 20, CHEST_BITS, 0.42, 6.5); if (!b.dud) dust(b.foot.x, b.foot.z, 16, 1.4);   // c24: 금고 — 먼지 + 상자 조각 (꽝 금고 포함. 꽝은 바로 아래에서 먼지를 낸다)\n"),
  ("if (k) dropPickup(k, b.foot.x, b.foot.z, b.space); else dust(b.foot.x, b.foot.z, 16, 1.4); return; }", "if (k) dropPickup(k, b.foot.x, b.foot.z, b.space); return; }"),
  ("    for (const p of pickups) scene.remove(p.s); pickups.length = 0;", "    for (const p of pickups) scene.remove(p.s); pickups.length = 0;\n    for (const c of chips) { scene.remove(c.m); c.m.material.dispose(); } chips.length = 0;   // c24"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, chips: () => chips.length, objs, breakObj,"),
]

LVUP_R = [   # c25: 레벨업 화면에 능력치 대신 가진 도구·장비
  ("    else if (e.t === 'lv') showLevelUp();", "    else if (e.t === 'lv') { if (CHAPTER) chLevelUp(); else showLevelUp(); }   // c25"),
  ("    while (lvQueued < pendingLv) { fxQueue.push({ t: 'lv' }); lvQueued++; }", "    while (lvQueued < pendingLv && (!CHAPTER || chUpPool().length)) { fxQueue.push({ t: 'lv' }); lvQueued++; }   // c25: 강화할 아이템이 있을 때만 줄을 세운다 (없으면 모아 둔다)"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, xp: (n) => { for (let i = 0; i < n; i++) gainXp(); return { level, xp, pendingLv }; }, lvInfo: () => ({ level, xp, pendingLv, need: needXp(level + pendingLv) }),"),
]

STAR_R = [   # c26: 유전자(능력치) 버튼은 챕터에서 안 쓴다
  ("    statBtn.classList.toggle('on', Object.values(up).some((v) => v > 0));", "    statBtn.classList.toggle('on', !CHAPTER && Object.values(up).some((v) => v > 0));   // c26: 챕터는 능력치 카드가 없어서 유전자 버튼도 없다"),
]

XP_R = [   # c28: 레벨업에 필요한 감염 수 — 처음 20명, 그다음부터 1.2배씩
  ("const needXp = (L) => Math.round(10 * Math.pow(1.3, L));", "const needXp = (L) => CHAPTER ? Math.round(20 * Math.pow(1.2, L)) : Math.round(10 * Math.pow(1.3, L));   /* c28: 챕터는 처음 20명, 1.2배씩 */"),
]

AWAKE_R = [   # c29: 각성 주사 — 쓰는 동안은 게이지가 줄어들고(남은 변이 시간), 0이 되면 변이가 끝나고 그때부터 다시 모인다
  ("      awakenMe(it.acc); it.acc = 0; refreshItems(); return;   // c21: 모인 시간을 한 번에 다 쓴다 (다 안 찼어도 된다)",
   "      awakenMe(it.acc); it.drain = true; refreshItems(); return;   // c21: 모인 시간을 한 번에 다 쓴다 (다 안 찼어도 된다) · c29: 쓰는 동안 게이지가 줄어든다"),
  ("      if (it.kind === 'awaken') { const m = chAccMax(); it.acc = Math.min(m, (it.acc || 0) + dt * m / (40 * (1 - bookCut()))); continue; }   // c21: 각성 주사 — 가득 차는 데 늘 40초 (백과사전이 줄여 준다)",
   "      if (it.kind === 'awaken') {\n"
   "        if (it.drain) { if (me.mut) { it.acc = Math.max(0, me.mutT); continue; } it.drain = false; it.acc = 0; }   // c29: 변이하는 동안은 남은 시간만큼 게이지가 줄어든다 (모이지 않는다). 변이가 끝나면 0에서 다시 모인다\n"
   "        const m = chAccMax(); it.acc = Math.min(m, (it.acc || 0) + dt * m / (40 * (1 - bookCut()))); continue;   // c21: 가득 차는 데 늘 40초 (백과사전이 줄여 준다)\n"
   "      }"),
  ("it.el.querySelector('.n').textContent = Math.floor(it.acc); it.el.classList.toggle('empty', it.acc < 1); }   // 각성 주사는 모인 시간(초)",
   "it.el.querySelector('.n').textContent = it.drain ? Math.ceil(it.acc) : Math.floor(it.acc); it.el.classList.toggle('empty', !it.drain && it.acc < 1); }   // 각성 주사는 모인 시간(초) — c29: 쓰는 동안은 남은 시간이 거꾸로 줄어든다"),
  ("    awaken: ['모아 둔 시간만큼 내가 변이 좀비로 변합니다. 쓰지 않는 동안 시간이 모입니다.', '강화 시 모을 수 있는 시간이 늘어납니다.'],",
   "    awaken: ['모아 둔 시간만큼 내가 변이 좀비로 변합니다. 변이가 끝나면 다시 시간이 모입니다.', '강화 시 모을 수 있는 시간이 늘어납니다.'],"),
  ("    awaken: (n) => `최대 ${10 + 3 * n}초 변이 · 가득 모이는 데 40초`,", "    awaken: (n) => `최대 ${10 + 3 * n}초 변이 · 변이가 끝나고 가득 모이는 데 40초`,"),
]

SLOT_FN = r"""  // c34: 빈 도구 칸 — 쓸 수 있는 칸이 남아 있으면 그 자리에 가방 그림이 박혀 있다 (처음엔 1칸이라 시작하자마자 하나). 누르면 '도구를 하나 채울 수 있습니다'
  const chEmpty = [];
  function chEmptySlots() {
    const want = Math.max(0, chToolCap() - items.length);
    while (chEmpty.length > want) chEmpty.pop().remove();
    chEmpty.forEach((el, j) => { const [dx, dy] = slotPos(items.length + j); el.style.left = `calc(50% + ${dx}px)`; el.style.bottom = `calc(118px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px) + ${dy}px)`; });
    while (chEmpty.length < want) {
      const i = items.length + chEmpty.length, [dx, dy] = slotPos(i), el = document.createElement('div');
      el.className = 'item'; el.style.left = `calc(50% + ${dx}px)`; el.style.bottom = `calc(118px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px) + ${dy}px)`;
      el.style.setProperty('--c', '#6b6b78'); el.style.setProperty('--p', 100); el.style.opacity = '0.6';
      el.innerHTML = `<div class="core"><span class="ic" style="font-size:22px">${IC.bag}</span></div>`;
      el.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); toast('도구를 하나 채울 수 있습니다'); });
      stage.appendChild(el); chEmpty.push(el);
    }
  }
"""
SLOT_R = [
  ("  function showDud() {", SLOT_FN + "  function showDud() {"),
  ("      if ((it.t += dt) >= itemReload(it.kind)) { it.t = 0; it.ammo++; }\n    }\n    refreshItems();", "      if ((it.t += dt) >= itemReload(it.kind)) { it.t = 0; it.ammo++; }\n    }\n    refreshItems();\n    if (CHAPTER) chEmptySlots();   // c34"),
  ("color:${has ? '#ffd34d' : '#7dffa0'}\">${has ? chStars(n) : 'NEW'}", "color:#ffd34d\">${has ? chStars(n + 1) : 'NEW'}"),   # c34: 강화 카드 = 강화 뒤 별 수 (노랑), NEW도 노랑
]

AWK_TXT_R = [   # c35: 각성 주사 설명 글
  ("    awaken: ['모아 둔 시간만큼 내가 변이 좀비로 변합니다. 변이가 끝나면 다시 시간이 모입니다.', '강화 시 모을 수 있는 시간이 늘어납니다.'],",
   "    awaken: ['충전한 시간만큼 변이합니다.', '강화 시 최대 사용 시간과 게이지 충전 속도가 늘어납니다.'],"),
  ("    awaken: (n) => `최대 ${10 + 3 * n}초 변이 · 변이가 끝나고 가득 모이는 데 40초`,",
   "    awaken: (n) => `최대 사용 시간 ${10 + 3 * n}초 · 게이지 충전 속도 ${n ? '+' + 30 * n + '%' : '기본'}`,"),
]
