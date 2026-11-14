# c69: 구역 순환도로(맵은 map_roads.py) · 차종(민간 5 + 소방차·구급차) · 주차된 차 꾸미기
C69B_FN = r"""  // ── c69: 차종 — 길이·폭·체력·무게 = 경찰차(2.02 × 1.08칸 · 체력 459 · 무게 1)의 몇 배 ──
  const CH_CAR = {
    compact: { name: '소형차', kl: 0.82, kw: 0.9,  hp: 0.8, mass: 0.8, col: [0xe9e9e4, 0x3f7fd9, 0xe0b23c, 0x4fa35a, 0xc94a3a, 0x8d6fc4, 0x2e2e33] },
    sedan:   { name: '세단',   kl: 1.0,  kw: 1.0,  hp: 1.0, mass: 1.0, col: [0x2b2c31, 0xf0f0ee, 0x9097a1, 0x24508a, 0x7c2323, 0x4b5a3a] },
    sports:  { name: '스포츠카', kl: 1.06, kw: 0.96, hp: 0.8, mass: 0.9, col: [0xe22828, 0xf5c518, 0x1e9cf0, 0xff6a13, 0x16161a] },
    van:     { name: '밴',     kl: 1.22, kw: 1.1,  hp: 1.3, mass: 1.4, col: [0xf4f4f2, 0x9aa3ad, 0x2f5d50, 0x374a7a, 0x6b4a2e] },
    truck:   { name: '트럭',   kl: 1.58, kw: 1.2,  hp: 1.8, mass: 2.2, col: [0x3b6fd4, 0xd97a1a, 0x4f8a3a, 0x8c8c8c, 0xb53a2e] },
    fire:    { name: '소방차', kl: 1.62, kw: 1.25, hp: 2.0, mass: 2.4, col: [0xd42a1e] },
    ambul:   { name: '구급차', kl: 1.25, kw: 1.12, hp: 1.3, mass: 1.4, col: [0xf6f6f4] },
  };
  const CH_CAR_MIX = [['compact', 30], ['sedan', 34], ['sports', 8], ['van', 17], ['truck', 11]];   // 길에서 보이는 비율
  const chCarPick = () => { let r = Math.random() * 100; for (const [k, w] of CH_CAR_MIX) if ((r -= w) < 0) return k; return 'sedan'; };
  const chCarTexCache = new Map();
  function chCarTex(type, col) {              // 위에서 본 차 그림 (오른쪽 = 앞)
    const key = type + ':' + col; let t = chCarTexCache.get(key); if (t) return t;
    const c = document.createElement('canvas'); c.width = 256; c.height = 128; const g = c.getContext('2d');
    const mix = (v, k) => { const f = (x) => Math.max(0, Math.min(255, Math.round(k >= 0 ? x + (255 - x) * k : x * (1 + k)))); return 'rgb(' + f((v >> 16) & 255) + ',' + f((v >> 8) & 255) + ',' + f(v & 255) + ')'; };
    const rr = (x, y, w, h, r, fill) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); g.fillStyle = fill; g.fill(); };
    const GL = '#232d3a', GL2 = '#4a5d73', lamps = (y0, y1) => { rr(240, y0, 9, 20, 3, '#fff4b8'); rr(240, y1, 9, 20, 3, '#fff4b8'); rr(7, y0, 7, 20, 3, '#d02222'); rr(7, y1, 7, 20, 3, '#d02222'); };
    const cabin = (x0, x1, y0, y1) => {       // 유리로 둘러싼 지붕
      rr(x0, y0, x1 - x0, y1 - y0, 10, GL);
      rr(x0 + 14, y0 + 9, x1 - x0 - 32, y1 - y0 - 18, 6, mix(col, 0.16));
      g.fillStyle = GL2; g.fillRect(x1 - 15, y0 + 12, 4, y1 - y0 - 24);
    };
    rr(2, 4, 252, 120, type === 'truck' || type === 'fire' ? 10 : 24, '#0c0c0e');
    if (type === 'truck') {
      rr(6, 8, 168, 112, 6, '#d6d6cf'); g.strokeStyle = 'rgba(0, 0, 0, 0.28)'; g.lineWidth = 3; for (let x = 28; x < 170; x += 24) { g.beginPath(); g.moveTo(x, 10); g.lineTo(x, 118); g.stroke(); }
      rr(180, 12, 70, 104, 12, mix(col, 0)); rr(200, 20, 34, 88, 8, GL); rr(206, 28, 14, 72, 4, mix(col, 0.16)); lamps(18, 90);
    } else if (type === 'fire') {
      rr(6, 8, 244, 112, 8, mix(col, 0)); g.fillStyle = '#f2f2ee'; g.fillRect(8, 16, 176, 6); g.fillRect(8, 106, 176, 6);
      g.fillStyle = '#c9ccd1'; g.fillRect(20, 44, 150, 7); g.fillRect(20, 77, 150, 7); for (let x = 26; x < 168; x += 16) g.fillRect(x, 44, 5, 40);
      rr(196, 18, 38, 92, 8, GL); rr(202, 26, 16, 76, 4, mix(col, 0.14)); g.fillStyle = '#2f6bff'; g.fillRect(186, 34, 7, 22); g.fillStyle = '#ff3b30'; g.fillRect(186, 72, 7, 22); lamps(16, 92);
    } else if (type === 'ambul') {
      rr(6, 8, 244, 112, 14, mix(col, 0)); g.fillStyle = '#d42a1e'; g.fillRect(10, 14, 170, 7); g.fillRect(10, 107, 170, 7);
      g.fillRect(82, 54, 46, 20); g.fillRect(95, 41, 20, 46);
      rr(190, 18, 44, 92, 9, GL); rr(196, 26, 20, 76, 4, mix(col, -0.08)); g.fillStyle = '#2f6bff'; g.fillRect(176, 40, 8, 48); lamps(16, 92);
    } else {
      rr(6, 10, 244, 108, type === 'van' ? 14 : 24, mix(col, 0));
      g.fillStyle = mix(col, -0.22); g.fillRect(22, 10, 212, 5); g.fillRect(22, 113, 212, 5);
      if (type === 'compact') cabin(48, 196, 20, 108);
      else if (type === 'sports') { cabin(76, 168, 24, 104); g.fillStyle = 'rgba(255, 255, 255, 0.85)'; g.fillRect(170, 52, 70, 7); g.fillRect(170, 69, 70, 7); g.fillRect(10, 52, 64, 7); g.fillRect(10, 69, 64, 7); }
      else if (type === 'van') { cabin(30, 216, 18, 110); g.strokeStyle = 'rgba(0, 0, 0, 0.3)'; g.lineWidth = 3; for (const x of [84, 132]) { g.beginPath(); g.moveTo(x, 30); g.lineTo(x, 98); g.stroke(); } }
      else cabin(64, 184, 20, 108);
      lamps(18, 90);
    }
    t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; chCarTexCache.set(key, t); return t;
  }
  function chCivCar(type, x, z, h, ci) {      // 민간 차 한 대 (서 있는 채로) — 경찰차와 같은 물건, 크기·체력·무게만 차종대로
    const T = CH_CAR[type], col = T.col[ci === undefined ? Math.floor(Math.random() * T.col.length) : ci % T.col.length];
    const g = new THREE.Group(), body = new THREE.Mesh(carGeo, new THREE.MeshBasicMaterial({ map: chCarTex(type, col), transparent: true, depthTest: false, depthWrite: false })), pad = new THREE.Mesh(lampGeo, carMat(0x000000)), dm = carMat(0x000000);
    body.renderOrder = -0.45; pad.visible = false; g.add(body, pad); g.scale.set(T.kl, 1, T.kw); scene.add(g);
    const car = { g, red: dm, blue: dm, x, z, vx: 0, vz: 0, h, calls: [], n: 0, squad: null, mil: false, state: 'parked', flashT: 0, sight: 0, foot: new THREE.Vector3(x, 0, z), civ: type, kl: T.kl, kw: T.kw, massK: T.mass, hpK: T.hp, tint0: 0xffffff };
    cars.push(car); return car;
  }
  function chCarObj(car, deco) {               // 서 있는 차를 때릴 수 있는 사물로 — 꾸밈 차는 따로 목록에 (좀비가 일부러 찾지 않으니 늘 훑지 않는다)
    const hp = MY_DAMAGE * 9.5 * (car.hpK || 1);
    car.obj = { kind: 'obj', type: 'car', car, foot: new THREE.Vector3(car.x, 0, car.z), hp, maxHp: hp, dead: false };
    addHpBar(car.obj, hpFoeMat); (deco ? chDecoObjs : objs).push(car.obj);
    car.g.position.set(car.x, 0.05, car.z); car.g.rotation.y = -car.h; car.g.visible = false;
  }
  function chDecoCar(type, x, z, h) {         // 꾸밈 차 — 빈 차. 부술 수 있고 좀비가 밀 수 있다. 일부러 찾아가 때리지는 않는다 (붙어 있을 때 · 내가 때릴 때만)
    let car;
    if (type === 'police' || type === 'mil') { addCar(x, z, h, null, 0, type === 'mil' ? ['soldier'] : undefined); car = cars[cars.length - 1]; car.squad = null; car.state = 'parked'; car.tint0 = type === 'mil' ? 0x4a5a32 : 0x24305a;
      car.red.color.setHex(type === 'mil' ? 0x2a3320 : 0x4a3a3a); car.blue.color.setHex(type === 'mil' ? 0x2a3320 : 0x3a3f4a); }
    else car = chCivCar(type, x, z, h);
    car.deco = true; chCarObj(car, true); return car;
  }
  const chDecoCarNow = (type, x, z, h) => { const c = chDecoCar(type, x, z, h); updateCarObs(); return c; };
  // ── c69: 주차 — 공터의 주차 칸(맵과 함께 고정, 선이 그려져 있다) · 집 앞 한두 대 · 랜드마크 옆 (경찰서 경찰차 2 · 군사시설 군인차 1 · 소방서 소방차 · 병원 구급차 · 가게 손님 차) ──
  const CH_BAY_PITCH = 1.95, CH_BAY_LEN = 2.5;
  const chRoadRects = CH_MAP.roads.concat(CH_MAP.bridges), chBays = [];
  const chBoxHit = (a, b, m) => a[0] < b[2] + m && a[2] > b[0] - m && a[1] < b[3] + m && a[3] > b[1] - m;
  function chDecoStatic(box, host) {           // 맵에 걸리나 — 건물(벽에서 0.35칸) · 다른 건물과의 사이 통로(1.3칸) · 길·다리 · 강 · 지도 밖
    if (box[0] < MM.x0 + 1 || box[2] > MM.x1 - 1 || box[1] < MM.z0 + 1 || box[3] > MM.z1 - 1) return false;
    for (const B of buildings) { if (B.parent) continue; if (chBoxHit(box, [B.x0, B.z0, B.x1, B.z1], B === host ? 0.3 : 1.3)) return false; }
    for (const r of chRoadRects) if (chBoxHit(box, r, 0.25)) return false;
    for (const r of CH_MAP.rivers) if (chBoxHit(box, r, 0.8)) return false;
    return true;
  }
  const chCarBox = (x, z, h, type) => { const T = type === 'police' ? { kl: 1, kw: 1 } : type === 'mil' ? { kl: MIL_K, kw: MIL_K } : CH_CAR[type], L = CAR_L * T.kl, W = CAR_W * T.kw, c = Math.abs(Math.cos(h)), s = Math.abs(Math.sin(h)), hx = (L * c + W * s) / 2, hz = (L * s + W * c) / 2; return [x - hx, z - hz, x + hx, z + hz]; };
  {                                           // 공터마다 주차 칸 한두 줄 — 긴 변을 따라, 차는 세로로 댄다. 씨앗 고정 (판마다 같은 자리)
    let seed = 90217; const rnd = () => (seed = seed * 16807 % 2147483647) / 2147483647;
    const lineMat = new THREE.MeshBasicMaterial({ color: 0xf2f2ea, transparent: true, opacity: 0.55, depthTest: false, depthWrite: false });
    const pos = []; const quad = (x0, z0, x1, z1) => pos.push(x0, 0, z0, x0, 0, z1, x1, 0, z1, x0, 0, z0, x1, 0, z1, x1, 0, z0);
    for (const [x0, z0, x1, z1] of CH_MAP.lots) {
      const alongX = x1 - x0 >= z1 - z0, a0 = alongX ? x0 : z0, a1 = alongX ? x1 : z1, b0 = alongX ? z0 : x0, b1 = alongX ? z1 : x1;
      if (b1 - b0 < CH_BAY_LEN + 1) continue;
      for (const edge of [0, 1]) {
        if (edge === 1 && (b1 - b0 < CH_BAY_LEN * 2 + 2.6 || rnd() < 0.45)) { rnd(); rnd(); continue; }
        const want = 5 + Math.floor(rnd() * 5), bc = edge ? b1 - 0.35 - CH_BAY_LEN / 2 : b0 + 0.35 + CH_BAY_LEN / 2, at0 = a0 + 0.6 + rnd() * Math.max(0, a1 - a0 - 1.2 - want * CH_BAY_PITCH);
        let run = [];
        const flush = () => { if (run.length >= 2) { for (const q of run) chBays.push(q); const f = run[0].a - CH_BAY_PITCH / 2, l = run[run.length - 1].a + CH_BAY_PITCH / 2, e0 = bc - CH_BAY_LEN / 2, e1 = bc + CH_BAY_LEN / 2, head = edge ? e1 : e0;
            for (let a = f; a <= l + 1e-6; a += CH_BAY_PITCH) alongX ? quad(a - 0.035, e0, a + 0.035, e1) : quad(e0, a - 0.035, e1, a + 0.035);
            alongX ? quad(f, head - 0.035, l, head + 0.035) : quad(head - 0.035, f, head + 0.035, l); } run = []; };
        for (let i = 0; i < want; i++) { const a = at0 + (i + 0.5) * CH_BAY_PITCH, x = alongX ? a : bc, z = alongX ? bc : a, h = alongX ? Math.PI / 2 : 0;
          const box = alongX ? [x - CH_BAY_PITCH / 2 + 0.2, z - CH_BAY_LEN / 2, x + CH_BAY_PITCH / 2 - 0.2, z + CH_BAY_LEN / 2] : [x - CH_BAY_LEN / 2, z - CH_BAY_PITCH / 2 + 0.2, x + CH_BAY_LEN / 2, z + CH_BAY_PITCH / 2 - 0.2];
          if (a + CH_BAY_PITCH / 2 > a1 - 0.3 || !chDecoStatic(box, null)) { flush(); continue; }
          run.push({ x, z, h, a }); }
        flush();
      }
    }
    // 도로 가운데 점선 — 대로와 순환도로 (다리 앞·길목 앞 넓은 길은 빼고)
    const dashMat = new THREE.MeshBasicMaterial({ color: 0xe6d27a, transparent: true, opacity: 0.6, depthTest: false, depthWrite: false }), dp = [];
    const dq = (x0, z0, x1, z1) => dp.push(x0, 0, z0, x0, 0, z1, x1, 0, z1, x0, 0, z0, x1, 0, z1, x1, 0, z0);
    for (const [x0, z0, x1, z1] of CH_MAP.roads) { const w = x1 - x0, d = z1 - z0; if (Math.min(w, d) > 7 || Math.max(w, d) < 30) continue;
      if (w > d) for (let x = x0 + 1; x < x1 - 1.6; x += 2.4) dq(x, (z0 + z1) / 2 - 0.06, x + 1.1, (z0 + z1) / 2 + 0.06); else for (let z = z0 + 1; z < z1 - 1.6; z += 2.4) dq((x0 + x1) / 2 - 0.06, z, (x0 + x1) / 2 + 0.06, z + 1.1); }
    for (const [P, mat, o] of [[pos, lineMat, -0.89], [dp, dashMat, -0.895]]) { if (!P.length) continue; const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(P), 3)); const m = new THREE.Mesh(geo, mat); m.position.y = 0.031; m.renderOrder = o; m.frustumCulled = false; scene.add(m); }
  }
  const chObjLists1 = [objs], chObjLists2 = [objs, chDecoObjs];
  let chDeco = { boxes: [], n: {} };
  function chDecoOk(box) {                     // 판마다 달라지는 것 — 문 앞 · 먼저 놓은 차 · 시작 자리
    for (const k of chDeco.keep) if (chBoxHit(box, k, 0)) return false;
    for (const b of chDeco.boxes) if (chBoxHit(box, b, 0.3)) return false;
    return true;
  }
  function chDecoPut(type, x, z, h, host, tag) {
    const hh = h + rand(-0.06, 0.06), box = chCarBox(x, z, h, type);
    if (!chDecoStatic(box, host) || !chDecoOk(box)) return false;
    chDecoCar(type, x + rand(-0.08, 0.08), z + rand(-0.08, 0.08), hh); chDeco.boxes.push(box); chDeco.n[tag] = (chDeco.n[tag] || 0) + 1; return true;
  }
  function chDecoBeside(B, types, perp, sides) {   // 그 건물 벽 옆에 한 줄로 — 벽을 따라(가로) 또는 벽에 머리를 대고(세로). 자리가 안 나면 다른 벽으로
    const dim = (t) => t === 'police' ? [CAR_L, CAR_W] : t === 'mil' ? [CAR_L * MIL_K, CAR_W * MIL_K] : [CAR_L * CH_CAR[t].kl, CAR_W * CH_CAR[t].kw];
    for (const s of sides) {
      const nx = s === 'e' ? 1 : s === 'w' ? -1 : 0, nz = s === 's' ? 1 : s === 'n' ? -1 : 0, span = nx ? B.z1 - B.z0 : B.x1 - B.x0, mid = nx ? (B.z0 + B.z1) / 2 : (B.x0 + B.x1) / 2, wall = nx > 0 ? B.x1 : nx < 0 ? B.x0 : nz > 0 ? B.z1 : B.z0;
      const pitch = types.map((t) => (perp ? dim(t)[1] : dim(t)[0]) + (perp ? 0.85 : 0.7)), total = pitch.reduce((a, b) => a + b, 0);
      for (let tr = 0; tr < 6; tr++) {
        let at = mid + rand(-1, 1) * Math.max(0, (span + 2 - total) / 2) - total / 2; const plan = [];
        const flip = Math.random() < 0.5 ? Math.PI : 0;
        for (let i = 0; i < types.length; i++) { const [L, W] = dim(types[i]), a = at + pitch[i] / 2, off = 0.5 + (perp ? L : W) / 2; at += pitch[i];
          const x = nx ? wall + nx * off : a, z = nx ? a : wall + nz * off, h = (perp ? (nx ? 0 : Math.PI / 2) : (nx ? Math.PI / 2 : 0)) + (perp ? flip : (Math.random() < 0.5 ? Math.PI : 0));
          plan.push([types[i], x, z, h]); }
        if (!plan.every(([t, x, z, h]) => { const b = chCarBox(x, z, h, t); return chDecoStatic(b, B) && chDecoOk(b); })) continue;
        for (const [t, x, z, h] of plan) chDecoPut(t, x, z, h, B, B.type);
        return true;
      }
    }
    return false;
  }
  function chDecoPlace() {                     // 새 판 — 주차된 차를 다시 놓는다 (판마다 조금씩 다르다)
    chDeco = { boxes: [], n: {}, keep: [] };
    for (const o of objs) if (o.type === 'door' && !o.off && !(o.B.parent && !o.L.ext)) { const L = o.L, cx = L.cx + L.nx * 1.9, cz = L.cz + L.nz * 1.9, hx = Math.abs(L.tx) * 2.5 + Math.abs(L.nx) * 2.1, hz = Math.abs(L.tz) * 2.5 + Math.abs(L.nz) * 2.1; chDeco.keep.push([cx - hx, cz - hz, cx + hx, cz + hz]); }
    for (const B of buildings) for (const D of B.doors || []) { const cx = D.cx + D.nx * 1.9, cz = D.cz + D.nz * 1.9, w = (D.w || DOOR) / 2 + 0.8, hx = Math.abs(D.tx) * w + Math.abs(D.nx) * 2.1, hz = Math.abs(D.tz) * w + Math.abs(D.nz) * 2.1; chDeco.keep.push([cx - hx, cz - hz, cx + hx, cz + hz]); }
    chDeco.keep.push([me.foot.x - 5, me.foot.z - 5, me.foot.x + 5, me.foot.z + 5]);
    const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
    const others = (B) => shuffle(['n', 'e', 's', 'w'].filter((s) => !(B.locks || []).some((L) => L.front && (L.nx > 0 ? 'e' : L.nx < 0 ? 'w' : L.nz > 0 ? 's' : 'n') === s)));
    const front = (B) => (B.locks || []).filter((L) => L.front).map((L) => L.nx > 0 ? 'e' : L.nx < 0 ? 'w' : L.nz > 0 ? 's' : 'n');
    const civ = (n) => Array.from({ length: n }, chCarPick);
    for (const B of buildings) {               // 랜드마크·창고 먼저 (자리가 정해진 차)
      if (B.parent) continue;
      const t = B.type, fo = front(B).concat(others(B)), of = others(B).concat(front(B));
      if (t === 'police') { if (!chDecoBeside(B, ['police', 'police'], Math.random() < 0.5, fo)) chDecoBeside(B, ['police'], false, fo); }
      else if (t === 'army') chDecoBeside(B, ['mil'], false, of);
      else if (t === 'fire') { if (!(Math.random() < 0.4 && chDecoBeside(B, ['fire', 'fire'], true, of))) chDecoBeside(B, ['fire'], Math.random() < 0.5, of); }
      else if (t === 'hospital') chDecoBeside(B, ['ambul'], Math.random() < 0.5, fo);
      else if (t === 'mart') { for (const n of [4, 3, 2]) if (chDecoBeside(B, civ(n), true, fo)) break; }
      else if (t === 'bank' || t === 'gym' || t === 'library' || t === 'conv') { for (const n of [t === 'conv' ? 2 : 3, 2, 1]) if (chDecoBeside(B, civ(n), Math.random() < 0.6, fo)) break; }
      else if (t === 'store') { if (Math.random() < 0.6) chDecoBeside(B, [Math.random() < 0.65 ? 'truck' : 'van'], Math.random() < 0.35, of); }
    }
    for (const q of chBays) if (Math.random() < 0.5) chDecoPut(chCarPick(), q.x, q.z, q.h + (Math.random() < 0.5 ? Math.PI : 0), null, 'lot');   // 공터 주차 칸 — 절반쯤 차 있다
    for (const B of buildings) {               // 집 앞 한두 대 — 가로로도 세로로도
      if (B.parent || B.type !== 'house') continue;
      const r = Math.random(), n = r < 0.16 ? 2 : r < 0.72 ? 1 : 0; if (!n) continue;
      const sides = Math.random() < 0.5 ? front(B).concat(others(B)) : others(B).concat(front(B));
      if (!chDecoBeside(B, civ(n), Math.random() < 0.45, sides) && n === 2) chDecoBeside(B, civ(1), Math.random() < 0.45, sides);
    }
    for (const b of bodies) {                  // 먼저 깔린 사람이 차 밑에 깔렸으면 차 옆으로 빼 준다
      if (b.kind !== 'citizen' || b.space) continue;
      for (const c of cars) { if (!c.deco) continue; const dx = b.foot.x - c.x, dz = b.foot.z - c.z; if (Math.abs(dx) > 3 || Math.abs(dz) > 3) continue;
        const fx = Math.cos(c.h), fz = Math.sin(c.h), u = dx * fx + dz * fz, v = -dx * fz + dz * fx, hu = CAR_L * ckl(c) / 2 + BODY + 0.3, hv = CAR_W * ck(c) / 2 + BODY + 0.3;
        if (Math.abs(u) >= hu - 0.2 || Math.abs(v) >= hv - 0.2) continue;
        const cand = [[u, hv], [u, -hv], [hu, v], [-hu, v]].map(([cu, cv]) => [c.x + cu * fx - cv * fz, c.z + cu * fz + cv * fx]).filter(([x, z]) => freeSpot(x, z, null) && !spaceOf(x, z) && !chOnCar(x, z))
          .sort((p, q) => Math.hypot(p[0] - b.foot.x, p[1] - b.foot.z) - Math.hypot(q[0] - b.foot.x, q[1] - b.foot.z));
        if (cand.length) { b.foot.x = cand[0][0]; b.foot.z = cand[0][1]; b.px = b.foot.x; b.pz = b.foot.z; } }
    }
    updateCarObs();
  }
  function chOnCar(x, z) {                     // 그 자리가 서 있는 차(꾸밈 차 포함) 위나 바로 옆인가 — 배회 목표로는 안 뽑는다
    for (const c of cars) { if (c.state !== 'parked' || c.wall || c.wreck) continue; const dx = x - c.x, dz = z - c.z; if (Math.abs(dx) > 3 || Math.abs(dz) > 3) continue;
      const fx = Math.cos(c.h), fz = Math.sin(c.h); if (Math.abs(dx * fx + dz * fz) < CAR_L * ckl(c) / 2 + BODY + 0.25 && Math.abs(-dx * fz + dz * fx) < CAR_W * ck(c) / 2 + BODY + 0.25) return true; }
    return false;
  }
"""
C69B_R = [
  # 차 크기 — 길이와 폭을 따로 (차종마다)
  ("const ck = (c) => c.mil ? MIL_K : 1;", "const ck = (c) => c.kw || (c.mil ? MIL_K : 1), ckl = (c) => c.kl || (c.mil ? MIL_K : 1);   // c69: ck = 폭 배율, ckl = 길이 배율"),
  ("CAR_L * ck(car)", "CAR_L * ckl(car)", 7),
  ("CAR_L * ck(c)", "CAR_L * ckl(c)", 2),
  ("CAR_L * 1.6 * Math.max(ck(A), ck(B))", "CAR_L * 1.6 * Math.max(ckl(A), ckl(B))"),
  ("CAR_L / 2 * kA * ck(A)", "CAR_L / 2 * kA * ckl(A)"),
  ("CAR_L / 2 * kB * ck(B)", "CAR_L / 2 * kB * ckl(B)"),
  ("      c.g.scale.set(0.8 * ck(c), 1, 0.8 * ck(c));", "      c.g.scale.set(0.8 * ckl(c), 1, 0.8 * ck(c));"),
  # 서 있는 차 밀기 — 무게는 차종대로. 꾸밈 차는 좀비만 민다 (사람은 돌아간다)
  ("sh = f / (f + CAR_MASS * 2 / 3),", "sh = CHAPTER && car.deco && !isZombie(b) ? 0 : f / (f + CAR_MASS * 2 / 3 * (car.massK || 1)),   /* c69 */"),
  # 꾸밈 차는 일부러 찾아가 때리지 않는다 — 동료는 내가 때리는 차만, 나는 손 닿는 차만
  ("    nearObj.any = any;",
   "    if (CHAPTER && !z.space) {               // c69: 꾸밈 차 — 나는 손 닿는 차(와 이미 때리던 차)만, 동료는 내가 때리는 차만\n"
   "      if (z === me) { const reach = MELEE - RADIUS + Math.max(0, (z.r || BODY) - BODY);\n"
   "        for (const o of chDecoObjs) { if (o.dead || Math.abs(o.car.x - z.foot.x) > 5 || Math.abs(o.car.z - z.foot.z) > 5) continue; const g = objGap(o, z); if (g > reach && !(hotObj(o) && g <= z.sense)) continue; if (g < ad) { ad = g; any = o; } if (g < bd) { bd = g; best = o; } } }\n"
   "      else if (chHotDeco && !chHotDeco.dead && hotObj(chHotDeco)) { const o = chHotDeco, g = objGap(o, z);\n"
   "        if (g <= z.sense) { const [px, pz] = objPoint(o, z); if (!blocked(z.foot.x, z.foot.z, px, pz)) { if (g < ad) { ad = g; any = o; } const n = (objCrowd.get(o) || 0) - (z.objC === o ? 1 : 0); if (g < bd && n < CROWD_MAX) { bd = g; best = o; } } } }\n"
   "    }\n"
   "    nearObj.any = any;"),
  ("    if (z === me) o.hotF = objFrame;   // v360: 내가 붙어서 때리는 중", "    if (z === me) { o.hotF = objFrame; if (CHAPTER && o.car && o.car.deco) chHotDeco = o; }   // v360: 내가 붙어서 때리는 중"),
  ("if (o.type === 'car' && !o.dead && Math.abs(o.car.x - z.foot.x) < 4 && Math.abs(o.car.z - z.foot.z) < 4) { const g = objGap(o, z);",
   "if (o.type === 'car' && !o.dead && Math.abs(o.car.x - z.foot.x) < 4 && Math.abs(o.car.z - z.foot.z) < 4) { const g = objGap(o, z);"),
  ("          if (!z.space) for (const o of objs) if (o.type === 'car'", "          if (!z.space) for (const OL of (CHAPTER && z === me ? chObjLists2 : chObjLists1)) for (const o of OL) if (o.type === 'car'"),
  ("  function drawObjBars(dt) {                  // 깎인 사물만 체력바\n    for (const o of objs) {", "  function drawObjBars(dt) {                  // 깎인 사물만 체력바\n    for (const OL of chObjLists2) for (const o of OL) {"),
  ("    tintTarget(redObj, false); redObj = null;   // v288\n    for (let i = objs.length - 1; i >= 0; i--) {", "    tintTarget(redObj, false); redObj = null;   // v288\n    for (const o of chDecoObjs) if (o.hpBar) scene.remove(o.hpBar); chDecoObjs.length = 0; chHotDeco = null;   // c69\n    for (let i = objs.length - 1; i >= 0; i--) {"),
  ("        const j = objs.indexOf(c.obj); if (j >= 0) { if (c.obj.hpBar) scene.remove(c.obj.hpBar); objs.splice(j, 1); }",
   "        const j = objs.indexOf(c.obj); if (j >= 0) { if (c.obj.hpBar) scene.remove(c.obj.hpBar); objs.splice(j, 1); }\n        { const j2 = chDecoObjs.indexOf(c.obj); if (j2 >= 0) { if (c.obj.hpBar) scene.remove(c.obj.hpBar); chDecoObjs.splice(j2, 1); } }   // c69"),
  # (1) 길 찾기 장애물은 차가 정말 밀렸을 때만, 0.25초에 한 번
  ("          carClampB(car); if (car.obj) car.obj.foot.set(car.x, 0, car.z); pushedCar = true;", "          carClampB(car); if (car.obj) car.obj.foot.set(car.x, 0, car.z); if (sh > 0) { pushedCar = true; car.pushT = clock; }"),
  ("          if (sh) { car.x -= ex * sh; car.z -= ez * sh;", "          if (sh) { car.x -= ex * sh; car.z -= ez * sh; car.pushT = clock;"),
  ("    if (pushedCar) { pushedCar = false; updateCarObs(); }", "    if (pushedCar && (!CHAPTER || clock - chObsAt >= 0.25 || clock < chObsAt)) { pushedCar = false; chObsAt = clock; updateCarObs(); }   // c69: 챕터는 0.25초에 한 번"),
  ("    if (obsDirty) updateCarObs();             // 서 있는 차가 밀렸으면 길 찾기 장애물도 다시", "    if (obsDirty) { if (CHAPTER) pushedCar = true; else updateCarObs(); }   // 서 있는 차가 밀렸으면 길 찾기 장애물도 다시 (c69: 챕터는 carCollide 끝에서 모아서)"),
  # (3) 차끼리 부딪힘 — 달리는 차와 방금 밀린 차만 다른 차들과 견준다 (서 있는 차끼리는 안 본다)
  ("    for (let i = 0; i < cars.length; i++) for (let j = i + 1; j < cars.length; j++) {\n      const A = cars[i], B = cars[j];\n      if (Math.hypot(A.x - B.x, A.z - B.z) > CAR_L * 1.6 * Math.max(ckl(A), ckl(B))) continue;",
   "    const live = (c) => c.state !== 'parked' || (c.pushT !== undefined && clock - c.pushT < 0.12 && clock >= c.pushT), act = CHAPTER ? cars.filter(live) : null;\n"
   "    if (act) cars.forEach((c, k) => { c.ix = k; });\n"
   "    for (let i = 0; i < (act ? act.length : cars.length); i++) for (let j = act ? 0 : i + 1; j < cars.length; j++) {\n"
   "      const A = act ? act[i] : cars[i], B = cars[j];\n"
   "      if (act && (B === A || (B.ix < A.ix && live(B)))) continue;   // 둘 다 움직이는 쌍은 한 번만\n"
   "      if (Math.abs(A.x - B.x) > 6 || Math.abs(A.z - B.z) > 6 || Math.hypot(A.x - B.x, A.z - B.z) > CAR_L * 1.6 * Math.max(ckl(A), ckl(B))) continue;"),
  ("      A.x -= nx * best / 2; A.z -= nz * best / 2; B.x += nx * best / 2; B.z += nz * best / 2;", "      A.x -= nx * best / 2; A.z -= nz * best / 2; B.x += nx * best / 2; B.z += nz * best / 2; A.pushT = B.pushT = clock;"),
  ("o.car.g.children[0].material.color.setHex(on ? TARGET_RED : o.car.barr ? 0xffffff : 0x24305a);", "o.car.g.children[0].material.color.setHex(on ? TARGET_RED : o.car.barr ? 0xffffff : o.car.tint0 !== undefined ? o.car.tint0 : o.car.mil ? 0x4a5a32 : 0x24305a);"),
  # 길 찾기 장애물 — 차가 많아져서 합치기를 다시 처음부터 돌지 않게
  ("    for (let merged = true; merged; ) {\n      merged = false;",
   "    if (CHAPTER) {                           // c69: 가까운 것끼리만 합친다 (i가 커지면 그 i만 다시 본다)\n"
   "      for (let i = 0; i < cs.length; i++) for (let j = i + 1; j < cs.length; j++) {\n"
   "        const a = cs[i], b = cs[j], d = Math.hypot(a.x - b.x, a.z - b.z);\n"
   "        if (d >= a.r + b.r + 2 * BODY + 0.2) continue;\n"
   "        if (d + b.r > a.r) { if (d + a.r <= b.r) cs[i] = b; else { const r = (d + a.r + b.r) / 2, t = (r - a.r) / d; cs[i] = { x: a.x + (b.x - a.x) * t, z: a.z + (b.z - a.z) * t, r }; } }\n"
   "        cs.splice(j, 1); j = i;\n"
   "      }\n"
   "      carObs = cs; chCarBoxes = chCarBoxesBuild(); return;\n"
   "    }\n"
   "    for (let merged = true; merged; ) {\n      merged = false;"),
  # 배회 목표 — 서 있는 차 위는 안 뽑는다 · 못 가는 목표는 버리고 새로 뽑는다
  ("      if (a.doors ? !(a.rooms && a.rooms.some((R) => g.x > R.x0 - 0.6 && g.x < R.x1 + 0.6 && g.y > R.z0 - 0.6 && g.y < R.z1 + 0.6)) : freeSpot(g.x, g.y, null)) break;",
   "      if (a.doors ? !(a.rooms && a.rooms.some((R) => g.x > R.x0 - 0.6 && g.x < R.x1 + 0.6 && g.y > R.z0 - 0.6 && g.y < R.z1 + 0.6)) : freeSpot(g.x, g.y, null) && !(CHAPTER && chOnCar(g.x, g.y))) break;"),
  ("      if (d < 0.1) { c.goal = null; c.back = false; c.timer = CHAPTER && !c.gar ? 0 : rand(...IDLE_TIME); }   /* c68 */",
   "      if (CHAPTER && c.goalRef !== c.goal) { c.goalRef = c.goal; c.goalT = clock + d / ((c.back ? WALK_SPEED : CIT_WANDER) * (c.police ? POLICE_PACE : 1)) * 2.5 + 2; c.gkT = clock + 2.5; c.gkX = c.foot.x; c.gkZ = c.foot.z; }   // c69: 이 목표까지 넉넉히 걸릴 시간\n"
   "      if (CHAPTER && clock >= c.gkT) { if (Math.hypot(c.foot.x - c.gkX, c.foot.z - c.gkZ) < 0.3) c.goalT = 0; c.gkT = clock + 2.5; c.gkX = c.foot.x; c.gkZ = c.foot.z; }   // 2.5초 동안 0.3칸도 못 갔다 = 막혔다 → 목표를 버린다\n"
   "      if (d < 0.1 || (CHAPTER && clock > c.goalT)) { c.goal = null; c.back = false; c.timer = CHAPTER && !c.gar ? 0 : rand(...IDLE_TIME); }   /* c68 · c69: 차·물건에 막혀 못 가는 목표는 버린다 */"),
  ("  let carObs = [];", "  function chBoxEscape(px, pz, tx, tz, Q, e, ok) {   // 네모(부딪힘 + 0.26) 둘레 e 안에 붙어 있고 그쪽으로 파고드는 길이면 → 가까운 면의 두 끝 중 목적지까지 더 짧은 끝 [x, z]. 멀어지는 중이면 0, 붙어 있지 않으면 null\n"
   "    if (px <= Q.x0 - e || px >= Q.x1 + e || pz <= Q.z0 - e || pz >= Q.z1 + e) return null;\n"
   "    const dW = px - (Q.x0 - e), dE = Q.x1 + e - px, dN = pz - (Q.z0 - e), dS = Q.z1 + e - pz, k = Math.min(dW, dE, dN, dS), nx = k === dW ? -1 : k === dE ? 1 : 0, nz = nx ? 0 : k === dN ? -1 : 1;\n"
   "    const L0 = Math.hypot(tx - px, tz - pz) || 1e-6;\n"
   "    if ((tx - px) / L0 * nx + (tz - pz) / L0 * nz >= -0.05) return 0;\n"
   "    const o = e + 0.3, c1 = nx ? [nx < 0 ? Q.x0 - o : Q.x1 + o, Q.z0 - o] : [Q.x0 - o, nz < 0 ? Q.z0 - o : Q.z1 + o], c2 = nx ? [c1[0], Q.z1 + o] : [Q.x1 + o, c1[1]];\n"
   "    const cost = (c) => ok(c[0], c[1]) ? Math.hypot(c[0] - px, c[1] - pz) + Math.hypot(tx - c[0], tz - c[1]) : Infinity, d1 = cost(c1), d2 = cost(c2);\n"
   "    return d1 === Infinity && d2 === Infinity ? 0 : d1 <= d2 ? c1 : c2;\n"
   "  }\n"
   "  let carObs = [], chCarBoxes = [], chCarRects = [], chObsAt = 0, chHotDeco = null; const chDecoObjs = [];   // c69: 서 있는 차의 네모 (사람·차가 건물처럼 모서리를 돌아간다)\n"
   "  function chCarBoxesBuild() {             // 서 있는 차(잔해·바리케이트 빼고)의 부딪힘 네모 + 0.1칸. 사이로 몸이 못 지나갈 만큼 붙은 것들은 한 네모로 합친다 (주차 줄 = 긴 네모 하나)\n"
   "    const out = [];\n"
   "    for (const c of cars) { if (c.state !== 'parked' || c.wall || c.wreck) continue;\n"
   "      const L = CAR_L * ckl(c) * PARKED_K / 2, W = CAR_W * ck(c) * PARKED_K / 2, cs = Math.abs(Math.cos(c.h)), sn = Math.abs(Math.sin(c.h)), hx = L * cs + W * sn + 0.26, hz = L * sn + W * cs + 0.26;   // c70: 길 찾기가 0.2칸 더 넓혀 보니까 합쳐서 0.46 — 몸 반지름(0.4)보다 넉넉하게 (끝을 스치지 않게)\n"
   "      out.push({ x0: c.x - hx, z0: c.z - hz, x1: c.x + hx, z1: c.z + hz }); }\n"
   "    chCarRects = out.map((a) => ({ x0: a.x0, z0: a.z0, x1: a.x1, z1: a.z1 }));   // 합치기 전 — 차 하나하나\n"
   "    for (let i = 0; i < out.length; i++) for (let j = i + 1; j < out.length; j++) { const a = out[i], b = out[j];\n"
   "      if (b.x0 - a.x1 >= 0.9 || a.x0 - b.x1 >= 0.9 || b.z0 - a.z1 >= 0.9 || a.z0 - b.z1 >= 0.9) continue;\n"
   "      a.x0 = Math.min(a.x0, b.x0); a.z0 = Math.min(a.z0, b.z0); a.x1 = Math.max(a.x1, b.x1); a.z1 = Math.max(a.z1, b.z1); out.splice(j, 1); j = i; }\n"
   "    for (const a of out) for (const B of buildings) { if (B.parent) continue;   // 벽과 차 사이 좁은 틈(0.9칸 안)은 막힌 걸로 — 네모를 벽까지 늘린다\n"
   "      const ox = Math.min(a.x1, B.x1) - Math.max(a.x0, B.x0), oz = Math.min(a.z1, B.z1) - Math.max(a.z0, B.z0);\n"
   "      if (oz > 0.2) { if (B.x0 >= a.x1 && B.x0 - a.x1 < 0.9) a.x1 = B.x0; else if (a.x0 >= B.x1 && a.x0 - B.x1 < 0.9) a.x0 = B.x1; }\n"
   "      if (ox > 0.2) { if (B.z0 >= a.z1 && B.z0 - a.z1 < 0.9) a.z1 = B.z0; else if (a.z0 >= B.z1 && a.z0 - B.z1 < 0.9) a.z0 = B.z1; } }\n"
   "    return out;\n"
   "  }"),
  ("      const t = segRect(px, pz, tx, tz, B, pad);\n      if (t < first) { first = t; hit = B; }\n    }",
   "      const t = segRect(px, pz, tx, tz, B, pad);\n      if (t < first) { first = t; hit = B; }\n    }\n"
   "    if (CHAPTER && aroundCars) for (const B of chCarBoxes) {   // c69: 서 있는 차도 건물처럼 — 모서리를 돌아간다\n"
   "      if (Math.min(px, tx) > B.x1 + pad || Math.max(px, tx) < B.x0 - pad || Math.min(pz, tz) > B.z1 + pad || Math.max(pz, tz) < B.z0 - pad) continue;\n"
   "      if (px > B.x0 - pad && px < B.x1 + pad && pz > B.z0 - pad && pz < B.z1 + pad) continue;\n"
   "      const t = segRect(px, pz, tx, tz, B, pad);\n      if (t < first) { first = t; hit = B; }\n    }\n"
   "    if (CHAPTER && aroundCars && pad <= GAP) for (const B of chCarRects) {   // c69 · c70: 차에 붙어 있다 — 차 쪽으로 파고드는 길이면 가까운 면의 끝으로 빠져나간다 (끝을 스치며 제자리걸음하던 것)\n"
   "      const w = chBoxEscape(px, pz, tx, tz, B, 0.24, (x, z) => !buildings.some((Q) => !Q.parent && x > Q.x0 - 0.36 && x < Q.x1 + 0.36 && z > Q.z0 - 0.36 && z < Q.z1 + 0.36) && !chCarRects.some((Q) => Q !== B && x > Q.x0 - 0.2 && x < Q.x1 + 0.2 && z > Q.z0 - 0.2 && z < Q.z1 + 0.2));\n"
   "      if (w) return wp.set(w[0], w[1]);\n"
   "    }"),
  ("    for (const O of aroundCars ? carObs : []) {", "    for (const O of aroundCars && !CHAPTER ? carObs : []) {   /* c69: 챕터는 위의 네모로 */"),
  ("    dist[0] = 0;\n    for (;;) {\n      let u = -1;",
   "    dist[0] = 0;\n"
   "    if (CHAPTER && aroundCars) for (let i = 1; i <= 4; i++) {   // c69: 다른 건물 벽 속·다른 차 위에 걸린 모서리로는 안 돌아간다 (집과 차 사이 좁은 틈으로 들어가 끼던 것)\n"
   "      const [cx, cz] = pts[i];\n"
   "      if (buildings.some((B) => B !== hit && !B.parent && cx > B.x0 - 0.36 && cx < B.x1 + 0.36 && cz > B.z0 - 0.36 && cz < B.z1 + 0.36) || chCarBoxes.some((B) => B !== hit && cx > B.x0 - 0.3 && cx < B.x1 + 0.3 && cz > B.z0 - 0.3 && cz < B.z1 + 0.3)) done[i] = true;\n"
   "    }\n"
   "    for (;;) {\n      let u = -1;"),
  ("chSafes(); chDispReset(); chBarReset(); return; }", "chSafes(); chDispReset(); chBarReset(); chDecoPlace(); return; }"),
  ("bar: () => chBar, teams: () => teamWait,", "bar: () => chBar, deco: () => chDeco, bays: () => chBays, civCar: chDecoCarNow, decoObjs: () => chDecoObjs, carObs: () => carObs, carBoxes: () => chCarBoxes, teams: () => teamWait,"),
  ("  function showDud() {", C69B_FN + "  function showDud() {"),
]
