# c437: 총동원령(5단계)부터 — 샷건 경찰 · 사각 로봇(새로 나오는 5명 중 1명) + 건널목마다 고정 터렛 1기 · 샷건 경찰 2명 (빨간 해골은 계엄부터 그대로)
src = open('c436.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    if (CHAPTER && chAL >= 6) { if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c);", "    if (CHAPTER && chAL >= 5 && !chNoMix) { if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c);   /* c437: 총동원령부터 */")
rep("  let chPolN = 0, chSolN = 0;", "  let chPolN = 0, chSolN = 0, chNoMix = false, chRobotAny = false;   // c437: chNoMix = 건널목 터렛 · 샷건을 직접 만들 때")
rep("    c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 2;", "    chRobotAny = true; c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 2;")
rep("    if (CHAPTER && chSolN) for (let i = bodies.length - 1; i >= 0; i--)", "    if (CHAPTER && chRobotAny) for (let i = bodies.length - 1; i >= 0; i--)")
rep("c.burstN = 4; c.burstT = 0; c.burstZ = z;", "c.burstN = c.turret ? 8 : 4; c.burstT = 0; c.burstZ = z;   /* c437: 터렛 8발 */", 2)
rep("for (const c of bodies) { if (!c.robot || c.state === 'held' || c.state === 'lured') continue;", "for (const c of bodies) { if (!c.robot || c.turret || c.state === 'held' || c.state === 'lured') continue;")
rep("      chBarForm(X);\n    }\n  }\n", """      if (CHAPTER && s === 5) chBarTurret(X);   // c437: 총동원령 — 터렛 1기 · 샷건 경찰 2명
      chBarForm(X);
    }
  }
  function chBarTurret(X) {                    // c437: 건널목 통로 한가운데 한쪽 벽에 고정 터렛 (군인 바탕 · 체력 3배 · 한 번에 8발 · 감염 안 됨 · 부서지면 터짐) + 샷건 경찰 2명
    chNoMix = true;
    const [x, z] = chBarXZ(X, 0, CH_BAR_HALF - 0.75), t = addCitizen(x, z, square(x, z), 'soldier');
    t.robot = t.turret = true; chRobotAny = true; t.noLure = true; t.fixed = true; t.met = true; t.sleep = false; t.tick = 0; t.hp = t.maxHp = t.maxHp * 3;
    t.r = BODY * 1.35; t.halfH = RADIUS * 1.35; t.mesh.scale.setScalar(1.35); t.mesh.geometry = chSqGeo; t.mesh.material.color.setHex(0x4d5560); chAddGun(t, 0.6, 0.2, 0x1a1d21);
    for (let i = 0; i < 2; i++) { const c = addCitizen(X.cx, X.cz, square(X.cx, X.cz), 'police'); chMakeSg(c); c.gar = X; c.fresh = true; X.units.push(c); }
    chNoMix = false;
  }
""")
open('c437_patch.py', 'w').write("# c437: 총동원령 — 터렛 · 샷건 경찰\nC437_R = " + repr(R) + "\n")
print(len(R))
