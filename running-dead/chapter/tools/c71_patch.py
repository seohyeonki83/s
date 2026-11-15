# c71: 돌아다니는 민간 차 — 구역 안 도로만 돈다 · 좀비를 보면 선다 · 막히면 내린다 · 맞으면 얼어붙고 10~30% 깎이면 내린다
import pathlib
C71_FN = pathlib.Path(__file__).with_name('c71_fn.js').read_text(encoding='utf8')
C71_R = [
  ("    updateCars(dt);                           // 경찰차 달리기·서기·내리기",
   "    if (CHAPTER) chTrafficTick(dt);           // c71: 돌아다니는 민간 차\n    updateCars(dt);                           // 경찰차 달리기·서기·내리기"),
  ("chSafes(); chFurnPlace(); chDispReset(); chBarReset(); chDecoPlace(); return; }", "chSafes(); chFurnPlace(); chDispReset(); chBarReset(); chDecoPlace(); chTrReset(); return; }"),
  # 부딪힘 — 둘레 몸만 본다 · 자는 사람은 그냥 지나간다 (안 보이는 곳) · 느리면 서 있는 차 크기 · 사람은 안 친다 · 좀비는 경찰차와 같은 넉백·데미지
  ("      for (const b of (CHAPTER && car.state === 'parked' ? chNearBodies(car) : bodies)) {\n        if (b.fixed || b.knockT > 0) continue;",
   "      for (const b of (CHAPTER && (car.state === 'parked' || car.tr) ? chNearBodies(car) : bodies)) {\n        if (b.fixed || b.knockT > 0 || (car.tr && b.sleep)) continue;   // c71"),
  ("        const k = car.wall ? (car.wreck ? 0.16 : 1) : car.state === 'parked' ? PARKED_K * (car.wreck ? 0.16 : 1) : MOVING_K;",
   "        const k = car.wall ? (car.wreck ? 0.16 : 1) : car.state === 'parked' || (car.tr && Math.abs(car.vx) + Math.abs(car.vz) < 0.8) ? PARKED_K * (car.wreck ? 0.16 : 1) : car.tr ? 1 : MOVING_K;   /* c73: 달리는 민간 차는 보이는 크기 그대로 (경찰차는 1.22배) */"),
  ("        if (sp > 0.8 && !b.hitT) {            // 치였다",
   "        if (sp > 0.8 && !b.hitT && !(car.tr && (!isZombie(b) || (b.trHit === car && b.trHitT > clock)))) {   /* c71: 민간 차는 사람을 안 친다 · c73: 방금 친 좀비는 3초 동안 다시 안 친다 */            // 치였다"),
  ("          b.knockVX = kx / kl * sp * KNOCK;\n          b.knockVZ = kz / kl * sp * KNOCK;",
   "          const se = car.tr ? CAR_SPEED * Math.min(1, sp / car.tr.spd) : sp;   // c71: 민간 차 — 제 속도로 달리다 치면 경찰차 최고 속도와 같은 넉백·데미지\n          if (car.tr) { b.trHit = car; b.trHitT = clock + 3; }\n          b.knockVX = kx / kl * se * KNOCK;\n          b.knockVZ = kz / kl * se * KNOCK;"),
  ("          const dmg = CAR_HIT_DMG * sp / CAR_SPEED;   // 모두 데미지", "          const dmg = CAR_HIT_DMG * se / CAR_SPEED;   // 모두 데미지"),
  # 시작 자리 — 순환도로 바로 안쪽 (도로 위에서 시작하면 첫 차가 곧바로 내 앞에 서서 사람을 내린다)
  ("q = Math.random() * 2 * (W + H), j = rand(0, 3.5);", "q = Math.random() * 2 * (W + H), j = CH_MAP.ring - 1.7 + rand(0, 2.7);   /* c71: 가장자리에서 5.3~8칸 = 순환도로를 0.8칸 넘게 벗어난 안쪽 */"),
  ("      if (chNearRiver(x, z, 2) || buildings.some((B) => x > B.x0 - 1.5 && x < B.x1 + 1.5 && z > B.z0 - 1.5 && z < B.z1 + 1.5) || cop(x, z) || !far(x, z)) continue;",
   "      if (chNearRiver(x, z, 2) || buildings.some((B) => x > B.x0 - 1.5 && x < B.x1 + 1.5 && z > B.z0 - 1.5 && z < B.z1 + 1.5) || cop(x, z) || !far(x, z)) continue;\n"
   "      if (CH_MAP.roads.some(([a, b, c, d]) => x > a - 0.8 && x < c + 0.8 && z > b - 0.8 && z < d + 0.8)) continue;   // c71: 도로 위(와 바로 옆)는 뺀다"),
  # 탄 채로 부서지면 먼저 내린다
  ("      const c = o.car;\n      c.wreck = true;", "      const c = o.car;\n      if (CHAPTER && c.tr && c.tr.mode !== 'left') chTrExit(c);   // c71: 탄 채로 부서지면 먼저 내린다\n      c.wreck = true;"),
  # 성능 — 먼 문은 거리를 재기 전에 거른다 (좀비마다 문 480개의 가장 가까운 점을 구하던 것)
  ("      if (o.type === 'car' && (Math.abs(o.car.x - z.foot.x) > z.sense + 2 || Math.abs(o.car.z - z.foot.z) > z.sense + 2)) continue;   // c59",
   "      if (o.type === 'car' && (Math.abs(o.car.x - z.foot.x) > z.sense + 2 || Math.abs(o.car.z - z.foot.z) > z.sense + 2)) continue;   // c59\n"
   "      if (CHAPTER && o.type === 'door' && (Math.abs(o.L.cx - z.foot.x) > z.sense + 3.5 || Math.abs(o.L.cz - z.foot.z) > z.sense + 3.5)) continue;   // c71: 인지거리보다 먼 문 (문 반폭 여유 3.5칸)"),
  # 달리는 차는 '길을 막는 차'로도 안 친다
  ("for (const o of OL) if (o.type === 'car' && !o.dead && Math.abs(o.car.x - z.foot.x) < 4", "for (const o of OL) if (o.type === 'car' && !o.dead && !o.off && Math.abs(o.car.x - z.foot.x) < 4"),
  ("bar: () => chBar, furn:", "bar: () => chBar, tr: () => chTr, roadG: () => chRoadG, trSpawn: chTrSpawn, trExit: chTrExit, trReset: chTrReset, trOff: () => { for (const c of chTr.cars) { chTrGone(c); c.tr.mode = 'gone'; } chTr.cars.length = 0; for (const Z of chTr.Z) { Z.n = 0; Z.want = 0; } }, furn:"),
  ("  function showDud() {", C71_FN + "  function showDud() {"),
]
