# c166: 보스 테스트 맵 — 맵 선택에 '보스 테스트' (큰 맵). 시작하자마자 보스(장갑차) 출동 · 동료 30명 · 나는 무적 · 사람 없음
#   · 환경은 보스전 그대로: 장갑차 + 15초마다 특공대 1팀 · 경보는 난리남 (경찰 출동도 그대로) · 다 잡으면 승리
#   · 사람(하양·노랑·주황·빨강·분홍)과 처음부터 서 있는 경찰·수비대는 치운다. 다시 채우기·길거리 차(사람을 태운다)도 끈다
C166_R = [
 ("  const CH_SMALL = (window.__map || await new Promise((res) => {", "  const CH_PICK = (window.__map || await new Promise((res) => {"),
 ("[['b', '큰 맵', '구역 4개 · 다리와 산길 · 랜드마크 9'], ['s', '작은 맵', '구역 1개 · 사방이 산 · 랜드마크 2']]", "[['b', '큰 맵', '구역 4개 · 다리와 산길 · 랜드마크 9'], ['s', '작은 맵', '구역 1개 · 사방이 산 · 랜드마크 2'], ['k', '보스 테스트', '큰 맵 · 동료 30 · 무적 · 바로 보스 출동']]"),
 ("    document.body.appendChild(ov);\n  })) === 's';\n", "    document.body.appendChild(ov);\n  }));\n  const CH_SMALL = CH_PICK === 's', CH_BT = CH_PICK === 'k';   // c166: 보스 테스트\n"),
 ("v.textContent = v.textContent.replace('챕터', CH_SMALL ? '작은 맵' : '큰 맵');", "v.textContent = v.textContent.replace('챕터', CH_SMALL ? '작은 맵' : CH_BT ? '보스 테스트' : '큰 맵');"),
 ("  function chRespawnTick(dt) {\n", "  function chRespawnTick(dt) {\n    if (CH_BT) return;   // c166\n"),
 ("    if (!chTr) return;\n    chTrProps();", "    if (!chTr) return;\n    if (CH_BT) return;   // c166: 길거리 차 없음 (사람을 태운다)\n    chTrProps();"),
 ("  function killZombie(z) {\n", "  function killZombie(z) {\n    if (CH_BT && z === me) { me.hp = me.maxHp; return; }   // c166: 보스 테스트 — 나는 무적\n"),
 ("  function stepWorld(dt) {\n    clock += dt;\n", "  function stepWorld(dt) {\n    clock += dt;\n    if (CHAPTER && CH_BT) chBossTest(dt);   // c166\n"),
 ("  let chTkMark = false;\n", """  let chTkMark = false;
  let chBTdone = false, chBTt = 0;
  function chBTgone(c) { for (const o of [c.mesh, c.icon, c.gauge, c.hpBar, c.tracer, c.tracer2, c.mark]) if (o) scene.remove(o); const i = bodies.indexOf(c); if (i >= 0) bodies.splice(i, 1); c.kind = 'gone'; }
  function chBossTest(dt) {                    // c166: 보스 테스트 맵
    if (!me) return;
    if (isZombie(me)) me.hp = me.maxHp;        // 무적
    if (!chBTdone) {
      chBTdone = true;
      for (const c of bodies.slice()) if (c.kind === 'citizen') chBTgone(c);   // 사람 · 처음부터 서 있는 경찰 · 수비대 다 치운다
      for (let i = 0, t = 0; i < 30 && t < 3000; t++) {   // 동료 30명 — 내 둘레
        const a = Math.random() * Math.PI * 2, r = 1.2 + Math.random() * 3.2, x = me.foot.x + Math.cos(a) * r, z = me.foot.z + Math.sin(a) * r;
        if (spaceOf(x, z) || !freeSpot(x, z, null) || bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.85)) continue;
        const c = addCitizen(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, ''); c.met = true; makeZombie(c); i++;
      }
      deaths = Math.max(deaths, STAR_AT[1]); stars = Math.max(stars, 2);   // 난리남
      chSf.on = true; chSf.n = 4; chSf.T = chSfAt(5) - 0.05;   // 다음 걸음에 보스 출동
    }
    if ((chBTt -= dt) <= 0) { chBTt = 0.5; for (const c of bodies.slice()) if (c.kind === 'citizen' && !c.police && !c.military) chBTgone(c); }   // 새로 생기는 사람(시작 하양 등)도 치운다
  }
"""),
 ("Object.assign(chSf, { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0, hide: false, hideT: 0 });", "Object.assign(chSf, { on: false, susT: 0, T: 0, n: 0, boss: false, waveT: 0, won: false, chk: 0, hide: false, hideT: 0 }); chBTdone = false;   /* c166 */"),
]
