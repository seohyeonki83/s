# c55: 테이저건·자폭·히드라 우선순위 티어 (자경단 > 주황) · 각성하면 게이지만큼 체력 회복
C55_FN = r"""  function chTier(c) { return c.sniper ? 6 : c.soldier ? 5 : c.police ? 4 : c.vig || c.boss ? 3 : c.attacker ? 2 : c.guard ? 1 : 0; }   // c55: 위험 티어 — 저격수 > 군인 > 경찰 > 자경단(빨강·분홍) > 주황 > 노랑 > 하양
"""
C55_R = [
  ("  const DANGER = (c) => c.sniper ? 5 : c.soldier ? 4 : c.police ? 3 :", "  const DANGER = (c) => CHAPTER ? chTier(c) : c.sniper ? 5 : c.soldier ? 4 : c.police ? 3 :"),
  ("    const tier = (c) => c.sniper ? 5 : c.soldier ? 4 : c.police ? 3 : c.attacker ? 2 : c.guard ? 1 : 0;", "    const tier = (c) => CHAPTER ? chTier(c) : c.sniper ? 5 : c.soldier ? 4 : c.police ? 3 : c.attacker ? 2 : c.guard ? 1 : 0;"),
  ("const t = b.sniper ? 5 : b.soldier ? 4 : b.police ? 3 : b.attacker ? 2 : b.guard ? 1 : 0; if (t > hT", "const t = CHAPTER ? chTier(b) : b.sniper ? 5 : b.soldier ? 4 : b.police ? 3 : b.attacker ? 2 : b.guard ? 1 : 0; if (t > hT"),
  ("      awakenMe(it.acc); it.drain = true; refreshItems(); return;", "      if (CHAPTER) me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.2 * Math.min(1, it.acc / chAccMax()));   // c55: 각성하면 체력 회복 — 게이지가 가득이면 최대 체력의 20%, 덜 찼으면 찬 만큼만\n      awakenMe(it.acc); it.drain = true; refreshItems(); return;"),
  ("    } else if ((c.timer -= dt) <= 0) c.goal = pickGoal(c.area);   // 일반: 서 있다가 다음 곳으로", "    } else if ((c.timer -= dt) <= 0) { if (CHAPTER && c.area.roam) chRoam(c); c.goal = pickGoal(c.area); if (CHAPTER && c.area.roam && !inArea(c)) c.back = true; }   // 일반: 서 있다가 다음 곳으로 (c55: 길거리 사람은 가끔 자리째 옮겨 간다 — 그땐 걷는 속도로)"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, use: useItem, tier: chTier, hold: () => items,"),
  ("  function showDud() {", C55_FN + "  function showDud() {"),
]
