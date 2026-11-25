# 챕터 줄기 c1 — 테스트 버전 v589를 바탕으로 새 파일을 뜬다 (v589는 그대로). 구역 4개 · 건물만 · 지붕 아이콘 · 세 겹 미니맵
import pathlib, json, sys
SRC = pathlib.Path('/home/user/s/running-dead/v589.html'); OUT = pathlib.Path('/home/user/s/running-dead/chapter/' + sys.argv[1] + '.html')
s = SRC.read_text(encoding='utf8'); MAP = pathlib.Path('map_c85.json').read_text(encoding='utf8')   # c83: 새 맵 · c85: 꾸민 맵
VER = sys.argv[1]
ICONS = r'''
  // ── 챕터: 건물 종류 (c1) — 지붕 색 + 지붕 위 아이콘 (금고 건물의 보물상자처럼 어둠 위에 뜬다). 들어가면 지붕과 같이 사라지고, 잠식하면 X ──
  const CH_DEF = {
    bank: { name: '은행', col: '#2e9e5b', roof: 0x183a28 }, police: { name: '경찰서', col: '#3b6fd4', roof: 0x18264a }, fire: { name: '소방서', col: '#e2452c', roof: 0x471d16 },
    mart: { name: '마트', col: '#f08a24', roof: 0x47301a }, hospital: { name: '병원', col: '#f4f4f6', roof: 0x3c3c44 }, army: { name: '군부대', col: '#5b6b2f', roof: 0x2a3218 },
    library: { name: '도서관', col: '#8b5a2b', roof: 0x3a2a1a }, conv: { name: '편의점', col: '#18a6a6', roof: 0x143c3c }, gym: { name: '헬스장', col: '#b0408f', roof: 0x3a1c36 },
    store: { name: '창고', col: '#7d6e5a', roof: 0x34302a },
  };
  function chIcon(type) {                     // 둥근 네모 배지 + 흰 그림 (128px) — 지붕 위 표시와 미니맵 아이콘에 같이 쓴다
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const rr = (x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
    const pass = type === 'passH' || type === 'passV';   // c4: 다른 구역으로 가는 길목 (다리 · 산 길목) — c16: 배지·테두리 없이 노란 양쪽 화살표만 (건물의 둥근 네모와 모양부터 다르게)
    const col = type === 'x' ? '#4a4a52' : pass ? '#f2c230' : CH_DEF[type].col, ink = type === 'hospital' ? '#e02b2b' : pass ? '#17171a' : '#ffffff';
    if (!pass && type !== 'x') { rr(6, 6, 116, 116, 26); g.fillStyle = 'rgba(0, 0, 0, 0.88)'; g.fill(); rr(14, 14, 100, 100, 19); g.fillStyle = col; g.fill(); }   // c58: X는 배지·테두리 없이 흰 X만
    g.fillStyle = g.strokeStyle = pass ? col : ink; g.lineCap = 'round'; g.lineJoin = 'round';
    const text = (t, px, y) => { g.font = `900 ${px}px system-ui, -apple-system, "Segoe UI", sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(t, 64, y || 68); };
    const star = (cx, cy, R) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? R * 0.42 : R; g[i ? 'lineTo' : 'moveTo'](cx + Math.cos(a) * r, cy + Math.sin(a) * r); } g.closePath(); g.fill(); };
    if (pass) {                               // 양쪽을 가리키는 화살표 — 가로(동서로 건넌다) · 세로(남북으로 넘는다)
      if (type === 'passV') { g.translate(64, 64); g.rotate(Math.PI / 2); g.translate(-64, -64); }
      g.fillRect(40, 45, 48, 38);             // 그림 칸을 꽉 채운다 — 가운데 막대 + 양 끝 세모
      for (const k of [-1, 1]) { g.beginPath(); g.moveTo(64 + k * 62, 64); g.lineTo(64 + k * 20, 12); g.lineTo(64 + k * 20, 116); g.closePath(); g.fill(); }
    } else if (type === 'bank') text('₩', 78);
    else if (type === 'conv') text('24', 60);
    else if (type === 'army') star(64, 66, 38);
    else if (type === 'police') {             // 방패 + 별
      g.beginPath(); g.moveTo(64, 26); g.lineTo(96, 38); g.lineTo(96, 64); g.quadraticCurveTo(96, 92, 64, 104); g.quadraticCurveTo(32, 92, 32, 64); g.lineTo(32, 38); g.closePath(); g.fill();
      g.fillStyle = col; star(64, 64, 19);
    } else if (type === 'fire') {             // 불꽃
      g.beginPath(); g.moveTo(66, 22); g.bezierCurveTo(92, 44, 100, 62, 94, 82); g.bezierCurveTo(89, 99, 76, 107, 64, 107); g.bezierCurveTo(49, 107, 35, 98, 33, 80);
      g.bezierCurveTo(31, 65, 41, 57, 45, 44); g.bezierCurveTo(51, 55, 56, 57, 58, 51); g.bezierCurveTo(61, 41, 61, 32, 66, 22); g.fill();
      g.fillStyle = col; g.beginPath(); g.moveTo(64, 66); g.bezierCurveTo(76, 78, 78, 88, 72, 95); g.bezierCurveTo(68, 99, 60, 99, 56, 95); g.bezierCurveTo(50, 88, 56, 78, 64, 66); g.fill();
    } else if (type === 'mart') {             // 카트
      g.lineWidth = 9; g.beginPath(); g.moveTo(24, 36); g.lineTo(39, 36); g.lineTo(50, 80); g.lineTo(92, 80); g.lineTo(101, 50); g.lineTo(43, 50); g.stroke();
      for (const x of [56, 88]) { g.beginPath(); g.arc(x, 96, 7.5, 0, Math.PI * 2); g.fill(); }
    } else if (type === 'hospital') { g.fillRect(53, 28, 22, 72); g.fillRect(28, 53, 72, 22); }   // 십자
    else if (type === 'library') {            // 펼친 책
      for (const k of [-1, 1]) { g.beginPath(); g.moveTo(64, 42); g.quadraticCurveTo(64 + k * 20, 30, 64 + k * 40, 36); g.lineTo(64 + k * 40, 90); g.quadraticCurveTo(64 + k * 20, 84, 64, 96); g.closePath(); g.fill(); }
      g.strokeStyle = col; g.lineWidth = 5; g.beginPath(); g.moveTo(64, 42); g.lineTo(64, 96); g.stroke();
    } else if (type === 'gym') { g.fillRect(40, 58, 48, 12); g.fillRect(28, 40, 15, 48); g.fillRect(85, 40, 15, 48); g.fillRect(17, 50, 10, 28); g.fillRect(101, 50, 10, 28); }   // 아령
    else if (type === 'store') {              // 나무 상자
      g.beginPath(); g.moveTo(64, 26); g.lineTo(102, 52); g.lineTo(102, 100); g.lineTo(26, 100); g.lineTo(26, 52); g.closePath(); g.fill();   // c33: 창고 — 세모 지붕 건물 + 셔터 문
      g.fillStyle = col; g.fillRect(42, 64, 44, 36); g.fillStyle = ink; for (const y of [72, 81, 90]) g.fillRect(46, y, 36, 4);
    } else if (type === 'x') { g.lineWidth = 22; g.beginPath(); g.moveTo(24, 24); g.lineTo(104, 104); g.moveTo(104, 24); g.lineTo(24, 104); g.stroke(); }   // 잠식한 건물 (c58: 칸을 채우는 흰 X)
    return c;
  }
  function riverCollide(b) {                  // c3: 강은 못 건넌다 — 물에 겹치면 가장 가까운 물가로 밀어낸다 (다리 자리는 강 토막 사이라 비어 있다)
    const r = b.r || BODY;
    for (const [x0, z0, x1, z1] of CH_MAP.rivers) {
      const x = b.foot.x, z = b.foot.z;
      if (x <= x0 - r || x >= x1 + r || z <= z0 - r || z >= z1 + r) continue;
      const dl = x - (x0 - r), dr = x1 + r - x, dn = z - (z0 - r), ds = z1 + r - z, m = Math.min(dl, dr, dn, ds);
      if (m === dl) { b.foot.x = x0 - r; if (b.vel.x > 0) b.vel.x = 0; } else if (m === dr) { b.foot.x = x1 + r; if (b.vel.x < 0) b.vel.x = 0; }
      else if (m === dn) { b.foot.z = z0 - r; if (b.vel.y > 0) b.vel.y = 0; } else { b.foot.z = z1 + r; if (b.vel.y < 0) b.vel.y = 0; }
    }
  }
  // ── c11: 인간(하양) 깔기 + 먼 사람 재우기 ──
  const CH_WAKE = 40;                         // 깨울 사람을 고를 때 쓰는 굵은 격자 한 칸 (칸)
  const CH_SLEEP = 20;                        // c54: 깨어 있던 사람은 좀비가 전부 이만큼 멀어지면 그 자리에 다시 선다 (깨어나는 거리 14보다 넉넉히)
  function chCanSleep(b) {                    // 지금 다시 서도 되나 — 나와 얽힌 중(싸움·도망·경계·추적·출동)이면 안 된다
    return b.state === 'normal' && !(b.police && !b.post) && !b.guardOf && !b.fb && !(b.infect > 0) && !(b.stunT > 0) && !(b.knockT > 0) && !(b.pushT > 0) && !b.lureAlert && !b.goo && !b.marked && !(b.home && b.back && b.goal);   // c59: 자기 건물로 돌아가는 중이면 끝까지 걸어간다 (도중에 서 버리지 않게)
  }
  function chWakeUp(b) {                      // 깨어나는 순간 — 서 있지 않고 바로 돌아다니기 시작한다 (내 눈에 들어올 땐 이미 걷는 중)
    if (b.state !== 'normal' || b.goal || !b.area) return;
    if (b.area.roam && Math.random() < 0.5) chRoam(b);   // c55: 길거리 사람은 절반쯤 깨어나자마자 자리를 옮긴다
    if (Math.random() < 0.75 || !inArea(b)) { b.goal = pickGoal(b.area); b.back = !inArea(b); } else b.timer = rand(0.2, 1.5);
  }
  const CH_MEET = 14;                         // c12: 좀비가 이만큼(칸) 안에 오면 깨어난다 — 좀비 시야(7.2칸)의 두 배쯤이라, 내 눈에 들어올 땐 이미 돌아다니고 있다
  let chHot = null, CH_GW = 0, CH_GH = 0;
  const chNearRiver = (x, z, m) => CH_MAP.rivers.some(([x0, z0, x1, z1]) => x > x0 - m && x < x1 + m && z > z0 - m && z < z1 + m);
  // c40: 사람 깔기 — 판마다 자리는 랜덤, 종류별 수와 패턴은 늘 같다
  //   하양 145 (건물 안 먼저 골고루, 빈집 3분의 1) · 노랑 48 (길거리에 띄엄띄엄, 4분의 1은 건물 안에 한 명씩) · 배회 경찰 20 (길거리)
  //   주황 48 · 빨강(자경단) 48 = 길거리에 2~4명씩 무리. 주황 2 + 빨강 3 (또는 3 + 2)이 섞인 5명 무리도 몇 개
  const CH_WHITE = 145, CH_YELLOW = 48, CH_YELLOW_IN = 12, CH_GANG = 48, CH_COPS = 20, CH_ROOM = 45;
  const CH_WHITE_OUT = 81, CH_YELLOW_OUT = 36;   // c48: 길거리 하양 · 노랑 (건물 안은 아래 표)
  const CH_RED_K = 0.9;                          // c59: 빨강(자경단) 10% 줄임 — 길거리 무리 · 건물 안 · 집 안 모두. 1 밑으로는 안 내려간다
  const chRedN = (k) => { const v = k * CH_RED_K, f = Math.floor(v); return Math.max(1, f + (Math.random() < v - f ? 1 : 0)); };   // 소수는 확률로 올림 (2명 → 80%는 2명, 20%는 1명)
  const CH_WHITE_GANG = 0.5;                     // c58: 길거리 하양 가운데 무리(2~3명)로 다니는 몫
  const CH_ONE_K = 1.1;                          // c57: 길거리에 혼자 다니는 사람 (하양 · 노랑 · 배회 경찰) 10% 더 — 무리는 그대로
  const CH_INSIDE = {                         // c48: 건물 안 인원 [종류, 최소, 최대] — '' 하양 · guard 노랑 · attacker 주황 · vig 빨강 · police 경찰 · soldier 군인
    army: [['sniper', 1, 1], ['soldier', 2, 4]],   // c51: 저격수 1명은 늘
    hospital: [['', 5, 10], ['attacker', 2, 3], ['vig', 1, 2], ['police', 1, 2]],   // c54: 빨강은 건물마다 한 명씩 뺐다 (최소 1)
    police: [['police', 4, 7], ['', 2, 4]],
    fire: [['police', 1, 2], ['vig', 2, 4], ['attacker', 2, 4]],
    conv: [['', 1, 3], ['guard', 1, 2]],
    mart: [['', 7, 12], ['police', 3, 4], ['vig', 1, 2], ['guard', 2, 4]],
    gym: [['', 2, 3], ['guard', 3, 5], ['attacker', 7, 10], ['vig', 1, 1], ['police', 1, 1]],
    store: [['attacker', 3, 5], ['vig', 2, 5]],   // c55: 창고는 주황·빨강 한 명씩 더 뺐다
    bank: [['', 4, 7], ['guard', 4, 7], ['attacker', 1, 2], ['police', 3, 4], ['vig', 2, 3]],
    library: [['police', 1, 2], ['guard', 2, 3], ['', 4, 5]],
  };
  function chOutSpot(placed, minOwn, keepStart) {   // 바깥 빈자리 — placed(같은 종류 자리들)에서 최대한 먼 곳 (고르게)
    let best = null, bd = -1;
    for (let t = 0; t < 400 && (bd < 0 || t < 50); t++) {
      const x = rand(MM.x0 + 3, MM.x1 - 3), z = rand(MM.z0 + 3, MM.z1 - 3);
      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null)) continue;
      if (Math.hypot(x - me.foot.x, z - me.foot.z) < keepStart || bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < minOwn)) continue;
      const d = placed.reduce((m, p) => Math.min(m, Math.hypot(p[0] - x, p[1] - z)), 1e9);
      if (d > bd) { bd = d; best = [x, z]; }
    }
    return best;
  }
  // c55: 길거리 사람은 돌아다닌다 — 자리(area)가 처음 자리(anchor)에서 R칸(7~20, 사람마다 랜덤) 안을 옮겨 다니고, 사람은 그 자리로 걸어가 그 둘레를 서성인다.
  //   무리는 자리를 같이 쓰니까 함께 옮겨 간다. 자는 사람(좀비가 멀리 있다)은 안 움직인다. 강·산 건너로는 안 간다 (처음 구역 안에서만)
  function chRoamArea(x, z) { return Object.assign(square(x, z), { roam: { ax: x, az: z, R: rand(7, 20), next: 0, zone: chZoneOf(x, z), members: null } }); }
  function chRoam(c) {
    const A = c.area, rm = A.roam;
    if (clock < rm.next) return;
    rm.next = clock + rand(4, 12);
    for (let t = 0; t < 30; t++) {
      const a = Math.random() * Math.PI * 2, r = rm.R * Math.sqrt(Math.random()), x = rm.ax + Math.cos(a) * r, z = rm.az + Math.sin(a) * r;
      if (x < MM.x0 + 3 || x > MM.x1 - 3 || z < MM.z0 + 3 || z > MM.z1 - 3 || chZoneOf(x, z) !== rm.zone || spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null)) continue;
      A.x0 = x - AREA / 2; A.z0 = z - AREA / 2; A.x1 = x + AREA / 2; A.z1 = z + AREA / 2;
      if (rm.members) for (const m of rm.members) if (m !== c && m.kind === 'citizen' && !m.sleep && m.state === 'normal' && m.area === A) { m.goal = pickGoal(A); m.back = true; }   // 무리는 같이 간다
      return;
    }
  }
  function chPut(x, z, area, type, B) {
    const c = addCitizen(x, z, area, type === 'vig' ? 'attacker' : type);
    if (type === 'police') { c.post = area; c.area = area; }     // 배회 경찰 = 자기 자리 둘레를 돈다 (c56: 만들 때 자리가 다른 네모로 바뀌어서 경찰만 안 돌아다녔다 — 같은 자리로 맞춘다)
    if (type === 'vig') chVig(c);
    if (B) c.home = B;
    c.space = B || null; c.sleep = true;
    enterNormal(c);
    return c;
  }
  function chVig(c) {                         // 자경단 = 공격형과 같은 수치 + 근접 넉백 1, 빨강, 몽둥이
    c.vig = true; c.mesh.material.color.setHex(0xc62828);
    const s = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.95), new THREE.MeshBasicMaterial({ color: 0x8a5a30, transparent: true, depthTest: false, depthWrite: false }));
    s.geometry.translate(0, 0.45, 0);         // 손잡이 쪽이 축
    s.position.set(0.42, 0.05, 0.01); s.rotation.z = -0.5; s.renderOrder = 1;
    c.mesh.add(s); c.stick = s;
  }
  // c56: 다시 채우기 — 구역마다 따로. 길거리 한 명짜리(하양·노랑·배회 경찰)는 색마다 40초에 한 명씩 (줄어든 만큼만), 전멸한 무리는 60초에 한 무리 (어느 무리일지는 랜덤, 무리 전체가 한꺼번에 · 한 명이라도 남은 무리는 안 채운다)
  //   내 화면과 좀비 시야 밖 빈자리에 나온다 (그런 자리가 없으면 아무 빈자리). 건물 안 사람과 경찰서 둘레 경찰은 안 채운다
  const CH_RE_ONE = 40, CH_RE_GANG = 60;
  let chPop = null;
  function chPopReset() { chPop = { one: CH_MAP.zones.map(() => ({ '': { want: 0, list: [], t: CH_RE_ONE }, guard: { want: 0, list: [], t: CH_RE_ONE }, police: { want: 0, list: [], t: CH_RE_ONE } })), gangs: [], wg: [], gt: CH_MAP.zones.map(() => CH_RE_GANG), acc: 0 }; for (const B of buildings) if (B.type === 'house') { B.res = []; B.taken = false; B.seen = false; } }
  function chReg(c, type) { const P = chPop.one[chZoneOf(c.foot.x, c.foot.z)][type]; P.list.push(c); P.want++; return c; }
  function chGang(G, p) {                       // 무리 하나를 그 자리에 놓는다 — 자리(area)를 같이 쓴다 (함께 옮겨 다닌다)
    const area = chRoamArea(p[0], p[1]); area.roam.members = G.members = [];
    G.types.forEach((t, i) => {
      let x = p[0], z = p[1];
      for (let tt = 0; tt < 40; tt++) { const a = Math.random() * Math.PI * 2, r = i ? rand(0.9, 1.8) : 0; x = p[0] + Math.cos(a) * r; z = p[1] + Math.sin(a) * r; if (!spaceOf(x, z) && freeSpot(x, z, null) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)) break; }
      G.members.push(chPut(x, z, area, t));
    });
  }
  function chHiddenSpot(zi, minOwn) {          // 그 구역 길거리 빈자리 — 내 화면과 좀비 시야 밖 (없으면 아무 빈자리)
    const [x0, z0, x1, z1] = CH_MAP.zones[zi];
    const ok = (x, z, strict) => !spaceOf(x, z) && !chNearRiver(x, z, AREA / 2 + 1) && freeSpot(x, z, null) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < minOwn) && (!strict || (!onView(x, z, 3) && !zombies.some((zb) => Math.hypot(zb.foot.x - x, zb.foot.z - z) < zb.sense + 2)));
    for (const strict of [true, false]) for (let k = 0; k < 200; k++) { const x = rand(x0 + 3, x1 - 3), z = rand(z0 + 3, z1 - 3); if (ok(x, z, strict)) return [x, z]; }
    return null;
  }
  function chRespawnTick(dt) {
    if ((chPop.acc += dt) < 0.5) return;
    const d = chPop.acc; chPop.acc = 0;
    for (let zi = 0; zi < chPop.one.length; zi++) {
      for (const type of ['', 'guard', 'police']) {
        const P = chPop.one[zi][type]; P.list = P.list.filter((c) => c.kind === 'citizen');
        // c58: 하양 무리 — 전멸한 무리만 통째로 돌아온다 (한 명이라도 남았으면 안 채운다). 하양은 혼자든 무리든 한 시계를 같이 쓴다:
        //      무리가 돌아오면 그 인원수만큼 다음 차례가 늦어져서, 하양이 돌아오는 빠르기는 전과 같다 (구역마다 40초에 한 명꼴)
        const miss = Math.max(0, P.want - P.list.length), deadW = type === '' ? chPop.wg.filter((G) => G.zone === zi && !G.members.some((c) => c.kind === 'citizen')) : [];
        if (!miss && !deadW.length) { P.t = CH_RE_ONE; continue; }
        if ((P.t -= d) > 0) continue;
        P.t = CH_RE_ONE;
        const gSum = deadW.reduce((n, G) => n + G.types.length, 0);
        if (gSum && Math.random() * (miss + gSum) >= miss) { const G = deadW[Math.floor(Math.random() * deadW.length)], p = chHiddenSpot(zi, 2.5); if (p) { chGang(G, p); P.t = CH_RE_ONE * G.types.length; } }
        else { const p = chHiddenSpot(zi, 1.2); if (p) P.list.push(chPut(p[0], p[1], chRoamArea(p[0], p[1]), type)); }
      }
      const dead = chPop.gangs.filter((G) => G.zone === zi && !G.members.some((c) => c.kind === 'citizen'));
      if (!dead.length) { chPop.gt[zi] = CH_RE_GANG; continue; }
      if ((chPop.gt[zi] -= d) > 0) continue;
      chPop.gt[zi] = CH_RE_GANG; const p = chHiddenSpot(zi, 2.5); if (p) chGang(dead[Math.floor(Math.random() * dead.length)], p);
    }
    for (const B of buildings) {               // c56: 집 점령 표시 — 문이 하나라도 부서졌고(차고는 좀비가 들어가 봤고) 안에 있던 사람이 전부 감염됐으면 (원래 빈집이면 문만)
      if (B.type !== 'house' || B.taken) continue;
      if (B.garage && !B.seen && zombies.some((z) => z.space === B)) B.seen = true;
      const open = B.garage ? B.seen || B.locks.some((L) => L.obj && L.obj.dead) : B.doors.length > 0;
      if (open && B.res.every((c) => c.kind !== 'citizen')) B.taken = true;
    }
  }
  function chPopulate() {
    chPopReset();
    const placed = [];
    for (let k = 0; k < Math.round(CH_COPS * CH_ONE_K); k++) { const p = chOutSpot(placed, 1.2, 18); if (!p) continue; placed.push(p); chReg(chPut(p[0], p[1], chRoamArea(p[0], p[1]), 'police'), 'police'); }
    // 무리: 주황·빨강 각 48 — 2~4명 무리로 쪼갠다. 섞인 5명 무리 2개 (주황 2 + 빨강 3, 주황 3 + 빨강 2)
    // c44: 무리 세 가지 — 주황만 (2~4) · 빨강만 (2~4) · 섞인 무리 (4~6, 둘 다 2명 이상). 섞인 무리에 주황·빨강 각 3분의 1쯤
    const groups = [];
    let mo = Math.round(CH_GANG / 3), mr = Math.round(CH_GANG * CH_RED_K / 3);   // c59: 빨강은 10% 적게
    while (mo >= 2 && mr >= 2) {
      let k = 4 + Math.floor(Math.random() * 3), o = 2 + Math.floor(Math.random() * (k - 3));   // 주황 2 ~ k-2
      o = Math.min(o, mo); let r = Math.min(k - o, mr); if (r < 2) break;
      groups.push([...Array(o).fill('attacker'), ...Array(r).fill('vig')]); mo -= o; mr -= r;
    }
    for (const t of ['attacker', 'vig']) {
      let left = (t === 'vig' ? Math.round(CH_GANG * CH_RED_K) : CH_GANG) - groups.flat().filter((x) => x === t).length;
      while (left > 0) { let k = 2 + Math.floor(Math.random() * 3); if (left - k === 1) k = k > 2 ? k - 1 : 3; k = Math.min(k, left); groups.push(Array(k).fill(t)); left -= k; }
    }
    const centers = [];
    for (const types of groups.sort(() => Math.random() - 0.5)) {
      const p = chOutSpot(centers, 2.5, 20); if (!p) continue; centers.push(p);
      const G = { zone: chZoneOf(p[0], p[1]), types, members: [] }; chPop.gangs.push(G); chGang(G, p);
    }
    // c48: 건물 안 — 랜드마크·창고는 건물마다 정한 인원, 집은 넓이대로 하양 (빈집 3분의 1)
    const hs = buildings.filter((B) => B.type === 'house').sort(() => Math.random() - 0.5), empty = new Set(hs.slice(0, Math.round(hs.length / 3)));
    const inPut = (B, type) => { let g = pickGoal(B); for (let t = 0; t < 30 && bodies.some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.0); t++) g = pickGoal(B); const c = chPut(g.x, g.y, B, type, B); if (type === 'police' || type === 'soldier' || type === 'sniper') c.post = B; return c; };
    const R2 = (a, b) => a + Math.floor(Math.random() * (b - a + 1)), houseSlots = [];
    for (const B of buildings) {
      if (B.type === 'hill') continue;
      const T = CH_INSIDE[B.type];
      if (T) { for (const [type, lo, hi] of T) { let k = R2(lo, hi); if (B.type !== 'store' && (type === '' || type === 'guard')) k = Math.round(k * 2 / 3);   /* c49: 랜드마크 하양·노랑 3분의 1 줄임 */ for (let i = 0; i < k; i++) inPut(B, type); } continue; }
      if (B.type !== 'house' || empty.has(B)) continue;
      const base = Math.max(1, Math.round((B.x1 - B.x0) * (B.z1 - B.z0) / CH_ROOM)), k = Math.max(1, base + Math.floor(Math.random() * 3) - 1);
      for (let i = 0; i < k; i++) houseSlots.push(B);
    }
    houseSlots.sort(() => Math.random() - 0.5);
    const houseOut = Math.round(houseSlots.length / 3);   // c49: 집 사람 3분의 1은 집 밖(길거리)으로
    houseSlots.slice(houseOut).forEach((B) => { const q = Math.random(); B.res.push(inPut(B, q < 0.15 ? 'attacker' : q < 0.15 + 0.15 * CH_RED_K ? 'vig' : '')); });   /* c59: 빨강 13.5% */   // c54: 집 안 하양은 15%는 주황, 15%는 빨강으로 (c55: 시작 자리 둘레 집은 하양만)
    for (const B of buildings) if (B.type === 'police') for (let i = 0; i < 3; i++) {   // 경찰서 밖 배회 경찰 3명 (죽어도 채워지지 않는다)
      const ring = { x0: B.x0 - 5, z0: B.z0 - 5, x1: B.x1 + 5, z1: B.z1 + 5 }; let g = pickGoal(ring); for (let t = 0; t < 40 && (spaceOf(g.x, g.y) || chNearRiver(g.x, g.y, 1)); t++) g = pickGoal(ring);
      chPut(g.x, g.y, ring, 'police');
    }
    // c58: 처음 만나는 사람을 하양·노랑으로 맞추던 것(c55)을 뺐다 — 시작 자리 둘레도 다른 곳과 똑같이 놓는다
    const ys = [];
    for (let k = 0; k < Math.round(CH_YELLOW_OUT * CH_ONE_K); k++) { const p = chOutSpot(ys, 1.2, 14); if (!p) continue; ys.push(p); chReg(chPut(p[0], p[1], chRoamArea(p[0], p[1]), 'guard'), 'guard'); }
    const whiteOut = Math.round((CH_WHITE_OUT + houseOut) * 1.15 * CH_ONE_K);   // c54: 길거리 하양 15% 더 · c57: 10% 더
    // c58: 길거리 하양의 절반은 2~3명 무리 — 같은 자리를 쓰며 함께 돌아다닌다 (전체 수는 그대로, 무리끼리는 고르게 떨어뜨린다)
    let w = 0;
    { let left = Math.round(whiteOut * CH_WHITE_GANG); const wc = [];
      while (left >= 2) {
        const k = left <= 3 ? left : left === 4 ? 2 : 2 + (Math.random() < 0.5 ? 1 : 0), p = chOutSpot(wc, 2.5, 14); if (!p) break; wc.push(p);
        const G = { zone: chZoneOf(p[0], p[1]), types: Array(k).fill(''), members: [] }; chPop.wg.push(G); chGang(G, p); left -= k; w += k;
      }
    }
    for (let t = 0; t < 40000 && w < whiteOut; t++) {   // 길거리 하양
      const x = rand(MM.x0 + 3, MM.x1 - 3), z = rand(MM.z0 + 3, MM.z1 - 3);
      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null) || Math.hypot(x - me.foot.x, z - me.foot.z) < 14) continue;
      if (bodies.some((b) => Math.hypot(b.foot.x - x, b.foot.z - z) < 1.2)) continue;
      chReg(chPut(x, z, chRoamArea(x, z), ''), ''); w++;
    }
    // c58: 처음엔 하양부터 놓던 걸 빼면서 시작 자리 14칸 안에는 아무도 없다 (전부 서 있다) — 그대로 두면 내가 가만히 있는 동안 아무도 안 온다.
    //      그래서 시작할 때 '다시 서는 거리'(20칸) 안 길거리 사람은 깨워 둔다: 누구든 (하양·노랑·경찰·무리) 돌아다니다가 나를 먼저 발견할 수 있다
    for (const b of bodies) if (b.kind === 'citizen' && !b.space && b.sleep && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) < CH_SLEEP) { b.met = true; b.sleep = false; chWakeUp(b); }
  }
  const chRiverSegs = CHAPTER ? CH_MAP.rivers.flatMap(([x0, z0, x1, z1]) => [[x0, z0, x1, z0], [x0, z1, x1, z1], [x0, z0, x0, z1], [x1, z0, x1, z1]]) : [];
  // ── c13: 먼 길 찾기 — 목적지가 강·산 건너 다른 구역이면 길목(다리·산 길목)을 거쳐 간다. 같은 구역 안에서는 지금까지의 길 찾기 그대로 ──
  //    구역 넷(0 남서 · 1 남동 · 2 북서 · 3 북동)은 땅이 네모반듯해서, 같은 구역 땅 위의 두 자리는 강·산을 안 건너고 곧장 이어진다.
  //    길목마다 양 끝에 마디를 하나씩 두고 (다리 3 + 산 길목 2 = 마디 10개) 마디 사이 가장 짧은 거리를 미리 구해 둔다.
  //    걸음마다: 목적지가 곧장 닿는 곳이면 그대로, 아니면 '내가 곧장 닿는 마디 → … → 목적지에 곧장 닿는 마디'가 가장 짧은 길의 첫 마디로 간다
  const chZoneOf = (x, z) => (x > 0 ? 1 : 0) + (z < CH_MAP.zrMid ? 2 : 0);   // 강 한가운데 x = 0, 산줄기 한가운데 z = zrMid 기준
  const CH_PH = CH_MAP.passW / 2, CH_PIN = CH_MAP.gap / 2, CH_PEND = CH_MAP.gap / 2 + 2.5;   // 길목 반폭 · 강/산 한가운데에서 그 가장자리까지 · 마디(길목 끝)까지
  const chNode = [];                          // 마디 {x, z, zone: 닿는 구역, p: 길목 번호}
  CH_MAP.passes2.forEach((P, i) => { chNode.push({ x: P.ax, z: P.az, zone: P.za, p: i }, { x: P.bx, z: P.bz, zone: P.zb, p: i }); });
  const chND = chNode.map((a, i) => chNode.map((b, j) => i === j ? 0 : a.p === b.p || a.zone === b.zone ? Math.hypot(a.x - b.x, a.z - b.z) : Infinity));   // 같은 길목의 두 끝, 같은 구역의 두 마디는 곧장 이어진다
  for (let k = 0; k < chNode.length; k++) for (let i = 0; i < chNode.length; i++) for (let j = 0; j < chNode.length; j++) if (chND[i][k] + chND[k][j] < chND[i][j]) chND[i][j] = chND[i][k] + chND[k][j];
  // 자리 하나가 어디에 속하나 — corr = 길목 번호 (길목 통로와 그 어귀. 아니면 -1), land = 구역 땅 위인가 (강 위 다리·산 사이 통로 한가운데면 false)
  const chS = { zone: 0, corr: -1, land: true }, chT = { zone: 0, corr: -1, land: true };
  function chClass(x, z, o) {
    o.corr = -1; o.land = true; o.zone = chZoneOf(x, z);
    for (let i = 0; i < CH_MAP.passes2.length; i++) {
      const P = CH_MAP.passes2[i], v = P.axis === 'v', s = Math.abs(v ? x : z - CH_MAP.zrMid), l = Math.abs((v ? z : x) - P.c);
      if (l < CH_PH && s < CH_PEND + 0.5) { o.corr = i; o.land = s >= CH_PIN; return o; }
    }
    return o;
  }
  const chSees = (o, n) => o.corr === n.p || (o.land && o.zone === n.zone);   // 그 자리에서 이 마디까지 곧장 갈 수 있나
  const chRouteOut = [0, 0], chTD = [];
  function chRoute(b, tx, tz) {
    const px = b.foot.x, pz = b.foot.z;
    chRouteOut[0] = tx; chRouteOut[1] = tz;
    chClass(px, pz, chS); chClass(tx, tz, chT);
    if ((chS.corr >= 0 && chS.corr === chT.corr) || (chS.land && chT.land && chS.zone === chT.zone)) return chRouteOut;   // 곧장 닿는다 (같은 구역 땅 · 같은 길목)
    const N = chNode.length;
    for (let j = 0; j < N; j++) chTD[j] = chSees(chT, chNode[j]) ? Math.hypot(chNode[j].x - tx, chNode[j].z - tz) : Infinity;
    let best = Infinity, bi = -1;
    for (let i = 0; i < N; i++) {
      const n = chNode[i]; if (!chSees(chS, n)) continue;
      const d0 = Math.hypot(n.x - px, n.z - pz), d = d0 + (d0 < 0.6 ? 0.05 : 0);   // 이미 그 마디에 와 있으면 다음 마디가 이기게 (제자리에 서지 않게)
      for (let j = 0; j < N; j++) { const c = d + chND[i][j] + chTD[j]; if (c < best) { best = c; bi = i; } }
    }
    if (bi < 0) return chRouteOut;
    const n = chNode[bi], v = CH_MAP.passes2[n.p].axis === 'v';
    if (b.laneK === undefined) b.laneK = Math.random() * 2 - 1;   // 길목 폭 안에서 저마다 다른 줄로 — 한 줄로 몰리지 않게
    const off = b.laneK * (CH_PH - 1.3);
    chRouteOut[0] = n.x + (v ? 0 : off); chRouteOut[1] = n.z + (v ? off : 0);
    return chRouteOut;
  }
  // 동료 자리가 강물·산 속에 걸리거나 그 너머로 넘어가면 내 쪽 물가·산기슭으로 당긴다 — 자리가 건너편이 돼서 동료가 길목을 돌아 반대편으로 가 버리지 않게
  let chBlocks = null;
  const chSlotOut = [0, 0];
  function chSlotFix(x, y) {
    if (!chBlocks) chBlocks = CH_MAP.rivers.map(([x0, z0, x1, z1]) => ({ x0, z0, x1, z1 })).concat(buildings.filter((B) => B.type === 'hill'));
    const mx = me.foot.x, mz = me.foot.z, m = 0.7;
    for (let k = 0; k < 2; k++) for (const R of chBlocks) {
      const t = segRect(mx, mz, x, y, R, 0);  // 나 → 자리 선이 강·산에 처음 닿는 곳
      if (t < Infinity) { x = mx + (x - mx) * t; y = mz + (y - mz) * t; }
      if (x <= R.x0 - m || x >= R.x1 + m || y <= R.z0 - m || y >= R.z1 + m) continue;
      const l = x - (R.x0 - m), r = R.x1 + m - x, u = y - (R.z0 - m), w = R.z1 + m - y, q = Math.min(l, r, u, w);   // 가장 가까운 가장자리 밖으로 (0.7칸)
      if (q === l) x = R.x0 - m; else if (q === r) x = R.x1 + m; else if (q === u) y = R.z0 - m; else y = R.z1 + m;
    }
    chSlotOut[0] = x; chSlotOut[1] = y; return chSlotOut;
  }
  // ── c13: 나에게 가는 흐름 — 멀리 있는 동료는 멀리 있는 자기 자리까지 길을 따로 찾지 않고, 내 자리에서 맵 전체로 퍼뜨린 '걸어서 가는 거리'를 따라 내려온다 ──
  //    거리는 한 번만 계산해서 전원이 같이 읽는다 (동료가 몇 명이든 계산은 한 번). 강·산·막다른 길처럼 건물 하나보다 큰 장애물도 크기와 상관없이 돌아 나온다.
  //    가까이 와서 자기 자리까지 곧게 뚫리면 그때부터는 지금까지처럼 자기 자리로 간다 (무리가 커서 자리가 멀수록 '일단 나한테'가 먼저)
  const CF = 1, CF_INF = 65535;               // 칸 크기 (칸) · 못 닿는 칸
  let cfW = 0, cfH = 0, cfBlock = null, cfD = null, cfN8 = null, cfNA = null, cfNB = null, cfAt = -1e9, cfKey = '', cfReady = false, cfRuns = 0;
  const cfQ = [[], [], [], [], [], [], [], []], cfSeedI = [], cfSeedD = [];
  function cfInit() {
    cfW = Math.ceil((MM.x1 - MM.x0) / CF) + 2; cfH = Math.ceil((MM.z1 - MM.z0) / CF) + 2;   // 둘레 한 줄은 늘 막힌 칸 — 이웃을 볼 때 가장자리 검사를 안 하려고
    cfBlock = new Uint8Array(cfW * cfH); cfD = new Uint16Array(cfW * cfH);
    cfN8 = [-1, 1, -cfW, cfW, -cfW - 1, -cfW + 1, cfW - 1, cfW + 1]; cfNA = [0, 0, 0, 0, -1, 1, -1, 1]; cfNB = [0, 0, 0, 0, -cfW, -cfW, cfW, cfW];   // 대각선 이웃은 그 옆 두 칸이 다 비어야 지난다 (모서리를 가로지르지 않게)
    for (let cz = 0; cz < cfH; cz++) { cfBlock[cz * cfW] = 1; cfBlock[cz * cfW + cfW - 1] = 1; }
    for (let cx = 0; cx < cfW; cx++) { cfBlock[cx] = 1; cfBlock[(cfH - 1) * cfW + cx] = 1; }
    const m = BODY + 0.05;                    // 칸 가운데가 벽·물가에서 몸 반지름 넘게 떨어져야 빈 칸
    const mark = (x0, z0, x1, z1) => {
      const a = Math.max(1, Math.ceil((x0 - m - MM.x0) / CF + 0.5)), b = Math.min(cfW - 2, Math.floor((x1 + m - MM.x0) / CF + 0.5));
      const c = Math.max(1, Math.ceil((z0 - m - MM.z0) / CF + 0.5)), d = Math.min(cfH - 2, Math.floor((z1 + m - MM.z0) / CF + 0.5));
      for (let cz = c; cz <= d; cz++) for (let cx = a; cx <= b; cx++) cfBlock[cz * cfW + cx] = 1;
    };
    for (const B of buildings) mark(B.x0, B.z0, B.x1, B.z1);
    for (const [x0, z0, x1, z1] of CH_MAP.rivers) mark(x0, z0, x1, z1);
  }
  const cfCell = (x, z) => { const cx = Math.floor((x - MM.x0) / CF) + 1, cz = Math.floor((z - MM.z0) / CF) + 1; return cx < 1 || cz < 1 || cx >= cfW - 1 || cz >= cfH - 1 ? -1 : cz * cfW + cx; };
  const cfX = (i) => MM.x0 + ((i % cfW) - 0.5) * CF, cfZ = (i) => MM.z0 + (((i / cfW) | 0) - 0.5) * CF;   // 칸 가운데
  function cfSeed(x, z, c0) {                 // (x, z) 둘레의 빈 칸을 출발 칸으로 — 처음 거리 = c0 + 그 칸 가운데까지 (내 칸이 벽 옆이라 막힌 칸이어도 출발할 수 있게 둘레를 같이 넣는다)
    const cx0 = Math.floor((x - MM.x0) / CF) + 1, cz0 = Math.floor((z - MM.z0) / CF) + 1;
    for (let dz = -2; dz <= 2; dz++) for (let dx = -2; dx <= 2; dx++) {
      const cx = cx0 + dx, cz = cz0 + dz; if (cx < 1 || cz < 1 || cx >= cfW - 1 || cz >= cfH - 1) continue;
      const i = cz * cfW + cx; if (cfBlock[i]) continue;
      const d = Math.hypot(cfX(i) - x, cfZ(i) - z); if (d > 1.6 * CF) continue;
      cfSeedI.push(i); cfSeedD.push(Math.round((c0 + d) / CF * 5));
    }
  }
  function cfCompute() {                      // 나(안에 있으면 그 건물의 열린 문 앞)에서 모든 빈 칸까지 걸어서 가는 거리 — 곧은 걸음 5, 대각선 7
    if (!cfBlock) cfInit();
    cfD.fill(CF_INF); for (const q of cfQ) q.length = 0; cfSeedI.length = 0; cfSeedD.length = 0; cfReady = false; cfRuns++;
    const S = me.space;
    if (!S) cfSeed(me.foot.x, me.foot.z, 0);
    else for (const D of S.doors) cfSeed(D.cx + D.nx * 1.2, D.cz + D.nz * 1.2, Math.hypot(D.cx - me.foot.x, D.cz - me.foot.z) + 1.2);
    if (!cfSeedI.length) return;
    const order = cfSeedI.map((_, k) => k).sort((a, b) => cfSeedD[a] - cfSeedD[b]), W = cfW, blk = cfBlock, D = cfD;
    let si = 0, cur = cfSeedD[order[0]], pend = 0;
    for (;;) {
      while (si < order.length && cfSeedD[order[si]] <= cur) { const k = order[si++], i = cfSeedI[k], d = cfSeedD[k]; if (d < D[i]) { D[i] = d; cfQ[d & 7].push(i); pend++; } }
      const q = cfQ[cur & 7], o5 = cur + 5, o7 = cur + 7, q5 = cfQ[o5 & 7], q7 = cfQ[o7 & 7];
      for (let k = 0; k < q.length; k++) {
        const i = q[k]; if (D[i] !== cur) continue;   // 더 가까운 길로 이미 다시 들어간 칸
        const l = !blk[i - 1], r = !blk[i + 1], u = !blk[i - W], d = !blk[i + W];
        if (l && D[i - 1] > o5) { D[i - 1] = o5; q5.push(i - 1); pend++; }
        if (r && D[i + 1] > o5) { D[i + 1] = o5; q5.push(i + 1); pend++; }
        if (u && D[i - W] > o5) { D[i - W] = o5; q5.push(i - W); pend++; }
        if (d && D[i + W] > o5) { D[i + W] = o5; q5.push(i + W); pend++; }
        if (l && u && !blk[i - W - 1] && D[i - W - 1] > o7) { D[i - W - 1] = o7; q7.push(i - W - 1); pend++; }
        if (r && u && !blk[i - W + 1] && D[i - W + 1] > o7) { D[i - W + 1] = o7; q7.push(i - W + 1); pend++; }
        if (l && d && !blk[i + W - 1] && D[i + W - 1] > o7) { D[i + W - 1] = o7; q7.push(i + W - 1); pend++; }
        if (r && d && !blk[i + W + 1] && D[i + W + 1] > o7) { D[i + W + 1] = o7; q7.push(i + W + 1); pend++; }
      }
      pend -= q.length; q.length = 0;
      if (pend <= 0 && si >= order.length) break;
      cur++;
    }
    cfReady = true;
  }
  function cfFresh() {                        // 내가 다른 칸으로 옮겼을 때만, 많아야 0.25초에 한 번 다시 계산한다 (곧게 못 오는 동료가 있을 때만 불린다)
    if (clock < cfAt) cfAt = -1e9;            // 새 판
    const S = me.space, key = S ? 'b' + S.local + ':' + S.doors.length : 'c' + cfCell(me.foot.x, me.foot.z);
    if (cfReady && (key === cfKey || clock - cfAt < 0.25)) return;
    if (!cfReady && clock - cfAt < 0.25 && key === cfKey) return;   // 출발 칸을 못 잡은 채면 같은 자리에서 되풀이하지 않는다
    cfCompute(); cfKey = key; cfAt = clock;
  }
  function cfDist(x, z) {                     // 그 자리에서 나까지 걸어서 가는 거리 (칸) — 막힌 칸(벽에 바짝)이면 둘레 빈 칸 값으로, 닿는 길이 없으면 Infinity
    const i = cfCell(x, z); if (i < 0) return Infinity;
    if (cfD[i] !== CF_INF) return cfD[i] / 5 * CF;
    let m = CF_INF; for (let n = 0; n < 8; n++) if (cfD[i + cfN8[n]] < m) m = cfD[i + cfN8[n]];
    return m === CF_INF ? Infinity : m / 5 * CF + CF;
  }
  function cfLos(ax, az, bx, bz) {            // 칸 지도에서 두 자리가 곧게 이어지나 (출발 쪽 0.75칸은 안 본다 — 벽에 붙어 서 있을 수 있다)
    const L = Math.hypot(bx - ax, bz - az), n = Math.ceil(L / (0.45 * CF));
    for (let k = 1; k <= n; k++) {
      const t = k / n; if (t * L < 0.75) continue;
      const i = cfCell(ax + (bx - ax) * t, az + (bz - az) * t); if (i < 0 || cfBlock[i]) return false;
    }
    return true;
  }
  const cfOut = [0, 0];
  function cfStep(b) {                        // 흐름을 따라 내려가는 길 위에서, 지금 자리에서 곧게 보이는 가장 먼 칸 (최대 14칸 앞) — 칸마다 꺾지 않고 길게 보고 간다
    const px = b.foot.x, pz = b.foot.z;
    let i = cfCell(px, pz); if (i < 0) return null;
    let first = true;
    if (cfD[i] === CF_INF) {                  // 벽에 바짝 붙어 막힌 칸에 서 있으면 둘레에서 나에게 가장 가까운 빈 칸부터
      let m = CF_INF, bi = -1; for (let n = 0; n < 8; n++) { const j = i + cfN8[n]; if (cfD[j] < m) { m = cfD[j]; bi = j; } }
      if (bi < 0) return null; i = bi; first = false; cfOut[0] = cfX(i); cfOut[1] = cfZ(i);
    }
    for (let k = 0; k < 14; k++) {
      let m = cfD[i], ni = -1;
      for (let n = 0; n < 8; n++) { const j = i + cfN8[n]; if (cfD[j] >= m) continue; if (n >= 4 && (cfBlock[i + cfNA[n]] || cfBlock[i + cfNB[n]])) continue; m = cfD[j]; ni = j; }
      if (ni < 0) break;                      // 출발 칸(내 자리)에 닿았다
      i = ni;
      const x = cfX(i), z = cfZ(i);
      if (!first && !cfLos(px, pz, x, z)) break;   // 첫 칸은 바로 옆 빈 칸이라 그냥 간다
      first = false; cfOut[0] = x; cfOut[1] = z;
    }
    return first ? null : cfOut;
  }
  let chBlk = null;                           // 길을 막는 것 전부 — 건물(산 포함) + 강 토막
  function chLos(px, pz, tx, tz) {            // 두 자리가 곧게 이어지나 — around()와 같은 기준 (0.2칸 넓혀서 보고, 내가 그 둘레 안이면 그 건물은 뺀다)
    for (const R of chBlk) {
      if (px > R.x0 - GAP && px < R.x1 + GAP && pz > R.z0 - GAP && pz < R.z1 + GAP) continue;
      if (segRect(px, pz, tx, tz, R, GAP) < Infinity) return false;
    }
    return true;
  }
  // c13 길잡이 — 밖에 있는 몸이 (tx, tz)로 갈 때 이번에 향할 자리. null이면 목적지 그대로 (곧게 뚫렸거나, 건물 모서리 돌아가기에 맡긴다)
  //   ① 목적지까지 곧게 뚫렸으면 그대로
  //   ② 강·산 건너면 길목(다리·산 길목)을 거쳐서 — 길목 폭 안에서 저마다 다른 줄로 (큰 무리가 한 줄로 몰리지 않게)
  //   ③ 같은 구역인데 막혔고 나에게서 멀면 (걸어서 목적지보다 4칸 넘게 멀다) 자기 자리 대신 '나에게 가는 흐름'을 따라온다
  //   ④ 어느 경우든 1.5초 동안 제자리에서 못 움직이면 (모서리 하나로 안 풀리는 막다른 곳·낀 곳) 3초 동안 흐름을 타고 빠져나온다
  function chGuide(b, tx, tz) {
    const px = b.foot.x, pz = b.foot.z;
    if (Math.hypot(tx - me.foot.x, tz - me.foot.z) > DOMAIN * armyK * 1.5 + 6) {   // 내 둘레가 아닌 목적지 — 흐름('나에게 가는 길')은 못 쓴다. 다른 구역이면 길목만 거친다
      const r = chRoute(b, tx, tz); return r[0] === tx && r[1] === tz ? null : r;
    }
    if (!chBlk) chBlk = buildings.concat(CH_MAP.rivers.map(([x0, z0, x1, z1]) => ({ x0, z0, x1, z1 })));
    if (chLos(px, pz, tx, tz)) { b.flow = false; b.cfForce = 0; b.cfSeen = -1; return null; }
    const r = chRoute(b, tx, tz), cross = r[0] !== tx || r[1] !== tz;
    cfFresh();
    const fb = cfReady ? cfDist(px, pz) : Infinity;
    if (fb === Infinity) return cross ? r : null;           // 흐름을 못 쓰는 자리 (칸 지도에서 닿는 길이 없다)
    if (b.cfForce > clock && fb > 2) { const w = cfStep(b); if (w) return w; }
    if (!(clock - b.cfSeen < 0.5) || Math.hypot(px - b.cfAx, pz - b.cfAz) > 1.2) { b.cfAx = px; b.cfAz = pz; b.cfSince = clock; }   // 제자리에 묶여 있나 — 1.2칸 넘게 움직일 때마다 다시 잰다
    b.cfSeen = clock;
    if (clock - b.cfSince > 1.5 && fb > 2.5) { b.cfForce = clock + 3; b.cfSince = clock; const w = cfStep(b); if (w) return w; }
    if (cross) { b.flow = false; return r; }
    const fT = cfDist(tx, tz); if (fT > DOMAIN * armyK * 1.5 + 6) return null;   // 곧은 거리는 가까워도 걸어서는 먼 목적지
    if (fb <= fT + (b.flow ? 1.5 : 4)) { b.flow = false; return null; }           // 이미 내 둘레 — 여기서부터는 건물 모서리 돌아가기
    const w = cfStep(b); if (!w) return null;
    b.flow = true; return w;
  }
  let chShadow = () => {};
  const chNearBuf = [];
  function chWallsNear(x, z, R) {             // 도망 방향을 잴 때 볼 벽 — 둘레 R칸 안 건물 벽(닫힌 문 포함)과 강가. 강도 벽처럼 막힌 것으로 본다
    chNearBuf.length = 0;
    for (const B of buildings) if (x > B.x0 - R && x < B.x1 + R && z > B.z0 - R && z < B.z1 + R) for (const w of B.walls) chNearBuf.push(w);
    for (const g of chRiverSegs) if (x > Math.min(g[0], g[2]) - R && x < Math.max(g[0], g[2]) + R && z > Math.min(g[1], g[3]) - R && z < Math.max(g[1], g[3]) + R) chNearBuf.push(g);
    return chNearBuf;
  }
  const CH_ICON = {}, CH_TEX = {};
  const CH_HOUSE_ROOF = [0x26231f, 0x2a2622, 0x22252a, 0x2c241f, 0x25282b, 0x302a24, 0x1f2226];   // 집 지붕은 조금씩 다르게
  if (CHAPTER) {
    for (const k of [...Object.keys(CH_DEF), 'x', 'passH', 'passV']) { CH_ICON[k] = chIcon(k); CH_TEX[k] = new THREE.CanvasTexture(CH_ICON[k]); CH_TEX[k].colorSpace = THREE.SRGBColorSpace; }
    const roadMat = flatMat(0x858585), lotMat = flatMat(0xa7a294);
    for (const [x0, z0, x1, z1] of CH_MAP.lots) flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, lotMat, -0.93);   // c5: 공터 — 나중에 기물이 들어갈 자리 (지금은 흙빛 바닥만)
    for (const [x0, z0, x1, z1] of CH_MAP.roads) flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, roadMat, -0.9);   // 대로 — 어둠 밑에 깔린다
    // c3: 강 — 못 건너지만 건너편은 보인다 (벽이 아니라 시야를 안 가린다). 물 무늬는 땅 기준, 어둠 밑에 깔린다. 다리 = 상판 + 양쪽 난간
    const waterTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
      g.fillStyle = '#2c6c9a'; g.fillRect(0, 0, 256, 256); g.lineCap = 'round';
      let sd = 5; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      for (let i = 0; i < 40; i++) { const x = rnd() * 256, y = rnd() * 256, L = 18 + rnd() * 34; g.strokeStyle = rnd() < 0.5 ? 'rgba(150, 205, 235, 0.45)' : 'rgba(18, 60, 96, 0.45)'; g.lineWidth = 3 + rnd() * 3;
        for (const ox of [0, 256, -256]) { g.beginPath(); g.moveTo(x + ox, y); g.quadraticCurveTo(x + ox + L / 2, y - 5, x + ox + L, y); g.stroke(); } }
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })();
    const waterMat = new THREE.MeshBasicMaterial({ map: waterTex, transparent: true, depthTest: false, depthWrite: false });
    for (const [x0, z0, x1, z1] of CH_MAP.rivers) {
      const w = x1 - x0, d = z1 - z0, geo = new THREE.PlaneGeometry(w, d).rotateX(-Math.PI / 2), uv = geo.attributes.uv;
      for (let i = 0; i < uv.count; i++) uv.setXY(i, (x0 + uv.getX(i) * w) / 10, (z0 + (1 - uv.getY(i)) * d) / 10);
      const m = new THREE.Mesh(geo, waterMat); m.position.set((x0 + x1) / 2, 0.03, (z0 + z1) / 2); m.renderOrder = -0.92; scene.add(m);
    }
    const deckMat = flatMat(0x8d7c66), railMat = flatMat(0x4a3f33);
    for (const [x0, z0, x1, z1] of CH_MAP.bridges) {
      flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, deckMat, -0.9);
      if (x1 - x0 >= z1 - z0) for (const z of [z0 + 0.25, z1 - 0.25]) flat(x1 - x0, 0.5, (x0 + x1) / 2, z, railMat, -0.89);
      else for (const x of [x0 + 0.25, x1 - 0.25]) flat(0.5, z1 - z0, x, (z0 + z1) / 2, railMat, -0.89);
    }
    // c2: 산 — 구역 사이를 막는 문 없는 덩어리. 벽 선은 안 그리고(겹친 자리에 줄이 생긴다), 덩어리끼리 무늬가 이어지게 땅 기준으로 무늬를 입힌다
    const hillTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
      g.fillStyle = '#3e5a36'; g.fillRect(0, 0, 256, 256);
      let sd = 11; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      for (let i = 0; i < 46; i++) { const x = rnd() * 256, y = rnd() * 256, r = 14 + rnd() * 26, lit = rnd() < 0.5;
        for (const [ox, oy] of [[0, 0], [256, 0], [-256, 0], [0, 256], [0, -256]]) { g.fillStyle = lit ? 'rgba(98, 134, 78, 0.5)' : 'rgba(30, 48, 28, 0.5)'; g.beginPath(); g.ellipse(x + ox, y + oy, r, r * 0.7, 0, 0, Math.PI * 2); g.fill(); } }
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })();
    const hillMat = new THREE.MeshBasicMaterial({ map: hillTex, transparent: true, depthTest: false, depthWrite: false });
    for (const B of buildings) if (B.type === 'hill') {
      scene.remove(B.roof);
      const w = B.x1 - B.x0 + 0.3, d = B.z1 - B.z0 + 0.3, geo = new THREE.PlaneGeometry(w, d).rotateX(-Math.PI / 2), uv = geo.attributes.uv;
      for (let i = 0; i < uv.count; i++) uv.setXY(i, (B.x0 + uv.getX(i) * w) / 14, (B.z0 + (1 - uv.getY(i)) * d) / 14);   // 땅 기준 무늬 (14칸마다 반복)
      B.roof = new THREE.Mesh(geo, hillMat); B.roof.position.set((B.x0 + B.x1) / 2, 0.03, (B.z0 + B.z1) / 2); B.roof.renderOrder = -0.46; scene.add(B.roof);   // c13: 산 그림자(-0.47) 위 — 산 자체는 늘 보인다
    }
    // c13: 산 그림자 — 산 너머(나에게서 산에 가려진 쪽)는 안 보인다. 산 덩어리마다 나를 기준으로 그 뒤쪽을 검게 덮는다 (지붕·아이콘 위, 캐릭터 밑).
    //      지금 좀비들이 보고 있는 자리는 덮지 않는다 (시야 표시와 같은 스텐실). 강은 그림자가 없어서 건너편이 그대로 보인다
    {
      const hs = buildings.filter((B) => B.type === 'hill'), pos = new Float32Array(hs.length * 18), geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, depthTest: false, depthWrite: false, side: THREE.DoubleSide,
        stencilWrite: true, stencilRef: 1, stencilFunc: THREE.NotEqualStencilFunc, stencilFail: THREE.KeepStencilOp, stencilZFail: THREE.KeepStencilOp, stencilZPass: THREE.KeepStencilOp }));
      mesh.frustumCulled = false; mesh.renderOrder = -0.47; scene.add(mesh);   // 지붕(-0.51)·아이콘·벽 위, 거리 원(-0.45)·캐릭터 밑
      chShadow = () => {
        const px = me.foot.x, pz = me.foot.z, L = 400; let o = 0;
        for (const B of hs) {
          const cs = [[B.x0, B.z0], [B.x1, B.z0], [B.x1, B.z1], [B.x0, B.z1]];
          let bi = 0, bj = 1, low = 2;                // 나에게서 가장 벌어져 보이는 두 모서리 = 그 덩어리의 윤곽
          for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) {
            const ax = cs[i][0] - px, az = cs[i][1] - pz, bx = cs[j][0] - px, bz = cs[j][1] - pz, c = (ax * bx + az * bz) / ((Math.hypot(ax, az) || 1e-6) * (Math.hypot(bx, bz) || 1e-6));
            if (c < low) { low = c; bi = i; bj = j; }
          }
          const [ax, az] = cs[bi], [bx, bz] = cs[bj], da = Math.hypot(ax - px, az - pz) || 1e-6, db = Math.hypot(bx - px, bz - pz) || 1e-6;
          const ax2 = ax + (ax - px) / da * L, az2 = az + (az - pz) / da * L, bx2 = bx + (bx - px) / db * L, bz2 = bz + (bz - pz) / db * L;
          pos.set([ax, 0.05, az, bx, 0.05, bz, bx2, 0.05, bz2, ax, 0.05, az, bx2, 0.05, bz2, ax2, 0.05, az2], o); o += 18;
        }
        geo.attributes.position.needsUpdate = true;
      };
    }
    buildings.forEach((B, i) => {
      if (B.type === 'hill') return;
      B.roof.material = flatMat(B.type === 'house' ? CH_HOUSE_ROOF[i % CH_HOUSE_ROOF.length] : CH_DEF[B.type].roof);
      if (B.type === 'house') return;
      B.sign = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 3.4), new THREE.MeshBasicMaterial({ map: CH_TEX[B.type], transparent: true, depthTest: false, depthWrite: false }));
      B.sign.quaternion.copy(camera.quaternion);
      B.sign.position.set((B.x0 + B.x1) / 2, 0.06, (B.z0 + B.z1) / 2);
      B.sign.renderOrder = -0.507;            // 금고 건물 보물상자와 같은 자리 — 어둠 위
      scene.add(B.sign);
    });
  }
'''
MINIMAP = r'''
  // ── 챕터 미니맵 (c1) — 스타크래프트처럼 세 겹: 못 가 본 곳 = 새까맣게 · 가 본 곳 = 안개(어두운 땅과 건물) · 지금 보이는 곳 = 밝게.
  //    집 말고 모든 건물(랜드마크·창고)은 한 번 밝혀지면 그 자리에 아이콘이 남는다. 잠식한 건물은 X ──
  let chDim = null, chLit = null, chMask = null;
  function chLayer(W, H, X, Z, sx, sz, ground, road, house, other, hill, water, deck) {
    const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
    g.fillStyle = ground; g.fillRect(0, 0, W, H);
    g.fillStyle = water; for (const [x0, z0, x1, z1] of CH_MAP.rivers) g.fillRect(X(x0), Z(z0), (x1 - x0) * sx, (z1 - z0) * sz);
    g.fillStyle = road; for (const [x0, z0, x1, z1] of CH_MAP.roads) g.fillRect(X(x0), Z(z0), (x1 - x0) * sx, (z1 - z0) * sz);
    g.fillStyle = deck; for (const [x0, z0, x1, z1] of CH_MAP.bridges) g.fillRect(X(x0), Z(z0), (x1 - x0) * sx, (z1 - z0) * sz);
    for (const B of buildings) { g.fillStyle = B.type === 'hill' ? hill : B.type === 'house' ? house : other; g.fillRect(X(B.x0), Z(B.z0), (B.x1 - B.x0) * sx, (B.z1 - B.z0) * sz); }
    return c;
  }
  function chMinimap(eyes, W, H, X, Z, sx, sz) {
    const u = W / MM_CW;                       // c18: 그림 한 칸 크기 — 작게 볼 때는 화면 배율 그대로, 크게 볼 때는 커진 만큼 (아이콘·내 점이 같은 비율로 커진다)
    if (!chDim || chDim.width !== W || chDim.height !== H) {   // c18: 크기가 바뀌면(크게 보기) 바탕 그림을 그 크기로 새로 만든다
      chDim = chLayer(W, H, X, Z, sx, sz, '#303036', '#27272c', '#141417', '#1b1b20', '#1a2a1a', '#14283a', '#3a342c');     // 안개 속
      chLit = chLayer(W, H, X, Z, sx, sz, '#9c9ca4', '#85858d', '#3a3a42', '#4c4c56', '#4f7447', '#3d82b6', '#a8957b');     // 지금 보이는 곳
      chMask = document.createElement('canvas'); chMask.width = W; chMask.height = H;
    }
    const g = mmCtx, m = chMask.getContext('2d');
    g.fillStyle = '#000'; g.fillRect(0, 0, W, H);                         // 못 가 본 곳 = 새까맣게
    m.globalCompositeOperation = 'source-over'; m.clearRect(0, 0, W, H); m.drawImage(chDim, 0, 0);
    m.globalCompositeOperation = 'destination-in'; m.imageSmoothingEnabled = true; m.drawImage(mmFog, 0, 0, W, H);   // 가 본 칸만 남긴다
    g.drawImage(chMask, 0, 0);                                            // 가 본 곳 = 안개
    g.save(); g.beginPath();
    for (const z of eyes) { if (!isZombie(z)) continue; const cx = X(z.foot.x), cz = Z(z.foot.z), r = z.sense * sx; g.moveTo(cx + r, cz); g.arc(cx, cz, r, 0, Math.PI * 2); }
    g.clip(); g.drawImage(chLit, 0, 0); g.restore();                      // 지금 보이는 곳 = 밝게
    const sz2 = 8 * u, szB = 13.2 * u;   /* c33: 1.1배 더 (12 → 13.2) */   /* c15: 2배는 너무 커서 1.5배로 (8 → 12) */   /* c14: 건물 아이콘 2배 (8 → 16) — 미니맵은 건물이 나에게서 어느 쪽에 있는지만 보이면 된다 (자세한 지형은 가려져도 된다). 길목 화살표는 그대로 */   /* c6: 미니맵이 작아진 만큼 아이콘도 (10.5 → 8) */
    for (let pass = 0; pass < 3; pass++) for (const B of buildings) {   // 커진 아이콘이 겹치면 중요한 것이 위로 — 잠식한 건물(X) → 창고 → 랜드마크 순으로 그린다
      if (B.type === 'house' || B.type === 'hill') continue;             // 집과 산은 표시 없음
      if (pass === 0 && !B.found) {                                      // 건물 자리를 한 칸이라도 밝혔으면 그때부터 표시
        const cx0 = Math.max(0, Math.floor((B.x0 - MM.x0) / MM_CELL)), cx1 = Math.min(mmW - 1, Math.floor((B.x1 - MM.x0) / MM_CELL));
        const cz0 = Math.max(0, Math.floor((B.z0 - MM.z0) / MM_CELL)), cz1 = Math.min(mmH - 1, Math.floor((B.z1 - MM.z0) / MM_CELL));
        for (let cz = cz0; cz <= cz1 && !B.found; cz++) for (let cx = cx0; cx <= cx1; cx++) if (explored[cz * mmW + cx]) { B.found = true; break; }
      }
      if (!B.found || (B.done ? 0 : B.type === 'store' ? 1 : 2) !== pass) continue;
      g.drawImage(CH_ICON[B.done ? 'x' : B.type], Math.max(0, Math.min(W - szB, X((B.x0 + B.x1) / 2) - szB / 2)), Math.max(0, Math.min(H - szB, Z((B.z0 + B.z1) / 2) - szB / 2)), szB, szB);   // 가장자리 건물은 미니맵 안쪽으로 당겨서 잘리지 않게
    }
    for (const B of buildings) if (B.type === 'house' && B.taken) { const s = szB / 3; g.drawImage(CH_ICON.x, X((B.x0 + B.x1) / 2) - s / 2, Z((B.z0 + B.z1) / 2) - s / 2, s, s); }   // c56: 점령한 집 = 3분의 1 크기 X (지붕엔 표시 없음)
    for (const P of CH_MAP.passPts) {                                     // c4: 길목 — 그 자리를 밝혔으면 양쪽 화살표
      if (!P.found && explored[Math.floor((P.z - MM.z0) / MM_CELL) * mmW + Math.floor((P.x - MM.x0) / MM_CELL)]) P.found = true;
      if (P.found) g.drawImage(CH_ICON[P.dir === 'h' ? 'passH' : 'passV'], X(P.x) - sz2 / 2, Z(P.z) - sz2 / 2, sz2, sz2);
    }
    for (const p of pickups) {                                            // c20: 안 주운 아이템 — 테스트맵처럼 미니맵에 늘 보인다 (금색 동그라미 + 아이콘). 건물 아이콘 위에 그린다
      const px = X(p.x), py = Z(p.z), pr = 5.5 * u;
      g.fillStyle = 'rgba(0, 0, 0, 0.85)'; g.beginPath(); g.arc(px, py, pr + 1.2 * u, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#ffd25a'; g.beginPath(); g.arc(px, py, pr, 0, Math.PI * 2); g.fill();
      if (p.img && p.img.complete && p.img.naturalWidth) g.drawImage(p.img, px - pr * 0.8, py - pr * 0.8, pr * 1.6, pr * 1.6);
    }
    const r = 2.1 * u;                                                    // 나 = 빨간 점
    g.beginPath(); g.arc(X(me.foot.x), Z(me.foot.z), r, 0, Math.PI * 2);
    g.fillStyle = '#ff3b30'; g.fill(); g.lineWidth = 1 * u; g.strokeStyle = 'rgba(255, 255, 255, 0.9)'; g.stroke();
  }
  // ── c18: 미니맵을 누르면 화면 한가운데에 크게, 다시 누르면 제자리로. 보여 주는 내용은 같다 (크게 볼 때는 그 크기로 새로 그려서 또렷하게) ──
  let mmBig = false;
  function mmLayout() {
    const S = mmEl.style;
    if (!mmBig) {
      S.width = MM_CW + 'px'; S.height = MM_CH + 'px'; S.top = ''; S.left = ''; S.right = ''; S.transform = ''; S.zIndex = ''; S.borderRadius = ''; S.boxShadow = '';
      mmEl.width = Math.round(MM_CW * mmDpr); mmEl.height = Math.round(MM_CH * mmDpr);
    } else {                                  // 화면 폭의 92% (높이의 70%를 넘지 않게), 한가운데보다 살짝 위 — 조이스틱을 가리지 않는다
      const vw = stage.clientWidth, vh = stage.clientHeight, k = Math.min(vw * 0.92 / MM_CW, vh * 0.7 / MM_CH), w = Math.round(MM_CW * k), h = Math.round(MM_CH * k), d = Math.min(mmDpr, 2);
      S.width = w + 'px'; S.height = h + 'px'; S.top = '46%'; S.left = '50%'; S.right = 'auto'; S.transform = 'translate(-50%, -50%)'; S.zIndex = '15'; S.borderRadius = '12px'; S.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.65)';
      mmEl.width = Math.round(w * d); mmEl.height = Math.round(h * d);
    }
    mmT = 0; updateMinimap(0);                // 크기를 바꾸면 그림이 지워진다 — 바로 다시 그린다 (일시정지 중이어도)
  }
  if (CHAPTER) {
    mmEl.style.pointerEvents = 'auto'; mmEl.style.touchAction = 'none'; mmEl.style.cursor = 'pointer';
    mmEl.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); mmBig = !mmBig; mmLayout(); });   // 누른 손가락은 조이스틱으로 안 넘어간다
    window.addEventListener('resize', () => { if (mmBig) mmLayout(); });
  }
'''
SLEEP = r'''    if (CHAPTER) {                            // c12: 사람은 좀비가 CH_MEET칸 안으로 다가오기 전까지 잔다 — 스폰된 자리에 그대로 (생각·이동·부딪힘 없음). 한 번 깨어난 사람은 그 뒤로 멀어져도 계속 움직인다
      if (!chHot) { CH_GW = Math.ceil((MM.x1 - MM.x0) / CH_WAKE); CH_GH = Math.ceil((MM.z1 - MM.z0) / CH_WAKE); chHot = new Uint8Array(CH_GW * CH_GH); }
      const col = (x) => Math.max(0, Math.min(CH_GW - 1, Math.floor((x - MM.x0) / CH_WAKE))), row = (z) => Math.max(0, Math.min(CH_GH - 1, Math.floor((z - MM.z0) / CH_WAKE)));
      chHot.fill(0); chHot[row(me.foot.z) * CH_GW + col(me.foot.x)] = 1;   // 먼저 굵은 격자로 거른다 — 좀비가 있는 칸과 이웃 칸에 있는 사람만 거리를 잰다
      for (const z of zombies) chHot[row(z.foot.z) * CH_GW + col(z.foot.x)] = 1;
      const near = (b, z) => { const dx = z.foot.x - b.foot.x, dz = z.foot.z - b.foot.z; return dx * dx + dz * dz < CH_MEET * CH_MEET; };
      for (const b of bodies) if (b.kind === 'citizen') {
        if (b.met) {                          // c54: 깨어 있는 사람 — 좀비가 전부 멀어지면(CH_SLEEP칸 밖) 그 자리에 다시 선다 (연산 안 함). 싸우거나 도망치거나 나를 쫓는 중이면 그대로 움직인다
          if ((b.zzT = (b.zzT === undefined ? Math.random() * 0.5 : b.zzT) - dt) > 0) continue;
          b.zzT = 0.5;
          if (!chCanSleep(b)) continue;
          const far = (z) => { const dx = z.foot.x - b.foot.x, dz = z.foot.z - b.foot.z; return dx * dx + dz * dz > CH_SLEEP * CH_SLEEP; };
          if (far(me) && zombies.every(far)) { b.met = false; b.sleep = true; b.vel.set(0, 0); }
          continue;
        }
        const cx = col(b.foot.x), cz = row(b.foot.z); let hot = false;
        for (let dz = -1; dz <= 1 && !hot; dz++) for (let dx = -1; dx <= 1; dx++) { const X = cx + dx, Z = cz + dz; if (X >= 0 && X < CH_GW && Z >= 0 && Z < CH_GH && chHot[Z * CH_GW + X]) { hot = true; break; } }
        if (hot && (near(b, me) || zombies.some((z) => near(b, z)))) { b.met = true; chWakeUp(b); }
        b.sleep = !b.met;
      }
    }
'''
R = [
  ('<title>러닝데드 이동 테스트</title>', '<title>러닝데드 챕터</title>'),
  ('<div id="ver">v589</div>', f'<div id="ver">챕터 {VER}</div>'),
  ("  const TEST_MAP = CAR_TEST || false;", "  const CHAPTER = true;   // 챕터 줄기 (c1~): 구역 4개짜리 맵, 지금은 건물만 — 사람·경찰·금고 없음\n  const TEST_MAP = CAR_TEST || CHAPTER;"),
  ("  const BUILDINGS = TEST_MAP ? TEST_BLDGS : ", "  const CH_MAP = " + MAP + ";   // 생성기(씨앗 7)가 만든 고정 맵 — c2: 건물 71채 (랜드마크 9 · 창고 8 · 집 54) · c3: 세로 경계 = 강(다리 3곳), 가로 경계 = 산(길목 2곳) · c4·c5: 집을 작게, 1~4채씩 바짝 뭉치고 블록마다 공터, 집 8채는 차고\n  const BUILDINGS = CHAPTER ? CH_MAP.b : TEST_MAP ? TEST_BLDGS : "),
  ("local: s.local, block: s.block };", "local: s.local, block: s.block, type: s.t || '', zone: s.zone, sideK: s.sideK, garage: !!s.garage };"),
  ("  const SCREEN_Y = 0.40;  // 내 자리 = 화면 위에서 40%", "  const FULL = window.navigator.standalone === true || window.matchMedia('(display-mode: fullscreen), (display-mode: standalone)').matches;   // c7: 홈 화면 앱으로 연 전체 화면\n  const SCREEN_Y = FULL ? 0.45 : 0.40;  // 내 자리 = 화면 위에서 40% (c8: 전체 화면에선 45% — 화면이 길어진 만큼 나를 조금 아래로. 조이스틱은 화면이 바닥까지 내려가면서 같이 내려간다 — 따로 더 내리려면 --joyd)"),
  ("    position: absolute; left: 50%; bottom: calc(56px + env(safe-area-inset-bottom, 0px)); box-sizing: border-box; width: 124px; height: 124px; margin-left: -62px;", "    position: absolute; left: 50%; bottom: calc(56px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px)); box-sizing: border-box; width: 124px; height: 124px; margin-left: -62px;"),
  ("    position: fixed !important; left: 50% !important; top: auto !important; bottom: calc(56px + env(safe-area-inset-bottom, 0px)) !important;", "    position: fixed !important; left: 50% !important; top: auto !important; bottom: calc(56px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px)) !important;"),
  ("    position: absolute; left: calc(50% + 54px); bottom: calc(172px + env(safe-area-inset-bottom, 0px));", "    position: absolute; left: calc(50% + 54px); bottom: calc(172px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px));"),
  ("    el.style.bottom = `calc(118px + env(safe-area-inset-bottom, 0px) + ${dy}px)`;", "    el.style.bottom = `calc(118px - var(--joyd, 0px) + env(safe-area-inset-bottom, 0px) + ${dy}px)`;"),
  ("    const el = document.getElementById(id); el.style.bottom = 'auto';", "    const el = document.getElementById(id); el.style.bottom = 'auto'; if (CHAPTER) el.style.opacity = '0';   /* c9: 되감기·일시정지 버튼은 안 보이게 (자리와 누르는 건 그대로) */"),
  ("citizen: 0xffcf33, guard: 0xff8c1a, attacker: 0xc62828,", "citizen: CHAPTER ? 0xf2f2f2 : 0xffcf33, guard: CHAPTER ? 0xffcf33 : 0xff8c1a, attacker: CHAPTER ? 0xff8c1a : 0xc62828,"),   # c43: 원래 attacker 항목까지 바꿔야 주황이 먹는다   # c32: 강한 인간 = 노랑
  ("    guard: { col: '#ff8c1a', name: '헬창',", "    guard: { col: CHAPTER ? '#ffcf33' : '#ff8c1a', name: CHAPTER ? '강한 인간' : '헬창',"),   # c11: 인간 = 하양
  ("    citizen: { col: '#ffcf33', name: '좃밥',", "    citizen: { col: CHAPTER ? '#f2f2f2' : '#ffcf33', name: CHAPTER ? '인간' : '좃밥',"),
  ("    for (const b of bodies) if (isZombie(b)) zombies.push(b);\n    while (teamQueue.length)", "    for (const b of bodies) if (isZombie(b)) zombies.push(b);\n" + SLEEP + "    while (teamQueue.length)"),
  ("      b.px = b.foot.x; b.pz = b.foot.z;\n      const sp0 = spaceOf(b.foot.x, b.foot.z);", "      if (b.sleep) continue;\n      b.px = b.foot.x; b.pz = b.foot.z;\n      const sp0 = spaceOf(b.foot.x, b.foot.z);"),
  ("    for (const b of bodies) if (b.kind === 'citizen') {   // 화면 밖·좀비와 먼 조용한 시민은 판단을 4프레임에 한 번 (v177)", "    for (const b of bodies) if (b.kind === 'citizen' && !b.sleep) {   // 화면 밖·좀비와 먼 조용한 시민은 판단을 4프레임에 한 번 (v177)"),
  ("      if (!b.fixed) { const gk = b.goo ? 0.56 : 1;", "      if (!b.fixed && !b.sleep) { const gk = b.goo ? 0.56 : 1;"),
  ("    for (const b of bodies) byX.push(b);", "    for (const b of bodies) if (!b.sleep) byX.push(b);"),
  ("    for (const b of bodies) {                 // 지도(미니맵) 밖으로는 못 나간다 (v174)\n      const r = b.r || BODY;", "    for (const b of bodies) {                 // 지도(미니맵) 밖으로는 못 나간다 (v174)\n      if (b.sleep) continue;\n      const r = b.r || BODY;"),
  ("    const sp = c.vel.length();\n    let best = -Infinity, bx = 1, bz = 0;", "    const sp = c.vel.length();\n    const chNear = CHAPTER ? chWallsNear(c.foot.x, c.foot.z, PANIC_SPEED * LOOK + BODY + 1) : walls;   // c11: 가까운 벽과 강가만\n    let best = -Infinity, bx = 1, bz = 0;"),
  ("      const room = wallRay(c.foot.x, c.foot.z, dx, dz, PANIC_SPEED * LOOK + BODY) - BODY;", "      const room = wallRay(c.foot.x, c.foot.z, dx, dz, PANIC_SPEED * LOOK + BODY, chNear) - BODY;"),
  ("    aroundCars = b.kind === 'citizen'; const w = around(b.foot.x, b.foot.z, tx, tz); aroundCars = true; return w;", "    if (CHAPTER) { const g = chGuide(b, tx, tz); if (g) { tx = g[0]; tz = g[1]; } }   // c13: 강·산 건너면 길목을 거쳐서, 멀리서 막혔으면 '나에게 가는 흐름'을 따라\n    aroundCars = b.kind === 'citizen'; const w = around(b.foot.x, b.foot.z, tx, tz); aroundCars = true; return w;"),
  ("    draw(dt);\n    checkTut();", "    draw(dt);\n    if (CHAPTER) chShadow();                  // c13: 산 그림자\n    checkTut();"),
  ("    const B = me.space, m = 0.7;\n    if (B) { x = Math.max(B.x0 + m,", "    if (CHAPTER && !me.space) { const f = chSlotFix(x, y); x = f[0]; y = f[1]; }   // c13: 강물·산 속 자리는 내 쪽으로\n    const B = me.space, m = 0.7;\n    if (B) { x = Math.max(B.x0 + m,"),
  ("    B.doors = [].map((side) => {", "    B.doors = (s.open || []).map((side) => {   /* c5: 차고 — 한쪽 벽이 처음부터 통째로 뚫려 있다 */"),
  ("w: s.station ? DOOR * 4 / 9 : DOOR };", "w: s.garage ? (nx ? s.d : s.w) - 0.5 : s.station ? DOOR * 4 / 9 : DOOR };"),
  ("o.hp = o.maxHp = B.side ? MY_DAMAGE * 3.5 : MY_DAMAGE * 19.5;", "o.hp = o.maxHp = B.side || B.garage ? MY_DAMAGE * 3.5 : MY_DAMAGE * 19.5;   /* c5: 차고 문도 집 문과 같다 */"),
  ("  // 잠긴 문 (v239) — 문 자리를 막는 벽 한 토막 + 철문 그림.", ICONS.strip('\n') + "\n  // 잠긴 문 (v239) — 문 자리를 막는 벽 한 토막 + 철문 그림."),
  ("  const MM = TEST_MAP ? {", "  const MM = CHAPTER ? CH_MAP.mm : TEST_MAP ? {"),
  ("  const MM_S = Math.min(128 * 2 / 3 / (MM.x1 - MM.x0), 136 * 2 / 3 / (MM.z1 - MM.z0));", "  const MM_S = Math.min((CHAPTER ? 88 : 128 * 2 / 3) / (MM.x1 - MM.x0), (CHAPTER ? 107 : 136 * 2 / 3) / (MM.z1 - MM.z0));   /* c6: 미니맵을 3분의 1 줄여 테스트맵 크기쯤으로 (132×160 → 88×107) */"),
  ("  function updateMinimap(dt) {                // 0.1초마다", MINIMAP.strip('\n') + "\n  function updateMinimap(dt) {                // 0.1초마다"),
  ("    mmCtx.clearRect(0, 0, W, H);", "    if (CHAPTER) { chMinimap(eyes, W, H, X, Z, sx, sz); return; }\n    mmCtx.clearRect(0, 0, W, H);"),
  ("    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;", "    if (CHAPTER) { me.foot.set(CH_MAP.start[0], 0, CH_MAP.start[1]); me.space = null; chPopulate();   /* c42: 시작 체력은 테스트맵과 같다 (최대의 20%) */ return; }   // c1: 남서쪽 큰 구역 아래 대로에서 시작 · c11: 인간 200명\n    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;"),
  ("      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;", "      if (B.sign) { B.sign.visible = !B.open; const tx = CH_TEX[B.done ? 'x' : B.type]; if (B.sign.material.map !== tx) { B.sign.material.map = tx; B.sign.material.needsUpdate = true; } }   // c1: 지붕 아이콘 — 들어가면 사라지고, 잠식하면 X\n      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;"),
  ("    for (const B of buildings) if (!B.station) B.found = false;", "    for (const B of buildings) if (!B.station) { B.found = false; B.done = false; }\n    if (CHAPTER) for (const P of CH_MAP.passPts) P.found = false;"),
  ("  const starsEl = document.getElementById('stars');", "  const starsEl = document.getElementById('stars');\n  if (CHAPTER) { const v = document.getElementById('ver'); v.style.setProperty('display', 'block', 'important'); v.style.top = 'auto'; v.style.bottom = 'calc(2px + env(safe-area-inset-bottom, 0px))'; v.style.left = '50%'; v.style.transform = 'translateX(-50%)';   /* c40: 레벨·경보는 테스트맵처럼 보이고, 버전 글자는 아래 가운데로 */ v.style.fontSize = '10px'; v.style.opacity = '0.55'; }   // c1: 맵만 보는 판 — 경보·레벨 표시는 가린다. c10: 왼쪽 위에 버전 글자 (새 버전이 떴는지 보려고)"),
  ("    for (const b of bodies) if (!b.fixed) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게", "    for (const b of bodies) if (!b.fixed && !b.sleep) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게\n    if (CHAPTER) for (const b of bodies) if (!b.fixed && !b.sleep) riverCollide(b);   // c3: 강"),
  ("  for (const [ax, az, bx, bz] of walls) flat(", "  for (const [ax, az, bx, bz] of buildings.flatMap((B) => (B.type === 'hill' ? [] : B.walls))) flat("),   # c2: 산은 벽 선을 안 그린다
  ("|| cand[Math.floor(Math.random() * cand.length)];   /* v431", "|| cand[B.sideK !== undefined ? B.sideK % cand.length : Math.floor(Math.random() * cand.length)];   /* c1: 챕터 맵은 쪽문 자리도 고정 */   /* v431"),
  ("bodies, spawn, fleeDir, step: stepWorld };", "bodies, spawn, fleeDir, step: stepWorld, buildings, explored, ch: CHAPTER ? CH_MAP : null, zombify: makeZombie, slotOf, route: CHAPTER ? chRoute : null, cf: () => ({ D: cfD, W: cfW, H: cfH, block: cfBlock, ready: cfReady, runs: cfRuns, dist: cfDist }), get armyK() { return armyK; } };"),
]
from loot_patch import LOOT_R, ITEM_R, FX_R, LVUP_R, STAR_R, XP_R, AWAKE_R, SLOT_R, AWK_TXT_R, AWK_UI_R, AWK_RING_R, RANK_R, VIG_R, STICK_R, COPKB_R, HP_R, DMG_R, DISP_R, CAR_R, TEAM_R   # c19: 금고와 아이템 · c21: 아이템 수치 · c24: 파편 · c25: 레벨업 · c26: 별 · c28: 경험치 · c29: 각성 주사
R += LOOT_R + ITEM_R + FX_R + LVUP_R + STAR_R + XP_R + AWAKE_R + SLOT_R + AWK_TXT_R + AWK_UI_R + AWK_RING_R + RANK_R + VIG_R + STICK_R + COPKB_R + HP_R + DMG_R + DISP_R + CAR_R + TEAM_R
from room_patch import ROOM_R   # c53: 건물 안 방 · 철창 · 랜덤 시작
R += ROOM_R
from c54_patch import C54_R   # c54: 시야 1.3배 · 경계 시간 · 두 번째 출동 조건
R += C54_R
from c55_patch import C55_R   # c55: 위험 티어 · 각성 체력 회복
R += C55_R
from c56_patch import C56_R   # c56: 내 테두리 · 다시 채우기
R += C56_R
from c57_patch import C57_R   # c57: 변이한 나는 덮치기 맨 끝
R += C57_R
from c58_patch import C58_R   # c58: 맞은 동료는 사물을 안 노린다 · 문이 뚫린 건물은 안팎이 한 공간
R += C58_R
from c59_patch import C59_R   # c59: 군인팀 출동 · 건널목 바리케이트와 수비대 · 건물 사람은 건물로 돌아간다
R += C59_R
from c62_patch import C62_R   # c62: 특수부대 출동 차례표
R += C62_R
from c64_patch import C64_R   # c64: 경찰 출동 간격 · 근접 적 먼저
R += C64_R
from c65_patch import C65_R   # c65: 바리케이트 체력 2배 · 체력바 여러 겹
R += C65_R
from c68_patch import C68_R   # c68: 배회 멈춤 0 · 주황·빨강 바로 공격
R += C68_R
from c69_patch import C69B_R   # c69: 순환도로 · 차종 · 주차된 차
R += C69B_R
from c70_patch import C70_R   # c70: 건물 안 사물 · 하트
R += C70_R
from c71_patch import C71_R   # c71: 돌아다니는 민간 차
R += C71_R
from c72_patch import C72_R   # c72: 건널목 수비대 절반 · 바리케이트 3분의 2
R += C72_R
from c74_patch import C74_R   # c74: 레벨업 10명·1.3배 · 가장 큰 무리에서 빨강 한 명
R += C74_R
from c75_patch import C75_R   # c75: 5명·4명 무리에서도 빨강 한 명씩
R += C75_R
from c76_patch import C76_R   # c76: 차 무게 최소 = 경찰차 · 편의점 경찰 · 길거리 주황 5분의 1은 노랑
R += C76_R
from c77_patch import C77_R   # c77: 차 크기 등급 · 체력 높은 사물 20% 깎음
R += C77_R
from c78_patch import C78_R   # c78: 사람은 평소 도로를 피한다 · 도망·싸움 중엔 차에 치인다
R += C78_R
from c79_patch import C79_R   # c79: 횡단보도 · 달리는 차와 몸의 진짜 물리
R += C79_R
from c80_patch import C80_R   # c80: 물음표 수송차 · 운전자 성격과 패닉
R += C80_R
from c81_patch import C81_R   # c81: 길거리 차 수·미는 힘 3분의 1 줄임 · 속도 20% 줄임
R += C81_R
from c82_patch import C82_R   # c82: 사물·주차된 차 줄임 · 길거리 하양·노랑 늘림 · 오토바이
R += C82_R
from c83_patch import C83_R   # c83: 건널목을 길게 (만·산 덩어리·휜 순환도로) · 교통망
R += C83_R
from c84_patch import C84_R   # c84: 하양·노랑·주황 — 알아보는 거리 80% · 경계 시간 60% · 이동 속도 115%
R += C84_R
from c85_patch import C85_R   # c85: 마을 꾸미기 (공원·주유소·농구장·공사 현장·길거리 사물)
R += C85_R
from c86_patch import C86_R   # c86: 사물·차 통일 규칙 · 경보단계 조건 2배 · 포인트 군집 · 자폭 점수
R += C86_R
from c87_patch import C87_R   # c87: 내가 치는 차도 동료를 부른다
R += C87_R
from c88_patch import C88_R   # c88: 수비대 인원 · 바리케이트 한계
R += C88_R
from c89_patch import C89_R   # c89: 줄인 맵
R += C89_R
from c90_patch import C90_R   # c90: 하트 3배 · 물음표 차 2배
R += C90_R
from c91_patch import C91_R   # c91: 집 7채만 뺀 맵
R += C91_R
from c92_patch import C92_R   # c92: 레벨업 처음 7명
R += C92_R
from c93_patch import C93_R   # c93: 집 넓이 80% · 골목 넓힘
R += C93_R
from c94_patch import C94_R   # c94: 집 문 폭 3분의 2
R += C94_R
from c95_patch import C95_R   # c95: 모든 건물 15% 줄임 · 골목 넓힘
R += C95_R
from c96_patch import C96_R   # c96: 레벨업 1.2배씩
R += C96_R
from c97_patch import C97_R   # c97: 노랑·주황·빨강 체력 10% 줄임
R += C97_R
from c98_patch import C98_R   # c98: 길거리 경찰 줄임 · 색 한 단계씩 10%
R += C98_R
from c99_patch import C99_R   # c99: 경보단계 조건 1.3배 더
R += C99_R
from c100_patch import C100_R   # c100: 수송차 비율 · 경보 5% · 덩치 체력 · 변이 줄기세포
R += C100_R
from c101_patch import C101_R   # c101: 현금 수송차 탑승자
R += C101_R
from c102_patch import C102_R   # c102: 부활 체력 100%
R += C102_R
from c103_patch import C103_R   # c103: 경보 출동 빈도 15% 줄임
R += C103_R
from c104_patch import C104_R   # c104: 얻은 변이 좀비
R += C104_R
from c105_patch import C105_R   # c105: 덩치 무게 +2
R += C105_R
from c106_patch import C106_R   # c106: 덩치 무게 11 · 얻은 덩치 체력 570
R += C106_R
from c107_patch import C107_R   # c107: 집 15채 · 열린 집
R += C107_R
from c108_patch import C108_R   # c108: 집 금고 · 하트 · 유전자
R += C108_R
from c109_patch import C109_R   # c109: 미는 힘 그대로
R += C109_R
from c110_patch import C110_R   # c110: 주유소 지붕 없앰 · 시작 하양
R += C110_R
from c111_patch import C111_R   # c111: 주유소 기둥 없앰
R += C111_R
from c112_patch import C112_R   # c112: 사물에서 하트·유전자 안 나옴
R += C112_R
from c113_patch import C113_R   # c113: 시작 하양 — 움직인 뒤 앞쪽에
R += C113_R
from c114_patch import C114_R   # c114: 큰 무리 성능 · 경보 20% 앞당김
R += C114_R
from c115_patch import C115_R   # c115: 얻은 변이 좀비 체력 3분의 2
R += C115_R
from c116_patch import C116_R   # c116: 수송차 전부 돌진형
R += C116_R
from c117_patch import C117_R   # c117: 수송차 속도 +10%
R += C117_R
from c118_patch import C118_R   # c118: 특수부대 첫 출동 앞당김
R += C118_R
from c119_patch import C119_R   # c119: 건물 찾기 격자 NaN 방어
R += C119_R
from c120_patch import C120_R   # c120: 맵 선택 · 테이저건 우선순위
R += C120_R
from c121_patch import C121_R   # c121: 자폭 점수 — 분홍 40점
R += C121_R
from c122_patch import C122_R   # c122: 시간제 특공대 · 보스 장갑차
R += C122_R
from c123_patch import C123_R   # c123: 산성 10초 · 도트 2
R += C123_R
from c124_patch import C124_R   # c124: 레벨업에 새 도구 없음
R += C124_R
from c125_patch import C125_R   # c125: 무기/장비 분리 · 특공대 시간표
R += C125_R
from c126_patch import C126_R   # c126: 특공대 120초부터 5초씩 · 보스 카운트다운
R += C126_R
from c127_patch import C127_R   # c127: 카운트다운 검은 판
R += C127_R
from c128_patch import C128_R   # c128: 보스 단독 · 15초마다 1팀
R += C128_R
from c129_patch import C129_R   # c129: 길거리 빨강·주황 10% 하양
R += C129_R
from c130_patch import C130_R   # c130: 배회 경찰 10% 노랑
R += C130_R
from c131_patch import C131_R   # c131: 길거리 빨강·경찰 10% 줄임
R += C131_R
from c132_patch import C132_R   # c132: 길거리 빨강 10% 더 하양
R += C132_R
from c133_patch import C133_R   # c133: 안 보이는 사물 고침 · 빨강·경찰 10% 더
R += C133_R
from c134_patch import C134_R   # c134: 장갑차 돌진 멈춤 고침
R += C134_R
from c135_patch import C135_R   # c135: 길거리 노랑·주황 20% 줄임 · 공격력 15%
R += C135_R
from c136_patch import C136_R   # c136: 좀비 최대 체력 10% 깎음 · 길거리 하양 20% 줄임
R += C136_R
from c137_patch import C137_R   # c137: 장갑차는 눈에 띄기 전까지 빠르다
R += C137_R
from c138_patch import C138_R   # c138: 현금 알아채는 거리 통일
R += C138_R
from c139_patch import C139_R   # c139: 무기 수치표 (0~6단계)
R += C139_R
from c140_patch import C140_R   # c140: 현금 거리 +1칸씩 · 각성 충전 35초
R += C140_R
from c141_patch import C141_R   # c141: 집 금고 확률 3배
R += C141_R
from c142_patch import C142_R   # c142: 금고 꽝 없음
R += C142_R
from c143_patch import C143_R   # c143·c144: 빨강 20% 늘림 · 적 공격력 15% · 경찰차 출동 빈도
R += C143_R
from c145_patch import C145_R   # c145: 나의 문 거리·순위 · 큰 사물도 부서진다
R += C145_R
from c146_patch import C146_R   # c146: 적 공격력 20% 더 (장갑차 빼고)
R += C146_R
from c147_patch import C147_R   # c147: 조이스틱 이동 중 사물 안 침
R += C147_R
from c148_patch import C148_R   # c148: 사물 체력바 없음
R += C148_R
from c149_patch import C149_R   # c149: 적 공격력 5% 줄임
R += C149_R
from c150_patch import C150_R   # c150: 장갑차 데미지 = 군인
R += C150_R
from c151_patch import C151_R   # c151: 경찰 출동 빈도 15% 줄임
R += C151_R
from c152_patch import C152_R   # c152: 내 최대 체력 15% 올림
R += C152_R
from c153_patch import C153_R   # c153: 적 체력 5% 줄임
R += C153_R
from c154_patch import C154_R   # c154: 성능 (결과 그대로)
R += C154_R
from c155_patch import C155_R   # c155: 성능 (덜 자주 계산)
R += C155_R
from c156_patch import C156_R   # c156: 몸 묶어 그리기
R += C156_R
from c157_patch import C157_R   # c157: 집 금고 50%
R += C157_R
from c158_patch import C158_R   # c158: 레벨업 처음 5명
R += C158_R
from c159_patch import C159_R   # c159: 적 공격력 7% 줄임
R += C159_R
from c160_patch import C160_R   # c160: 동료 공격력 10% 올림
R += C160_R
from c161_patch import C161_R   # c161: 무기 강화 카드 2배
R += C161_R
from c162_patch import C162_R   # c162: 동료 공격력 7% 올림
R += C162_R
from c163_patch import C163_R   # c163: 동료 체력 · 빠루 · 흡수복
R += C163_R
from c164_patch import C164_R   # c164: 동료 체력 되돌림 · 적 공격력 7% 줄임
R += C164_R
from c165_patch import C165_R   # c165: 내 최대 체력 10% 올림
R += C165_R
from c166_patch import C166_R   # c166: 보스 테스트 맵
R += C166_R
from c167_patch import C167_R   # c167: 보스 테스트 동료 60
R += C167_R
from c168_patch import C168_R   # c168: 장갑차 조정 · 보스 뒤 출동 · 동료 70
R += C168_R
from c169_patch import C169_R   # c169: 장갑차 이동 사격
R += C169_R
from c170_patch import C170_R   # c170: 장갑차 포탑 회전
R += C170_R
from c171_patch import C171_R   # c171: 장갑차 돌진 (후진 → 돌진)
R += C171_R
from c172_patch import C172_R   # c172: 장갑차 돌진 기세
R += C172_R
from c173_patch import C173_R   # c173: 돌진 중 기관포 멈춤
R += C173_R
from c174_patch import C174_R   # c174: 돌진 속도 +30% · 시간 -30%
R += C174_R
from c175_patch import C175_R   # c175: 장갑차 돌진 연기
R += C175_R
from c176_patch import C176_R   # c176: 보스 뒤 군인만 · 장갑차 호위 거리
R += C176_R
from c177_patch import C177_R   # c177: 장갑차 길이 · 회전 부드럽게
R += C177_R
from c178_patch import C178_R   # c178: 장갑차 기관총
R += C178_R
from c179_patch import C179_R   # c179: 장갑차 팔각형 · 길이 · 출동 속도
R += C179_R
from c180_patch import C180_R   # c180: 궤도 연기 2배
R += C180_R
from c181_patch import C181_R   # c181: 총구 불꽃 위치
R += C181_R
from c182_patch import C182_R   # c182: 보스 뒤 군인 주인 없음 · 장갑차 길이 · 총열
R += C182_R
from c183_patch import C183_R   # c183: 장갑차 체력·돌진 주기·속도
R += C183_R
from c184_patch import C184_R   # c184: 장갑차 20% 크게
R += C184_R
from c185_patch import C185_R   # c185: 첫 카운트다운 글자 · 보스 체력 · 보스 체력바
R += C185_R
from c186_patch import C186_R   # c186: 문·금고 우선순위 = 사람
R += C186_R
from c187_patch import C187_R   # c187: 금고·문 붙잡기
R += C187_R
from c188_patch import C188_R   # c188: 사람 수 · 처음부터 열린 문
R += C188_R
from c189_patch import C189_R   # c189: 길거리 경찰 경보 따라 · 무기 강화 카드
R += C189_R
from c190_patch import C190_R   # c190: 길거리 경찰 시간표
R += C190_R
from c191_patch import C191_R   # c191: 보스 감전
R += C191_R
from c192_patch import C192_R   # c192: 길거리 경찰 두 번
R += C192_R
from c193_patch import C193_R   # c193: 지붕 한 번 열리면 계속
R += C193_R
from c194_patch import C194_R   # c194: 보스 감전 건물 안에서도
R += C194_R
from c195_patch import C195_R   # c195: 장갑차 거리 몸 둘레부터 · 시작 체력 80%
R += C195_R
from c196_patch import C196_R   # c196: 분노 바이러스 강화마다 +10%
R += C196_R
from c197_patch import C197_R   # c197: 빠루 20%씩
R += C197_R
from c198_patch import C198_R   # c198: 장비 수치
R += C198_R
from c199_patch import C199_R   # c199: 흡수 2.5씩 · 촉매 7%씩
R += C199_R
from c200_patch import C200_R   # c200: 벽 부수기 · 보스 인지거리 · 보스 사망 군인
R += C200_R
from c201_patch import C201_R   # c201: 보스 난사
R += C201_R
from c202_patch import C202_R   # c202: 난사 튀는 이펙트
R += C202_R
from c203_patch import C203_R   # c203: 집 면마다 2토막 · 어그로 20%·나 100%
R += C203_R
from c204_patch import C204_R   # c204: 벽 어그로 면 단위
R += C204_R
from c205_patch import C205_R   # c205: 계산 정리
R += C205_R
from c206_patch import C206_R   # c206: 벽은 내가 칠 때만 동료 대상
R += C206_R
from c207_patch import C207_R   # c207: 벽 체력바 없음 · 뒤틀림
R += C207_R
from c208_patch import C208_R   # c208: 창고 벽
R += C208_R
from c209_patch import C209_R   # c209: 나 — 벽도 금고처럼
R += C209_R
from c210_patch import C210_R   # c210: 다른 면은 절반
R += C210_R
from c211_patch import C211_R   # c211: 죽은 장갑차 멈춤
R += C211_R
from c212_patch import C212_R   # c212: 방 쪽문 자리 · 벽 번쩍
R += C212_R
from c213_patch import C213_R   # c213: 벽 체력
R += C213_R
from c214_patch import C214_R   # c214: 벽 체력 25% 줄임
R += C214_R
from c215_patch import C215_R   # c215: 벽 토막 30% 줄임
R += C215_R
from c216_patch import C216_R   # c216: 체력바 고정 길이·색 겹
R += C216_R
from c217_patch import C217_R   # c217: 넘치면 가로 늘림
R += C217_R
from c218_patch import C218_R   # c218: 4겹 고정 · 가로 무제한 · 보스도
R += C218_R
from c219_patch import C219_R   # c219: 보스 바 빨강 한 줄
R += C219_R
from c220_patch import C220_R   # c220: 처음 발견 빨강·경찰 약화
R += C220_R
from c221_patch import C221_R   # c221: 보스 피해 · 첫 발견 확률
R += C221_R
from c222_patch import C222_R   # c222: 보스 돌진·기관포·체력
R += C222_R
from c223_patch import C223_R   # c223: 특공대 구성
R += C223_R
from c224_patch import C224_R   # c224: 운동화·틀니·산성 폭발·무기 분해
R += C224_R
from c225_patch import C225_R   # c225: 설명 문구
R += C225_R
from c226_patch import C226_R   # c226: 틀니 문구 · 현금 강도
R += C226_R
from c227_patch import C227_R   # c227: 돋보기 가로 정렬
R += C227_R
from c228_patch import C228_R   # c228: 다시 채우기 절반
R += C228_R
from c229_patch import C229_R   # c229: 벽 체력 20% 올림
R += C229_R
from c230_patch import C230_R   # c230: 나 빼고 체력 10% 줄임
R += C230_R
from c231_patch import C231_R   # c231: 내 공격력 10% 줄임
R += C231_R
from c232_patch import C232_R   # c232: 적 체력 10% 올림
R += C232_R
from c233_patch import C233_R   # c233: 내 공격력 20% 더 줄임
R += C233_R
from c234_patch import C234_R   # c234: 첫 발견 빨강 4 · 경찰 1
R += C234_R
from c235_patch import C235_R   # c235: 적 피해 숫자
R += C235_R
from c236_patch import C236_R   # c236: 빨강 바뀐 수 5명까지
R += C236_R
from c237_patch import C237_R   # c237: 그대로 남은 수 기준
R += C237_R
from c238_patch import C238_R   # c238: 배회 경찰만 굴림
R += C238_R
from c239_patch import C239_R   # c239: 적 공격력 10% 줄임
R += C239_R
from c240_patch import C240_R   # c240: 나·동료 공격력 10% 올림
R += C240_R
from c241_patch import C241_R   # c241: 덩치 사물 2배
R += C241_R
from c242_patch import C242_R   # c242: 동료 10% 되돌림
R += C242_R
from c243_patch import C243_R   # c243: 나·동료 공격력 10%
R += C243_R
from c244_patch import C244_R   # c244: 10% → 3%
R += C244_R
from c245_patch import C245_R   # c245: 적 체력·공격력 5% 줄임
R += C245_R
from c246_patch import C246_R   # c246: 첫 발견 60% · 합 7명
R += C246_R
from c247_patch import C247_R   # c247: 사수 경찰차 = 들어오는 순간
R += C247_R
from c248_patch import C248_R   # c248: 경보 출동 인원·간격·섞기
R += C248_R
from c249_patch import C249_R   # c249: 특공대 4분의 1 줄임
R += C249_R
from c250_patch import C250_R   # c250: 특공대 걸어서·군인차
R += C250_R
from c251_patch import C251_R   # c251: 테이저 쿨타임·장탄
R += C251_R
from c252_patch import C252_R   # c252: 70% · 14명
R += C252_R
from c253_patch import C253_R   # c253: 적 피해 2% 줄임
R += C253_R
from c254_patch import C254_R   # c254: 레벨업 1.13배
R += C254_R
from c255_patch import C255_R   # c255: 보스 체력 1/4 줄임
R += C255_R
from c256_patch import C256_R   # c256: 분노 문구
R += C256_R
from c257_patch import C257_R   # c257: 운동화 5%
R += C257_R
from c258_patch import C258_R   # c258: 현금 최대 10초·9대·18칸
R += C258_R
from c259_patch import C259_R   # c259: 산성 강도
R += C259_R
from c260_patch import C260_R   # c260: 산성 자폭 스위치
R += C260_R
from c261_patch import C261_R   # c261: 산성 겹침 없음
R += C261_R
from c262_patch import C262_R   # c262: 주황 4 · 노랑 3 바뀜
R += C262_R
from c263_patch import C263_R   # c263: 수상함 전 경계 5배
R += C263_R
from c264_patch import C264_R   # c264: 주황·빨강 경계 = 경찰
R += C264_R
from c265_patch import C265_R   # c265: 도트 숫자
R += C265_R
from c266_patch import C266_R   # c266: 도트 숫자 맨 위
R += C266_R
from c267_patch import C267_R   # c267: 경계 5~6초 · 3초
R += C267_R
from c268_patch import C268_R   # c268: 테이저 0.5초씩
R += C268_R
from c269_patch import C269_R   # c269: 테이저 0.5초부터
R += C269_R
from c270_patch import C270_R   # c270: 보스 감전 같게
R += C270_R
from c271_patch import C271_R   # c271: 도트 숫자 크기·사라짐
R += C271_R
from c272_patch import C272_R   # c272: 산성 자폭 돌진
R += C272_R
from c273_patch import C273_R   # c273: 방탄복 = 총격 + 충격 흡수
R += C273_R
from c274_patch import C274_R   # 카드 설명 · 바로 강화 · 가방 분해
R += C274_R
from c275_patch import C275_R   # 방 벽 부서짐 · 철창만 안 부서짐
R += C275_R
from c276_patch import C276_R   # 분노 바이러스 설명
R += C276_R
from c277_patch import C277_R   # 카드 위로 · 설명 짧게
R += C277_R
from c278_patch import C278_R   # 카드 글 넘침
R += C278_R
from c279_patch import C279_R   # 자폭 쿨타임 -25%
R += C279_R
from c280_patch import C280_R   # 산성 폭발 확률
R += C280_R
from c281_patch import C281_R   # 빠루 50%씩
R += C281_R
from c282_patch import C282_R   # 촉매제
R += C282_R
from c283_patch import C283_R   # 틀니 덮치기 · MAX
R += C283_R
from c284_patch import C284_R   # 틀니 아이콘
R += C284_R
from c285_patch import C285_R   # 산성 폭발 시간
R += C285_R
from c286_patch import C286_R   # 산성 시간 긴 쪽
R += C286_R
from c287_patch import C287_R   # 자폭 산성 우선
R += C287_R
from c288_patch import C288_R   # 틀니 새로 · 자폭 변이 제외
R += C288_R
from c289_patch import C289_R   # 튜토리얼 1
R += C289_R
from c290_patch import C290_R   # 튜토리얼 박스 · 탐험 안개
R += C290_R
from c291_patch import C291_R   # 안개 벽선
R += C291_R
from c292_patch import C292_R   # 튜토리얼 실험실 축소 · ㄱ자 복도 · 사람
R += C292_R
from c293_patch import C293_R   # 실험 연구소 · 두 번째 방
R += C293_R
from c294_patch import C294_R   # 좀비 수조
R += C294_R
from c295_patch import C295_R   # 수조 안 동그란 좀비
R += C295_R
from c296_patch import C296_R   # 수조 표시 · 첫 방 2배
R += C296_R
from c297_patch import C297_R   # 첫 방 크기 조정
R += C297_R
from c298_patch import C298_R   # 박스 줄임
R += C298_R
from c299_patch import C299_R   # 구속 침대
R += C299_R
from c300_patch import C300_R   # 세 번째 방
R += C300_R
from c301_patch import C301_R   # 바리케이트 · 덩치 방
R += C301_R
from c302_patch import C302_R   # 먼지 · 수조 순위 · 문 금고
R += C302_R
from c303_patch import C303_R   # 아이콘 · 수조 자리
R += C303_R
from c304_patch import C304_R   # 바리케이트 너머 덮치기 금지
R += C304_R
from c305_patch import C305_R   # 바닥 화살표
R += C305_R
from c306_patch import C306_R   # 수조 고정
R += C306_R
from c307_patch import C307_R   # 문 앞 세모
R += C307_R
from c308_patch import C308_R   # 바리케이트끼리 안 밀기
R += C308_R
from c309_patch import C309_R   # 큰 맵 바리케이트 그대로
R += C309_R
from c310_patch import C310_R   # 세모 문 바로 앞
R += C310_R
from c311_patch import C311_R   # 바리케이트 복도 안에 가둠
R += C311_R
from c312_patch import C312_R   # 긴 탁자 줄임
R += C312_R
from c313_patch import C313_R   # 히드라 속도
R += C313_R
from c314_patch import C314_R   # 긴 복도 · 군인
R += C314_R
from c315_patch import C315_R   # avat gem
R += C315_R
from c316_patch import C316_R   # mutant ally award popup
R += C316_R
from c317_patch import C317_R   # C9 soldiers 4 snipers 2 further in
R += C317_R
from c318_patch import C318_R   # longer L, mid squad, down corridor
R += C318_R
from c319_patch import C319_R   # hit dust 2x at contact
R += C319_R
from c320_patch import C320_R   # tutorial soldiers escort snipers
R += C320_R
from c321_patch import C321_R   # wide sniper corridors, maze rooms, exit
R += C321_R
from c322_patch import C322_R   # longer sniper corridors, 45 cuts, generated maze, global wall attack
R += C322_R
from c323_patch import C323_R   # door overlap width, ally grid nav in room spaces
R += C323_R
from c324_patch import C324_R   # vomit projectile look
R += C324_R
from c325_patch import C325_R   # spit 1.5x
R += C325_R
from c326_patch import C326_R   # 5 big maze rooms
R += C326_R
from c327_patch import C327_R   # second armor vat room, maze people in corridors too
R += C327_R
from c328_patch import C328_R   # two gate doors across the maze corridor
R += C328_R
from c329_patch import C329_R   # double citizens before sniper corridor
R += C329_R
from c330_patch import C330_R   # cash works inside buildings outside map bounds
R += C330_R
from c331_patch import C331_R   # room2 white +1 orange -1
R += C331_R
from c332_patch import C332_R   # citizen room, breakable maze walls, merge tiny rooms
R += C332_R
from c333_patch import C333_R   # parking lot finale
R += C333_R
from c334_patch import C334_R   # safe-blocked last corridor, smaller bite clock, no minimap in tutorial
R += C334_R
from c335_patch import C335_R   # lot mid posts, rebalance thin maze spaces
R += C335_R
from c336_patch import C336_R   # narrower lot and road
R += C336_R
from c337_patch import C337_R   # shorter lot, clustered barricades, more defenders, lot decor
R += C337_R
from c338_patch import C338_R   # police-car lot, barricade-only last road, spread snipers, bright floor
R += C338_R
from c339_patch import C339_R   # one horizontal police-car line mid lot, snipers only in last road
R += C339_R
from c340_patch import C340_R   # scattered movie-like police line, centered lot entrance
R += C340_R
from c341_patch import C341_R   # tutorial white discovery + first ally popup
R += C341_R
from c342_patch import C342_R   # diagonal wall crossing fix
R += C342_R
from c343_patch import C343_R   # fewer lot police and cars, civilians in last road
R += C343_R
from c344_patch import C344_R   # half the gate defenders, 4 barricades
R += C344_R
from c345_patch import C345_R   # +10 white +5 yellow in maze
R += C345_R
from c346_patch import C346_R   # goal popup 0.5s after start
R += C346_R
from c347_patch import C347_R   # door at first corridor turn
R += C347_R
from c348_patch import C348_R   # partition-wall corridor after armor room, move road civilians to maze
R += C348_R
from c349_patch import C349_R   # narrower wall compartments, mixed people
R += C349_R
from c350_patch import C350_R   # mutant ally names include 변이
R += C350_R
from c351_patch import C351_R   # minimap me dot 2x
R += C351_R
from c352_patch import C352_R   # minimap dot 1.5x, bomb pick by score at target within my circle
R += C352_R
from c353_patch import C353_R   # bomber runs then pounces, explodes on contact
R += C353_R
from c354_patch import C354_R   # base map 1 (police stronghold, vertical, figure-8 ring)
R += C354_R
from c355_patch import C355_R   # c355: 거점 맵 주차장 · 집 정리
R += C355_R
from c356_patch import C356_R   # c356: 거점 맵 세로 골목
R += C356_R
from c357_patch import C357_R   # c357: 거점 맵 꾸미기 · 사람 없음
R += C357_R
from c358_patch import C358_R   # c358: 거점 맵 방 · 사람 (큰 맵 비율)
R += C358_R
from c359_patch import C359_R   # c359: 본 맵
R += C359_R
from c360_patch import C360_R   # c360: 다리 난간 자르기
R += C360_R
from c361_patch import C361_R   # c361: 느린 동료는 벽을 스스로 친다
R += C361_R
from c362_patch import C362_R   # c362: 느린 동료만 사물을 친다
R += C362_R
from c363_patch import C363_R   # c363: 실제 이동 속도
R += C363_R
from c364_patch import C364_R   # c364: 15%
R += C364_R
from c365_patch import C365_R   # c365: 적 테스트
R += C365_R
from c366_patch import C366_R   # c366: 큰 맵 건널목 · 30%
R += C366_R
from c367_patch import C367_R   # c367: 단단한 주먹
R += C367_R
from c368_patch import C368_R   # c368: 벽 체력 +25%
R += C368_R
from c369_patch import C369_R   # c369: 산성 폭발 시간
R += C369_R
from c370_patch import C370_R   # c370: 기생체
R += C370_R
from c371_patch import C371_R   # c371
R += C371_R
from c372_patch import C372_R   # c372: 분열세포
R += C372_R
from c373_patch import C373_R   # c373: 촉매제 · 백과사전
R += C373_R
from c374_patch import C374_R   # c374: 드론
R += C374_R
from c375_patch import C375_R   # c375: 드론 번개 · 출동 수
R += C375_R
from c376_patch import C376_R   # c376: 내 미는 힘 7
R += C376_R
from c377_patch import C377_R   # c377: 덩치 최대 13
R += C377_R
from c378_patch import C378_R   # c378: 덩치 개편
R += C378_R
from c379_patch import C379_R   # c379: 테이저
R += C379_R
from c380_patch import C380_R   # c380: 드론 사격 효과
R += C380_R
from c381_patch import C381_R   # c381: 드론 보이기
R += C381_R
from c382_patch import C382_R   # c382: 드론 출동 단계
R += C382_R
from c383_patch import C383_R   # c383: 분열세포 설명
R += C383_R
from c384_patch import C384_R   # c384: 작은 좀비 색 · 설명 확률
R += C384_R
from c385_patch import C385_R   # c385: 산성 폭발 섬광
R += C385_R
from c386_patch import C386_R   # c386: 섬광 · 작은 좀비 색
R += C386_R
from c387_patch import C387_R   # c387: 드론 체력 30
R += C387_R
from c388_patch import C388_R   # c388: 드론 주기 60초
R += C388_R
from c389_patch import C389_R   # c389: 섬광 2배
R += C389_R
from c390_patch import C390_R   # c390: 떨어진 드론
R += C390_R
from c391_patch import C391_R   # c391: 드론 폭발
R += C391_R
from c392_patch import C392_R   # c392: 산성 섬광 2/3
R += C392_R
from c393_patch import C393_R   # c393
R += C393_R
from c394_patch import C394_R   # c394: 보스 산성 덩어리
R += C394_R
from c395_patch import C395_R   # c395: 분열세포 20%
R += C395_R
from c396_patch import C396_R   # c396: 레벨업 제곱 곡선
R += C396_R
from c397_patch import C397_R   # c397: 가방 연출
R += C397_R
from c398_patch import C398_R   # c398: 떨어진 드론 최우선
R += C398_R
from c399_patch import C399_R   # c399: 산성 폭발 20% · 5
R += C399_R
from c400_patch import C400_R   # c400: 산성 폭발 30% · 3→10
R += C400_R
from c401_patch import C401_R   # c401: 산성 도트 1초
R += C401_R
from c402_patch import C402_R   # c402: 산성 폭발 지속 3초 고정
R += C402_R
from c403_patch import C403_R   # c403: 빠지는 적 붙어서 치기
R += C403_R
from c404_patch import C404_R   # c404: 따라다니는 미니맵
R += C404_R
from c405a_patch import C405A_R   # c405 1단계
R += C405A_R
from c405b_patch import C405B_R   # c405 2단계: 내 단락만
R += C405B_R
from c406_patch import C406_R   # c406: 새 본 맵
R += C406_R
from c407_patch import C407_R   # c407: 본 맵 테스트 · 원형 미니맵
R += C407_R
from c408_patch import C408_R   # c408: 깨어 있는 사람은 안 뺀다
R += C408_R
from c409_patch import C409_R   # c409: 물과 산 반반
R += C409_R
from c410_patch import C410_R   # c410: 잔해는 부딪힘이 없다
R += C410_R
from c411_patch import C411_R   # c411: 작은 좀비 미는 힘 3분의 1
R += C411_R
from c412_patch import C412_R   # c412: 작은 좀비 색 더 밝게
R += C412_R
from c413_patch import C413_R   # c413: 또 얻은 가방도 분해
R += C413_R
from c414_patch import C414_R   # c414: 본 맵 건널목·작은 단락 줄이기
R += C414_R
from c415_patch import C415_R   # c415: 마주 보는 면마다 건널목 하나
R += C415_R
from c416_patch import C416_R   # c416: 건널목 25% 길게
R += C416_R
from c417_patch import C417_R   # c417: 건널목 50% 더 길게
R += C417_R
from c418_patch import C418_R   # c418: 체력이 다한 적 공격·이동 속도 반
R += C418_R
from c419_patch import C419_R   # c419: 드론 주기 2배 · 한 번에 2배
R += C419_R
from c420_patch import C420_R   # c420: 장비 개편
R += C420_R
from c421_patch import C421_R   # c421: 자폭 산성 둔화 없앰
R += C421_R
from c422_patch import C422_R   # c422: 무기 갈림길 · 드론 경험치
R += C422_R
from c423_patch import C423_R   # c423: 드론 주기 1.5배
R += C423_R
from c424_patch import C424_R   # c424: 장비 배지 촘촘하게
R += C424_R
from c425_patch import C425_R   # c425: 장비 배지 위아래 간격만
R += C425_R
from c426_patch import C426_R   # c426: 배지 줄 원래대로
R += C426_R
from c427_patch import C427_R   # c427: 갈림길 모양 + 현금 갈림길
R += C427_R
from c428_patch import C428_R   # c428: 자폭 기본 아이콘 · 현금 거리
R += C428_R
from c429_patch import C429_R   # c429: 현금 사거리 · 다이아몬드 싸울 확률
R += C429_R
from c430_patch import C430_R   # c430: 변이·각성 갈림길
R += C430_R
from c431_patch import C431_R   # c431: 테이저건 갈림길
R += C431_R
from c432_patch import C432_R   # c432: 자폭 지정 동료
R += C432_R
from c433_patch import C433_R   # c433: 드론
R += C433_R
from c434_patch import C434_R   # c434: 드론 체력 8
R += C434_R
from c435_patch import C435_R   # c435: 자폭 — 적 먼저
R += C435_R
from c436_patch import C436_R   # c436: 경보 10단계 · 불도저 · 샷건 경찰 · 로봇
R += C436_R
from c437_patch import C437_R   # c437: 총동원령 — 터렛 · 샷건
R += C437_R
from c438_patch import C438_R   # c438: 드론 정리 · 불도저 노랑
R += C438_R
from c439_patch import C439_R   # c439: 괴물 테두리 · 드론 끼임
R += C439_R
from c440_patch import C440_R   # c440: 갈림길 카드 색
R += C440_R
from c441_patch import C441_R   # c441: 잔류제 변이 시간
R += C441_R
from c442_patch import C442_R   # c442: c441 되돌림
R += C442_R
from c443_patch import C443_R   # c443: 현금 거리 15%
R += C443_R
from c444_patch import C444_R   # c444: 차 콜라이더 10%
R += C444_R
from c445_patch import C445_R   # c445: 미는 힘 5
R += C445_R
from c446_patch import C446_R   # c446: 내 미는 힘 4
R += C446_R
from c447_patch import C447_R   # c447: 미는 힘
R += C447_R
from c448_patch import C448_R   # c448: 괴물 뿔 · 빨간 토사물
R += C448_R
from c449_patch import C449_R   # c449: 변이 동료 카메라
R += C449_R
from c450_patch import C450_R   # c450: 덩치 사물 피해
R += C450_R
from c451_patch import C451_R   # c451: 덩치 사물 1.5배
R += C451_R
from c452_patch import C452_R   # c452: 감염 시간
R += C452_R
from c453_patch import C453_R   # c453
R += C453_R
from c454_patch import C454_R   # c454: 불도저 2대
R += C454_R
from c455_patch import C455_R
R += C455_R
from c456_patch import C456_R
R += C456_R
from c457_patch import C457_R
R += C457_R
from c458_patch import C458_R
R += C458_R
for e in R:
    a, b, n = (e + (1,))[:3]
    assert s.count(a) == n, (s.count(a), n, a[:70])
    s = s.replace(a, b)
OUT.parent.mkdir(exist_ok=True); OUT.write_text(s, encoding='utf8')
import re
pathlib.Path('c.mjs').write_text(re.findall(r'<script type="module">(.*?)</script>', s, re.S)[-1], encoding='utf8')
print('wrote', OUT, len(s))
