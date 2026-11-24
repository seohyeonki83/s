# c430: 변이 주사 · 각성 주사 갈림길 — 괴물 좀비 / 흡수 좀비 (변이 주사 = 동료 변이 좀비, 각성 주사 = 각성한 나 · 빨간 별은 각 무기 것)
#  · 모든 덩치 스플래시 거리 0.5배 (괴물이면 0.5 → 1.5배, 피해 100%)
#  · 괴물: 히드라 사거리 ×1 → ×2 · 덩치 미는 힘 10 → 14 · 덩치가 차·바리케이트도 넉백(인간과 같은 만큼) · 차를 쳐도 스플래시
#  · 흡수: 내가 마지막으로 쓴 무기(테이저건 · 산성 자폭)의 효과를 공격(스플래시 포함)에 맞은 적에게 건다 — 지속 시간 = 그 무기 지속 시간 × 빨간 별 ÷ 6
src = open('c429.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    ],\n  };\n  const chBr = {};", """    ],
    mutate: [   // c430: 동료 변이 좀비
      { id: 'monster', name: '괴물 좀비', desc: '변이한 동료가 괴물이 됩니다. 히드라는 사거리가, 덩치는 미는 힘과 범위 공격이 커지고 범위 공격 피해가 줄지 않습니다. 덩치는 차와 바리케이트도 밀어냅니다.', line: (r) => `히드라 사거리 ×${(1 + r / 6).toFixed(2)} · 덩치 미는 힘 ${(10 + 4 * r / 6).toFixed(1)} · 범위 ×${(0.5 + r / 6).toFixed(2)}`, short: ['괴물', (r) => `×${(1 + r / 6).toFixed(1)}`] },
      { id: 'absorb', name: '흡수 좀비', desc: '변이한 동료가 내가 마지막으로 쓴 무기(테이저건 · 산성 자폭)의 효과를 흡수해, 공격에 맞은 적에게 겁니다.', line: (r) => `흡수한 효과 지속 시간 ${Math.round(100 * r / 6)}%`, short: ['흡수', (r) => `${Math.round(100 * r / 6)}%`] },
    ],
    awaken: [   // c430: 각성한 나
      { id: 'monster', name: '괴물 좀비', desc: '각성한 내가 괴물이 됩니다. 히드라는 사거리가, 덩치는 미는 힘과 범위 공격이 커지고 범위 공격 피해가 줄지 않습니다. 덩치는 차와 바리케이트도 밀어냅니다.', line: (r) => `히드라 사거리 ×${(1 + r / 6).toFixed(2)} · 덩치 미는 힘 ${(10 + 4 * r / 6).toFixed(1)} · 범위 ×${(0.5 + r / 6).toFixed(2)}`, short: ['괴물', (r) => `×${(1 + r / 6).toFixed(1)}`] },
      { id: 'absorb', name: '흡수 좀비', desc: '각성한 내가 마지막으로 쓴 무기(테이저건 · 산성 자폭)의 효과를 흡수해, 공격에 맞은 적에게 겁니다.', line: (r) => `흡수한 효과 지속 시간 ${Math.round(100 * r / 6)}%`, short: ['흡수', (r) => `${Math.round(100 * r / 6)}%`] },
    ],
  };
  const chBr = {};
  let chAbsK = null;                           // c430: 흡수 좀비가 흡수한 무기 (내가 마지막으로 쓴 테이저건 · 산성 자폭)""")
rep("ITEM[k].name = B ? B.nm : O.name; ITEM[k].icon = B ? B.icon : O.icon; ITEM[k].col = B ? B.col : O.col;", "ITEM[k].name = B && B.nm ? B.nm : O.name; ITEM[k].icon = B && B.icon ? B.icon : O.icon; ITEM[k].col = B && B.col ? B.col : O.col;")
rep("for (const k of Object.keys(CH_BRANCH)) chBrLook(k);   /* c427 */", "for (const k of Object.keys(CH_BRANCH)) chBrLook(k);   /* c427 */ chAbsK = null;   /* c430 */")
# 원래 수치는 흰 ★6에서 멈춘다
rep("  const MUT_T = () => 6 + 3 * lv('mutate');", "  const MUT_T = () => 6 + 3 * chLvB('mutate');   /* c430 */")
rep("  const chAccMax = () => 5 + 3 * lv('awaken');", "  const chAccMax = () => 5 + 3 * chLvB('awaken');   /* c430 */")
# 변이 좀비 갈림길 수치
rep("  function chHydK() { return 1; }", """  function chMB(z) { if (!CHAPTER || !z) return null; const k = z === me ? 'awaken' : 'mutate', id = chBr[k]; return id ? { id, r: Math.max(0, lv(k) - 6) } : null; }   // c430: 그 좀비의 갈림길 (나 = 각성 주사 · 동료 = 변이 주사)
  const chMonster = (z) => { const B = chMB(z); return !!B && B.id === 'monster'; };
  function chArmF(z) { const B = chMB(z); return 10 + (B && B.id === 'monster' ? 4 * B.r / 6 : 0); }   // c430: 덩치 미는 힘 (괴물 10 → 14)
  function chHydK(z) { const B = chMB(z); return B && B.id === 'monster' ? 1 + B.r / 6 : 1; }""")
rep("  function chSplK() { return 1; }", "  function chSplK(z) { const B = chMB(z); return B && B.id === 'monster' ? 0.5 + B.r / 6 : 0.5; }   // c430: 덩치 범위 공격 거리 — 0.5배 (괴물이면 1.5배까지)")
R.append(("chHydK()", "chHydK(z)", 5))   # 정의는 위에서 바뀐 뒤라 쓰는 곳 5개만
rep("(CHAPTER ? chSplK() : 1)", "(CHAPTER ? chSplK(a) : 1)")
rep("    if (CHAPTER) for (const z of zombies) if (z.mut === 'armor') z.force = 11 * chArmK();", "    if (CHAPTER) for (const z of zombies) { if (z.mut === 'armor') z.force = chArmF(z);   /* c430 */ if (z.mut || z.brHalo) chMutLook(z); }")
rep("z.force = CHAPTER ? 10 : MY_FORCE * 1.3;   /* c420: 덩치 미는 힘 10 */", "z.force = CHAPTER ? chArmF(z) : MY_FORCE * 1.3;   /* c430 */   /* c420: 덩치 미는 힘 10 */")
rep("me.force = CHAPTER ? 10 : MY_FORCE * 1.3; }   /* c420: 10 */", "me.force = CHAPTER ? chArmF(me) : MY_FORCE * 1.3; }   /* c430 */   /* c420: 10 */")
# 스플래시: 괴물은 피해 100% · 차를 쳐도 터진다
rep("if (a.mut === 'armor' && v.kind === 'citizen' && !a.splashing) {", "if (a.mut === 'armor' && (v.kind === 'citizen' || (CHAPTER && v.kind === 'obj' && v.type === 'car' && !v.dead && chMonster(a))) && !a.splashing) {   /* c430: 괴물 덩치는 차·바리케이트를 쳐도 */")
rep(": dmg) * (CHAPTER ? 0.5 : 0.3));", ": v.kind === 'citizen' ? dmg : zDamage(a)) * (CHAPTER ? (chMonster(a) ? 1 : 0.5) : 0.3));   /* c430: 괴물은 범위 피해 100% */")
# 괴물 덩치 — 차·바리케이트 넉백
rep("    if (v.kind === 'obj') { if (!v.dead) { v.hp = Math.max(0, v.hp - dmg);", "    if (CHAPTER && v.kind === 'obj' && v.type === 'car' && !v.dead && a && a.mut === 'armor' && !a.splashing && chMonster(a) && !v.car.tank) { const car = v.car, kx = car.x - a.foot.x, kz = car.z - a.foot.z, kl = Math.hypot(kx, kz) || 1; car.knT = ARMOR_KT; car.knVX = kx / kl * ARMOR_KB * 1.5; car.knVZ = kz / kl * ARMOR_KB * 1.5; }   // c430: 괴물 덩치 — 차·바리케이트도 인간과 같은 만큼 밀린다\n    if (v.kind === 'obj') { if (!v.dead) { v.hp = Math.max(0, v.hp - dmg);")
rep("    if (CHAPTER) for (const car of cars) { chStuckTick(car, dt);", "    if (CHAPTER) for (const car of cars) { if (car.knT > 0) { const f = car.knT / ARMOR_KT; car.x += car.knVX * f * dt; car.z += car.knVZ * f * dt; car.knT -= dt; carClampB(car); if (car.obj) car.obj.foot.set(car.x, 0, car.z); car.pushT = clock; pushedCar = true; }   /* c430 */ chStuckTick(car, dt);")
# 흡수
rep("    if (!it || it.ammo <= 0 || !isZombie(me)) return;\n", "    if (!it || it.ammo <= 0 || !isZombie(me)) return;\n    if (CHAPTER && (kind === 'taser' || kind === 'bomb')) chAbsK = kind;   // c430: 흡수 좀비가 흡수한다 (마지막으로 쓴 것)\n")
rep("    v.hp = Math.max(0, v.hp - dmg);\n    if (v.kind === 'safe') { if (v.hp <= 0) breakSafe(v); return; }", "    if (CHAPTER && chAbsK && v.kind === 'citizen' && a && a.mut) chAbsorbHit(a, v);   // c430: 흡수 좀비 (스플래시 포함)\n    v.hp = Math.max(0, v.hp - dmg);\n    if (v.kind === 'safe') { if (v.hp <= 0) breakSafe(v); return; }")
rep("  function gooOn(c) {", """  function chAbsorbHit(a, v) {                 // c430: 흡수 좀비에게 맞은 적 — 흡수한 무기 효과 (그 무기 지속 시간 × 빨간 별 ÷ 6)
    const B = chMB(a); if (!B || B.id !== 'absorb' || !B.r) return; const k = B.r / 6;
    if (chAbsK === 'taser' && chHas('taser')) { v.stunT = Math.max(v.stunT || 0, CH_WV('taserT', chLvB('taser')) * chLingK() * k); v.vel.set(0, 0); }
    else if (chAbsK === 'bomb' && chHas('bomb')) gooOn(v, (4 + 2 * chLvB('bomb')) * chLingK() * k);
  }
  function gooOn(c, T) {""")
rep("    c.gooLeft = Math.max(c.goo ? c.gooLeft : 0, (4 + 2 * chLvB('bomb')) * chLingK());   /* c420: 잔류제 */", "    c.gooLeft = Math.max(c.goo ? c.gooLeft : 0, T ?? (4 + 2 * chLvB('bomb')) * chLingK());   /* c430: T = 흡수 좀비 */   /* c420: 잔류제 */")
# 모양 — 괴물 빨간 후광 · 흡수 = 흡수한 무기 색으로 깜빡이는 후광
R.append(("  function chAbsorbHit(a, v) {", """  function chMutLook(z) {                      // c430: 괴물 = 빨간 후광 · 흡수 = 흡수한 무기 색 후광 (깜빡)
    const B = z.mut ? chMB(z) : null, bc = chBr.bomb === 'sticky' ? 0x9b59ff : chBr.bomb === 'split' ? 0xff7fbf : 0x5fcf3a;
    const want = !B ? null : B.id === 'monster' ? 0xff2a2a : chAbsK === 'taser' ? 0xffe14a : chAbsK === 'bomb' ? bc : 0xdfe6f0;
    if (want === null) { if (z.brHalo) { z.mesh.remove(z.brHalo); z.brHalo.material.dispose(); z.brHalo = null; } return; }
    if (!z.brHalo) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: flashTex, transparent: true, depthTest: false, depthWrite: false })); s.position.set(0, 0, -0.05); s.scale.setScalar(1.9); s.renderOrder = (z.mesh.renderOrder || 0) - 0.05; z.mesh.add(s); z.brHalo = s; }
    z.brHalo.material.color.setHex(want); z.brHalo.material.opacity = B.id === 'monster' ? 0.75 : 0.45 + 0.35 * Math.sin(clock * 6);
  }
  function chAbsorbHit(a, v) {"""))
# 이름 — 동료 획득창
rep("    const name = type === 'armor' ? '덩치 변이 좀비'", "    const name = chBr.mutate && type !== 'zombie' ? (chBr.mutate === 'monster' ? '괴물 ' : '흡수 ') + (type === 'armor' ? '덩치' : '히드라') : type === 'armor' ? '덩치 변이 좀비'")
open('c430_patch.py', 'w').write("# c430: 변이·각성 갈림길 (괴물 · 흡수)\nC430_R = " + repr(R) + "\n")
print(len(R))
