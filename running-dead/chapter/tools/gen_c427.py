# c427: 갈림길 모양 + 현금 갈림길
#  · 자폭 스위치: 끈적 → '끈적 스위치'(보라) · 분열 → '분열 스위치'(분홍). 적에게 묻는 자폭 산성 색도 보라 / 분홍. 기본 아이콘은 보라·분홍 반반
#  · 새끼 좀비(분열 산성 · 분열세포) 연분홍 · 분열세포 아이콘 분홍
#  · 현금: 다이아몬드(인간끼리 싸움 · 민간 차가 서고 사람이 내려 뛰어옴 · 별마다 유혹 시간 +5%) / 금(기계도 홀림 — 드론 20%부터 · 보스 5%부터, 별마다 +5%)
#  · 뿌리는 것도 반짝이는 다이아몬드 / 금괴 (돈다발보다 살짝 크게)
src = open('c426.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# ── 아이콘 ──
rep('<circle cx="12" cy="3.5" r="2" fill="#5fcf3a"/><circle cx="9" cy="14.5" r="2.4" fill="#e8455a"/>', '<path d="M12 1.5a2 2 0 0 0 0 4z" fill="#a764ff"/><path d="M12 1.5a2 2 0 0 1 0 4z" fill="#ff8fc8"/><circle cx="9" cy="14.5" r="2.4" fill="#e8455a"/>')
rep('fill="#9be35a" fill-opacity="0.9" stroke="#1f4a14" stroke-width="1.3"/><path d="M12 7.6v8.8" stroke="#1f4a14" stroke-width="1" stroke-dasharray="1.6 1.2"/><circle cx="7.2" cy="12" r="2.4" fill="#3c8a24"/><circle cx="16.8" cy="12" r="2.4" fill="#3c8a24"/><circle cx="6.5" cy="11.3" r="0.8" fill="#d8ffb0"/><circle cx="16.1" cy="11.3" r="0.8" fill="#d8ffb0"/>',
    'fill="#ffa6d2" fill-opacity="0.92" stroke="#7a2350" stroke-width="1.3"/><path d="M12 7.6v8.8" stroke="#7a2350" stroke-width="1" stroke-dasharray="1.6 1.2"/><circle cx="7.2" cy="12" r="2.4" fill="#d9478c"/><circle cx="16.8" cy="12" r="2.4" fill="#d9478c"/><circle cx="6.5" cy="11.3" r="0.8" fill="#ffe0ef"/><circle cx="16.1" cy="11.3" r="0.8" fill="#ffe0ef"/>')   # 분열세포 분홍
rep("  IC.blood = svgI(", """  IC.bombSticky = svgI('<rect x="4" y="9" width="16" height="11" rx="2" fill="#6c5a96"/><rect x="11" y="3" width="2" height="6" fill="#9aa4b5"/><circle cx="12" cy="3.5" r="2.2" fill="#a764ff"/><circle cx="9" cy="14.5" r="2.4" fill="#c79bff"/><path d="M4 17.5c2 0 2 2.5 4 2.5s2-2.5 4-2.5 2 2.5 4 2.5 2-2.5 4-2.5V20H4z" fill="#a764ff"/>');   /* c427: 끈적 스위치 (보라) */
  IC.bombSplit = svgI('<rect x="4" y="9" width="16" height="11" rx="2" fill="#96637f"/><rect x="11" y="3" width="2" height="6" fill="#9aa4b5"/><circle cx="12" cy="3.5" r="2.2" fill="#ff8fc8"/><circle cx="8.6" cy="14.6" r="2.1" fill="#ffc2df"/><circle cx="12.4" cy="14.6" r="2.1" fill="#ffc2df"/><rect x="15" y="12.5" width="3.5" height="1.6" rx="0.8" fill="#e8b3cd"/><rect x="15" y="15.5" width="3.5" height="1.6" rx="0.8" fill="#e8b3cd"/>');   /* c427: 분열 스위치 (분홍) */
  IC.diamond = svgI('<path d="M7 3.5h10l4.5 5.5L12 21 2.5 9z" fill="#7fe3ff"/><path d="M2.5 9h19M9.2 3.5 7.4 9 12 21l4.6-12-1.8-5.5" stroke="#e6fbff" stroke-width="1" fill="none"/><path d="M7.4 9 12 3.5 16.6 9z" fill="#c4f4ff"/><path d="M19.5 2.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6z" fill="#fff"/>');   /* c427: 다이아몬드 */
  IC.gold = svgI('<path d="M3 20l2.2-6h13.6L21 20z" fill="#d49a1e"/><path d="M6.2 13l2.2-6h7.2l2.2 6z" fill="#f2c94c"/><path d="M8.6 7.6h6.8l1.6 4.4H7z" fill="#ffe28a"/><path d="M6 19l1.4-4h9.2L18 19z" fill="#f2c94c"/><path d="M19 3l.5 1.3 1.3.5-1.3.5-.5 1.3-.5-1.3-1.3-.5 1.3-.5z" fill="#fff"/>');   /* c427: 금괴 */
  IC.blood = svgI(""")
# ── 갈림길 표: 이름 · 아이콘 · 색 + 현금 ──
rep("      { id: 'sticky', name: '끈적 산성', desc: '자폭 산성을 맞은 적이 느려집니다.',", "      { id: 'sticky', nm: '끈적 스위치', icon: IC.bombSticky, col: '#a764ff', goo: 0x9b59ff, name: '끈적 산성', desc: '자폭 산성을 맞은 적이 느려집니다.',")
rep("      { id: 'split', name: '분열 산성', desc:", "      { id: 'split', nm: '분열 스위치', icon: IC.bombSplit, col: '#ff8fc8', goo: 0xff7fbf, name: '분열 산성', desc:")
rep("    ],\n  };\n  const chBr = {};", """    ],
    cash: [   // c427
      { id: 'dia', nm: '다이아몬드', icon: IC.diamond, col: '#7fe3ff', name: '다이아몬드', desc: '인간들이 다이아몬드를 두고 서로 싸웁니다. 자동차도 반응합니다.', line: (r) => `유혹(싸우는) 시간 +${5 * r}%`, short: ['싸움', (r) => `+${5 * r}%`] },
      { id: 'gold', nm: '금', icon: IC.gold, col: '#f2c94c', name: '금', desc: '기계들도 정신을 못 차립니다.', line: (r) => `기계 유혹 — 드론 ${20 + 5 * (r - 1)}% · 보스 ${5 * r}% (유혹 시간의)`, short: ['기계', (r) => `${20 + 5 * (r - 1)}%`] },
    ],
  };
  const chBr = {};
  const chItem0 = {};                          // c427: 갈림길 전 이름 · 아이콘 · 색
  function chBrLook(k) {                       // c427: 고른 길에 맞춰 무기 이름 · 아이콘 · 색 (안 골랐으면 원래대로)
    const B = CH_BRANCH[k] && CH_BRANCH[k].find((b) => b.id === chBr[k]), O = chItem0[k] || (chItem0[k] = { name: ITEM[k].name, icon: ITEM[k].icon, col: ITEM[k].col });
    ITEM[k].name = B ? B.nm : O.name; ITEM[k].icon = B ? B.icon : O.icon; ITEM[k].col = B ? B.col : O.col;
    if (k === 'bomb') gooMat.color.setHex(B ? B.goo : 0x5fcf3a);
    const it = items.find((x) => x.kind === k); if (it && it.el) { const ic = it.el.querySelector('.ic'); if (ic) ic.innerHTML = ITEM[k].icon; it.el.style.setProperty('--c', ITEM[k].col); }
  }""")
rep("for (const k of Object.keys(chBr)) delete chBr[k];   /* c422 */", "for (const k of Object.keys(chBr)) delete chBr[k];   /* c422 */ for (const k of Object.keys(CH_BRANCH)) chBrLook(k);   /* c427 */")
rep("chPickWin(ov, card.dataset.k); chBr[k] = card.dataset.k; chItemChanged(k); chPopBtn(k);", "chPickWin(ov, card.dataset.k); chBr[k] = card.dataset.k; chBrLook(k); chItemChanged(k); chPopBtn(k);")
rep("`<div class=\"ic\" style=\"margin-top:4px\">${ITEM[k].icon}</div><div class=\"nm\" style=\"margin-top:8px\">${B.name}</div>", "`<div class=\"ic\" style=\"margin-top:4px\">${B.icon || ITEM[k].icon}</div><div class=\"nm\" style=\"margin-top:8px\">${B.name}</div>")
# ── 새끼 좀비 연분홍 ──
rep("c.mesh.material.color.setHex(0xdce4fc);", "c.mesh.material.color.setHex(0xffb6d9);   /* c427: 연분홍 */")
# ── 현금 갈림길 ──
rep("  const cashGeo = new THREE.PlaneGeometry(0.62, 0.36).rotateX(-Math.PI / 2)", """  const chDiaGeo = new THREE.CircleGeometry(0.42, 4).rotateX(-Math.PI / 2).scale(1, 1, 0.72), chDiaGeo2 = new THREE.CircleGeometry(0.24, 4).rotateX(-Math.PI / 2).scale(1, 1, 0.72);   // c427: 다이아몬드 (돈다발보다 살짝 크게)
  const chDiaMat = new THREE.MeshBasicMaterial({ color: 0x6fdcff, transparent: true, depthWrite: false }), chDiaMat2 = new THREE.MeshBasicMaterial({ color: 0xd6f8ff, transparent: true, depthWrite: false });
  const chGoldGeo = new THREE.PlaneGeometry(0.74, 0.4).rotateX(-Math.PI / 2), chGoldGeo2 = new THREE.PlaneGeometry(0.56, 0.24).rotateX(-Math.PI / 2);   // c427: 금괴 (돈다발보다 살짝 크게)
  const chGoldMat = new THREE.MeshBasicMaterial({ color: 0xd49a1e, transparent: true, depthWrite: false }), chGoldMat2 = new THREE.MeshBasicMaterial({ color: 0xffd864, transparent: true, depthWrite: false });
  function chCashMesh() {                      // c427: 고른 길에 맞는 뿌리는 것 (다이아몬드 · 금괴 · 돈다발) + 반짝임
    const br = chBr.cash; if (br !== 'dia' && br !== 'gold') return null;
    const g = new THREE.Mesh(br === 'dia' ? chDiaGeo : chGoldGeo, br === 'dia' ? chDiaMat : chGoldMat), top = new THREE.Mesh(br === 'dia' ? chDiaGeo2 : chGoldGeo2, br === 'dia' ? chDiaMat2 : chGoldMat2); top.position.y = 0.003; g.add(top);
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: flashTex, color: 0xffffff, transparent: true, depthTest: false, depthWrite: false })); s.position.set(0.12, 0.15, -0.05); s.scale.setScalar(0.3); s.renderOrder = -0.5; g.add(s); g.glint = s; g.ph = Math.random() * 6.28;
    return g;
  }
  const cashGeo = new THREE.PlaneGeometry(0.62, 0.36).rotateX(-Math.PI / 2)""")
rep("          const mesh = new THREE.Mesh(cashGeo, cashMat);\n          const band = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.38).rotateX(-Math.PI / 2), cashBandMat); band.position.y = 0.002; mesh.add(band);",
    "          let mesh = CHAPTER ? chCashMesh() : null;   // c427: 다이아몬드 · 금괴\n          if (!mesh) { mesh = new THREE.Mesh(cashGeo, cashMat); const band = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.38).rotateX(-Math.PI / 2), cashBandMat); band.position.y = 0.002; mesh.add(band); }")
rep("t: CHAPTER ? CH_WV('cashT', lv('cash')) * chLingK() :", "t: CHAPTER ? CH_WV('cashT', lv('cash')) * chLingK() * chDiaK() :")
rep("if ((c.lureT = (c.lureT || 0) + dt) >= CH_WV('cashT', lv('cash')) * chLingK() * (c.military", "if ((c.lureT = (c.lureT || 0) + dt) >= CH_WV('cashT', lv('cash')) * chLingK() * chDiaK() * (c.military")
rep("    for (const k of cashes.slice()) if ((k.t -= dt) <= 0) removeCash(k);", "    for (const k of cashes.slice()) { if ((k.t -= dt) <= 0) { removeCash(k); continue; } const gl = k.mesh.glint; if (gl) { const p = Math.max(0, Math.sin(clock * 5 + k.mesh.ph)); gl.material.opacity = p * p; gl.scale.setScalar(0.18 + 0.32 * p); } }   // c427: 반짝임")
# 뿌린 순간: 다이아몬드 → 민간 차가 선다 · 금 → 기계가 홀린다
rep("        if (bd <= SENSE * cashK()) enterLured(c);", "        if (bd <= SENSE * cashK()) enterLured(c);   // (c427: 아래 줄 다음에 차 · 기계)")
i = src.index("        if (bd <= SENSE * cashK()) enterLured(c);"); j = src.index("\n      }\n    }\n    refreshItems();", i)
R.append(("\n      }\n    }\n    refreshItems();\n  }\n  function removeCash(k)", "\n      }\n      if (CHAPTER && chBr.cash === 'dia') chDiaCars(fresh);   // c427\n      if (CHAPTER && chBr.cash === 'gold') chGoldMachines(fresh);   // c427\n    }\n    refreshItems();\n  }\n  function removeCash(k)"))
rep("  function enterLured(c) {", """  const chDiaK = () => 1 + 0.05 * chBrR('cash', 'dia');   // c427: 다이아몬드 — 유혹(싸우는) 시간 별마다 +5%
  const chNearFresh = (fresh, x, z, R, sp) => { let best = null, bd = R; for (const k of fresh) { if (k.space !== sp) continue; const d = Math.hypot(k.x - x, k.z - z); if (d < bd && !blocked(x, z, k.x, k.z)) { bd = d; best = k; } } return best; };
  function chDiaCars(fresh) {                  // c427: 다이아몬드 — 본 민간 차는 서고 사람이 내려 뛰어온다 (유혹이 끝나도 다시 안 탄다)
    for (const car of chTr.cars.slice()) { const T = car.tr; if (!T || T.mode === 'left' || T.mode === 'gone' || car.wreck) continue;
      if (!chNearFresh(fresh, car.x, car.z, SIGHT * cashK(), null)) continue;
      const n0 = bodies.length; chTrExit(car);
      for (const c of bodies.slice(n0)) if (c.kind === 'citizen') { for (const k of fresh) k.who.add(c); enterLured(c); } }
  }
  function chGoldMachines(fresh) {             // c427: 금 — 기계도 홀린다 (날아와 내려앉는 시간까지 유혹 시간)
    const r = chBrR('cash', 'gold'); if (!r) return; const T0 = CH_WV('cashT', 6) * chLingK();
    for (const d of chDrones) { if (d.dead) continue; const k = chNearFresh(fresh, d.x, d.z, SIGHT * cashK() + 4, null); if (!k) continue; d.lureT = T0 * (0.2 + 0.05 * (r - 1)); d.lureK = k; d.tg = null; }
    const tk = chTank; if (tk && !tk.wreck) { const k = chNearFresh(fresh, tk.x, tk.z, SIGHT * cashK() + 4, null); if (k) { tk.lureT = T0 * 0.05 * r; tk.lureX = k.x; tk.lureZ = k.z; } }
  }
  const chDiaBuf = [];
  function chDiaFight(c, dt) {                 // c427: 다이아몬드 — 공격할 수 있는 인간은 유혹 시간 동안 가장 가까운 인간을 친다 (근접 = 다가가 때림 · 원거리 = 쏘면서 다이아몬드로)
    if (c.atkT > 0) c.atkT -= dt * chDownK(c);
    const rng = c.police || c.soldier || c.sniper, R = rng ? c.sight : c.sense;
    let t = null, bd = R;
    for (const o of nearIn(cCells, c.foot.x, c.foot.z, R, chDiaBuf)) { if (o === c || o.kind !== 'citizen' || o.state === 'held' || o.space !== c.space || o.sleep) continue; const d = Math.hypot(o.foot.x - c.foot.x, o.foot.z - c.foot.z); if (d < bd && !(rng ? fireBlocked : blocked)(c.foot.x, c.foot.z, o.foot.x, o.foot.z)) { bd = d; t = o; } }
    if (!t) return false;
    if (rng) { if (c.atkT <= 0) { shoot(c, t); c.atkT = HIT_EVERY * (c.sniper ? 4 : 1); if (c.sniper) c.shotStop = 0.3; } return false; }   // 쏘고 다이아몬드 쪽으로 (저격수는 쏠 때 잠깐 선다)
    if (bd > MELEE) { const sp = PANIC_SPEED * (c.police ? POLICE_PACE : 1) * (c.guard ? GUARD_PACE : 1) * (c.soft ? CH_SOFT_MOVE : 1); steer(c.vel, toward(c, t.foot.x, t.foot.z, sp), ACCEL * dt); return true; }
    c.vel.set(0, 0); if (c.atkT <= 0) { strike(c, t); c.atkT = HIT_EVERY; }
    return true;
  }
  function enterLured(c) {""")
rep("    const s = seeCash(c, SIGHT * cashK());\n    if (!s) { enterNormal(c); return; }", "    if (CHAPTER && chBr.cash === 'dia' && c.maxHp > 0 && c.hp > 0 && chDiaFight(c, dt)) return;   // c427: 다이아몬드 — 근접형은 싸우는 중 (원거리는 쏘고 아래로 — 다이아몬드 쪽으로)\n    const s = seeCash(c, SIGHT * cashK());\n    if (!s) { enterNormal(c); return; }")
# 드론 · 보스 — 금에 홀림
rep("      if (d.stunT > 0) { if ((d.air ?? 0) <= 0.45) d.stunT -= dt; chDroneDraw(d, dt); continue; }", """      if (d.stunT > 0) { if ((d.air ?? 0) <= 0.45) d.stunT -= dt; chDroneDraw(d, dt); continue; }
      if (d.lureT > 0) {                        // c427: 금 — 금까지 날아가 내려앉는다 (남은 유혹 시간만큼 앉아 있다)
        d.lureT -= dt; const k = d.lureK, dx = k.x - d.x, dz = k.z - d.z, q = Math.hypot(dx, dz);
        if (q < 0.6 || d.lureT <= 0) { if (d.lureT > 0) d.stunT = d.lureT; d.lureT = 0; d.lureLand = true; chDroneDraw(d, dt); continue; }
        const f = chDroneWay(d, k.x, k.z) || [dx / q, dz / q], l = Math.hypot(f[0], f[1]) || 1, sp = CH_DRONE_SPEED * dt * (d.goo > 0 ? chStickyK() : 1), nx = d.x + f[0] / l * Math.min(sp, q), nz = d.z + f[1] / l * Math.min(sp, q);
        if (chDroneFree(nx, nz)) { d.x = nx; d.z = nz; } d.foot.set(d.x, 0, d.z); chDroneDraw(d, dt); continue;
      }""")
rep("    // 기관포\n    car.atkT -= dt;", """    if (CHAPTER && car.lureT > 0) {             // c427: 금 — 보스도 금 쪽으로 가서 선다 (안 쏘고 · 돌진 안 함)
      car.lureT -= dt; car.burstN = 0; car.tkPh = null; car.dashT = 0; car.spOn = false; const dx = car.lureX - car.x, dz = car.lureZ - car.z, q = Math.hypot(dx, dz);
      if (q > CAR_L * CH_TK_KL / 2 + 0.6) { car.vx = dx / q * spd; car.vz = dz / q * spd; car.tkV = spd; } else { car.vx = car.vz = 0; car.tkV = 0; }
      return;
    }
    // 기관포
    car.atkT -= dt;""")
open('c427_patch.py', 'w').write("# c427: 갈림길 모양 + 현금 갈림길\nC427_R = " + repr(R) + "\n")
print(len(R))
