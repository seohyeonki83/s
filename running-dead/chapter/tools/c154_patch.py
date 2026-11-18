# c154: 성능 — 결과는 그대로 두고 겹치는 계산만 줄인다
#   ① 지붕 열림 · 문틈 시야: 건물마다 좀비 전부를 훑던 것을, 좀비 무리를 감싼 네모 밖의 문은 바로 넘긴다 + 좀비가 든 건물은 미리 한 번 모아 둔다 + 같은 문은 한 프레임에 한 번만 본다
#   ② 벽 부딪힘: 몸마다 건물 전부를 훑던 것을 8칸 격자로 둘레 건물만 본다 (보는 순서는 전과 같게)
C154_R = [
 ("  function draw(dt) {\n", "  let chDrawN = 0;\n  function draw(dt) {\n"),
 ("    eyeMaxR = 0; for (const z of eyes) if (z.sense > eyeMaxR) eyeMaxR = z.sense;\n",
  "    eyeMaxR = 0; for (const z of eyes) if (z.sense > eyeMaxR) eyeMaxR = z.sense;\n"
  "    let eX0 = Infinity, eZ0 = Infinity, eX1 = -Infinity, eZ1 = -Infinity; const eyeSp = new Set(); chDrawN++;   // c154\n"
  "    for (const z of eyes) { const s = z.sense; if (z.foot.x - s < eX0) eX0 = z.foot.x - s; if (z.foot.x + s > eX1) eX1 = z.foot.x + s; if (z.foot.z - s < eZ0) eZ0 = z.foot.z - s; if (z.foot.z + s > eZ1) eZ1 = z.foot.z + s; if (z.space) { eyeSp.add(z.space); if (z.space.parent) eyeSp.add(z.space.parent); } }\n"
  "    const doorSeen = (D) => {                 // 이 문 앞을 보는 좀비가 있나 (전과 같은 판정 — 무리 밖의 문은 바로 넘기고, 한 프레임에 한 번만 잰다)\n"
  "      if (D.seenF === chDrawN) return D.seenV; D.seenF = chDrawN;\n"
  "      const ox = D.cx + D.nx * 0.4, oz = D.cz + D.nz * 0.4;\n"
  "      if (ox < eX0 || ox > eX1 || oz < eZ0 || oz > eZ1) return D.seenV = false;\n"
  "      return D.seenV = eyes.some((z) => (D.out ? z.space === D.out : !z.space) && Math.hypot(z.foot.x - ox, z.foot.z - oz) <= z.sense && !blocked(z.foot.x, z.foot.z, ox, oz));\n"
  "    };\n"),
 ("B.open = B.tkCut || eyes.some((z) => z.space === B || (B.rooms && z.space && z.space.parent === B)) || B.doors.some((D) => { const ox = D.cx + D.nx * 0.4, oz = D.cz + D.nz * 0.4; return eyes.some((z) => (D.out ? z.space === D.out : !z.space) && Math.hypot(z.foot.x - ox, z.foot.z - oz) <= z.sense && !blocked(z.foot.x, z.foot.z, ox, oz)); });",
  "B.open = B.tkCut || eyeSp.has(B) || B.doors.some(doorSeen);   /* c154 */"),
 ("        D.see.visible = eyes.some((z) => (D.out ? z.space === D.out : !z.space) && Math.hypot(z.foot.x - ox, z.foot.z - oz) <= z.sense && !blocked(z.foot.x, z.foot.z, ox, oz));", "        D.see.visible = doorSeen(D);   /* c154 */"),
 ("  const nearW = [];\n  function wallCollide(b) {\n",
  "  let chWcGrid = null, chWcN = 0; const chWcBuf = [];\n"
  "  function chWcNear(x0, z0, x1, z1) {          // c154: 그 네모 둘레의 건물만 (8칸 격자) — 건물 목록 순서 그대로 돌려준다\n"
  "    if (!chWcGrid) { chWcGrid = new Map(); buildings.forEach((B, i) => { B.wcI = i; for (let cx = Math.floor((B.x0 - 1) / 8); cx <= Math.floor((B.x1 + 1) / 8); cx++) for (let cz = Math.floor((B.z0 - 1) / 8); cz <= Math.floor((B.z1 + 1) / 8); cz++) { const k = cx * 4096 + cz; let L = chWcGrid.get(k); if (!L) chWcGrid.set(k, L = []); L.push(B); } }); }\n"
  "    chWcBuf.length = 0; chWcN++;\n"
  "    for (let cx = Math.floor(x0 / 8), cxe = Math.floor(x1 / 8); cx <= cxe; cx++) for (let cz = Math.floor(z0 / 8), cze = Math.floor(z1 / 8); cz <= cze; cz++) { const L = chWcGrid.get(cx * 4096 + cz); if (L) for (let i = 0; i < L.length; i++) { const B = L[i]; if (B.wcF !== chWcN) { B.wcF = chWcN; chWcBuf.push(B); } } }\n"
  "    if (chWcBuf.length > 1) chWcBuf.sort((a, c) => a.wcI - c.wcI);\n"
  "    return chWcBuf;\n"
  "  }\n"
  "  const nearW = [];\n  function wallCollide(b) {\n"),
 ("    for (const B of buildings) if (x1 >= B.x0 && x0 <= B.x1 && z1 >= B.z0 && z0 <= B.z1) for (const w of B.walls) nearW.push(w);", "    for (const B of (CHAPTER && isFinite(x0 + z0 + x1 + z1) ? chWcNear(x0, z0, x1, z1) : buildings)) if (x1 >= B.x0 && x0 <= B.x1 && z1 >= B.z0 && z0 <= B.z1) for (const w of B.walls) nearW.push(w);   /* c154 */"),
 # ③ 성능 표시: 아래쪽 버전 글자를 누르면 초당 프레임 · 계산 시간 · 그리기 시간 · 동료 수가 뜬다 (다시 누르면 꺼진다)
 ("  function frame(now) {\n", "  const chPf = { on: false, n: 0, w: 0, r: 0, t: 0, base: '' };\n  { const rr = renderer.render.bind(renderer); renderer.render = (sc, cam) => { if (!chPf.on) { rr(sc, cam); return; } const t0 = performance.now(); rr(sc, cam); chPf.r += performance.now() - t0; }; }\n  { const v = document.getElementById('ver'); if (v) { v.style.pointerEvents = 'auto'; v.style.padding = '8px 14px'; v.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); if (!chPf.base) chPf.base = v.textContent; chPf.on = !chPf.on; chPf.n = chPf.w = chPf.r = chPf.t = 0; if (!chPf.on) v.textContent = chPf.base; else v.textContent = chPf.base + ' · 재는 중'; }); } }\n  function chPerf(now, w) {                    // c154: 0.5초마다 평균을 버전 글자 옆에 쓴다\n    if (!chPf.on) return;\n    chPf.n++; chPf.w += w; if (!chPf.t) { chPf.t = now; chPf.n = 0; chPf.w = 0; chPf.r = 0; return; }\n    if (now - chPf.t < 500 || !chPf.n) return;\n    const v = document.getElementById('ver'), n = chPf.n;\n    v.textContent = chPf.base + ' · ' + Math.round(n * 1000 / (now - chPf.t)) + 'fps · 계산 ' + ((chPf.w - chPf.r) / n).toFixed(1) + ' · 그리기 ' + (chPf.r / n).toFixed(1) + 'ms · 동료 ' + Math.max(0, zombies.length - 1);\n    chPf.t = now; chPf.n = 0; chPf.w = 0; chPf.r = 0;\n  }\n  function frame(now) {\n"),
 ("    if (!paused) stepWorld(dt);\n    else if (camAnim) stepCamAnim(now);", "    if (!paused) { const t0 = performance.now(); stepWorld(dt); chPerf(now, performance.now() - t0); }\n    else if (camAnim) stepCamAnim(now);"),
]
