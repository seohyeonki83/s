# c65: 바리케이트 체력 = 경찰차의 2배 · 체력바 여러 겹 (덩치 좀비 체력까지가 한 줄 — 넘으면 파랑, 그 다음 주황으로 덮는다) · 체력바는 모두 초록
C65_R = [
  ("CH_BARR_HP = 4,", "CH_BARR_HP = 2,   /* c65: 경찰차의 4배 → 2배 */"),
  ("hp = MY_DAMAGE * 9.5 * (barr ? CH_BARR_HP : 1)", "hp = barr ? CH_HP_CAP * 3 : MY_DAMAGE * 9.5   /* c66: 바리케이트 = 체력바 딱 세 겹 (약 851) */"),
  ("  const hpFoeMat = new THREE.MeshBasicMaterial({ color: 0xff4d4d,", "  const hpFoeMat = new THREE.MeshBasicMaterial({ color: CHAPTER ? 0x43d17a : 0xff4d4d,   /* c65: 챕터는 적도 초록 */"),
  ("0.5 / POLICE_HP) * (b.maxHp || 0));",
   "0.5 / POLICE_HP) * (CHAPTER && !mine ? Math.min(b.maxHp || 0, CH_HP_CAP) : (b.maxHp || 0)));   /* c65: 챕터 — 덩치 좀비 체력보다 길어지지 않는다 (넘는 만큼은 겹으로) */\n"
   "  const CH_HP_CAP = ALLY_HP * 3;   // c65: 한 겹 = 덩치 좀비(동료) 기본 최대 체력 (약 284)\n"
   "  const chHpMat2 = new THREE.MeshBasicMaterial({ color: 0x3d8bff, transparent: true, depthTest: false, depthWrite: false }), chHpMat3 = new THREE.MeshBasicMaterial({ color: 0xff9a1f, transparent: true, depthTest: false, depthWrite: false });\n"
   "  function chHpFill(b) {                       // c65: 한 겹을 넘는 체력은 초록 위를 파랑으로, 두 겹을 넘으면 주황으로 덮는다\n"
   "    const C = CH_HP_CAP, M = b.maxHp || 1, h = Math.max(0, b.hpDisp);\n"
   "    if (M <= C + 1e-6) { b.hpFill.scale.x = Math.max(0.001, h / M); if (b.hpFill2) b.hpFill2.visible = b.hpFill3.visible = false; return; }\n"
   "    if (!b.hpFill2) for (const [k, mat, n] of [['hpFill2', chHpMat2, 1], ['hpFill3', chHpMat3, 2]]) { const m = new THREE.Mesh(gaugeFillGeo, mat); m.position.copy(b.hpFill.position); m.position.z += 0.001 * n; m.renderOrder = b.hpFill.renderOrder + n; b.hpBar.add(m); b[k] = m; }\n"
   "    const f2 = Math.min(1, Math.max(0, h - C) / C), f3 = Math.min(1, Math.max(0, h - 2 * C) / C);\n"
   "    b.hpFill.scale.x = Math.max(0.001, Math.min(h, C) / C);\n"
   "    b.hpFill2.visible = f2 > 0; b.hpFill2.scale.x = Math.max(0.001, f2);\n"
   "    b.hpFill3.visible = f3 > 0; b.hpFill3.scale.x = Math.max(0.001, f3);\n"
   "  }"),
  ("          b.hpFill.scale.x = Math.max(0.001, b.hpDisp / b.maxHp);", "          if (CHAPTER && b !== me) chHpFill(b); else b.hpFill.scale.x = Math.max(0.001, b.hpDisp / b.maxHp);   // c65"),
  ("o.hpFill.scale.x = Math.max(0.001, o.hpDisp / o.maxHp);", "if (CHAPTER) chHpFill(o); else o.hpFill.scale.x = Math.max(0.001, o.hpDisp / o.maxHp);   // c65"),
]
