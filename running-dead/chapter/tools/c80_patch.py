# c80: 물음표 수송차 3종 (현금 수송차 · 구급차 · 택배차 — 차가 생길 때 30분의 1, 싣는 가짓수에 비례) · 부수면 아이템 + 경찰 출동
#      운전자 성격 4종과 패닉 (밟기 · 후진했다 다시 들이밀기 · 좀비 무시) · 기본 속도 차마다 다르게 (지금 속도 ~ 1.25배) · 오래 돈 차는 눈 밖에서 새 차로 바뀐다
import pathlib
C80_FN = pathlib.Path(__file__).with_name('c80_fn.js').read_text(encoding='utf8')
C80_R = [
  # ── 차종: 현금 수송차 · 택배차 ──
  ("    ambul:   { name: '구급차', kl: 1.3, kw: 1.3, hp: 1.3, mass: 1.4, col: [0xf6f6f4] },\n  };",
   "    ambul:   { name: '구급차', kl: 1.3, kw: 1.3, hp: 1.3, mass: 1.4, col: [0xf6f6f4] },\n"
   "    cash:    { name: '현금 수송차', kl: 1.3, kw: 1.3, hp: 1.3, mass: 1.4, col: [0x55615a] },   // c80: 크기·체력·무게는 밴(구급차)과 똑같다 — 새로 지어내지 않는다\n"
   "    parcel:  { name: '택배차', kl: 1.58, kw: 1.36, hp: 1.8, mass: 2.2, col: [0xd9a020, 0x2f6fb0, 0xc8452c] },   // c80: 크기·체력·무게는 트럭과 똑같다\n  };"),
  ("    rr(2, 4, 252, 120, type === 'truck' || type === 'fire' ? 10 : 24, '#0c0c0e');",
   "    rr(2, 4, 252, 120, type === 'truck' || type === 'fire' || type === 'cash' || type === 'parcel' ? 10 : 24, '#0c0c0e');"),
  ("    } else if (type === 'ambul') {",
   "    } else if (type === 'cash') {             // c80: 현금 수송차 — 각진 장갑 몸통, 지붕 판과 해치, 노란 띠, 좁은 앞유리\n"
   "      rr(6, 8, 244, 112, 8, mix(col, 0)); g.fillStyle = mix(col, -0.32); g.fillRect(8, 14, 240, 6); g.fillRect(8, 108, 240, 6);\n"
   "      rr(22, 26, 150, 76, 6, mix(col, 0.16)); g.strokeStyle = 'rgba(0, 0, 0, 0.38)'; g.lineWidth = 3; g.strokeRect(40, 40, 60, 48); g.beginPath(); g.moveTo(70, 40); g.lineTo(70, 88); g.stroke();\n"
   "      g.fillStyle = '#e8c33a'; g.fillRect(120, 26, 11, 76);\n"
   "      rr(196, 22, 36, 84, 6, GL); rr(202, 30, 12, 68, 3, mix(col, 0.1)); g.fillStyle = '#ff9d1a'; g.fillRect(182, 54, 8, 20); lamps(16, 92);\n"
   "    } else if (type === 'parcel') {           // c80: 택배차 — 상자 짐칸 (테이프 십자) + 앞 운전석\n"
   "      rr(6, 8, 172, 112, 6, '#b98a4e'); g.fillStyle = '#ead9ae'; g.fillRect(84, 8, 14, 112); g.fillRect(6, 57, 172, 14); g.strokeStyle = 'rgba(0, 0, 0, 0.28)'; g.lineWidth = 3; g.strokeRect(8, 10, 168, 108);\n"
   "      rr(184, 12, 66, 104, 12, mix(col, 0)); rr(204, 20, 32, 88, 8, GL); rr(210, 28, 13, 72, 4, mix(col, 0.16)); lamps(18, 90);\n"
   "    } else if (type === 'ambul') {"),
  ("  const CH_TR_SPD = { compact: 0.62, sedan: 0.62, sports: 0.74, van: 0.55, truck: 0.48 };",
   "  const CH_TR_SPD = { compact: 0.62, sedan: 0.62, sports: 0.74, van: 0.55, truck: 0.48, ambul: 0.72, cash: 0.55, parcel: 0.48 };   /* c80: 구급차는 조금 빠르다 · 현금 수송차 = 밴 속도 · 택배차 = 트럭 속도 */"),
  # ── 생길 때: 수송차 뽑기 · 속도 · 운전자 ──
  ("      const type = chCarPick(), car = chCivCar(type, x, z, Math.atan2(g.d1z, g.d1x)), spd = CAR_SPEED * CH_TR_SPD[type], who = [];",
   "      const F = window.__trForce || null, loot = F && F.loot !== undefined ? F.loot : chLootRoll();   // c80: 30대 중 1대는 수송차\n"
   "      const type = loot || (F && F.type) || chCarPick(), car = chCivCar(type, x, z, Math.atan2(g.d1z, g.d1x)), spd = CAR_SPEED * CH_TR_SPD[type] * rand(1, CH_TR_FAST), who = [];"),
  ("      chTr.cars.push(car); return car;",
   "      if (loot === 'cash') { who.length = 0; who.push('guard', 'guard'); } else if (loot === 'ambul') { who.length = 0; who.push('', ''); }   // c80: 현금 수송차 = 경비 둘 · 구급차 = 구급대원 둘\n"
   "      chTrDriver(car, loot);\n"
   "      chTr.cars.push(car); return car;"),
  # ── 운전 ──
  ("    if (o.hp < T.hp) { T.hp = o.hp; T.hitT = 2; }     // 맞았다 → 얼어붙는다",
   "    if (o.hp < T.hp) { T.hp = o.hp; if (T.drv === 'calm') T.hitT = 2; else chTrPanic(T, rand(6, 10)); }     // 맞았다 → 조심형은 얼어붙고, 나머지는 패닉 (c80)"),
  ("    if (T.hitT > 0) T.hitT -= dt;\n",
   "    if (T.hitT > 0) T.hitT -= dt;\n"
   "    // c80: 패닉 — 가속형·돌진형은 냅다 밟고 (아무도 안 가린다 = rage), 비비기형은 물러났다가 옆으로 다시 들이민다\n"
   "    if (car.lastHit > T.seenHit) { T.seenHit = car.lastHit; chTrPanic(T, rand(5, 9)); }   // 누굴 쳤다\n"
   "    if (T.panicT > 0) T.panicT -= dt;\n"
   "    const panic = T.panicT > 0, rage = panic && (T.drv === 'floor' || T.drv === 'ram'); T.rage = rage; T.spdK = rage ? T.pk : panic ? 1.12 : 1;\n"
   "    if (rage) { if ((T.wvT -= dt) <= 0) { T.wvT = rand(0.5, 1.1); T.wv = rand(-0.45, 0.45); } if (sp > 2) chTrSmoke(car, T, dt); } else if (!T.wig) T.wv = 0;   // 밟는 동안은 좌우로 휘청거린다\n"
   "    if (T.wig && T.wig.ph === 'back') {        // 후진 — 뒤가 막혔거나 시간이 다 되면 다시 앞으로\n"
   "      const fx0 = Math.cos(car.h), fz0 = Math.sin(car.h);\n"
   "      if ((T.wig.t -= dt) <= 0 || chTrBehind(car, fx0, fz0)) { T.wig.ph = 'fwd'; T.wig.t = rand(1.3, 1.9); T.wig.x = car.x; T.wig.z = car.z; car.rev = false; T.mode = 'go'; T.clearT = 0; }\n"
   "      else { car.rev = true; carSteer(car, -fx0 * 2.2, -fz0 * 2.2, 10 * dt); return; }\n"
   "    }\n"
   "    const surge = !!T.wig;                     // 다시 들이미는 중 — 안 선다\n"
   "    if (surge && (T.wig.t -= dt) <= 0) { if (Math.hypot(car.x - T.wig.x, car.z - T.wig.z) > 2.5) T.wigN = 0; T.wig = null; T.wv = 0; }\n"),
  ("    const look = 2 + sp * 0.3, sa = s + look, lat = g.o1 + T.off;", "    const look = 2 + sp * 0.3, sa = s + look, lat = g.o1 + T.off + T.wv;   /* c80: 휘청 · 들이밀 옆자리 */"),
  ("    if ((T.scanT -= dt) <= 0) {                // 가려는 쪽 앞길을 막는 것",
   "    if (zL && zR && !zMid) zMid = true;        // c80: 양옆에 다 있다 → 비켜 갈 데가 없다 = 가운데가 막힌 것과 같다 (조심형은 선다)\n"
   "    if (T.drv === 'ram' || rage || surge) {     // c80: 돌진형 · 밟는 중 · 다시 들이미는 중 — 가운데 좀비에도 안 선다 (돌진형은 비켜 가지도 않는다, 나머지는 한쪽으로 비켜 가려 한다)\n"
   "      if (zMid || hMid) { if (T.drv !== 'ram') { if (T.swSide === undefined || clock - (T.swSideAt || 0) > 2) T.swSide = Math.random() < 0.5; T.swSideAt = clock; if (T.swSide) zL = true; else zR = true; } zMid = false; hMid = false; }\n"
   "      if (T.drv === 'ram') { zL = false; zR = false; }\n"
   "    }\n"
   "    if ((T.scanT -= dt) <= 0) {                // 가려는 쪽 앞길을 막는 것"),
  ("        if (b.sleep || b.space || chBlind(b)) continue;   // c78: 도망·싸움 중인 사람은 미리 못 본다 (띠에 들어와야 본다)",
   "        if (rage || b.sleep || b.space || chBlind(b)) continue;   // c78: 도망·싸움 중인 사람은 미리 못 본다 (띠에 들어와야 본다) · c80: 밟는 중엔 사람도 안 가린다"),
  ("    const halt = zMid || hMid || T.hitT > 0 || held;",
   "    const halt = !surge && (zMid || hMid || T.hitT > 0 || (held && T.drv === 'calm'));\n"
   "    // c80: 좀비 앞에 섰거나 몸들에 막혔을 때 — 가속형은 조금 뒤 (0.4~1.5초) 냅다 밟고, 비비기형은 물러났다가 옆으로 다시 들이민다. 밟아도 못 가면 가속형·돌진형도 물러났다가 들이민다. 몇 번 해도 안 되면 내린다\n"
   "    if (T.drv !== 'calm' && !surge) {\n"
   "      const jam = (zMid && sp < 0.5) || held || (rage && sp < 0.4 && car.load > 0);\n"
   "      if (jam) T.nerveT += dt; else T.nerveT = Math.max(0, T.nerveT - dt * 2);\n"
   "      if (T.nerveT >= T.nerve) { T.nerveT = 0;\n"
   "        if (T.drv === 'floor' && !panic && !held) chTrPanic(T, rand(6, 10));\n"
   "        else if (T.wigN >= T.wigMax) { chTrExit(car); return; }\n"
   "        else { T.wigN++; chTrPanic(T, rand(6, 10)); T.wig = { ph: 'back', t: rand(0.5, 0.9) }; T.wv = Math.max(limL, Math.min(limR, latNow + (Math.random() < 0.5 ? -1 : 1) * rand(0.5, 1))) - T.off; T.swT = 0; T.swLat = null; return; }\n"
   "      }\n"
   "    }"),
  ("    let want = T.spd;                          // 내고 싶은 속도", "    let want = T.spd * (surge ? Math.max(T.spdK, 1.3) : T.spdK);   /* c80: 패닉 중엔 더 밟는다 */                          // 내고 싶은 속도"),
  ("    if (g.turn && sc - s < 3.5) want *= 0.55;", "    if (want > CAR_SPEED * CH_TR_RAGE_MAX) want = CAR_SPEED * CH_TR_RAGE_MAX;\n    if (g.turn && sc - s < 3.5) want *= rage ? 0.72 : 0.55;"),
  ("    else carSteer(car, ux * want, uz * want, CH_TR_ACC * dt);\n  }", "    else carSteer(car, ux * want, uz * want, CH_TR_ACC * (rage || surge ? 1.5 : 1) * dt);\n  }"),
  # 오래 돈 차는 내 눈 밖에서 떠난다 (새 차가 들어온다 → 수송차가 나올 기회가 계속 생긴다)
  ("      chTrDrive(car, T, dt);\n    }\n  }",
   "      if (T.mode === 'go' && clock - T.born > T.life && (T.lifeT -= dt) <= 0) { T.lifeT = 1; if (!chTrSeen(car.x, car.z, 6)) { chTrGone(car); T.mode = 'gone'; T.swap = true; continue; } }   // c80\n"
   "      chTrDrive(car, T, dt);\n    }\n  }"),
  ("Z.n--; Z.want = 3 + (Math.random() < 0.5 ? 1 : 0); Z.t = rand(8, 16); continue; }", "Z.n--; Z.want = 3 + (Math.random() < 0.5 ? 1 : 0); Z.t = T.swap ? rand(1, 4) : rand(8, 16); continue; }   /* c80: 떠난 차 자리는 곧 새 차가 채운다 */"),
  ("      if (Math.hypot(car.vx, car.vz) > 0.3) car.h = Math.atan2(car.vz, car.vx);   // 앞 = 가는 쪽",
   "      if (!car.rev && Math.hypot(car.vx, car.vz) > 0.3) car.h = Math.atan2(car.vz, car.vx);   /* c80: 후진 중엔 머리를 안 돌린다 */   // 앞 = 가는 쪽"),
  # 물리 쪽: 밟는 차는 평소 상태의 사람도 친다 · 후진 중엔 앞에 걸린 무게를 안 따진다
  ("    if (car.tr && !isZombie(b) && !chBlind(b)) return;             // 평소 상태의 사람은 민간 차가 안 친다 (미리 보고 선다 — 닿아도 밀어내기만)",
   "    if (car.tr && !car.tr.rage && !isZombie(b) && !chBlind(b)) return;             // 평소 상태의 사람은 민간 차가 안 친다 (미리 보고 선다 — 닿아도 밀어내기만) · c80: 밟는 차는 친다"),
  ("      if (sp > vmax + 0.02) {", "      if (!car.rev && sp > vmax + 0.02) {"),
  # 수송차가 부서지면 — 아이템 + 경찰
  ("      c.wreck = true;\n      c.g.children[0].material.color.setHex(0x26221f);", "      c.wreck = true;\n      if (CHAPTER && c.loot) chLootDrop(c);   // c80\n      c.g.children[0].material.color.setHex(0x26221f);"),
  # 버려진 수송차는 꾸밈 차가 아니라 때릴 대상으로 남는다 (동료들이 알아서 부순다) · 후진 중에 내렸으면 후진 표시를 지운다
  ("    const j = objs.indexOf(car.obj); if (j >= 0) objs.splice(j, 1); car.obj.off = false; if (!car.obj.dead) chDecoObjs.push(car.obj);",
   "    const j = objs.indexOf(car.obj); if (j >= 0) objs.splice(j, 1); car.obj.off = false; car.rev = false; if (!car.obj.dead) (car.loot ? objs : chDecoObjs).push(car.obj);   /* c80: 수송차는 때릴 대상으로 남는다 */"),
  ("      const cand = Q.filter((c) => !chTrSeen(c.x, c.z, 3)); if (!cand.length) break;", "      const cand = Q.filter((c) => !c.loot && !chTrSeen(c.x, c.z, 3)); if (!cand.length) break;   /* c80: 수송차는 안 치운다 */"),
  # 한 번 본 수송차는 미니맵에 물음표로 따라다닌다 (부술 때까지)
  ("      car.g.visible = vis;\n      car.g.position.set(car.x, 0.05, car.z);", "      car.g.visible = vis; if (vis && car.loot) car.seenQ = true;   // c80\n      car.g.position.set(car.x, 0.05, car.z);"),
  ("    const r = 2.1 * u;                                                    // 나 = 빨간 점",
   "    for (const c of cars) if (c.loot && c.seenQ && !c.looted) {            // c80: 한 번 본 수송차 = 노란 물음표 (움직이는 대로 따라간다)\n"
   "      const px = X(c.x), py = Z(c.z), pr = 4.6 * u;\n"
   "      g.fillStyle = 'rgba(0, 0, 0, 0.9)'; g.beginPath(); g.arc(px, py, pr, 0, Math.PI * 2); g.fill(); g.lineWidth = 1 * u; g.strokeStyle = '#ffd34d'; g.stroke();\n"
   "      g.fillStyle = '#ffd34d'; g.font = '900 ' + Math.round(8.5 * u) + 'px system-ui, -apple-system, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('?', px, py + 0.4 * u);\n"
   "    }\n"
   "    const r = 2.1 * u;                                                    // 나 = 빨간 점"),
  # 비켜나기 시작했으면 그 좀비를 다 지나칠 때까지 비켜난 채로 간다 — 전에는 조금만 비켜나도 좀비가 좁은 띠 밖으로 나가 '안 보이는' 것이 되어, 곧장 제 차선으로 돌아오다 스쳤다 (앞을 멀리 봐도 소용이 없었다)
  ("    let zMid = false, zL = false, zR = false;", "    let zMid = false, zL = false, zR = false, zAl = 0;   /* c80: zAl = 옆 3분의 1에 보인 것까지의 거리 (가장 먼 것) */"),
  ("      if (lt > 0) zR = true; else zL = true;\n", "      if (lt > 0) zR = true; else zL = true; if (al > zAl) zAl = al;\n", 2),
  ("      const dir = zR ? -1 : 1; T.swT = CH_TR_SW_HOLD;\n", "      const dir = zR ? -1 : 1; T.swT = CH_TR_SW_HOLD; if (T.swLat === null || T.swDir !== dir) T.swS = 0; T.swS = Math.max(T.swS || 0, s + L + zAl + 0.2);   /* c80: 여기(그 좀비를 차 꽁무니까지 지나친 자리)까지는 비켜난 채로 */\n"),
  ("    } else if (T.swT > 0 && (T.swT -= dt) <= 0) T.swLat = null;",
   "    } else if (T.swLat !== null && !halt && !T.back && s < (T.swS || 0)) T.swT = CH_TR_SW_HOLD;   // c80: 아직 그 좀비 옆을 지나는 중\n"
   "    else if (T.swT > 0 && (T.swT -= dt) <= 0) { T.swLat = null; T.swS = 0; }"),
  # 앞을 보는 길이 2배 — 경찰차의 40% → 80% (약 2칸 → 4칸). 좀 더 일찍 반응한다. 폭은 그대로 (차 폭의 80%)
  ("  const CH_TR_SEE = 0.4, CH_TR_SEE_W = 0.8;", "  const CH_TR_SEE = 0.8, CH_TR_SEE_W = 0.8;   /* c80: 길이 2배 */"),
  ("bar: () => chBar, zebras: () => chZebras,", "bar: () => chBar, lootCars: CH_LOOT_CAR, lootType: chLootType, robbed: () => chRobbed, trDriver: chTrDriver, zebras: () => chZebras,"),
  ("  function showDud() {", C80_FN + "  function showDud() {"),
]
