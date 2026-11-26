import pathlib
s = pathlib.Path('c479.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
# ── 테이저 빨간 별: 기계 오작동 ──
rep("for (const { c } of hit) { if (c.drone) {", "for (const { c } of hit) { if (chRedR('taser')) { const f = puff(c.foot ? c.foot.x : c.x, 0.8, c.foot ? c.foot.z : c.z, 0x4aa8ff, 0.6, 2.2, 0.22, 0, 0, 0, 1); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; }   /* c480: 빨간 별 — 맞은 자리 파랑 번쩍 */ if (chMadRoll(c)) { zaps.push({ to: c, t: 0.45 }); continue; }   /* c480: 기계 오작동 */ if (c.drone) {")
rep("  function chTaserLook() {", r"""  // ── c480: 기계 오작동 — 테이저 빨간 별. 로봇 · 터렛 · 드론 (보스 제외) 25% + 빨간 별마다 5%.
  //   2초 동안 덜덜 떨며 감전 (무적) → 부정적 효과 다 풀림 · 체력 가득 · 머리 위 빙빙 표시 · 이동 · 공격 2배 · 목적 없이 마구 돌아다니며 인간을 쏜다 (적은 이걸 공격한다)
  const chMadDr = [], chMadBuf = [];
  const chMadTex = (() => { const cv = document.createElement('canvas'); cv.width = cv.height = 64; const g = cv.getContext('2d'); g.strokeStyle = '#ffe14a'; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath(); for (let t = 0; t < 14; t += 0.1) { const r = 3 + t * 2, x = 32 + Math.cos(t) * r, y = 32 + Math.sin(t) * r; if (t === 0) g.moveTo(x, y); else g.lineTo(x, y); } g.stroke(); const T = new THREE.CanvasTexture(cv); T.colorSpace = THREE.SRGBColorSpace; return T; })();
  function chMadIcon() { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: chMadTex, transparent: true, depthTest: false, depthWrite: false })); s.scale.setScalar(0.75); s.renderOrder = UI + 2; scene.add(s); return s; }
  function chMadRoll(c) {
    const r = chRedR('taser'); if (!r || c.tank || c.boss || c.mad || !(c.drone || c.robot)) return false;
    if (Math.random() >= 0.25 + 0.05 * (r - 1)) return false;
    if (c.drone) { const i = chDrones.indexOf(c); if (i >= 0) chDrones.splice(i, 1); Object.assign(c, { mad: true, madIn: 2, stunT: 0, goo: 0, acid: 0, statT: 0, lureT: 0, tg: null, burst: 0, atkT: 0.3, madT: 0, hp: c.maxHp }); c.madS = chMadIcon(); chMadDr.push(c); return true; }
    const col = c.mesh.material.color.getHex(), mh = c.maxHp, fixed = c.fixed;
    makeZombie(c);   // 우리 편 (적이 공격한다) — 그림은 로봇 그대로
    Object.assign(c, { mad: true, madIn: 2, madCol: col, madT: 0, madAtk: 0.3, stunT: 0, statT: 0, fixed });
    c.mesh.material.color.setHex(col); c.maxHp = mh; c.hp = mh; c.hpDisp = mh; if (c.acid) c.acid.length = 0; c.madS = chMadIcon();
    return true;
  }
  function chMadStep(z, dt) {                  // 오작동 로봇 · 터렛
    z.madS.position.set(z.foot.x, (z.halfH || RADIUS) * 2 + 0.75, z.foot.z); z.madS.material.rotation += dt * 7;
    if (z.madIn > 0) { z.madIn -= dt; z.vel.set(0, 0); z.hp = z.maxHp; z.mesh.material.color.setHex(Math.floor(clock * 20) % 2 ? 0x9fd8ff : z.madCol); if (z.madIn <= 0) z.mesh.material.color.setHex(z.madCol); return; }
    if (!z.fixed) { if ((z.madT -= dt) <= 0) { z.madT = rand(0.35, 0.9); z.madA = Math.random() * 6.283; } const sp = SPEED * 2; steer(z.vel, wantV.set(Math.cos(z.madA) * sp, Math.sin(z.madA) * sp), ACCEL * 2 * dt); } else z.vel.set(0, 0);
    if ((z.madAtk -= dt) <= 0) {
      let best = null, bd = SIGHT;
      for (const c of nearIn(cCells, z.foot.x, z.foot.z, SIGHT, chMadBuf)) { if (c.kind !== 'citizen' || !(c.hp > 0 || c.robot) || c.space !== z.space) continue; const q = Math.hypot(c.foot.x - z.foot.x, c.foot.z - z.foot.z); if (q < bd && !fireBlocked(z.foot.x, z.foot.z, c.foot.x, c.foot.z)) { bd = q; best = c; } }
      if (best) { z.madAtk = HIT_EVERY / 2; sniperFx(z, best); landHit(z, best, CH_DMG_SO * (z.turret ? 8 : 4)); } else z.madAtk = 0.2;   // 공격 속도 2배 · 한 번에 연사 몫
    }
  }
  function chMadDie(z) { if (z.madS) { scene.remove(z.madS); z.madS.material.dispose(); z.madS = null; } chRobotDie(z); }
  function chMadDroneTick(dt) {                // 오작동 드론 — 마구 날아다니며 인간을 쏜다
    for (let i = chMadDr.length - 1; i >= 0; i--) {
      const d = chMadDr[i];
      const gone = () => { scene.remove(d.s); d.s.material.dispose(); scene.remove(d.sh); if (d.tr) { scene.remove(d.tr); d.tr.material.dispose(); } scene.remove(d.madS); chMadDr.splice(i, 1); };
      if (Math.hypot(d.x - me.foot.x, d.z - me.foot.z) > me.sense * 2.5) { if ((d.farT = (d.farT || 0) + dt) > 25) { gone(); continue; } } else d.farT = 0;
      if (d.madIn > 0) { d.madIn -= dt; chDroneDraw(d, dt); d.s.position.x += rand(-0.12, 0.12); d.s.position.z += rand(-0.08, 0.08); d.s.material.color.setHex(Math.floor(clock * 20) % 2 ? 0x9fd8ff : 0xffffff); if (d.madIn <= 0) d.s.material.color.setHex(0xffffff); }
      else {
        if ((d.madT -= dt) <= 0) { d.madT = rand(0.4, 1.0); d.madA = Math.random() * 6.283; }
        const sp = CH_DRONE_SPEED * 2 * dt, nx = d.x + Math.cos(d.madA) * sp, nz = d.z + Math.sin(d.madA) * sp; if (chDroneFree(nx, nz)) { d.x = nx; d.z = nz; } else d.madT = 0;
        d.foot.set(d.x, 0, d.z);
        let t = d.tg; if (!t || t.kind !== 'citizen' || !bodies.includes(t) || !(t.hp > 0 || t.robot)) { t = null; let bd = CH_DRONE_SIGHT; for (const c of nearIn(cCells, d.x, d.z, CH_DRONE_SIGHT, chMadBuf)) { if (c.kind !== 'citizen' || c.space || !(c.hp > 0 || c.robot)) continue; const q = Math.hypot(c.foot.x - d.x, c.foot.z - d.z); if (q < bd && !fireBlocked(d.x, d.z, c.foot.x, c.foot.z)) { bd = q; t = c; } } d.tg = t; }
        if (d.burst > 0) { if ((d.burstT -= dt) <= 0) { d.burstT = 0.09; d.burst--; if (t) chDroneShot(d, t); } }
        else if ((d.atkT -= dt) <= 0 && t && Math.hypot(t.foot.x - d.x, t.foot.z - d.z) <= CH_DRONE_RANGE) { d.atkT = HIT_EVERY / 2; d.burst = 3; d.burstT = 0; }
        chDroneDraw(d, dt);
      }
      d.madS.position.set(d.s.position.x, d.s.position.y + 0.8, d.s.position.z); d.madS.material.rotation += dt * 7;
    }
  }
  function chTaserLook() {""")
rep("  function updateZombie(z, dt) {", "  function updateZombie(z, dt) {\n    if (z.mad) { if (z.knockT > 0) { knockStep(z, dt); return; } chMadStep(z, dt); return; }   // c480: 오작동 기계")
rep("    if (chEBL.length) chEBTick(dt);   // c464", "    if (chEBL.length) chEBTick(dt);   // c464\n    if (chMadDr.length) chMadDroneTick(dt);   // c480")
rep("  function killZombie(z) {\n", "  function killZombie(z) {\n    if (z.mad) { chMadDie(z); return; }   // c480: 오작동 기계는 터진다\n")
rep("      if (b.mode === 'bite' || b.state === 'held') { b.mesh.position.x += rand", "      if (b.madIn > 0) { b.mesh.position.x += rand(-0.13, 0.13); b.mesh.position.z += rand(-0.13, 0.13); }   // c480: 오작동 — 덜덜\n      if (b.mode === 'bite' || b.state === 'held') { b.mesh.position.x += rand")
rep("    if (CHAPTER && isZombie(v) && v.bombing) dmg *= 0.5;", "    if (v.madIn > 0) dmg = 0;   // c480: 오작동 연출 중 무적\n    if (CHAPTER && isZombie(v) && v.bombing) dmg *= 0.5;")
# 내 명령에서 빼기 (자폭 · 변이)
rep("    const all = zombies.filter((z) => z !== me && isZombie(z));", "    const all = zombies.filter((z) => z !== me && isZombie(z) && !z.mad);   /* c480 */")
rep("  function useMutate() {\n    const al = nearAllies().filter((z) => !z.mutPerm);", "  function useMutate() {\n    const al = nearAllies().filter((z) => !z.mutPerm && !z.mad);   /* c480 */")
# 적 테스트 — 오작동 기계는 진짜로 싸운다
rep("(CH_ET && (isZombie(v) || (a && isZombie(a))))", "(CH_ET && ((isZombie(v) && !v.mad) || (a && isZombie(a) && !a.mad)))")
rep("!(CH_TOUR && z === me) && !CH_ET   /* c465", "!(CH_TOUR && z === me) && (!CH_ET || z.mad)   /* c480 · c465")
rep("      if (!isZombie(z) || (CH_TOUR && z === me) || CH_ET) continue;", "      if (!isZombie(z) || (CH_TOUR && z === me) || (CH_ET && !z.mad)) continue;")
rep("if (isZombie(z) && !(CH_TOUR && z === me) && !CH_ET && z.space === c.space && Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z) <= ER)", "if (isZombie(z) && !(CH_TOUR && z === me) && (!CH_ET || z.mad) && z.space === c.space && Math.hypot(z.foot.x - c.foot.x, z.foot.z - c.foot.z) <= ER)")
rep("for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && !CH_ET && z.space", "for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && (!CH_ET || z.mad) && z.space")
rep("    for (const z of zombies) if (!z.bombing) { z.hp = z.maxHp; z.stunT = 0; }", "    for (const z of zombies) if (!z.bombing && !z.mad) { z.hp = z.maxHp; z.stunT = 0; }")
pathlib.Path('c480_patch.py').write_text('C480_R = ' + repr(R) + '\n')
print(len(R))
rep("function chDroneReset() { if (!chDrones) return;", "function chDroneReset() { if (!chDrones) return; for (const d of chMadDr) { scene.remove(d.s); scene.remove(d.sh); if (d.tr) scene.remove(d.tr); scene.remove(d.madS); } chMadDr.length = 0;   /* c480 */")
pathlib.Path('c480_patch.py').write_text('C480_R = ' + repr(R) + '\n')
