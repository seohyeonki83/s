# c436: 경보 10단계(계엄까지 새 내용) · 불도저(첫 보스) · 샷건 경찰 · 사각 로봇 · 덩치 넉백 = 방탄복 · 드론 주기 1.3배
src = open('c435.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# ── 드론 주기 ──
rep("CH_DRONE_EVERY = 144,   /* c433: 120 → 144초 (1.2배) */", "CH_DRONE_EVERY = 187.2,   /* c436: 144 → 187.2초 (1.3배) */   /* c433: 120 → 144초 (1.2배) */")
# ── 경보 10단계 ──
rep("let deaths = 0, stars = 0, dispatchT = 0,", "let chAL = 0, chSkullMode = false;   // c436: 경보 단계 (1~10) · 해골 표시로 넘어가는 중\n  let deaths = 0, stars = 0, dispatchT = 0,")
rep("    stars = Math.min(STAR_MAX, STAR_AT.filter((n) => deaths >= n).length);", "    stars = Math.min(STAR_MAX, STAR_AT.filter((n) => deaths >= n).length); if (CHAPTER) chAL = CH_AL_AT.filter((n) => deaths >= n).length;   // c436")
rep("    deaths = stars = dispatchT = 0;", "    deaths = stars = dispatchT = 0; chAL = 0; chSkullMode = false; chPolN = chSolN = 0;   /* c436 */")
rep("  const LEVEL_NAME = ['수상함', '난리남', '개판', '계엄', '데프콘'];", """  const CH_AL_AT = [5, 30, 164, 432, 711, 1021, 1384, 1821, 2353, 3000];   // c436: 경보 10단계 — 누적 감염 수 (팬데믹 = 앞 간격 2배, 그 뒤는 268 × (1 + 0.039 n²), 종말 3000)
  if (CHAPTER) { STAR_AT[3] = CH_AL_AT[3]; STAR_AT[4] = CH_AL_AT[4]; }   // c436: 1~5단계는 지금 5단계와 같은 내용 (기준 수만 새 표)
  const chALv = () => CHAPTER ? Math.max(stars, chAL) : stars;   // 보이는 경보 단계
  let chPolN = 0, chSolN = 0;                  // c436: 계엄부터 새로 나오는 경찰 · 군인 수 (5명마다 1명 = 샷건 경찰 · 사각 로봇)
  const LEVEL_NAME = CHAPTER ? ['수상함', '경계', '비상', '팬데믹', '총동원령', '계엄', '데프콘', '전면전', '대재앙', '종말'] : ['수상함', '난리남', '개판', '계엄', '데프콘'];   // c436""")
rep("    if (starSlots().length !== STAR_MAX) starsEl.innerHTML = '<b class=\"cap\">경보단계</b>' + '<span class=\"s\">!</span>'.repeat(STAR_MAX) + '<i class=\"lv\"></i>';", """    const sk = CHAPTER && (shownStars > 5 || chSkullMode);   // c436: 계엄부터 빨간 해골
    if (starSlots().length !== STAR_MAX || starsEl.dataset.m !== (sk ? 'k' : 'e')) { starsEl.dataset.m = sk ? 'k' : 'e'; starsEl.innerHTML = '<b class="cap">경보단계</b>' + (sk ? '<span class="s" style="color:#ff2a2a;width:0.9em">☠</span>' : '<span class="s">!</span>').repeat(STAR_MAX) + '<i class="lv"></i>'; }""")
rep("    for (let i = 0; i < STAR_MAX; i++) sl[i].classList.toggle('off', i >= shownStars);", "    for (let i = 0; i < STAR_MAX; i++) sl[i].classList.toggle('off', i >= (sk ? shownStars - 5 : shownStars));")
rep("    fly.className = 'fly'; fly.textContent = '!'; fly.style.fontWeight = '900';", "    const skl = CHAPTER && idx >= 5;   // c436: 계엄부터 해골\n    fly.className = 'fly'; fly.textContent = skl ? '☠' : '!'; fly.style.fontWeight = '900';")
rep("fontSize: '10px', color: '#b44ee6',", "fontSize: '10px', color: skl ? '#ff2a2a' : '#b44ee6',")
rep("      const slot = starSlots()[idx], r = slot.getBoundingClientRect();", "      if (skl) { chSkullMode = true; drawStars(); }   // c436\n      const slot = starSlots()[skl ? idx - 5 : idx], r = slot.getBoundingClientRect();")
rep("shownStars = idx + 1; drawStars(); const el = starSlots()[idx];", "shownStars = idx + 1; drawStars(); const el = starSlots()[skl ? idx - 5 : idx];")
rep("    while (starsQueued < stars) {", "    while (starsQueued < chALv()) {   /* c436 */")
# ── 덩치 넉백 = 방탄복 ──
rep("  function giveKnock(z, kx, kz, v, T) {", """  function chKbAbs(z) {                        // c436: 넉백 이기는 힘 = 방탄복 개수 (덩치는 2개를 타고난다 · 괴물 덩치는 빨간 별마다 +1 · 나는 내 방탄복에 더한다)
    let n = z === me && owned.vest ? 1 + lv('vest') : 0;
    if (z.mut === 'armor') { n += 2; const B = chMB(z); if (B && B.id === 'monster') n += B.r; }
    return n ? SNIPER_KD / 12 * (2 + 2.5 * (n - 1)) : 0;
  }
  function giveKnock(z, kx, kz, v, T) {""")
rep("    if (z.mut === 'armor' || z.mode === 'bite') return;   // 덩치 · 무는(감염 중) 좀비는 안 밀린다\n    if (z === me && absorbAmt() >= SNIPER_KD - 0.001) return;", "    if ((!CHAPTER && z.mut === 'armor') || z.mode === 'bite') return;   // 덩치 · 무는(감염 중) 좀비는 안 밀린다 (c436: 챕터 덩치는 방탄복으로)\n    if (CHAPTER ? chKbAbs(z) >= SNIPER_KD - 0.001 : z === me && absorbAmt() >= SNIPER_KD - 0.001) return;")
rep("    if (z.hp <= 0 || z.mut === 'armor' || z.mode === 'bite') return;\n    if (CHAPTER) {", "    if (z.hp <= 0 || (!CHAPTER && z.mut === 'armor') || z.mode === 'bite') return;   /* c436 */\n    if (CHAPTER) {")
rep("      if (z === me && absorbAmt() >= D - 0.001) return;", "      if (chKbAbs(z) >= D - 0.001) return;   /* c436 */")
rep("z.mut !== 'armor' && !(z === me && absorbAmt() >= SNIPER_KD * 3 / 12 - 0.001)", "!(chKbAbs(z) >= SNIPER_KD * 3 / 12 - 0.001)   /* c436 */")
rep("v.mut !== 'armor' && !(v === me && absorbAmt() >= SNIPER_KD * 2 / 12 - 0.001)", "!(chKbAbs(v) >= SNIPER_KD * 2 / 12 - 0.001)   /* c436 */")
rep("    if (v.hp <= 0 || v.mut === 'armor' || v.mode === 'bite') return;\n    const T = ARMOR_KT * 6 / 12, D = SNIPER_KD * 6 / 12, V = D * 4 / (1 - Math.exp(-4 * T));\n    if (v === me && absorbAmt() >= D - 0.001) return;", "    if (v.hp <= 0 || v.mode === 'bite') return;\n    const T = ARMOR_KT * 6 / 12, D = SNIPER_KD * 6 / 12, V = D * 4 / (1 - Math.exp(-4 * T));\n    if (chKbAbs(v) >= D - 0.001) return;   /* c436 */")
rep("hit.hp > 0 && hit.mut !== 'armor' && hit.mode !== 'bite' &&", "hit.hp > 0 && hit.mode !== 'bite' &&   /* c436 */")
rep("if (!(hit === me && absorbAmt() >= D - 0.001)) {", "if (!(chKbAbs(hit) >= D - 0.001)) {   /* c436 */")
# ── 불도저 (첫 보스) ──
rep("car.massK = 4; car.hpK = 10 * 0.95 * 3 * 0.9 * 1.5 * 0.9 * 1.1 * 0.95 * 0.75;", "car.massK = 4; car.hpK = 10 * 0.95 * 3 * 0.9 * 1.5 * 0.9 * 1.1 * 0.95 * 0.75; if (CHAPTER) { car.dozer = true; car.hpK *= 0.8; }   /* c436: 첫 보스 = 불도저 (체력 80%) */")
rep("    const tg = new THREE.Group(); tg.add(tur, brl, ...mgs); car.g.add(tg); car.tkTur = tg; car.tkAim = 0;", """    const tg = new THREE.Group(); tg.add(tur, brl, ...mgs); car.g.add(tg); car.tkTur = tg; car.tkAim = 0;
    if (car.dozer) {                           // c436: 불도저 — 노란 몸 · 앞에 큰 삽날 · 운전석 (포탑 · 기관포 없음)
      tg.visible = false; K[0].material.color.setHex(0xd9a21b);
      const Lb = CAR_L * 0.78 * 0.85;
      car.g.add(mg(0.16, CAR_W * 1.18, Lb / 2 + 0.1, 0, 0x6d7279, 0), mg(0.05, CAR_W * 1.18, Lb / 2 + 0.19, 0, 0xb9bfc6, 1), mg(0.36, 0.42, -0.12, 0, 0x2b2f33, 2), mg(0.22, 0.3, -0.1, 0, 0x7fb4d6, 3));   // 삽날 · 날 끝 · 운전석 · 창
    }""")
rep("rubBack: 0, rubCool: 0, crT: 0, goo: false, gooT: 0 });", "rubBack: 0, rubCool: 0, crT: 0, goo: false, gooT: 0 }); if (car.dozer) car.dashAt /= 1.5;   /* c436: 불도저는 돌진 1.5배 자주 */")
rep("    car.burstN = 0; chTankSpray(car, dt);   // c201: 난사", "    car.burstN = 0; if (!car.dozer) chTankSpray(car, dt);   // c201: 난사 (c436: 불도저는 직접 공격 없음)")
rep("      const v = MELEE * 3 / 2; car.tkPhT -= dt;", "      const v = MELEE * 3 / 2 * (car.dozer ? 1.5 : 1); car.tkPhT -= dt;   /* c436: 불도저 후진 1.5배 빠르게 */")
rep("car.tkPh = 'back'; car.tkPhT = 2;", "car.tkPh = 'back'; car.tkPhT = car.dozer ? 2 / 1.5 : 2;")
rep("car.tkPh = null; car.dashT = 0; car.dashAt = rand(10 * 2 / 3, 15 * 2 / 3); }", "car.tkPh = null; car.dashT = 0; car.dashAt = rand(10 * 2 / 3, 15 * 2 / 3) / (car.dozer ? 1.5 : 1); }")
rep("    if (!CHAPTER || car !== chTank) return;\n    for (let i = 0; i < 5; i++) {", "    if (!CHAPTER || car !== chTank) return;\n    if (car.dozer) { const pool = CH_ITEMS.filter((k) => !chFull(k)); if (pool.length) dropPickup(pool[Math.floor(Math.random() * pool.length)], car.x, car.z, null); chSf.chk = 1; return; }   // c436: 불도저 — 군인 · 특공대 없이 무기나 장비 하나\n    for (let i = 0; i < 5; i++) {")
# ── 샷건 경찰 · 사각 로봇 (계엄부터, 새로 나오는 5명 중 1명) ──
rep("    c.flee = new THREE.Vector2();\n", "    if (CHAPTER && chAL >= 6) { if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c); else if (type === 'soldier' && ++chSolN % 5 === 0) chMakeRobot(c); }   // c436\n    c.flee = new THREE.Vector2();\n")
rep("  function chVig(c) {", """  const chGunMat = new THREE.MeshBasicMaterial({ color: 0x1d2024, transparent: true, depthTest: false, depthWrite: false }), chSqGeo = new THREE.PlaneGeometry(RADIUS * 1.8, RADIUS * 1.8);
  function chAddGun(c, L, W, col) { const g = new THREE.Mesh(new THREE.PlaneGeometry(L, W).translate(L / 2 + 0.05, 0, 0), col ? new THREE.MeshBasicMaterial({ color: col, transparent: true, depthTest: false, depthWrite: false }) : chGunMat); g.position.z = 0.012; g.renderOrder = 1; c.mesh.add(g); c.aimGun = g; }
  function chMakeSg(c) {                       // c436: 샷건 경찰 — 경찰 + 늘 앞을 향한 샷건 · 체력 150% · 경찰 사거리 0.4배까지 다가가 쏜다
    c.sg = true; c.hp = c.maxHp = c.maxHp * 1.5; chAddGun(c, 0.62, 0.15);
  }
  function chMakeRobot(c) {                    // c436: 사각 로봇 — 군인 바탕 · 체력 2배 · 몸 1.5배 · 감염 안 됨(체력 0이면 터짐) · 현금 · 다이아몬드에 반응 안 함
    c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 2; c.r = BODY * 1.5; c.halfH = RADIUS * 1.5; c.mesh.scale.setScalar(1.5);
    c.mesh.geometry = chSqGeo; c.mesh.material.color.setHex(0x6f7a86); chAddGun(c, 0.55, 0.17, 0x2a2f35);
  }
  function chRobotDie(c) {                     // c436: 로봇 — 차처럼 터지고 사라진다 (경험치 1)
    boom(c.foot.x, c.foot.z); dust(c.foot.x, c.foot.z, 12, 1.6); debris(c.foot.x, c.foot.z, 12, [0x6f7a86, 0x2a2f35, 0x151515], 0.35, 6);
    for (const z of bodies) { if (z.target === c) { z.target = null; if (z.mode === 'pounce' || z.mode === 'bite') z.mode = 'free'; } if (z.foe === c) z.foe = null; if (z.engaging === c) z.engaging = null; }
    chBTgone(c); if (isZombie(me)) gainXp();
  }
  const chSgBuf = [];
  function chShotgun(c, z) {                   // c436: 샷건 — 앞쪽 60° 부채꼴, 경찰 사거리 0.5배 안 좀비 모두 (경찰 공격력 1/5) · 넉백 가까우면 저격수의 40% → 끝에서 0
    const R = c.sight * 0.5, dx = z.foot.x - c.foot.x, dz = z.foot.z - c.foot.z, d0 = Math.hypot(dx, dz) || 1, ux = dx / d0, uz = dz / d0, cs = Math.cos(Math.PI / 6);
    c.shotT = 0; c.shotAt = z; c.recoilT = 0; c.recoilX = -ux; c.recoilZ = -uz; c.recoilK = 2;
    { const f = puff(c.foot.x + ux * RADIUS, 0, c.foot.z + uz * RADIUS, 0xfff23a, 1.4, 1.6, 0.09, 0, 0, 0, 0.8); f.s.material.map = flashTex; f.s.position.addScaledVector(UP, RADIUS); f.s.renderOrder = UI - 0.5; f.peak = true; }
    for (let i = 0; i < 7; i++) { const a = Math.atan2(uz, ux) + rand(-0.5, 0.5), sp = rand(8, 14); const f = puff(c.foot.x + ux * 0.6, 0.6, c.foot.z + uz * 0.6, 0xffe9a0, 0.18, 0.08, 0.18, Math.cos(a) * sp, 0, Math.sin(a) * sp, 0.9); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; }
    const dmg = CH_DMG_PO / 5;
    for (const t of nearIn(zCells, c.foot.x, c.foot.z, R + 1, chSgBuf)) {
      if (!isZombie(t) || t.space !== c.space) continue;
      const ex = t.foot.x - c.foot.x, ez = t.foot.z - c.foot.z, e = Math.hypot(ex, ez);
      if (e > R + (t.r || BODY) || e < 1e-3 || (ex * ux + ez * uz) / e < cs || fireBlocked(c.foot.x, c.foot.z, t.foot.x, t.foot.z)) continue;
      landHit(c, t, t === me && hasVest ? dmg * vestK(lv('vest')) : dmg);
      const D = SNIPER_KD * 0.4 * Math.max(0, 1 - e / R);
      if (D > 0.001 && t.hp > 0 && t.mode !== 'bite' && chKbAbs(t) < D - 0.001) { const T = ARMOR_KT * D / SNIPER_KD, V = D * 4 / (1 - Math.exp(-4 * T)); if (t.mode === 'pounce') stopPounce(t); giveKnock(t, ex, ez, V, T); }
    }
  }
  const chGunQ = new THREE.Quaternion(), chGunV = new THREE.Vector3();
  function chGunAim(b) {                       // c436: 샷건 · 로봇 총이 늘 앞(노리는 쪽, 없으면 가는 쪽)을 향한다 (화면에서)
    const t = b.foe || b.shotAt; let dx, dz; if (t && t.foot) { dx = t.foot.x - b.foot.x; dz = t.foot.z - b.foot.z; } else { dx = b.vel.x; dz = b.vel.y; }
    if (Math.abs(dx) + Math.abs(dz) < 1e-4) return;
    chGunQ.copy(camera.quaternion).invert(); chGunV.set(dx, 0, dz).applyQuaternion(chGunQ); b.aimGun.rotation.z = Math.atan2(chGunV.y, chGunV.x);
  }
  function chVig(c) {""")
rep("    const range = c.boostT > 0 ? c.boostSight : c.fb ? c.sight0 : c.sight;", "    const range = (c.boostT > 0 ? c.boostSight : c.fb ? c.sight0 : c.sight) * (c.sg ? 0.4 : 1);   /* c436: 샷건 경찰은 경찰 사거리 0.4배까지 다가가 쏜다 */")
rep("c.burstZz = z.foot.z; } else shoot(c, z); c.atkT = HIT_EVERY * (c.sniper ? 4 : 1); }", "c.burstZz = z.foot.z; } else if (c.sg) chShotgun(c, z); else shoot(c, z); c.atkT = HIT_EVERY * (c.sniper ? 4 : c.sg ? 1.6 : 1); }   /* c436: 샷건 공속 = 저격수의 2.5배 */")
rep("        b.mesh.position.x += b.recoilX * 0.2 * k; b.mesh.position.z += b.recoilZ * 0.2 * k;", "        b.mesh.position.x += b.recoilX * 0.2 * k * (b.recoilK || 1); b.mesh.position.z += b.recoilZ * 0.2 * k * (b.recoilK || 1);   /* c436: 샷건 반동 2배 */")
rep("      if (b.knockT > 0 && !b.knockSlide) b.mesh.position.y +=", "      if (b.aimGun) chGunAim(b);   // c436\n      if (b.knockT > 0 && !b.knockSlide) b.mesh.position.y +=")
# 로봇: 쓰러지지 않는다 (체력 0 = 터짐) · 분열 산성 제외 · 금에 홀린다
rep("  const chDown = (b) => b.hp <= 0;", "  const chDown = (b) => b.hp <= 0 && !b.robot;   /* c436: 로봇은 쓰러지지 않는다 */")
rep("      if (CHAPTER && c.maxHp > 0 && c.hp <= 0 && !c.brSplitT", "      if (CHAPTER && c.maxHp > 0 && c.hp <= 0 && !c.robot && !c.brSplitT")
rep("    if (CHAPTER && chChainL.length) chChainTick(dt);   // c431\n", "    if (CHAPTER && chChainL.length) chChainTick(dt);   // c431\n    if (CHAPTER && chSolN) for (let i = bodies.length - 1; i >= 0; i--) { const c = bodies[i]; if (c && c.robot && c.hp <= 0) chRobotDie(c); }   // c436: 로봇은 체력 0이면 터진다\n")
rep("    const tk = chTank; if (tk && !tk.wreck) { const k = chNearFresh(fresh, tk.x, tk.z, SIGHT * cashK() + 4, null);", "    for (const c of bodies) { if (!c.robot || c.state === 'held' || c.state === 'lured') continue; const k = chNearFresh(fresh, c.foot.x, c.foot.z, SIGHT * cashK() + 4, c.space); if (!k) continue; c.robotLure = T0 * (0.2 + 0.05 * (r - 1)); for (const q of fresh) q.who.add(c); enterLured(c); }   // c436: 로봇도 금에 홀린다 (드론과 같은 비율)\n    const tk = chTank; if (tk && !tk.wreck) { const k = chNearFresh(fresh, tk.x, tk.z, SIGHT * cashK() + 4, null);")
rep("if ((c.lureT = (c.lureT || 0) + dt) >= CH_WV('cashT', lv('cash')) * chLingK() * chDiaK() * (c.military", "if ((c.lureT = (c.lureT || 0) + dt) >= (c.robot ? (c.robotLure || 0) : 1) * (c.robot ? 1 : CH_WV('cashT', lv('cash')) * chLingK() * chDiaK()) * (c.robot ? 1 : 1) * (c.robot ? 1 / 0.2 : 1) * (c.military")
open('c436_patch.py', 'w').write("# c436: 경보 10단계 · 불도저 · 샷건 경찰 · 로봇 · 덩치 넉백 · 드론 주기\nC436_R = " + repr(R) + "\n")
print(len(R))
R.append(("K0.material.color.setHex(car.stunT > 0 && Math.floor(clock * 14) % 2 ? 0xc8f0ff : 0x3c4a2a);", "K0.material.color.setHex(car.stunT > 0 && Math.floor(clock * 14) % 2 ? 0xc8f0ff : car.dozer ? 0xd9a21b : 0x3c4a2a);   /* c436: 불도저 노랑 */"))
open('c436_patch.py', 'w').write("# c436: 경보 10단계 · 불도저 · 샷건 경찰 · 로봇 · 덩치 넉백 · 드론 주기\nC436_R = " + repr(R) + "\n")
print(len(R))
