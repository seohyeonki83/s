# 챕터 줄기 c1 — 테스트 버전 v589를 바탕으로 새 파일을 뜬다 (v589는 그대로). 구역 4개 · 건물만 · 지붕 아이콘 · 세 겹 미니맵
import pathlib, json, sys
SRC = pathlib.Path('/home/user/s/running-dead/v589.html'); OUT = pathlib.Path('/home/user/s/running-dead/chapter/' + sys.argv[1] + '.html')
s = SRC.read_text(encoding='utf8'); MAP = pathlib.Path('map.json').read_text(encoding='utf8')
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
    if (!pass) { rr(6, 6, 116, 116, 26); g.fillStyle = 'rgba(0, 0, 0, 0.88)'; g.fill(); rr(14, 14, 100, 100, 19); g.fillStyle = col; g.fill(); }
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
    } else if (type === 'x') { g.lineWidth = 17; g.beginPath(); g.moveTo(40, 40); g.lineTo(88, 88); g.moveTo(88, 40); g.lineTo(40, 88); g.stroke(); }   // 잠식한 건물
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
  const CH_MEET = 14;                         // c12: 좀비가 이만큼(칸) 안에 오면 깨어난다 — 좀비 시야(7.2칸)의 두 배쯤이라, 내 눈에 들어올 땐 이미 돌아다니고 있다
  let chHot = null, CH_GW = 0, CH_GH = 0;
  const chNearRiver = (x, z, m) => CH_MAP.rivers.some(([x0, z0, x1, z1]) => x > x0 - m && x < x1 + m && z > z0 - m && z < z1 + m);
  // c40: 사람 깔기 — 판마다 자리는 랜덤, 종류별 수와 패턴은 늘 같다
  //   하양 145 (건물 안 먼저 골고루, 빈집 3분의 1) · 노랑 48 (길거리에 띄엄띄엄, 4분의 1은 건물 안에 한 명씩) · 배회 경찰 20 (길거리)
  //   주황 48 · 빨강(자경단) 48 = 길거리에 2~4명씩 무리. 주황 2 + 빨강 3 (또는 3 + 2)이 섞인 5명 무리도 몇 개
  const CH_WHITE = 145, CH_YELLOW = 48, CH_YELLOW_IN = 12, CH_GANG = 48, CH_COPS = 20, CH_ROOM = 45;
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
  function chPut(x, z, area, type, B) {
    const c = addCitizen(x, z, area, type === 'vig' ? 'attacker' : type);
    if (type === 'police') c.post = area;     // 배회 경찰 = 자기 자리 둘레를 돈다
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
  function chPopulate() {
    const placed = [];
    for (let k = 0; k < CH_COPS; k++) { const p = chOutSpot(placed, 1.2, 18); if (!p) continue; placed.push(p); chPut(p[0], p[1], square(p[0], p[1]), 'police'); }
    // 무리: 주황·빨강 각 48 — 2~4명 무리로 쪼갠다. 섞인 5명 무리 2개 (주황 2 + 빨강 3, 주황 3 + 빨강 2)
    const groups = [['attacker', 'attacker', 'vig', 'vig', 'vig'], ['attacker', 'attacker', 'attacker', 'vig', 'vig']];
    for (const t of ['attacker', 'vig']) {
      let left = CH_GANG - groups.flat().filter((x) => x === t).length;
      while (left > 0) { let k = 2 + Math.floor(Math.random() * 3); if (left - k === 1) k = left > 4 ? k - 1 : left; k = Math.min(k, left); groups.push(Array(k).fill(t)); left -= k; }
    }
    const centers = [];
    for (const G of groups.sort(() => Math.random() - 0.5)) {
      const p = chOutSpot(centers, 2.5, 20); if (!p) continue; centers.push(p);
      const area = square(p[0], p[1]);
      G.forEach((t, i) => {
        let x = p[0], z = p[1];
        for (let tt = 0; tt < 40; tt++) { const a = Math.random() * Math.PI * 2, r = i ? rand(0.9, 1.8) : 0; x = p[0] + Math.cos(a) * r; z = p[1] + Math.sin(a) * r; if (!spaceOf(x, z) && freeSpot(x, z, null) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)) break; }
        chPut(x, z, area, t);
      });
    }
    // 하양: 건물 안 먼저 (빈집 3분의 1은 그대로 비운다) · 노랑 12명은 건물 안 한 명씩
    const hs = buildings.filter((B) => B.type === 'house').sort(() => Math.random() - 0.5), empty = new Set(hs.slice(0, Math.round(hs.length / 3)));
    const rooms = buildings.filter((B) => B.type !== 'hill' && !empty.has(B));
    const inPut = (B, type) => { let g = pickGoal(B); for (let t = 0; t < 30 && bodies.some((b) => Math.hypot(b.foot.x - g.x, b.foot.z - g.y) < 1.2); t++) g = pickGoal(B); chPut(g.x, g.y, B, type, B); };
    let w = 0;
    for (const B of rooms) {
      const base = Math.max(1, Math.round((B.x1 - B.x0) * (B.z1 - B.z0) / CH_ROOM)), k = Math.max(1, base + Math.floor(Math.random() * 3) - 1);
      for (let i = 0; i < k && w < CH_WHITE; i++, w++) inPut(B, '');
    }
    for (const B of rooms.slice().sort(() => Math.random() - 0.5).slice(0, CH_YELLOW_IN)) inPut(B, 'guard');
    const ys = [];
    for (let k = 0; k < CH_YELLOW - CH_YELLOW_IN; k++) { const p = chOutSpot(ys, 1.2, 14); if (!p) continue; ys.push(p); chPut(p[0], p[1], square(p[0], p[1]), 'guard'); }
    for (let t = 0; t < 40000 && w < CH_WHITE; t++) {   // 남은 하양은 바깥 맵 전체에
      const x = rand(MM.x0 + 3, MM.x1 - 3), z = rand(MM.z0 + 3, MM.z1 - 3);
      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null) || Math.hypot(x - me.foot.x, z - me.foot.z) < 14) continue;
      if (bodies.some((b) => Math.hypot(b.foot.x - x, b.foot.z - z) < 1.2)) continue;
      chPut(x, z, square(x, z), ''); w++;
    }
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
      for (const b of bodies) if (b.kind === 'citizen' && !b.met) {
        const cx = col(b.foot.x), cz = row(b.foot.z); let hot = false;
        for (let dz = -1; dz <= 1 && !hot; dz++) for (let dx = -1; dx <= 1; dx++) { const X = cx + dx, Z = cz + dz; if (X >= 0 && X < CH_GW && Z >= 0 && Z < CH_GH && chHot[Z * CH_GW + X]) { hot = true; break; } }
        if (hot && (near(b, me) || zombies.some((z) => near(b, z)))) b.met = true;
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
  ("citizen: 0xffcf33, guard: 0xff8c1a,", "citizen: CHAPTER ? 0xf2f2f2 : 0xffcf33, guard: CHAPTER ? 0xffcf33 : 0xff8c1a, attacker: CHAPTER ? 0xff8c1a : 0xc62828,"),   # c32: 강한 인간 = 노랑
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
  ("    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;", "    if (CHAPTER) { me.foot.set(CH_MAP.start[0], 0, CH_MAP.start[1]); me.space = null; me.hp = me.maxHp; chPopulate(); return; }   // c1: 남서쪽 큰 구역 아래 대로에서 시작 · c11: 인간 200명\n    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;"),
  ("      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;", "      if (B.sign) { B.sign.visible = !B.open; const tx = CH_TEX[B.done ? 'x' : B.type]; if (B.sign.material.map !== tx) { B.sign.material.map = tx; B.sign.material.needsUpdate = true; } }   // c1: 지붕 아이콘 — 들어가면 사라지고, 잠식하면 X\n      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;"),
  ("    for (const B of buildings) if (!B.station) B.found = false;", "    for (const B of buildings) if (!B.station) { B.found = false; B.done = false; }\n    if (CHAPTER) for (const P of CH_MAP.passPts) P.found = false;"),
  ("  const starsEl = document.getElementById('stars');", "  const starsEl = document.getElementById('stars');\n  if (CHAPTER) { const v = document.getElementById('ver'); v.style.setProperty('display', 'block', 'important'); v.style.top = 'auto'; v.style.bottom = 'calc(2px + env(safe-area-inset-bottom, 0px))'; v.style.left = '50%'; v.style.transform = 'translateX(-50%)';   /* c40: 레벨·경보는 테스트맵처럼 보이고, 버전 글자는 아래 가운데로 */ v.style.fontSize = '10px'; v.style.opacity = '0.55'; }   // c1: 맵만 보는 판 — 경보·레벨 표시는 가린다. c10: 왼쪽 위에 버전 글자 (새 버전이 떴는지 보려고)"),
  ("    for (const b of bodies) if (!b.fixed) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게", "    for (const b of bodies) if (!b.fixed && !b.sleep) wallCollide(b);   // 벽은 마지막에 — 서로 밀다가 벽을 넘지 않게\n    if (CHAPTER) for (const b of bodies) if (!b.fixed && !b.sleep) riverCollide(b);   // c3: 강"),
  ("  for (const [ax, az, bx, bz] of walls) flat(", "  for (const [ax, az, bx, bz] of buildings.flatMap((B) => (B.type === 'hill' ? [] : B.walls))) flat("),   # c2: 산은 벽 선을 안 그린다
  ("|| cand[Math.floor(Math.random() * cand.length)];   /* v431", "|| cand[B.sideK !== undefined ? B.sideK % cand.length : Math.floor(Math.random() * cand.length)];   /* c1: 챕터 맵은 쪽문 자리도 고정 */   /* v431"),
  ("bodies, spawn, fleeDir, step: stepWorld };", "bodies, spawn, fleeDir, step: stepWorld, buildings, explored, ch: CHAPTER ? CH_MAP : null, zombify: makeZombie, slotOf, route: CHAPTER ? chRoute : null, cf: () => ({ D: cfD, W: cfW, H: cfH, block: cfBlock, ready: cfReady, runs: cfRuns, dist: cfDist }), get armyK() { return armyK; } };"),
]
from loot_patch import LOOT_R, ITEM_R, FX_R, LVUP_R, STAR_R, XP_R, AWAKE_R, SLOT_R, AWK_TXT_R, AWK_UI_R, AWK_RING_R, RANK_R, VIG_R, STICK_R, COPKB_R   # c19: 금고와 아이템 · c21: 아이템 수치 · c24: 파편 · c25: 레벨업 · c26: 별 · c28: 경험치 · c29: 각성 주사
R += LOOT_R + ITEM_R + FX_R + LVUP_R + STAR_R + XP_R + AWAKE_R + SLOT_R + AWK_TXT_R + AWK_UI_R + AWK_RING_R + RANK_R + VIG_R + STICK_R + COPKB_R
for e in R:
    a, b, n = (e + (1,))[:3]
    assert s.count(a) == n, (s.count(a), n, a[:70])
    s = s.replace(a, b)
OUT.parent.mkdir(exist_ok=True); OUT.write_text(s, encoding='utf8')
import re
pathlib.Path('c.mjs').write_text(re.findall(r'<script type="module">(.*?)</script>', s, re.S)[-1], encoding='utf8')
print('wrote', OUT, len(s))
