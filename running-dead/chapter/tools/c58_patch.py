# c58: 맞은 동료는 2초 동안 사물을 안 노린다 · 문이 뚫린 건물은 사람에게도 안팎이 한 공간 (좀비 인지 · 돈다발)
C58_R = [
  # ── 동료가 사람에게 맞으면 그때부터 2초 동안 사물(문·경찰차·금고)을 공격 대상에서 뺀다 (맞을 때마다 다시 2초). 2초 뒤 근처에 사물이 있으면 다시 노린다 ──
  ("  function landHit(a, v, dmg = DAMAGE) {\n",
   "  function landHit(a, v, dmg = DAMAGE) {\n    if (CHAPTER && a && a.kind === 'citizen' && v.kind === 'ally' && !v.dead) v.objOff = clock + 2;   // c58: 맞은 동료는 2초 동안 사물을 안 노린다\n"),
  ("        const sf = !t ? nearSafe(z) : null;",
   "        const noObj = CHAPTER && z !== me && z.objOff > clock;   /* c58 */\n        const sf = !t && !noObj ? nearSafe(z) : null;"),
  ("          if (z.carT >= 1.25) forced = z.carHold; }", "          if (z.carT >= 1.25) forced = z.carHold; if (noObj) forced = null; }"),
  ("        let ob = forced || (!t ? nearObj(z) : null);", "        let ob = forced || (!t && !noObj ? nearObj(z) : null);"),
  ("        if (!t && !ob && !go && !sf) ob = nearObj.any;", "        if (!noObj && !t && !ob && !go && !sf) ob = nearObj.any;"),
  ("    if (z.mut === 'armor') {\n      if (!t) { const ob = nearObj(z), sf = nearSafe(z);",
   "    if (!t && CHAPTER && z.objOff > clock) { allyIdle(z, dt); return; }   // c58: 맞은 변이 동료도 2초 동안 사물을 안 노린다\n    if (z.mut === 'armor') {\n      if (!t) { const ob = nearObj(z), sf = nearSafe(z);"),
  # ── 문이 뚫린(열린) 건물은 사람에게도 안팎이 한 공간 — 전엔 같은 편 누가 그 좀비와 같은 공간에서 보고 있을 때만 안↔밖으로 반응했다 ──
  ("      if (z.space !== c.space && !(linked(c.space, z.space) && hSeen(z))) continue;",
   "      if (z.space !== c.space && !(linked(c.space, z.space) && (CHAPTER || hSeen(z)))) continue;   /* c58: 챕터 — 문이 뚫려 이어진 공간은 한 공간으로 본다 */"),
  ("(z.space === c.space || (linked(c.space, z.space) && hSeen(z)));", "(z.space === c.space || (linked(c.space, z.space) && (CHAPTER || hSeen(z))));   /* c58 */"),
  # 돈다발: 뚫린 문으로 이어진 공간이면 문틈으로 보이는 사람도 홀린다 (벽에 가리면 여전히 못 본다)
  ("          if (k.space !== c.space) continue;", "          if (k.space !== c.space && !(CHAPTER && linked(k.space, c.space))) continue;   /* c58 */"),
  ("      if (k.space !== c.space || !k.who.has(c) || (c.ignoreCash && c.ignoreCash.has(k))) continue;",
   "      if ((k.space !== c.space && !(CHAPTER && linked(k.space, c.space))) || !k.who.has(c) || (c.ignoreCash && c.ignoreCash.has(k))) continue;   /* c58 */"),
]
