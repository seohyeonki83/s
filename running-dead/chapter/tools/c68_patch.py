# c68: 배회하다 서 있는 시간 0 · 주황·빨강(자경단)은 경계·놀람 없이 바로 덤빈다
C68_R = [
  ("    c.timer = rand(...IDLE_TIME);\n  }\n  function enterAlert(c)",
   "    c.timer = CHAPTER && !c.gar ? 0 : rand(...IDLE_TIME);   // c68: 챕터 — 배회하다 서 있는 시간 없음 (바리케이트 수비대는 그대로 선다)\n  }\n  function enterAlert(c)"),
  ("if (d < 0.1) { c.goal = null; c.back = false; c.timer = rand(...IDLE_TIME); }",
   "if (d < 0.1) { c.goal = null; c.back = false; c.timer = CHAPTER && !c.gar ? 0 : rand(...IDLE_TIME); }   /* c68 */"),
  ("      if (charges(c)) enterFight(c, nearZ);  // 공격형: 가장 가까운 좀비에게 덤빈다",
   "      if (charges(c)) enterFight(c, nearZ, CHAPTER && c.attacker && !c.boss);  // 공격형: 가장 가까운 좀비에게 덤빈다 (c68: 주황·빨강은 놀람 표시 없이)"),
  ("    else if (near <= c.sight) { if (c.state !== 'alert') { enterAlert(c);",
   "    else if (near <= c.sight && CHAPTER && c.attacker && !c.boss && c.hp > 0) enterFight(c, nearZ, true);   // c68: 주황·빨강 — 시야에 들어오면 경계 없이 바로 덤빈다\n"
   "    else if (near <= c.sight) { if (c.state !== 'alert') { enterAlert(c);"),
]
