# c122: 특공대 = 시간으로 (난리남부터 2분마다 4번, 수상함 3분이면 강제) · 5번째 = 보스 (군부대 장갑차) · 경보 수상함 5 / 난리남 30
import pathlib
BLOCK = pathlib.Path(__file__).with_name('c122_block.js').read_text(encoding='utf8')
C122_R = [
 # 경보 단계: 수상함 5 · 난리남 30 (그 뒤는 그대로)
 ("for (let i = 1; i < STAR_AT.length; i++) STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3 * 1.05 * 0.8);",
  "for (let i = 1; i < STAR_AT.length; i++) STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3 * 1.05 * 0.8); STAR_AT[0] = 5; STAR_AT[1] = 30;   /* c122: 수상함 5 · 난리남 30 → [5, 30, 164, 367, 791] */"),
 # 감염 수로 부르던 특공대는 끈다 (시간으로 온다)
 ("{ const EV = CHAPTER ? CH_TEAM_EVENTS : TEAM_EVENTS;", "if (!CHAPTER) { const EV = CHAPTER ? CH_TEAM_EVENTS : TEAM_EVENTS;"),
 ("    while (teamQueue.length) queueSquads(teamQueue.shift());", "    if (CHAPTER) chSfTick(dt);   // c122\n    while (teamQueue.length) queueSquads(teamQueue.shift());"),
 ("if (w.car) { const p = teamSpot(w.seg); addCar(p.x, p.z, Math.atan2(me.foot.z - p.z, me.foot.x - p.x), null, 0, w.car); }",
  "if (w.boss) chBossSpawn(w.seg); else if (w.car) { const p = teamSpot(w.seg); addCar(p.x, p.z, Math.atan2(me.foot.z - p.z, me.foot.x - p.x), null, 0, w.car); if (w.tk) cars[cars.length - 1].tkWave = true; }"),
 ("deaths = stars = dispatchT = 0; teamIdx = 0; teamQueue.length = 0; teamWait.length = 0;", "deaths = stars = dispatchT = 0; teamIdx = 0; teamQueue.length = 0; teamWait.length = 0; if (CHAPTER) chSfReset();"),
 # 알림: 특공대 출동 / 군부대 출동 (보스)
 ("el.innerHTML = '<div class=\"rbox\"><div class=\"rt\">특수부대 출동</div></div>';",
  "el.innerHTML = CHAPTER && chBanner.shift() === 'boss' ? '<div class=\"rbox\"><div class=\"rt\">군부대 출동</div><div class=\"rd\" style=\"color:#ff4a3a\">보스</div></div>' : '<div class=\"rbox\"><div class=\"rt\">특공대 출동</div></div>';"),
 ("    teamsSpawned++;                            // '특수부대 출동' 알림 한 번", "    teamsSpawned++; chBanner.push('sf');                            // '특공대 출동' 알림 한 번"),
 ("  function chQueueTeam(i) {\n", BLOCK + "  function chQueueTeam(i) {\n"),
 # 보스 뒤에 온 군인차에서 내린 사람 = 잡아야 할 사람
 ("if (t === 'sniper') sn = c; else if (CHAPTER && !sn) c.noMaster = true;", "if (car.tkWave) c.tkU = true; if (t === 'sniper') sn = c; else if (CHAPTER && !sn) c.noMaster = true;"),
 # 호위
 ("if (CHAPTER && (c.gar || c.noMaster)) { c.master = null; return null; }", "if (CHAPTER && (c.gar || c.noMaster)) { c.master = null; return null; } if (CHAPTER && c.tkE) return chTankMaster(c);   /* c122 */"),
 ("<= GUARD_DOMAIN) c.recall = false;", "<= GUARD_DOMAIN * (m.tank ? CH_TK_ESC : 1)) c.recall = false;"),
 ("let tx = m.foot.x + Math.cos(c.slotA) * GUARD_NEAR * c.slotK, tz = m.foot.z + Math.sin(c.slotA) * GUARD_NEAR * c.slotK;",
  "const ek = m.tank ? CH_TK_ESC : 1; let tx = m.foot.x + Math.cos(c.slotA) * GUARD_NEAR * ek * c.slotK, tz = m.foot.z + Math.sin(c.slotA) * GUARD_NEAR * ek * c.slotK;"),
 ("const lim = c.inRange ? GUARD_DOMAIN_FIGHT : GUARD_DOMAIN;", "const lim = (c.inRange ? GUARD_DOMAIN_FIGHT : GUARD_DOMAIN) * (m.tank ? CH_TK_ESC : 1);"),
 ("if (c.soldier && soldierLeash(c, dt)) { moveShoot(c, dt); return; }", "if ((c.soldier || c.tkE) && soldierLeash(c, dt)) { moveShoot(c, dt); return; }"),
 ("} else if (c.soldier && masterOf(c)) {", "} else if ((c.soldier || c.tkE) && masterOf(c)) {"),
 # 장갑차 몰기 · 건물은 산만 막는다
 ("      if (car.state === 'drive') {\n        let zombie = false;", "      if (car.tank) chTankDrive(car, dt);   // c122\n      if (car.state === 'drive') {\n        let zombie = false;"),
 ("      for (const B of buildings) {            // 혹시 건물에 파고들면 가장 가까운 벽 밖으로\n", "      for (const B of buildings) {            // 혹시 건물에 파고들면 가장 가까운 벽 밖으로\n        if (car.tank && B.type !== 'hill') continue;   // c122: 장갑차는 벽을 부순다 (chTankWalls)\n"),
 (": CAR_SPEED * (car.mil ? 2 / 3 : 1), vmax = base * car.loadK;", ": car.tank ? car.tkV : CAR_SPEED * (car.mil ? 2 / 3 : 1), vmax = base * car.loadK;"),
 # 사물 · 차를 깔아뭉갠다
 ("if (b.fixed) { if (CHAPTER && b.out) chCarSmash(car, b, fx, fz, rx, rz); continue; }", "if (car.tank && (b.fixed || b.prop || b.kind === 'safe')) { chTankCrush(car, b, fx, fz, rx, rz); continue; }   /* c122 */ if (b.fixed) { if (CHAPTER && b.out) chCarSmash(car, b, fx, fz, rx, rz); continue; }"),
 ("A.x -= nx * best / 2; A.z -= nz * best / 2; B.x += nx * best / 2; B.z += nz * best / 2; A.pushT = B.pushT = clock;",
  "{ const wA = A.tank ? 0 : B.tank ? 1 : 0.5; A.x -= nx * best * wA; A.z -= nz * best * wA; B.x += nx * best * (1 - wA); B.z += nz * best * (1 - wA); } A.pushT = B.pushT = clock; if (A.tank || B.tank) chTankCar(A.tank ? B : A);   /* c122: 장갑차는 안 밀린다 · 닿은 차는 부서진다 */"),
 ("      c.wreck = true;\n      if (CHAPTER && c.loot) chLootDrop(c);", "      c.wreck = true;\n      if (c.tank) chTankDead(c);   // c122\n      if (CHAPTER && c.loot) chLootDrop(c);"),
 # 산성
 ("    killZombie(z);                            // 자폭한 동료는 죽는다", "    if (CHAPTER && chTank && !chTank.wreck && Math.hypot(chTank.x - x, chTank.z - zz) <= R + 1.4) chTankGoo(chTank);   // c122\n    killZombie(z);                            // 자폭한 동료는 죽는다"),
 # 체력바 한 줄 · 총알 선 · 지붕 · 시야 · 벽 그림
 ("if (M <= C + 1e-6) { b.hpFill.scale.x", "if (M <= C + 1e-6 || b.oneBar) { b.hpFill.scale.x"),
 ("    drawCars(eyes);\n", "    drawCars(eyes);\n    if (CHAPTER) chTankDraw(dt);   // c122\n"),
 ("B.open = eyes.some((z) => z.space === B", "B.open = B.tkCut || eyes.some((z) => z.space === B"),
 ("  function rebuildSight(B) {\n    if (!(B.parent || B.rooms)) { rebuildSight0(B); return; }",
  "  function rebuildSight(B) {                   // c122: 장갑차가 벽을 뚫은 건물은 남은 벽 토막으로\n    rebuildSightA(B);\n    if (B.tkCut) chSightCut(B);\n    if (B.parent && B.parent.tkCut) chSightCut(B.parent);\n  }\n  function rebuildSightA(B) {\n    if (!(B.parent || B.rooms)) { rebuildSight0(B); return; }"),
 ("for (const [ax, az, bx, bz] of buildings.flatMap((B) => (B.type === 'hill' || B.parent ? [] : B.walls))) flat(Math.abs(bx - ax) + WALL, Math.abs(bz - az) + WALL, (ax + bx) / 2, (az + bz) / 2, wallMat, -0.505);",
  "for (const sg of buildings.flatMap((B) => (B.type === 'hill' || B.parent ? [] : B.walls))) { const [ax, az, bx, bz] = sg; sg.m = flat(Math.abs(bx - ax) + WALL, Math.abs(bz - az) + WALL, (ax + bx) / 2, (az + bz) / 2, wallMat, -0.505); }   /* c122: 벽 토막마다 그림을 기억한다 (뚫리면 지운다) */"),
 # 승리
 ("if (stationDown && !victoryOn) { showVictory(); return; }", "if ((stationDown || (CHAPTER && chSf.won)) && !victoryOn) { showVictory(); return; }"),
 ("<div class=\"vs\">경찰서 ' + stations.length + '곳 전부 박살", "<div class=\"vs\">' + (CHAPTER && chSf.won ? '군부대 전멸' : '경찰서 ' + stations.length + '곳 전부 박살') + '"),
]
