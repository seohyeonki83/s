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
    const col = type === 'x' ? '#4a4a52' : CH_DEF[type].col, ink = type === 'hospital' ? '#e02b2b' : '#ffffff';
    rr(6, 6, 116, 116, 26); g.fillStyle = 'rgba(0, 0, 0, 0.88)'; g.fill();
    rr(14, 14, 100, 100, 19); g.fillStyle = col; g.fill();
    g.fillStyle = g.strokeStyle = ink; g.lineCap = 'round'; g.lineJoin = 'round';
    const text = (t, px, y) => { g.font = `900 ${px}px system-ui, -apple-system, "Segoe UI", sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(t, 64, y || 68); };
    const star = (cx, cy, R) => { g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? R * 0.42 : R; g[i ? 'lineTo' : 'moveTo'](cx + Math.cos(a) * r, cy + Math.sin(a) * r); } g.closePath(); g.fill(); };
    if (type === 'bank') text('₩', 78);
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
      g.lineWidth = 8; g.strokeRect(32, 34, 64, 60); g.beginPath(); g.moveTo(32, 34); g.lineTo(96, 94); g.moveTo(96, 34); g.lineTo(32, 94); g.stroke();
    } else if (type === 'x') { g.lineWidth = 17; g.beginPath(); g.moveTo(40, 40); g.lineTo(88, 88); g.moveTo(88, 40); g.lineTo(40, 88); g.stroke(); }   // 잠식한 건물
    return c;
  }
  const CH_ICON = {}, CH_TEX = {};
  const CH_HOUSE_ROOF = [0x26231f, 0x2a2622, 0x22252a, 0x2c241f, 0x25282b, 0x302a24, 0x1f2226];   // 집 지붕은 조금씩 다르게
  if (CHAPTER) {
    for (const k of [...Object.keys(CH_DEF), 'x']) { CH_ICON[k] = chIcon(k); CH_TEX[k] = new THREE.CanvasTexture(CH_ICON[k]); CH_TEX[k].colorSpace = THREE.SRGBColorSpace; }
    const roadMat = flatMat(0x858585);
    for (const [x0, z0, x1, z1] of CH_MAP.roads) flat(x1 - x0, z1 - z0, (x0 + x1) / 2, (z0 + z1) / 2, roadMat, -0.9);   // 대로 — 어둠 밑에 깔린다
    buildings.forEach((B, i) => {
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
  function chLayer(W, H, X, Z, sx, sz, ground, road, house, other) {
    const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
    g.fillStyle = ground; g.fillRect(0, 0, W, H);
    g.fillStyle = road; for (const [x0, z0, x1, z1] of CH_MAP.roads) g.fillRect(X(x0), Z(z0), (x1 - x0) * sx, (z1 - z0) * sz);
    for (const B of buildings) { g.fillStyle = B.type === 'house' ? house : other; g.fillRect(X(B.x0), Z(B.z0), (B.x1 - B.x0) * sx, (B.z1 - B.z0) * sz); }
    return c;
  }
  function chMinimap(eyes, W, H, X, Z, sx, sz) {
    if (!chDim) {
      chDim = chLayer(W, H, X, Z, sx, sz, '#303036', '#27272c', '#141417', '#1b1b20');     // 안개 속
      chLit = chLayer(W, H, X, Z, sx, sz, '#9c9ca4', '#85858d', '#3a3a42', '#4c4c56');     // 지금 보이는 곳
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
    const sz2 = 10.5 * mmDpr;
    for (const B of buildings) {
      if (B.type === 'house') continue;                                  // 집은 표시 없음
      if (!B.found) {                                                    // 건물 자리를 한 칸이라도 밝혔으면 그때부터 표시
        const cx0 = Math.max(0, Math.floor((B.x0 - MM.x0) / MM_CELL)), cx1 = Math.min(mmW - 1, Math.floor((B.x1 - MM.x0) / MM_CELL));
        const cz0 = Math.max(0, Math.floor((B.z0 - MM.z0) / MM_CELL)), cz1 = Math.min(mmH - 1, Math.floor((B.z1 - MM.z0) / MM_CELL));
        for (let cz = cz0; cz <= cz1 && !B.found; cz++) for (let cx = cx0; cx <= cx1; cx++) if (explored[cz * mmW + cx]) { B.found = true; break; }
      }
      if (B.found) g.drawImage(CH_ICON[B.done ? 'x' : B.type], X((B.x0 + B.x1) / 2) - sz2 / 2, Z((B.z0 + B.z1) / 2) - sz2 / 2, sz2, sz2);
    }
    const r = 2.4 * mmDpr;                                                // 나 = 빨간 점
    g.beginPath(); g.arc(X(me.foot.x), Z(me.foot.z), r, 0, Math.PI * 2);
    g.fillStyle = '#ff3b30'; g.fill(); g.lineWidth = 1 * mmDpr; g.strokeStyle = 'rgba(255, 255, 255, 0.9)'; g.stroke();
  }
'''
R = [
  ('<title>러닝데드 이동 테스트</title>', '<title>러닝데드 챕터</title>'),
  ('<div id="ver">v589</div>', f'<div id="ver">챕터 {VER}</div>'),
  ("  const TEST_MAP = CAR_TEST || false;", "  const CHAPTER = true;   // 챕터 줄기 (c1): 구역 4개짜리 맵, 지금은 건물만 — 사람·경찰·금고 없음\n  const TEST_MAP = CAR_TEST || CHAPTER;"),
  ("  const BUILDINGS = TEST_MAP ? TEST_BLDGS : ", "  const CH_MAP = " + MAP + ";   // 생성기(씨앗 7)가 만든 고정 맵 — 건물 97채 (랜드마크 9 · 창고 8 · 집 80)\n  const BUILDINGS = CHAPTER ? CH_MAP.b : TEST_MAP ? TEST_BLDGS : "),
  ("local: s.local, block: s.block };", "local: s.local, block: s.block, type: s.t || '', zone: s.zone, sideK: s.sideK };"),
  ("  // 잠긴 문 (v239) — 문 자리를 막는 벽 한 토막 + 철문 그림.", ICONS.strip('\n') + "\n  // 잠긴 문 (v239) — 문 자리를 막는 벽 한 토막 + 철문 그림."),
  ("  const MM = TEST_MAP ? {", "  const MM = CHAPTER ? CH_MAP.mm : TEST_MAP ? {"),
  ("  const MM_S = Math.min(128 * 2 / 3 / (MM.x1 - MM.x0), 136 * 2 / 3 / (MM.z1 - MM.z0));", "  const MM_S = Math.min((CHAPTER ? 132 : 128 * 2 / 3) / (MM.x1 - MM.x0), (CHAPTER ? 160 : 136 * 2 / 3) / (MM.z1 - MM.z0));   /* c1: 맵이 3배라 미니맵도 크게 */"),
  ("  function updateMinimap(dt) {                // 0.1초마다", MINIMAP.strip('\n') + "\n  function updateMinimap(dt) {                // 0.1초마다"),
  ("    mmCtx.clearRect(0, 0, W, H);", "    if (CHAPTER) { chMinimap(eyes, W, H, X, Z, sx, sz); return; }\n    mmCtx.clearRect(0, 0, W, H);"),
  ("    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;", "    if (CHAPTER) { me.foot.set(CH_MAP.start[0], 0, CH_MAP.start[1]); me.space = null; me.hp = me.maxHp; return; }   // c1: 남서쪽 큰 구역 아래 대로에서 시작, 아무도 없다\n    me.foot.set((MM.x0 + MM.x1) / 2, 0, MM.z1 - 6); me.space = null;"),
  ("      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;", "      if (B.sign) { B.sign.visible = !B.open; const tx = CH_TEX[B.done ? 'x' : B.type]; if (B.sign.material.map !== tx) { B.sign.material.map = tx; B.sign.material.needsUpdate = true; } }   // c1: 지붕 아이콘 — 들어가면 사라지고, 잠식하면 X\n      if (B.qm) B.qm.visible = !B.open && !!B.safe && !B.safe.dead && !B.safe.hidden;"),
  ("    for (const B of buildings) if (!B.station) B.found = false;", "    for (const B of buildings) if (!B.station) { B.found = false; B.done = false; }"),
  ("  const starsEl = document.getElementById('stars');", "  const starsEl = document.getElementById('stars');\n  if (CHAPTER) { starsEl.style.display = 'none'; document.getElementById('lvbox').style.display = 'none'; }   // c1: 맵만 보는 판 — 경보·레벨 표시는 가린다"),
  ("|| cand[Math.floor(Math.random() * cand.length)];   /* v431", "|| cand[B.sideK !== undefined ? B.sideK % cand.length : Math.floor(Math.random() * cand.length)];   /* c1: 챕터 맵은 쪽문 자리도 고정 */   /* v431"),
  ("bodies, spawn, fleeDir, step: stepWorld };", "bodies, spawn, fleeDir, step: stepWorld, buildings, explored };"),
]
for a, b in R:
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
OUT.parent.mkdir(exist_ok=True); OUT.write_text(s, encoding='utf8')
import re
pathlib.Path('c.mjs').write_text(re.findall(r'<script type="module">(.*?)</script>', s, re.S)[-1], encoding='utf8')
print('wrote', OUT, len(s))
