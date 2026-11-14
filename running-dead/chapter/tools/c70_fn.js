  // ── c70: 건물 안 사물 — 본게임(튜토리얼)의 책상·의자(둥근 몸)와 큰 탁자(네모)를 가져와 종류를 늘렸다 ──
  //   작은 것 = 둥근 몸: 금고처럼 때릴 수 있지만 고정이 아니다 — 밀린다 (미는 힘이 작을수록 잘 밀린다. 책상·의자 = 좀비의 1/3).
  //   큰 것 = 네모: 서 있는 차처럼 좀비가 밀고 미는 자리에 따라 돈다. 사람은 못 밀고 돌아간다. 큰 탁자 = 경찰차 체력·무게의 1/3.
  //   공격은 맨 마지막 순위 — 때릴 게 정말 없을 때, 이미 근접 거리 안에 있는 것만 (때리려고 다가가지 않는다). 길을 막고 있으면(1.25초) 그것부터.
  //   부서지면 먼지 + 조각. 보관함(박스·상자·책상·옷장·사물함·캐비닛·냉장고·팔레트)은 50번에 한 번 하트 — 내가 닿으면 바로 최대 체력의 절반이 찬다.
  const CH_BITS = { wood: [0x8a5a30, 0x6b4426, 0x9c6a3c, 0x4a2f18], steel: [0x4a4f5c, 0x6c7386, 0x353944, 0x9aa3ad], card: [0xb98a54, 0xd9b77c, 0x8f6a3e, 0xe6cfa0], white: [0xf0f0ee, 0xc9ccd1, 0x8e949c, 0x6fb3e0],
    red: [0xd42a1e, 0x8f1c14, 0x2b2b2b, 0xf2c14e], green: [0x4c7a3a, 0xa8683a, 0x2f4d24, 0x6fa34f], olive: [0x5d6b3a, 0x3d4726, 0x8a8f5c, 0x2b2b2b], cloth: [0x7a4a36, 0xa9744f, 0x4a2f18, 0xd9c9a8], goods: [0xe2c84a, 0xd42a1e, 0x3f7fd9, 0x4fa35a, 0x9aa3ad] };
  const chTexOf = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.lineJoin = 'round'; draw(g, w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
  const chBx = (g, x, y, w, h, fill) => { g.lineWidth = 7; g.strokeStyle = 'rgba(0, 0, 0, 0.85)'; g.strokeRect(x, y, w, h); g.fillStyle = fill; g.fillRect(x, y, w, h); };
  const chFl = (g, x, y, w, h, fill) => { g.fillStyle = fill; g.fillRect(x, y, w, h); };
  const chDot = (g, x, y, r, fill) => { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fillStyle = fill; g.fill(); g.lineWidth = 6; g.strokeStyle = 'rgba(0, 0, 0, 0.85)'; g.stroke(); };
  // 둥근 몸 — r = 부딪힘 반지름, w·h = 그림 크기(칸), hits = 체력(내 기본 공격 몇 대), f = 미는 힘(좀비 = 1), store = 보관함
  const CH_PROP = {
    chair:  { r: 0.34, w: 0.72, h: 0.96, hits: 1.5, f: 1 / 3, bits: 'steel', px: [96, 128], draw: (g, w, h) => { chBx(g, 16, 10, 16, h - 18, '#4a4f5c'); chBx(g, w - 30, 70, 14, h - 78, '#4a4f5c'); chBx(g, 16, 58, w - 30, 18, '#6c7386'); } },
    desk:   { r: 0.6, w: 1.5, h: 1.0, hits: 3, f: 1 / 3, bits: 'wood', store: true, px: [192, 128], draw: (g, w, h) => { chBx(g, 26, 52, 18, h - 60, '#6b4426'); chBx(g, w - 44, 52, 18, h - 60, '#6b4426'); chBx(g, 8, 14, w - 16, 40, '#9a6638'); } },
    pc:     { r: 0.6, w: 1.5, h: 1.3, hits: 3, f: 1 / 3, bits: 'wood', store: true, px: [192, 166], draw: (g, w, h) => { chBx(g, 26, 98, 18, h - 106, '#6b4426'); chBx(g, w - 44, 98, 18, h - 106, '#6b4426'); chFl(g, 92, 60, 8, 20, '#3a3f47'); chBx(g, 60, 10, 72, 50, '#1d2430'); chFl(g, 66, 16, 60, 38, '#4fb3ff'); chBx(g, 8, 76, w - 16, 26, '#9a6638'); } },
    box:    { r: 0.4, w: 0.85, h: 0.75, hits: 1.5, f: 1 / 4, bits: 'card', store: true, px: [108, 96], draw: (g, w, h) => { chBx(g, 8, 22, w - 16, h - 30, '#b98a54'); chFl(g, 8, 22, w - 16, 9, '#caa066'); chFl(g, w / 2 - 6, 22, 12, h - 30, '#e0c891'); } },
    crate:  { r: 0.48, w: 1.0, h: 0.85, hits: 3, f: 1 / 2, bits: 'wood', store: true, px: [128, 108], draw: (g, w, h) => { chBx(g, 8, 12, w - 16, h - 20, '#9c6a3c'); g.strokeStyle = 'rgba(60, 35, 15, 0.8)'; g.lineWidth = 7; g.beginPath(); g.moveTo(14, 18); g.lineTo(w - 14, h - 14); g.moveTo(w - 14, 18); g.lineTo(14, h - 14); g.stroke(); chFl(g, 8, 12, w - 16, 10, '#7a4f28'); chFl(g, 8, h - 18, w - 16, 10, '#7a4f28'); } },
    ammo:   { r: 0.48, w: 1.05, h: 0.7, hits: 3, f: 1 / 2, bits: 'olive', store: true, px: [134, 90], draw: (g, w, h) => { chBx(g, 8, 14, w - 16, h - 22, '#5d6b3a'); chFl(g, 8, 40, w - 16, 10, '#e2c84a'); chFl(g, 18, 24, 18, 6, '#22251a'); chFl(g, w - 36, 24, 18, 6, '#22251a'); } },
    drum:   { r: 0.4, w: 0.78, h: 1.05, hits: 3, f: 1 / 2, bits: 'steel', px: [100, 134], draw: (g, w, h) => { chBx(g, 12, 10, w - 24, h - 18, '#2f6fb5'); chFl(g, 12, 42, w - 24, 7, '#1f4f85'); chFl(g, 12, 88, w - 24, 7, '#1f4f85'); chFl(g, 20, 16, 12, h - 30, 'rgba(255, 255, 255, 0.18)'); } },
    plant:  { r: 0.3, w: 0.7, h: 1.1, hits: 1, f: 1 / 4, bits: 'green', px: [90, 140], draw: (g, w, h) => { chDot(g, 45, 52, 34, '#3f8a3f'); chDot(g, 30, 44, 12, '#57a657'); chDot(g, 58, 60, 10, '#57a657'); chBx(g, 26, 92, 38, 40, '#a8683a'); } },
    wardrobe: { r: 0.55, w: 1.2, h: 1.9, hits: 4, f: 1, bits: 'wood', store: true, px: [152, 240], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#7a4f28'); chBx(g, 18, 18, 54, h - 36, '#9a6638'); chBx(g, 80, 18, 54, h - 36, '#9a6638'); chFl(g, 62, 114, 6, 16, '#e2c84a'); chFl(g, 84, 114, 6, 16, '#e2c84a'); } },
    locker: { r: 0.42, w: 0.85, h: 1.85, hits: 4, f: 1, bits: 'steel', store: true, px: [108, 236], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#5a6b7d'); for (const y of [26, 38, 50]) chFl(g, 26, y, w - 52, 5, '#2f3944'); chFl(g, w - 34, 112, 8, 26, '#c9ccd1'); chFl(g, 8, h - 30, w - 16, 6, '#42505e'); } },
    cabinet: { r: 0.45, w: 0.9, h: 1.3, hits: 3, f: 2 / 3, bits: 'steel', store: true, px: [116, 166], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#8e949c'); for (let i = 0; i < 3; i++) { chBx(g, 16, 16 + 47 * i, w - 32, 38, '#a9afb7'); chFl(g, w / 2 - 12, 30 + 47 * i, 24, 6, '#3a3f47'); } } },
    fridge: { r: 0.48, w: 0.95, h: 1.8, hits: 4, f: 1.2, bits: 'white', store: true, px: [120, 230], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#eef0f2'); chFl(g, 8, 84, w - 16, 5, '#b9bec4'); chFl(g, w - 28, 40, 6, 30, '#8e949c'); chFl(g, w - 28, 108, 6, 54, '#8e949c'); } },
    tv:     { r: 0.45, w: 1.2, h: 1.05, hits: 1.5, f: 1 / 3, bits: 'steel', px: [152, 134], draw: (g, w, h) => { chBx(g, 20, 90, w - 40, h - 98, '#6b4426'); chBx(g, 10, 8, w - 20, 76, '#15181d'); chFl(g, 18, 14, 62, 30, '#2d3a4d'); } },
    vending: { r: 0.55, w: 1.15, h: 1.9, hits: 6, f: 2.5, bits: 'red', px: [146, 242], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#c8281d'); chBx(g, 18, 20, 80, 130, '#1d2430'); for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) chFl(g, 24 + c * 19, 28 + r * 30, 13, 22, ['#e2c84a', '#3f7fd9', '#4fa35a', '#f2f2ee'][(r + c) % 4]); chFl(g, 108, 60, 16, 40, '#22262c'); chBx(g, 18, 172, w - 36, 34, '#22262c'); } },
    atm:    { r: 0.48, w: 0.95, h: 1.6, hits: 5, f: 2, bits: 'steel', px: [120, 204], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#39424e'); chBx(g, 22, 26, w - 44, 52, '#4fb3ff'); chFl(g, 34, 98, w - 68, 34, '#c9ccd1'); chFl(g, 30, 142, w - 60, 5, '#0d0f12'); chFl(g, 8, 154, w - 16, 10, '#3fbf6f'); } },
    iv:     { r: 0.22, w: 0.55, h: 1.7, hits: 1, f: 1 / 5, bits: 'white', px: [70, 218], draw: (g, w, h) => { chFl(g, 32, 30, 6, 172, '#b9bec4'); chFl(g, 10, 200, 50, 8, '#8e949c'); chFl(g, 14, 30, 42, 5, '#b9bec4'); chBx(g, 8, 36, 26, 44, '#dfeaf2'); chFl(g, 12, 58, 18, 18, '#9fd3f0'); } },
    cart:   { r: 0.4, w: 0.9, h: 0.9, hits: 1.5, f: 1 / 5, bits: 'steel', px: [116, 116], draw: (g, w, h) => { chBx(g, 16, 24, 82, 50, '#b9bec4'); g.strokeStyle = 'rgba(0, 0, 0, 0.45)'; g.lineWidth = 3; for (let x = 30; x < 96; x += 14) { g.beginPath(); g.moveTo(x, 26); g.lineTo(x, 72); g.stroke(); } chFl(g, 4, 16, 26, 7, '#d42a1e'); chFl(g, 26, 74, 6, 18, '#8e949c'); chFl(g, 84, 74, 6, 18, '#8e949c'); chDot(g, 30, 100, 9, '#2b2b2b'); chDot(g, 86, 100, 9, '#2b2b2b'); } },
    exting: { r: 0.22, w: 0.45, h: 0.85, hits: 1, f: 1 / 5, bits: 'red', px: [58, 108], draw: (g, w, h) => { chFl(g, 22, 8, 14, 18, '#2b2b2b'); chFl(g, 34, 14, 16, 5, '#2b2b2b'); chBx(g, 14, 26, 30, h - 34, '#d42a1e'); chFl(g, 18, 48, 22, 14, '#f2f2ee'); } },
    hose:   { r: 0.48, w: 0.95, h: 1.05, hits: 3, f: 2 / 3, bits: 'red', px: [122, 134], draw: (g, w, h) => { chBx(g, 8, 8, w - 16, h - 16, '#b3261c'); chDot(g, w / 2, h / 2, 38, '#e2c84a'); chDot(g, w / 2, h / 2, 17, '#8f1c14'); } },
    sandbag: { r: 0.34, w: 0.65, h: 1.8, hits: 4, f: 1 / 2, bits: 'cloth', px: [84, 230], draw: (g, w, h) => { chFl(g, 39, 0, 6, 42, '#8e949c'); chBx(g, 14, 40, w - 28, h - 60, '#7a4a36'); chFl(g, 14, 70, w - 28, 8, '#4a2f18'); chFl(g, 14, h - 60, w - 28, 8, '#4a2f18'); } },
    rack:   { r: 0.55, w: 1.3, h: 0.95, hits: 4, f: 2, bits: 'steel', px: [166, 122], draw: (g, w, h) => { chFl(g, 16, 18, 10, h - 24, '#353944'); chFl(g, w - 26, 18, 10, h - 24, '#353944'); chBx(g, 10, 30, w - 20, 12, '#4a4f5c'); chBx(g, 10, 78, w - 20, 12, '#4a4f5c'); for (let x = 30; x < w - 40; x += 26) { chBx(g, x, 14, 18, 14, '#1d2026'); chBx(g, x, 62, 18, 14, '#1d2026'); } } },
    radio:  { r: 0.48, w: 1.0, h: 1.25, hits: 3, f: 2 / 3, bits: 'olive', px: [128, 160], draw: (g, w, h) => { chFl(g, 96, 4, 5, 50, '#22251a'); chBx(g, 8, 50, w - 16, h - 58, '#5d6b3a'); chFl(g, 22, 64, 44, 26, '#9fe08a'); chDot(g, 90, 78, 11, '#22251a'); chDot(g, 40, 122, 9, '#22251a'); chDot(g, 72, 122, 9, '#22251a'); chFl(g, 92, 112, 18, 20, '#3d4726'); } },
  };
  for (const P of Object.values(CH_PROP)) { P.geo = new THREE.PlaneGeometry(P.w, P.h); P.tex = chTexOf(P.px[0], P.px[1], P.draw); }
  // 네모 — L·W = 크기(칸), hp·mass = 큰 탁자(경찰차의 1/3)의 몇 배. 위에서 본 그림
  const CH_SLAB = {
    table:  { L: 2.6, W: 1.5, hp: 1, mass: 1, bits: 'wood', px: [250, 144], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#2a1a0e'); chFl(g, 6, 6, w - 12, h - 12, '#8a5a30'); chFl(g, 14, 14, w - 28, h - 28, '#9c6a3c'); g.strokeStyle = 'rgba(60, 35, 15, 0.35)'; g.lineWidth = 3; for (let y = 28; y < h - 20; y += 16) { g.beginPath(); g.moveTo(18, y); g.lineTo(w - 18, y); g.stroke(); } } },
    bed:    { L: 2.0, W: 1.1, hp: 1, mass: 1, bits: 'white', px: [192, 106], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#2a1a0e'); chFl(g, 5, 5, w - 10, h - 10, '#6b4426'); chFl(g, 12, 10, w - 24, h - 20, '#f0f0ee'); chFl(g, 18, 22, 34, h - 44, '#ffffff'); chFl(g, 70, 10, w - 82, h - 20, '#4f7fbf'); chFl(g, 70, 10, 8, h - 20, '#6f9ad6'); } },
    hbed:   { L: 2.0, W: 1.0, hp: 1, mass: 1, bits: 'white', px: [192, 96], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#22262c'); chFl(g, 5, 5, w - 10, h - 10, '#b9bec4'); chFl(g, 12, 10, w - 24, h - 20, '#ffffff'); chFl(g, 18, 22, 30, h - 44, '#e3ebf2'); chFl(g, 70, 10, w - 82, h - 20, '#8fc3e8'); chFl(g, 5, 5, 6, h - 10, '#8e949c'); chFl(g, w - 11, 5, 6, h - 10, '#8e949c'); } },
    sofa:   { L: 1.9, W: 0.85, hp: 0.8, mass: 0.8, bits: 'cloth', px: [182, 82], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#1c2230'); chFl(g, 5, 5, w - 10, h - 10, '#5a6b8c'); chFl(g, 5, 5, w - 10, 20, '#465572'); chFl(g, 5, 5, 18, h - 10, '#465572'); chFl(g, w - 23, 5, 18, h - 10, '#465572'); chFl(g, w / 2 - 2, 27, 4, h - 34, '#3b4862'); } },
    bookshelf: { L: 2.4, W: 0.6, hp: 1.2, mass: 1.5, bits: 'wood', px: [230, 58], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#2a1a0e'); chFl(g, 5, 5, w - 10, h - 10, '#6b4426'); const C = ['#c94a3a', '#3f7fd9', '#e0b23c', '#4fa35a', '#8d6fc4', '#e9e9e4', '#d97a1a']; for (let x = 10, i = 0; x < w - 18; i++) { const bw = 7 + (i * 5) % 7; chFl(g, x, 11, bw, h - 22, C[(i * 3) % C.length]); x += bw + 2; } } },
    shelf:  { L: 2.6, W: 0.75, hp: 1, mass: 1.3, bits: 'goods', px: [250, 72], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#22262c'); chFl(g, 5, 5, w - 10, h - 10, '#9aa3ad'); const C = ['#e2c84a', '#d42a1e', '#3f7fd9', '#4fa35a', '#f2f2ee', '#ff6a13']; for (let x = 11, i = 0; x < w - 22; x += 19, i++) { chFl(g, x, 10, 15, 22, C[i % C.length]); chFl(g, x, 40, 15, 22, C[(i + 3) % C.length]); } chFl(g, 5, 34, w - 10, 4, '#6c7386'); } },
    counter: { L: 2.4, W: 0.8, hp: 1.3, mass: 1.8, bits: 'wood', px: [230, 77], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#2a1a0e'); chFl(g, 5, 5, w - 10, h - 10, '#b59a66'); chFl(g, 11, 11, w - 22, h - 22, '#e6d6b0'); chFl(g, 146, 16, 50, 44, '#22262c'); chFl(g, 150, 20, 42, 36, '#39424e'); chFl(g, 156, 26, 30, 14, '#4fb3ff'); } },
    treadmill: { L: 1.7, W: 0.75, hp: 1, mass: 1.2, bits: 'steel', px: [163, 72], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#0d0f12'); chFl(g, 5, 10, 120, h - 20, '#1d2026'); for (let x = 14; x < 120; x += 16) chFl(g, x, 12, 3, h - 24, '#2f343c'); chFl(g, 5, 5, 122, 5, '#6c7386'); chFl(g, 5, h - 10, 122, 5, '#6c7386'); chFl(g, 128, 5, 30, h - 10, '#4a4f5c'); chFl(g, 134, 22, 18, 28, '#ff6a13'); } },
    bench:  { L: 1.8, W: 1.0, hp: 1, mass: 1.2, bits: 'steel', px: [173, 96], draw: (g, w, h) => { chFl(g, 26, 30, 126, 36, '#0d0f12'); chFl(g, 30, 34, 118, 28, '#2b2b2b'); chFl(g, 58, 2, 14, h - 4, '#0d0f12'); chFl(g, 61, 5, 8, h - 10, '#c9ccd1'); chFl(g, 50, 2, 30, 20, '#0d0f12'); chFl(g, 53, 5, 24, 14, '#22262c'); chFl(g, 50, h - 22, 30, 20, '#0d0f12'); chFl(g, 53, h - 19, 24, 14, '#22262c'); } },
    pallet: { L: 1.3, W: 1.3, hp: 0.8, mass: 1.5, bits: 'card', store: true, px: [125, 125], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#2a1a0e'); chFl(g, 5, 5, w - 10, h - 10, '#9c6a3c'); for (let y = 22; y < h - 10; y += 24) chFl(g, 5, y, w - 10, 4, '#6b4426'); for (const [x, y, c] of [[14, 14, '#b98a54'], [66, 14, '#caa066'], [14, 66, '#caa066'], [66, 66, '#b98a54']]) { chFl(g, x - 2, y - 2, 48, 48, '#2a1a0e'); chFl(g, x, y, 44, 44, c); chFl(g, x + 18, y, 8, 44, '#e0c891'); } } },
    cooler: { L: 2.4, W: 0.7, hp: 1.2, mass: 1.8, bits: 'white', px: [230, 67], draw: (g, w, h) => { chFl(g, 0, 0, w, h, '#22262c'); chFl(g, 5, 5, w - 10, h - 10, '#e8eef4'); chFl(g, 11, 10, w - 22, 30, '#9fd3f0'); const C = ['#d42a1e', '#4fa35a', '#e2c84a', '#3f7fd9']; for (let x = 16, i = 0; x < w - 26; x += 17, i++) chFl(g, x, 16, 11, 18, C[i % 4]); chFl(g, 11, 45, w - 22, 12, '#c9ccd1'); } },
  };
  for (const S of Object.values(CH_SLAB)) S.tex = chTexOf(S.px[0], S.px[1], S.draw);
  const CH_SLAB_MASS = CAR_MASS * 2 / 3 / 3, CH_SLAB_HP = MY_DAMAGE * 9.5 / 3;   // 큰 탁자 = 경찰차의 1/3 (본게임 그대로)
  const chProps = [], chSlabs = [];
  let chFurnT = 0, chFurnN = {};
  function chAddProp(type, x, z) {             // 본게임 addProp 그대로 — 종류만 늘렸다
    const P = CH_PROP[type], b = addBody('safe', x, z);
    b.mesh.material.dispose();
    b.mesh.geometry = P.geo; b.mesh.material = new THREE.MeshBasicMaterial({ map: P.tex, color: 0xffffff, transparent: true, depthTest: false, depthWrite: false });
    b.prop = type; b.fixed = false; b.force = P.f; b.r = P.r; b.halfH = P.h / 2;
    b.hp = b.maxHp = MY_DAMAGE * P.hits; b.sleep = true;
    addHpBar(b, hpFoeMat);
    chProps.push(b); chFurnN[type] = (chFurnN[type] || 0) + 1;
    return b;
  }
  function chAddSlab(type, x, z, h, S) {       // 본게임 addTable 그대로 — 방(S) 안에만 있다
    const D = CH_SLAB[type], m = new THREE.Mesh(new THREE.PlaneGeometry(D.L, D.W).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: D.tex, transparent: true, depthTest: false, depthWrite: false }));
    m.renderOrder = -0.6; m.position.set(x, 0.04, z); m.rotation.y = -h; scene.add(m);   // 지붕(-0.46)·어둠(-0.52) 밑 — 지붕이 덮여 있으면 안 보이고, 시야 밖이면 어둡게 보인다
    const t = { room: S, B: S, x, z, h, L: D.L, W: D.W, m, type, mass: CH_SLAB_MASS * D.mass };
    t.obj = { kind: 'obj', type: 'table', t, B: S, foot: new THREE.Vector3(x, 0, z), hp: CH_SLAB_HP * D.hp, maxHp: CH_SLAB_HP * D.hp, dead: false };
    addHpBar(t.obj, hpFoeMat); objs.push(t.obj);
    chSlabs.push(t); S.fs.push(t); chFurnN[type] = (chFurnN[type] || 0) + 1;
    return t;
  }
  function chSlabClamp(t) {                    // 네모는 그 방 안에만
    const c = Math.abs(Math.cos(t.h)), s = Math.abs(Math.sin(t.h)), ex = t.L / 2 * c + t.W / 2 * s + 0.2, ez = t.L / 2 * s + t.W / 2 * c + 0.2, R = t.room;
    t.x = Math.max(R.x0 + ex, Math.min(R.x1 - ex, t.x)); t.z = Math.max(R.z0 + ez, Math.min(R.z1 - ez, t.z));
  }
  function chSlabCollide() {                   // 본게임 tableCollide — 깨어 있는 건물만, 둘레 칸의 몸만
    for (const B of chFurnSpaces) {
      if (!B.furnOn || !B.fs.length) continue;
      let moved = false;
      for (const t of B.fs) {
        if (t.obj.dead) continue;
        const fx = Math.cos(t.h), fz = Math.sin(t.h), rx = -fz, rz = fx;
        for (const b of chNearBodies(t)) {
          if (b.fixed || b.knockT > 0 || b.sleep || b.space !== B) continue;
          const dx = b.foot.x - t.x, dz = b.foot.z - t.z, hu = t.L / 2 + b.r, hv = t.W / 2 + b.r;
          let u = dx * fx + dz * fz, v = dx * rx + dz * rz;
          if (Math.abs(u) >= hu || Math.abs(v) >= hv) continue;
          const qu = Math.abs(u) - t.L / 2, qv = Math.abs(v) - t.W / 2;
          if (qu > 0 && qv > 0) {                // 모서리 밖 — 모서리 점에서 몸 반지름만큼 (둥근 모서리: 미끄러져 돌아간다)
            const d = Math.hypot(qu, qv); if (d >= b.r) continue;
            const k = b.r / (d || 1e-6); u = (u < 0 ? -1 : 1) * (t.L / 2 + qu * k); v = (v < 0 ? -1 : 1) * (t.W / 2 + qv * k);
          } else if (hu - Math.abs(u) < hv - Math.abs(v)) u = (u < 0 ? -1 : 1) * hu; else v = (v < 0 ? -1 : 1) * hv;
          const ex = t.x + u * fx + v * rx - b.foot.x, ez = t.z + u * fz + v * rz - b.foot.z;
          const f = b === me ? 1 : (b.force || 1) * (b.mut === 'armor' ? 2 / 3 : 1), sh = isZombie(b) ? f / (f + t.mass) : 0;   // 좀비만 민다 — 사람은 돌아간다
          b.foot.x += ex * (1 - sh); b.foot.z += ez * (1 - sh);
          if (!sh) continue;
          t.x -= ex * sh; t.z -= ez * sh;
          const px = b.foot.x - t.x, pz = b.foot.z - t.z, mx = -ex * sh, mz = -ez * sh;
          t.h += (px * mz - pz * mx) / ((t.L * t.L + t.W * t.W) / 12 + px * px + pz * pz);   // 미는 자리에 따라 돈다
          chSlabClamp(t); t.moved = moved = true;
        }
      }
      if (!moved) continue;
      for (let i = 0; i < B.fs.length; i++) for (let j = i + 1; j < B.fs.length; j++) {   // 네모끼리 — 한쪽의 몸통을 원 5개로 보고 다른 쪽 밖으로 반씩 밀어낸다
        const a = B.fs[i], b = B.fs[j];
        if (a.obj.dead || b.obj.dead || (!a.moved && !b.moved) || Math.hypot(a.x - b.x, a.z - b.z) > (a.L + b.L) / 2 + 1) continue;
        for (const [p, q] of [[a, b], [b, a]]) {
          const pfx = Math.cos(p.h), pfz = Math.sin(p.h), qfx = Math.cos(q.h), qfz = Math.sin(q.h), r = p.W / 2;
          for (let k = -2; k <= 2; k++) {
            const cx = p.x + pfx * k * (p.L / 2 - r) / 2, cz = p.z + pfz * k * (p.L / 2 - r) / 2, dx = cx - q.x, dz = cz - q.z;
            let u = dx * qfx + dz * qfz, v = -dx * qfz + dz * qfx; const hu = q.L / 2 + r, hv = q.W / 2 + r;
            if (Math.abs(u) >= hu || Math.abs(v) >= hv) continue;
            if (hu - Math.abs(u) < hv - Math.abs(v)) u = (u < 0 ? -1 : 1) * hu; else v = (v < 0 ? -1 : 1) * hv;
            const ex = (q.x + u * qfx - v * qfz - cx) / 2, ez = (q.z + u * qfz + v * qfx - cz) / 2;
            p.x += ex; p.z += ez; q.x -= ex; q.z -= ez; chSlabClamp(p); chSlabClamp(q); p.moved = q.moved = true;
          }
        }
      }
      for (const t of B.fs) if (t.moved) { t.moved = false; t.obj.foot.set(t.x, 0, t.z); t.m.position.set(t.x, 0.04, t.z); t.m.rotation.y = -t.h; }
      B.navDirty = true;                      // 길 찾기 격자를 다시 칠한다
    }
  }
  const chFurnSpaces = [];
  function chFurnTick(dt) {                    // 0.3초마다 — 좀비가 가까운 건물의 사물만 깨운다 (나머지는 부딪힘 계산을 안 한다)
    if ((chFurnT -= dt) > 0) return;
    chFurnT = 0.3;
    for (const B of chFurnSpaces) { const T = B.parent || B; let on = false;
      for (const z of zombies) if (z.foot.x > T.x0 - 16 && z.foot.x < T.x1 + 16 && z.foot.z > T.z0 - 16 && z.foot.z < T.z1 + 16) { on = true; break; }
      B.furnOn = on; B.fp.length = 0; }
    for (let i = chProps.length - 1; i >= 0; i--) { const p = chProps[i]; if (p.dead) { chProps.splice(i, 1); continue; }
      const S = p.space, T = S && (S.parent || S); p.sleep = !(T ? T.furnOn || (S.furnOn) : zombies.some((z) => Math.hypot(z.foot.x - p.foot.x, z.foot.z - p.foot.z) < 16));
      if (S && S.fp) { S.fp.push(p); if (!S.navDirty && S.nav && (Math.abs(p.foot.x - p.nvx) > 0.1 || Math.abs(p.foot.z - p.nvz) > 0.1)) S.navDirty = true; } }   // 밀린 사물 → 그 방 격자 다시
  }
  function chNearFurn(z) {                     // 본게임 nearProp — 같은 공간 · 근접 거리 안 · 벽에 안 가린 가장 가까운 사물 (둥근 것 + 네모). 때리려고 다가가지 않는다
    const S = z.space; if (!S || !S.fp) return null;
    let best = null, bd = MELEE;
    for (const p of S.fp) { if (p.dead || p.space !== S) continue; const d = Math.hypot(p.foot.x - z.foot.x, p.foot.z - z.foot.z) - p.r; if (d < bd && !blocked(z.foot.x, z.foot.z, p.foot.x, p.foot.z)) { bd = d; best = p; } }
    for (const t of S.fs) { if (t.obj.dead) continue; const d = objGap(t.obj, z) + RADIUS; if (d < bd) { bd = d; best = t.obj; } }
    return best;
  }
  const chHitFurn = (z, f, dt) => { if (f.kind === 'obj') fightObj(z, f, dt); else fight(z, f, dt); };
  function chHeartDrop(x, z, space) {          // 하트 — 닿으면 바로 최대 체력의 절반이 찬다 (한 번 쓰고 사라진다)
    const tex = chTexOf(96, 96, (g) => { g.translate(48, 50); g.beginPath(); g.moveTo(0, 30); g.bezierCurveTo(-52, -6, -30, -46, 0, -18); g.bezierCurveTo(30, -46, 52, -6, 0, 30); g.closePath(); g.fillStyle = '#ff3355'; g.fill(); g.lineWidth = 7; g.strokeStyle = '#5a0a18'; g.stroke(); g.beginPath(); g.arc(-14, -14, 7, 0, Math.PI * 2); g.fillStyle = 'rgba(255, 255, 255, 0.75)'; g.fill(); });
    const p = { kind: 'heart', x, z, space, t: 0 };
    p.s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, depthWrite: false })); p.s.renderOrder = UI - 1; p.s.scale.set(1.2, 1.2, 1); scene.add(p.s);
    pickups.push(p);
    for (let i = 0; i < 10; i++) { const a = i / 10 * Math.PI * 2; puff(x, 0.5, z, 0xff6a8a, 0.4, 1.2, 0.5, Math.cos(a) * 2.5, 0.6, Math.sin(a) * 2.5, 0.85); }
  }
  function chHeartEat() {
    if (!isZombie(me)) return;
    me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.5);
    for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; puff(me.foot.x, 0.8, me.foot.z, i % 2 ? 0xff5577 : 0x6dff9a, 0.5, 1.6, 0.6, Math.cos(a) * 2.2, 1.2, Math.sin(a) * 2.2, 0.9); }
  }
  const CH_HEART_P = 1 / 50;
  function chFurnBreak(x, z, D, space, n, size) {   // 먼지 + 조각 · 보관함이면 50번에 한 번 하트
    dust(x, z, Math.round(n * 0.8), 1.2); debris(x, z, n, CH_BITS[D.bits], size, 5.8);
    if (D.store && Math.random() < CH_HEART_P) chHeartDrop(x, z, space);
  }
  // ── 놓기 ──
  function chFurnPlace() {
    for (const t of chSlabs) { scene.remove(t.m); t.m.geometry.dispose(); t.m.material.dispose(); if (t.obj.hpBar) scene.remove(t.obj.hpBar); }
    chSlabs.length = 0; chProps.length = 0; chFurnSpaces.length = 0; chFurnN = {}; chFurnT = 0;
    for (const B of buildings) { B.fs = []; B.fp = []; B.nav = null; B.navDirty = false; B.furnOn = false; if (B.type !== 'hill') chFurnSpaces.push(B); }
    for (const B of chFurnSpaces) chFurnOne(B);
    for (const p of chProps) if (p.space && p.space.fp) p.space.fp.push(p);
    for (const c of bodies) {                  // 사물 자리에 겹친 사람은 그 방 안 빈자리로
      if (c.kind !== 'citizen' || !c.space || !c.space.fs) continue;
      const N = chNavOf(c.space); if (!N) continue;
      const k0 = chNavCell(N, c.foot.x, c.foot.z);
      if (!N.cost[k0] && N.comp[k0] === N.main) {   // 빈 칸이고 큰 덩어리(문과 이어진 바닥)면 그대로 — 옆 칸이 막혀 있으면 칸 한가운데로만 옮긴다 (사물에 살짝 겹쳐 서지 않게)
        const i = k0 % N.w, j = (k0 - i) / N.w; let tight = false;
        for (let d = 0; d < 8 && !tight; d++) { const ni = i + CH_NAV_DI[d], nj = j + CH_NAV_DJ[d]; if (ni >= 1 && nj >= 1 && ni < N.w - 1 && nj < N.h - 1 && N.cost[nj * N.w + ni]) tight = true; }
        if (tight) { c.foot.x = N.x0 + (i + 0.5) * CH_NAV_CS; c.foot.z = N.z0 + (j + 0.5) * CH_NAV_CS; c.px = c.foot.x; c.pz = c.foot.z; }
        continue;
      }
      let k = chNavNear(N, c.foot.x, c.foot.z, 12, N.main);
      for (let t = 0; t < 60 && k < 0; t++) { const q = Math.floor(Math.random() * N.cost.length); if (!N.cost[q] && N.comp[q] === N.main) k = q; }
      if (k >= 0) { c.foot.x = N.x0 + (k % N.w + 0.5) * CH_NAV_CS; c.foot.z = N.z0 + (Math.floor(k / N.w) + 0.5) * CH_NAV_CS; c.px = c.foot.x; c.pz = c.foot.z; }
    }
  }
  function chFurnOne(S) {
    const T = S.parent || S, type = S.type, I = { x0: S.x0 + 0.45, z0: S.z0 + 0.45, x1: S.x1 - 0.45, z1: S.z1 - 0.45 }, W = I.x1 - I.x0, H = I.z1 - I.z0;
    if (W < 1.6 || H < 1.6 || type === 'jail') return;
    const keep = [], occ = [];
    const doorKeep = (L, sgn, w) => { const cx = L.cx + L.nx * 0.6 * sgn, cz = L.cz + L.nz * 0.6 * sgn, hw = w / 2 + 0.2, hx = Math.abs(L.tx) * hw + Math.abs(L.nx) * 0.75, hz = Math.abs(L.tz) * hw + Math.abs(L.nz) * 0.75; keep.push([cx - hx, cz - hz, cx + hx, cz + hz]); };   // 문 안쪽 1.35칸
    for (const o of objs) { if (o.type !== 'door' || o.off) continue; if (o.B === S) doorKeep(o.L, -1, o.L.w || DOOR); else if (o.L.out === S) doorKeep(o.L, 1, o.L.w || DOOR); }
    for (const D of S.doors || []) doorKeep(D, -1, D.w || DOOR);
    for (const R of S.rooms || []) keep.push([R.x0 - 0.55, R.z0 - 0.55, R.x1 + 0.55, R.z1 + 0.55]);
    const sf = T.safe; if (sf && !sf.dead && (sf.room || T) === S) keep.push([sf.foot.x - sf.r - 0.6, sf.foot.z - sf.r - 0.6, sf.foot.x + sf.r + 0.6, sf.foot.z + sf.r + 0.6]);
    if (S.garage) return chFurnGarage(S, I, keep, occ);
    const F = { S, I, keep, occ };
    const J = { x0: S.x0 + 0.15, z0: S.z0 + 0.15, x1: S.x1 - 0.15, z1: S.z1 - 0.15 };   // 벽에 붙여 놓을 수 있는 한계 (벽 한가운데 선에서 0.15칸)
    const free = (b, aisle) => b[0] >= J.x0 - 1e-6 && b[2] <= J.x1 + 1e-6 && b[1] >= J.z0 - 1e-6 && b[3] <= J.z1 + 1e-6 && !keep.some((k) => chBoxHit(b, k, 0)) && !occ.some((o) => chBoxHit(b, o, aisle));
    const slabBox = (type, x, z, h) => { const D = CH_SLAB[type], hx = (h ? D.W : D.L) / 2, hz = (h ? D.L : D.W) / 2; return [x - hx, z - hz, x + hx, z + hz]; };
    const slab = (type, x, z, h, aisle = 1.1) => { const b = slabBox(type, x, z, h); if (!free(b, aisle)) return null; occ.push(b); return chAddSlab(type, x, z, h ? Math.PI / 2 : 0, S); };
    const prop = (type, x, z, aisle = 0.3) => { const r = CH_PROP[type].r, b = [x - r, z - r, x + r, z + r]; if (!free(b, aisle)) return null; occ.push(b); const p = chAddProp(type, x, z); p.space = S; return p; };
    const SIDES = [['n', 0, -1], ['s', 0, 1], ['w', -1, 0], ['e', 1, 0]];
    const wall = (kind, type, n, aisle) => {    // 벽에 붙여서 — 네모는 긴 변을 벽에 대고
      let done = 0;
      for (let t = 0; t < 40 * n && done < n; t++) {
        const [, nx, nz] = SIDES[Math.floor(Math.random() * 4)], dep = kind === 'slab' ? CH_SLAB[type].W / 2 + 0.24 : CH_PROP[type].r + 0.2, half = (kind === 'slab' ? CH_SLAB[type].L / 2 : CH_PROP[type].r) + 0.2;
        if ((nx ? J.z1 - J.z0 : J.x1 - J.x0) < 2 * half) continue;
        const a = nx ? rand(J.z0 + half, J.z1 - half) : rand(J.x0 + half, J.x1 - half);
        const x = nx ? (nx < 0 ? S.x0 + dep : S.x1 - dep) : a, z = nx ? a : (nz < 0 ? S.z0 + dep : S.z1 - dep);
        if (kind === 'slab' ? slab(type, x, z, nx ? 1 : 0, aisle) : prop(type, x, z, aisle === undefined ? 0.25 : aisle)) done++;
      }
      return done;
    };
    const rows = (type, n, cross, lane) => {   // 가운데에 나란히 — 줄 사이 통로 lane, 줄 안에서는 cross만큼 띄운다. 격자를 이리저리 밀어 보고 가장 많이 들어가는 배치로
      const D = CH_SLAB[type]; let best = [], bh = 0;
      for (let tr = 0; tr < 16 && best.length < n; tr++) {
        const alongX = tr < 11 ? W >= H : W < H, la = D.L + cross, lw = D.W + lane, plan = [];
        const A0 = alongX ? J.x0 : J.z0, A1 = alongX ? J.x1 : J.z1, B0 = alongX ? J.z0 : J.x0, B1 = alongX ? J.z1 : J.x1;
        for (let a = A0 + D.L / 2 + 0.3 + rand(0, la); a <= A1 - D.L / 2 - 0.3; a += la) for (let b = B0 + D.W / 2 + 0.6 + rand(0, lw); b <= B1 - D.W / 2 - 0.6; b += lw) {
          const x = alongX ? a : b, z = alongX ? b : a, bb = slabBox(type, x, z, alongX ? 0 : 1);
          if (free(bb, 1.75)) plan.push([x, z]);
        }
        if (plan.length > best.length) { best = plan; bh = alongX ? 0 : 1; }
      }
      let done = 0; for (const [x, z] of best) { if (done >= n) break; if (slab(type, x, z, bh, 1.1)) done++; }   // 다른 줄·사물과는 두 사람이 비켜 갈 폭(1.75)을 띄우고 고른 자리다
      return done;
    };
    const scatter = (type, n, aisle) => { let done = 0; for (let t = 0; t < 30 * n && done < n; t++) if (prop(type, rand(I.x0 + 0.5, I.x1 - 0.5), rand(I.z0 + 0.5, I.z1 - 0.5), aisle)) done++; return done; };
    const cluster = (types, n) => { for (let t = 0; t < 30; t++) { const cx = rand(I.x0 + 1, I.x1 - 1), cz = rand(I.z0 + 1, I.z1 - 1); let k = 0; for (let i = 0; i < n * 6 && k < n; i++) { const a = Math.random() * 6.283, r = rand(0, 0.5 + 0.35 * n); if (prop(types[Math.floor(Math.random() * types.length)], cx + Math.cos(a) * r, cz + Math.sin(a) * r, 0.06)) k++; } if (k) return k; } return 0; };
    const around = (t, type, n) => {            // 탁자 둘레 의자
      if (!t) return; const D = CH_SLAB[t.type], hz = t.h ? 1 : 0, P = CH_PROP[type];
      const spots = []; const m = Math.max(1, Math.floor(n / 2));
      for (let i = 0; i < m; i++) { const a = (i + 0.5) / m * D.L - D.L / 2, d = D.W / 2 + P.r + 0.12; spots.push([a, d], [a, -d]); }
      if (n > 2 * m - 1) spots.push([D.L / 2 + P.r + 0.12, 0], [-D.L / 2 - P.r - 0.12, 0]);
      for (const [a, d] of spots.slice(0, n)) prop(type, t.x + (hz ? d : a), t.z + (hz ? a : d), 0.02);
    };
    const tableSet = (nChairs) => { for (let t = 0; t < 40; t++) { const h = Math.random() < 0.5 ? 1 : 0, D = CH_SLAB.table, hx = (h ? D.W : D.L) / 2 + 0.9, hz = (h ? D.L : D.W) / 2 + 0.9; if (W < 2 * hx || H < 2 * hz) continue; const tb = slab('table', rand(I.x0 + hx, I.x1 - hx), rand(I.z0 + hz, I.z1 - hz), h, 1.3); if (tb) { tb.h = h ? Math.PI / 2 : 0; around({ x: tb.x, z: tb.z, h, type: 'table' }, 'chair', nChairs); return tb; } } return null; };
    const deskSet = (type = 'desk') => {       // 벽에 책상, 그 앞에 의자
      for (let t = 0; t < 40; t++) { const [, nx, nz] = SIDES[Math.floor(Math.random() * 4)], r = CH_PROP[type].r, a = nx ? rand(J.z0 + r + 0.2, J.z1 - r - 0.2) : rand(J.x0 + r + 0.2, J.x1 - r - 0.2);
        const x = nx ? (nx < 0 ? S.x0 + r + 0.2 : S.x1 - r - 0.2) : a, z = nx ? a : (nz < 0 ? S.z0 + r + 0.2 : S.z1 - r - 0.2), cx = x - nx * (r + 0.42), cz = z - nz * (r + 0.42);
        const cb = [cx - 0.34, cz - 0.34, cx + 0.34, cz + 0.34]; if (!free(cb, 0.25)) continue;
        if (prop(type, x, z, 0.25)) { prop('chair', cx, cz, 0.02); return true; } }
      return false;
    };
    const N = (a, b) => a + Math.floor(Math.random() * (b - a + 1)), P = (p) => Math.random() < p;
    if (S.parent) { if (type === 'room' && !(sf && !sf.dead && sf.room === S)) { if (P(0.5)) { deskSet(P(0.5) ? 'pc' : 'desk'); wall('prop', 'cabinet', 1); } else { cluster(['box', 'crate'], N(2, 3)); wall('prop', 'locker', 1); } } return; }
    switch (type) {
      case 'house': wall('slab', P(0.75) ? 'bed' : 'sofa', 1, 0.7); wall('prop', 'wardrobe', 1); if (P(0.6)) deskSet(); if (P(0.4)) wall('slab', 'sofa', 1, 0.7); if (P(0.45)) wall('prop', 'tv', 1); if (P(0.4)) wall('prop', 'plant', 1); if (P(0.3)) scatter('box', 1); if (P(0.3)) wall('prop', 'fridge', 1); break;
      case 'store': wall('slab', 'pallet', N(1, 2), 0.6); cluster(['box', 'box', 'crate'], N(3, 4)); cluster(['box', 'crate'], N(2, 4)); scatter('drum', N(2, 3)); scatter('crate', N(1, 2)); scatter('box', N(1, 3)); break;
      case 'bank': { const got = rows('counter', 2, 1.75, 2.4); if (got < 2) wall('slab', 'counter', 2 - got, 0.75); } wall('prop', 'atm', 2); wall('prop', 'cabinet', 2); deskSet('pc'); scatter('chair', N(3, 4)); wall('prop', 'plant', 2); break;
      case 'hospital': { const want = N(4, 6), got = rows('hbed', want, 1.75, 1.75); if (got < want) wall('slab', 'hbed', want - got, 0.75); } wall('slab', 'counter', 1, 0.8); scatter('iv', N(2, 4), 0.1); scatter('cart', 2); wall('prop', 'cabinet', 2); scatter('chair', N(2, 3)); break;
      case 'library': { const want = N(5, 7), got = rows('bookshelf', want, 1.75, 1.75); if (got < want) wall('slab', 'bookshelf', want - got, 0.75); } tableSet(4); wall('prop', 'pc', 2); wall('slab', 'counter', 1, 0.8); wall('prop', 'plant', 1); break;
      case 'conv': { const want = N(2, 3), got = rows('shelf', want, 1.75, 1.75); if (got < want) wall('slab', 'shelf', want - got, 0.75); } wall('slab', 'counter', 1, 0.8); wall('slab', 'cooler', N(1, 2), 0.8); wall('prop', 'vending', 1); break;
      case 'mart': { const want = N(6, 8), got = rows('shelf', want, 1.75, 1.75); if (got < want) wall('slab', 'shelf', want - got, 0.75); } wall('slab', 'counter', 2, 0.8); wall('slab', 'cooler', 2, 0.8); scatter('cart', N(3, 4)); cluster(['box'], N(2, 3)); wall('prop', 'vending', 1); break;
      case 'gym': { const w1 = N(3, 4), g1 = rows('treadmill', w1, 1.75, 1.75); if (g1 < w1) wall('slab', 'treadmill', w1 - g1, 0.75); const w2 = N(2, 3), g2 = rows('bench', w2, 1.75, 1.75); if (g2 < w2) wall('slab', 'bench', w2 - g2, 0.75); } wall('prop', 'rack', 2); scatter('sandbag', N(2, 3)); wall('prop', 'locker', 3, 0.02); break;
      case 'fire': wall('prop', 'locker', 4, 0.02); wall('prop', 'hose', 2); tableSet(4); scatter('exting', N(3, 4)); cluster(['crate', 'box'], 2); break;
      case 'army': wall('prop', 'locker', 4, 0.02); cluster(['ammo'], N(3, 4)); cluster(['ammo', 'crate'], N(2, 3)); scatter('drum', N(2, 3)); wall('prop', 'radio', 1); tableSet(4); break;
      case 'police': deskSet('pc'); deskSet(); deskSet(); wall('prop', 'cabinet', 3); wall('prop', 'locker', 2, 0.02); tableSet(6); wall('prop', 'vending', 1); break;
    }
  }
  function chFurnGarage(S, I, keep, occ) {      // 차고 — 박스 몇 개와 드럼통
    const n = 2 + Math.floor(Math.random() * 3);
    for (let i = 0, k = 0; i < 40 && k < n; i++) { const type = ['box', 'box', 'crate', 'drum'][Math.floor(Math.random() * 4)], r = CH_PROP[type].r, x = rand(I.x0 + r, I.x1 - r), z = rand(I.z0 + r, I.z1 - r), b = [x - r, z - r, x + r, z + r];
      if (keep.some((q) => chBoxHit(b, q, 0)) || occ.some((q) => chBoxHit(b, q, 0.1))) continue; occ.push(b); chAddProp(type, x, z).space = S; k++; }
  }
  // ── 건물 안 길 찾기 (격자) ──
  //   방마다 0.25칸 격자. 벽·안쪽 방·금고·사물 둘레(몸 반지름쯤)를 막힌 칸으로 칠해 두고, 사람은 A*로 빈 칸을 따라간다.
  //   사물이 밀리거나 부서지면 그 방 격자만 다시 칠한다 (0.3초에 한 번까지). 좀비는 안 쓴다 (밀고 부수며 간다)
  const CH_NAV_CS = 0.25, CH_NAV_R = 0.36, CH_NAV_RO = 0.42, chNavHF = [], chNavHI = [], CH_NAV_DI = [1, -1, 0, 0, 1, 1, -1, -1], CH_NAV_DJ = [0, 0, 1, -1, 1, -1, 1, -1];
  let chNavCap = 0, chNavGs = null, chNavFrom = null, chNavMark = null, chNavSeq = 0, chNavQ = null;
  function chNavBuild(S) {
    const cs = CH_NAV_CS, R = CH_NAV_R, w = Math.max(1, Math.ceil((S.x1 - S.x0) / cs)), h = Math.max(1, Math.ceil((S.z1 - S.z0) / cs)), n = w * h;
    let N = S.nav;
    if (!N || N.w !== w || N.h !== h) N = S.nav = { w, h, x0: S.x0, z0: S.z0, cost: new Uint8Array(n), comp: new Uint16Array(n), ver: 0, main: 0, any: false, at: 0 };
    const C = N.cost, K = N.comp; C.fill(0); K.fill(0); N.ver++; N.at = clock; N.any = false; S.navDirty = false;
    const lo = (v, o) => Math.max(0, Math.ceil((v - o) / cs - 0.5)), hi = (v, o, m) => Math.min(m - 1, Math.floor((v - o) / cs - 0.5));
    const box = (x0, z0, x1, z1) => { for (let j = lo(z0, S.z0), j1 = hi(z1, S.z0, h); j <= j1; j++) for (let i = lo(x0, S.x0), i1 = hi(x1, S.x0, w); i <= i1; i++) C[j * w + i] = 1; };
    const disc = (x, z, r) => { for (let j = lo(z - r, S.z0), j1 = hi(z + r, S.z0, h); j <= j1; j++) for (let i = lo(x - r, S.x0), i1 = hi(x + r, S.x0, w); i <= i1; i++) { const dx = S.x0 + (i + 0.5) * cs - x, dz = S.z0 + (j + 0.5) * cs - z; if (dx * dx + dz * dz < r * r) C[j * w + i] = 1; } };
    box(-1e9, -1e9, S.x0 + R, 1e9); box(S.x1 - R, -1e9, 1e9, 1e9); box(-1e9, -1e9, 1e9, S.z0 + R); box(-1e9, S.z1 - R, 1e9, 1e9);   // 벽
    for (const Q of S.rooms || []) { box(Q.x0 - R, Q.z0 - R, Q.x1 + R, Q.z1 + R); N.any = true; }
    for (const t of S.fs) {                    // 네모 사물 (돌아가 있을 수 있다)
      if (t.obj.dead) continue; N.any = true;
      const fx = Math.cos(t.h), fz = Math.sin(t.h), hu = t.L / 2 + CH_NAV_RO, hv = t.W / 2 + CH_NAV_RO, ex = Math.abs(fx) * hu + Math.abs(fz) * hv, ez = Math.abs(fz) * hu + Math.abs(fx) * hv;
      for (let j = lo(t.z - ez, S.z0), j1 = hi(t.z + ez, S.z0, h); j <= j1; j++) for (let i = lo(t.x - ex, S.x0), i1 = hi(t.x + ex, S.x0, w); i <= i1; i++) { const dx = S.x0 + (i + 0.5) * cs - t.x, dz = S.z0 + (j + 0.5) * cs - t.z; if (Math.abs(dx * fx + dz * fz) < hu && Math.abs(-dx * fz + dz * fx) < hv) C[j * w + i] = 1; }
    }
    for (const p of S.fp) { if (p.dead || p.space !== S) continue; N.any = true; p.nvx = p.foot.x; p.nvz = p.foot.z; disc(p.foot.x, p.foot.z, p.r + CH_NAV_RO); }
    const T = S.parent || S, sf = T.safe; if (sf && !sf.dead && (sf.room || T) === S) { N.any = true; disc(sf.foot.x, sf.foot.z, sf.r + CH_NAV_RO); }
    if (!chNavQ || chNavQ.length < n) chNavQ = new Int32Array(n);
    let id = 0, bestN = 0; N.main = 0;         // 이어진 바닥 덩어리 — 가장 큰 것이 '큰 바닥'
    for (let s = 0; s < n; s++) {
      if (C[s] || K[s]) continue;
      let a = 0, b2 = 0; chNavQ[b2++] = s; K[s] = ++id;
      while (a < b2) { const k = chNavQ[a++], i = k % w, j = (k - i) / w;
        if (i > 0 && !C[k - 1] && !K[k - 1]) { K[k - 1] = id; chNavQ[b2++] = k - 1; } if (i < w - 1 && !C[k + 1] && !K[k + 1]) { K[k + 1] = id; chNavQ[b2++] = k + 1; }
        if (j > 0 && !C[k - w] && !K[k - w]) { K[k - w] = id; chNavQ[b2++] = k - w; } if (j < h - 1 && !C[k + w] && !K[k + w]) { K[k + w] = id; chNavQ[b2++] = k + w; } }
      if (b2 > bestN) { bestN = b2; N.main = id; }
    }
    return N;
  }
  function chNavOf(S) {                        // 그 방의 격자 (없거나 낡았으면 다시 칠한다)
    if (!S || !S.fs) return null;
    const N = S.nav;
    return !N || (S.navDirty && (clock - N.at >= 0.3 || clock < N.at)) ? chNavBuild(S) : N;
  }
  const chNavCell = (N, x, z) => Math.max(0, Math.min(N.h - 1, Math.floor((z - N.z0) / CH_NAV_CS))) * N.w + Math.max(0, Math.min(N.w - 1, Math.floor((x - N.x0) / CH_NAV_CS)));
  function chNavNear(N, x, z, rad, comp) {     // (x, z)에서 가장 가까운 빈 칸 (comp가 있으면 그 덩어리 안에서). 없으면 -1
    const cs = CH_NAV_CS, w = N.w, ci = Math.floor((x - N.x0) / cs), cj = Math.floor((z - N.z0) / cs);
    let best = -1, bd = Infinity;
    for (let j = Math.max(0, cj - rad), j1 = Math.min(N.h - 1, cj + rad); j <= j1; j++) for (let i = Math.max(0, ci - rad), i1 = Math.min(w - 1, ci + rad); i <= i1; i++) {
      const k = j * w + i; if (N.cost[k] || (comp && N.comp[k] !== comp)) continue;
      const dx = N.x0 + (i + 0.5) * cs - x, dz = N.z0 + (j + 0.5) * cs - z, d = dx * dx + dz * dz; if (d < bd) { bd = d; best = k; }
    }
    return best;
  }
  function chNavLos(N, ax, az, bx, bz, skip) { // 곧장 갈 수 있나 — 반 칸씩 짚어 본다 (skip = 출발점에서 이만큼은 안 본다: 지금 서 있는 자리는 어쨌든 설 수 있는 자리)
    const dx = bx - ax, dz = bz - az, L = Math.hypot(dx, dz), st = CH_NAV_CS * 0.5, w = N.w, h = N.h, C = N.cost;
    if (L <= (skip || 0)) return true;
    for (let d = skip || 0; ; d += st) {
      if (d > L) d = L;
      const i = Math.floor((ax + dx * d / L - N.x0) / CH_NAV_CS), j = Math.floor((az + dz * d / L - N.z0) / CH_NAV_CS);
      if (i < 0 || j < 0 || i >= w || j >= h || C[j * w + i]) return false;
      if (d >= L) return true;
    }
  }
  function chNavAstar(N, s, g) {               // 칸 s → g (8방향, 모서리 스치기 없음). 길 = s 다음 칸부터 g까지, 못 가면 null
    const w = N.w, h = N.h, C = N.cost, n = w * h;
    if (chNavCap < n) { chNavCap = n; chNavGs = new Float32Array(n); chNavFrom = new Int32Array(n); chNavMark = new Uint32Array(n); chNavSeq = 0; }
    const seq = (chNavSeq += 2), G = chNavGs, F = chNavFrom, M = chNavMark, hf = chNavHF, hi = chNavHI, gi = g % w, gj = (g - gi) / w;
    let hn = 0, guard = 0;
    const H = (k) => { const dx = Math.abs(k % w - gi), dz = Math.abs(Math.floor(k / w) - gj); return dx > dz ? dx + dz * 0.4142 : dz + dx * 0.4142; };
    const push = (f, k) => { let i = hn++; while (i > 0) { const p = (i - 1) >> 1; if (hf[p] <= f) break; hf[i] = hf[p]; hi[i] = hi[p]; i = p; } hf[i] = f; hi[i] = k; };
    const pop = () => { const top = hi[0], f = hf[--hn], k = hi[hn]; let i = 0; for (;;) { let c = i * 2 + 1; if (c >= hn) break; if (c + 1 < hn && hf[c + 1] < hf[c]) c++; if (hf[c] >= f) break; hf[i] = hf[c]; hi[i] = hi[c]; i = c; } if (hn) { hf[i] = f; hi[i] = k; } return top; };
    G[s] = 0; F[s] = -1; M[s] = seq; push(H(s), s);
    while (hn) {
      const k = pop(); if (M[k] === seq + 1) continue; M[k] = seq + 1;
      if (k === g) break;
      if (++guard > 8000) return null;
      const i = k % w, j = (k - i) / w, gk = G[k];
      for (let d = 0; d < 8; d++) {
        const di = CH_NAV_DI[d], dj = CH_NAV_DJ[d], ni = i + di, nj = j + dj;
        if (ni < 0 || nj < 0 || ni >= w || nj >= h) continue;
        const q = nj * w + ni; if (C[q] || M[q] === seq + 1) continue;
        if (di && dj && (C[j * w + ni] || C[nj * w + i])) continue;
        const ng = gk + (di && dj ? 1.4142 : 1);
        if (M[q] === seq && G[q] <= ng) continue;
        G[q] = ng; F[q] = k; M[q] = seq; push(ng + H(q), q);
      }
    }
    if (M[g] !== seq + 1) return null;
    const out = []; for (let k = g; k !== s && k >= 0; k = F[k]) out.push(k);
    return out.reverse();
  }
  function chNavPlan(N, px, pz, tx, tz) {      // 경유점 [x, z, x, z …] — 마지막은 목적지 (막힌 자리면 그 옆 빈 칸). 못 가면 null
    const cs = CH_NAV_CS, w = N.w, C = N.cost, K = N.comp, cx = (k) => N.x0 + (k % w + 0.5) * cs, cz = (k) => N.z0 + (Math.floor(k / w) + 0.5) * cs;
    let s = chNavCell(N, px, pz), g = chNavCell(N, tx, tz), sOff = false, gOff = false;
    if (C[s]) { s = chNavNear(N, px, pz, 6, 0); sOff = true; if (s < 0) return null; }
    if (C[g] || K[g] !== K[s]) {              // 목적지가 막힌 칸이거나 걸어서 못 가는 덩어리 → 갈 수 있는 칸 중 가장 가까운 곳까지
      g = chNavNear(N, tx, tz, 8, K[s]); gOff = true;
      if (g < 0) { let bd = Infinity; for (let k = 0, n = C.length; k < n; k++) if (K[k] === K[s]) { const dx = cx(k) - tx, dz = cz(k) - tz, d = dx * dx + dz * dz; if (d < bd) { bd = d; g = k; } } }
      if (g < 0) return null;
    }
    const cells = s === g ? [] : chNavAstar(N, s, g); if (!cells) return null;
    const pts = []; let ax = px, az = pz, k = 0;
    if (sOff) { ax = cx(s); az = cz(s); pts.push(ax, az); }
    while (k < cells.length) {                 // 보이는 가장 먼 칸으로 건너뛴다
      let m = -1;
      for (let q = k; q < cells.length; q++) { if (chNavLos(N, ax, az, cx(cells[q]), cz(cells[q]), k || sOff ? 0 : 0.3)) m = q; else if (q - (m < 0 ? k : m) > 8) break; }
      if (m < 0) m = k;
      ax = cx(cells[m]); az = cz(cells[m]); pts.push(ax, az); k = m + 1;
    }
    if (gOff) { if (!pts.length) pts.push(cx(g), cz(g)); }
    else if (cells.length) { pts[pts.length - 2] = tx; pts[pts.length - 1] = tz; }
    else pts.push(tx, tz);
    return pts;
  }
  function chNav(b, S, tx, tz) {               // 이번 걸음에 향할 자리 (wp) — 격자가 없거나 못 가면 null (예전 방식으로)
    const N = chNavOf(S); if (!N || !N.any) return null;
    const px = b.foot.x, pz = b.foot.z;
    if (chNavLos(N, px, pz, tx, tz, 0.3)) { b.nav = null; return wp.set(tx, tz); }   // 곧장 보인다
    const P = b.nav;
    if (P && P.S === S && clock >= P.at) {
      const same = P.ver === N.ver && Math.abs(P.tx - tx) < 0.4 && Math.abs(P.tz - tz) < 0.4, L = P.pts;
      let i = P.i;
      while (i < L.length - 2 && Math.hypot(L[i] - px, L[i + 1] - pz) < 0.3) i += 2;
      if (i < L.length - 2 && chNavLos(N, px, pz, L[i + 2], L[i + 3], 0.3)) i += 2;
      P.i = i;
      const end = i >= L.length - 2 && Math.hypot(L[i] - px, L[i + 1] - pz) < 0.3;   // 길 끝 (목적지 옆 빈 칸)까지 왔다
      if (end && same) return wp.set(tx, tz);                                        // 거기서부터는 곧장 (막힌 자리의 상대에게 붙으러)
      if (!end && ((same && chNavLos(N, px, pz, L[i], L[i + 1], 0.3)) || clock < P.hold)) return wp.set(L[i], L[i + 1]);
    }
    const pts = chNavPlan(N, px, pz, tx, tz);
    if (!pts) { b.nav = null; b.navBad = true; return null; }
    b.nav = { S, ver: N.ver, tx, tz, pts, i: 0, at: clock, hold: clock + 0.3 };
    return wp.set(pts[0], pts[1]);
  }
  const chSideL = [];
  function chSidestep(c) {                     // 건물 안에서 걷다가 바로 앞에 사람이 있으면 (마주 오든 느리게 가든) 한쪽으로 비켜 간다 — 둘 다 자기 오른쪽이라 서로 엇갈린다
    const vx = wantV.x, vz = wantV.y, sp = Math.hypot(vx, vz); if (sp < 0.01) return;
    const ux = vx / sp, uz = vz / sp;
    for (const o of nearIn(cCells, c.foot.x, c.foot.z, 1.0, chSideL)) {
      if (o === c || o.sleep || o.space !== c.space) continue;
      const dx = o.foot.x - c.foot.x, dz = o.foot.z - c.foot.z, d = Math.hypot(dx, dz);
      if (d > 1.0 || d < 1e-6 || (dx * ux + dz * uz) / d < 0.6) continue;   // 앞쪽 53° 안, 한 칸 안
      let sx = -uz, sz = ux;
      const N = c.space.nav;
      if (N) { const bad = (k) => N.cost[chNavCell(N, c.foot.x + sx * 0.5 * k, c.foot.z + sz * 0.5 * k)]; if (bad(1)) { if (bad(-1)) return; sx = -sx; sz = -sz; } }   // 그쪽이 막혀 있으면 반대쪽, 둘 다 막혔으면 그대로
      wantV.set((ux * 0.5 + sx * 0.87) * sp, (uz * 0.5 + sz * 0.87) * sp); return;
    }
  }
  function chGoalBad(a, x, z, c) {             // 배회 목표로 못 쓰는 자리 — 막힌 칸이거나, 그 사람이 걸어서 못 가는 덩어리
    const N = chNavOf(a); if (!N) return false;
    const k = chNavCell(N, x, z); if (N.cost[k]) return true;
    if (c && c.space === a) { const s = chNavCell(N, c.foot.x, c.foot.z); if (!N.cost[s]) return N.comp[s] !== N.comp[k]; }
    return N.comp[k] !== N.main;
  }
