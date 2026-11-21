# c290: 튜토리얼 — 박스는 벽에서 떨어진 네 면 박스 · 탐험 안개 (스타크래프트 1처럼: 안 본 곳 = 검정, 본 적 있는 곳 = 기존 회색 암막, 지금 시야 = 밝음 · 나 + 동료 시야 · 블러 없음)
C290_R = [
  ("{ x: x0 + BS / 2, z: z1 - BS / 2, w: BS, d: BS,", "{ x: x0 + 1 + BS / 2, z: z1 - 1 - BS / 2, w: BS, d: BS,   /* c290: 벽에서 1칸 떨어진 네 면 박스 */"),
  # 튜토리얼 건물은 지붕을 안 쓴다 (가리는 건 탐험 안개가 한다)
  ("      B.open = B.everOpen || B.tkCut || eyeSp.has(B) || B.doors.some(doorSeen);", "      B.open = B.everOpen || B.tkCut || eyeSp.has(B) || B.doors.some(doorSeen) || (CH_TUT && (CH_TUTT.has(B.type) || B.type === 'box'));   /* c290: 튜토리얼은 지붕 대신 탐험 안개 */"),
  ("    const eyes = bodies.filter((b) => isZombie(b) || b === me);", "    const eyes = bodies.filter((b) => isZombie(b) || b === me);\n    if (CH_TUT) chFogTick(eyes);   // c290"),
  ("    if (CH_TUT) chTutFurn();   // c289", "    if (CH_TUT) { chTutFurn(); chFogInit(); }   // c289 · c290"),
  ("  function chTutFurn() {", """  let chFog = null;                           // c290: 탐험 안개 — 0.25칸 칸마다 한 번이라도 시야(나 + 동료)에 들어왔나. 안 들어온 칸은 검정
  function chFogInit() {
    const L = buildings.find((q) => q.type === 'lab'), C = buildings.find((q) => q.type === 'labc'), cs = 0.25, x0 = L.x0 - 30, z0 = C.z0 - 30, w = Math.ceil((L.x1 + 30 - x0) / cs), h = Math.ceil((L.z1 + 30 - z0) / cs);   // 사방 30칸 — 화면 밖까지 검게
    if (!chFog) {
      const data = new Uint8Array(w * h * 4), tex = new THREE.DataTexture(data, w, h, THREE.RGBAFormat); tex.magFilter = tex.minFilter = THREE.NearestFilter;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w * cs, h * cs).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthTest: false, depthWrite: false }));
      m.position.set(x0 + w * cs / 2, 0.05, z0 + h * cs / 2); m.renderOrder = 50; scene.add(m);   // 거의 맨 위 — 안 본 곳은 사람·사물까지 다 가린다
      chFog = { x0, zt: z0 + h * cs, cs, w, h, data, tex, seen: new Uint8Array(w * h), t: 0 };
    }
    const F = chFog; F.data.fill(0); for (let i = 3; i < F.data.length; i += 4) F.data[i] = 255; F.seen.fill(0); F.tex.needsUpdate = true; F.t = -1e9; F.wallN = -1;
  }
  function chFogTick(eyes) {                  // 0.1초마다 — 움직인 눈(0.25칸 넘게)만, 아직 안 본 칸만, 시야 반지름 안에서 벽에 안 가린 칸을 밝힌다
    const F = chFog; if (!F) return; const now = performance.now(); if (now - F.t < 100) return; F.t = now;
    const wn = walls.length, wallsMoved = wn !== F.wallN; F.wallN = wn;   // 벽이 뚫리면 (토막 수가 바뀌면) 다 다시 본다
    let ch = false;
    for (const z of eyes) {
      const R = z.sense, ex = z.foot.x, ez = z.foot.z;
      if (!wallsMoved && z.fogX !== undefined && Math.abs(z.fogX - ex) < 0.25 && Math.abs(z.fogZ - ez) < 0.25) continue; z.fogX = ex; z.fogZ = ez;
      const i0 = Math.max(0, Math.floor((ex - R - F.x0) / F.cs)), i1 = Math.min(F.w - 1, Math.floor((ex + R - F.x0) / F.cs)), j0 = Math.max(0, Math.floor((F.zt - ez - R) / F.cs)), j1 = Math.min(F.h - 1, Math.floor((F.zt - ez + R) / F.cs));
      for (let j = j0; j <= j1; j++) { const cz = F.zt - (j + 0.5) * F.cs;
        for (let i = i0; i <= i1; i++) { const k = j * F.w + i; if (F.seen[k]) continue;
          const cx = F.x0 + (i + 0.5) * F.cs, dx = cx - ex, dz = cz - ez, d = Math.hypot(dx, dz); if (d > R) continue;
          const pl = d > 0.4 ? 0.4 / d : 0; if (blocked(ex, ez, cx - dx * pl, cz - dz * pl)) continue;   // 벽 바로 뒤 0.4칸까지는 밝힌다 (벽 선이 다 보이게)
          F.seen[k] = 1; F.data[k * 4 + 3] = 0; ch = true; } }
    }
    if (ch) F.tex.needsUpdate = true;
  }
  function chTutFurn() {"""),
]
