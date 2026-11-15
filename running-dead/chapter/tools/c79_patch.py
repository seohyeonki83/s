# c79: 횡단보도 (꾸밈) · 달리는 차와 몸의 진짜 물리 — 치이면 뜨지 않고 바닥으로 밀린다 · 데미지는 처음 부딪힌 순간에만 (밀고 드는 빠르기에 비례)
#      그 뒤로는 밀리기만 한다 (범퍼 앞에 끼면 끌려간다) · 앞을 막은 몸들의 무게만큼 차가 느려지고, 차의 미는 힘을 넘으면 못 간다 (덩치는 6.93명 몫)
import pathlib
C79_FN = pathlib.Path(__file__).with_name('c79_fn.js').read_text(encoding='utf8')
C79_R = [
  # ── 횡단보도: 대로가 다른 길과 만나는 곳마다, 대로를 가로질러 (구역 안 큰 네거리 4 + 순환도로와 만나는 끝마다 1) ──
  ("    for (const [P, mat, o] of [[pos, lineMat, -0.89], [dp, dashMat, -0.895]]) { if (!P.length) continue;",
   "    const zebraMat = new THREE.MeshBasicMaterial({ color: 0xf3f3ef, transparent: true, opacity: 0.74, depthTest: false, depthWrite: false }), zp = [];   // c79: 횡단보도 — 꾸밈만 (아무 일도 안 한다)\n"
   "    const zq = (x0, z0, x1, z1) => zp.push(x0, 0, z0, x0, 0, z1, x1, 0, z1, x0, 0, z0, x1, 0, z1, x1, 0, z0);\n"
   "    const zebra = (alongZ, c, hw, at) => {   // alongZ = 길이 z쪽으로 뻗는다 (건너는 쪽 = x). c·hw = 그 길 한가운데·반폭, at = 횡단보도 한가운데 (길 방향)\n"
   "      let lo = c - hw, hi = c + hw;          // 그 자리에서 길이 더 넓으면 (다리 앞 넓은 길) 그 폭까지\n"
   "      for (const [a, b, c2, d] of CH_MAP.roads) { if (alongZ ? (at > b && at < d && c > a && c < c2 && d - b < 40) : (at > a && at < c2 && c > b && c < d && c2 - a < 40)) { lo = Math.min(lo, alongZ ? a : b); hi = Math.max(hi, alongZ ? c2 : d); } }\n"
   "      const n = Math.floor((hi - lo - 0.5) / 0.62), q0 = (lo + hi) / 2 - (n * 0.62 - 0.32) / 2;\n"
   "      for (let k = 0; k < n; k++) { const q = q0 + k * 0.62; alongZ ? zq(q, at - 0.7, q + 0.3, at + 0.7) : zq(at - 0.7, q, at + 0.7, q + 0.3); }\n"
   "      chZebras.push(alongZ ? [lo, at - 0.7, hi, at + 0.7] : [at - 0.7, lo, at + 0.7, hi]);\n"
   "    };\n"
   "    for (const G of chRoadGraphs()) { const nV = G.V.length, nH = G.H.length;\n"
   "      for (let i = 1; i < nV - 1; i++) for (let j = 0; j < nH; j++) { const v = G.V[i], h = G.H[j], d = h.hw + 1.25; if (j > 0) zebra(true, v.c, v.hw, h.c - d); if (j < nH - 1) zebra(true, v.c, v.hw, h.c + d); }\n"
   "      for (let j = 1; j < nH - 1; j++) for (let i = 0; i < nV; i++) { const h = G.H[j], v = G.V[i], d = v.hw + 1.25; if (i > 0) zebra(false, h.c, h.hw, v.c - d); if (i < nV - 1) zebra(false, h.c, h.hw, v.c + d); }\n"
   "    }\n"
   "    for (const [P, mat, o] of [[pos, lineMat, -0.89], [dp, dashMat, -0.895], [zp, zebraMat, -0.893]]) { if (!P.length) continue;"),
  ("  const CH_BAY_PITCH = 1.95, CH_BAY_LEN = 2.5;", "  const chZebras = [];   // c79: 횡단보도 자리 (네모)\n  const CH_BAY_PITCH = 1.95, CH_BAY_LEN = 2.5;"),
  # ── 물리 ──
  ("        if (b.fixed || b.knockT > 0 || (car.tr && b.sleep)) continue;   // c71",
   "        if (b.fixed || (car.tr && b.sleep)) continue;   // c71\n"
   "        if (b.knockT > 0 && (!CHAPTER || b.gar)) continue;   // c79: 미끄러지는 몸도 차에 걸린다 (통과하지 않는다)"),
  ("        if (sp > 0.8 && !b.hitT && !(car.tr && ((!isZombie(b) && !chBlind(b)) || (b.trHit === car && b.trHitT > clock)))) {",
   "        const mov = CHAPTER && car.state !== 'parked' && !car.barr && !car.wall;   // c79: 달리는 차 (민간 차 · 경찰차 · 군인차)\n"
   "        if (mov) { car.ldT = clock + 0.6; chCarHit(car, b, u, v, hu, hv, fx, fz, rx, rz, sp); }\n"
   "        else if (sp > 0.8 && !b.hitT && !(car.tr && ((!isZombie(b) && !chBlind(b)) || (b.trHit === car && b.trHitT > clock)))) {"),
  ("        b.foot.x = nx;\n        b.foot.z = nz;\n      }\n    }\n    if (pushedCar",
   "        b.foot.x = nx;\n        b.foot.z = nz;\n"
   "        if (mov && u > 0 && sp > 1.5 && Math.abs(v) < hv) chSkid(b, chDt);   // c79: 범퍼에 끌려간다\n"
   "      }\n"
   "      if (CHAPTER && car.state !== 'parked' && !car.barr && !car.wall && !car.wreck && (car.load > 0 || clock < car.ldT)) chCarLoad(car, fx, fz); else if (car.load) { car.load = 0; car.loadK = 1; }   // c79\n"
   "    }\n    if (pushedCar"),
  # 치여 미끄러지는 몸 — 먼지
  ("    b.vel.set(b.knockVX, b.knockVZ);\n    const f = Math.exp(-4 * dt);",
   "    b.vel.set(b.knockVX, b.knockVZ);\n    if (b.knockCar) chSkid(b, dt);   // c79\n    const f = Math.exp(-4 * dt);"),
  ("      b.knockT = 0; b.knockSlide = false;", "      b.knockT = 0; b.knockSlide = false; b.knockCar = false;"),
  # 경찰차·군인차도 앞을 막은 무게만큼 느려진다
  ("            const sp = CAR_SPEED * (car.mil ? 2 / 3 : 1);   // v447: 군인차는 1/3 느리다",
   "            const sp = CAR_SPEED * (car.mil ? 2 / 3 : 1) * (car.loadK ?? 1);   /* c79 */   // v447: 군인차는 1/3 느리다"),
  # 민간 차 운전자 — 무게만큼 느려지고, 꽉 막혀 못 가면 좀비에 막힌 것으로 친다 (서서 3~5초 뒤 내린다)
  ("    const halt = zMid || hMid || T.hitT > 0;", "    const held = car.load > 0 && car.loadK < 0.4 && sp < 1;   // c79: 몸들에 막혀 못 간다\n    const halt = zMid || hMid || T.hitT > 0 || held;"),
  ("    if (halt && T.mode !== 'stop') { T.resume = T.mode; T.mode = 'stop'; T.clearT = 0; T.swT = 0; T.swLat = null; }",
   "    if (car.load > 0) want *= car.loadK;   // c79: 앞을 막은 몸들 무게만큼 느려진다\n"
   "    if (halt && T.mode !== 'stop') { T.resume = T.mode; T.mode = 'stop'; T.clearT = 0; T.swT = 0; T.swLat = null; }"),
  ("    if (T.mode === 'stop') { if (sp < 0.6 && (zMid || T.hitT > 0) && (T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }   /* c78: 사람 때문에 선 시간은 안 센다 */",
   "    if (T.mode === 'stop') { if (sp < 0.6 && (zMid || T.hitT > 0 || held) && (T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }   /* c78: 사람 때문에 선 시간은 안 센다 · c79: 몸들에 막힌 시간은 센다 */"),
  ("  function chTrafficTick(dt) {\n    if (!chTr) return;", "  function chTrafficTick(dt) {\n    chDt = dt;   // c79\n    if (!chTr) return;"),
  ("bar: () => chBar, tr: () => chTr,", "bar: () => chBar, zebras: () => chZebras, carLoad: chCarLoad, carCap: chCarCap, carW: chCarW, tr: () => chTr,"),
  ("  function showDud() {", C79_FN + "  function showDud() {"),
]
