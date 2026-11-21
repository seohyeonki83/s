# c283: 틀니 — 적 체력이 5·10·15·20·25·30% 이하면 덮칠 수 있다 (덮치는 속도 그대로) · 끝까지 강화하면 별 대신 노란 MAX
C283_R = [
  # 덮칠 수 있나 = 체력 0, 또는 틀니 기준 이하 (보스 빼고)
  ("  function pounceable(z) {", "  const chDown = (b) => b.hp <= 0 || (CHAPTER && owned.teeth && !b.boss && b.hp <= b.maxHp * 0.05 * (1 + lv('teeth')));   // c283: 틀니 — 체력이 이만큼 남으면 덮칠 수 있다\n  function pounceable(z) {"),
  ("      if (b.kind !== 'citizen' || b.marked || b.hp > 0 || b.space !== z.space) continue;", "      if (b.kind !== 'citizen' || b.marked || !chDown(b) || b.space !== z.space) continue;   /* c283 */"),
  ("&& !b.marked && b.hp <= 0 && b.space === z.space && inSight(z, b) && dashOk(z, b)", "&& !b.marked && chDown(b) && b.space === z.space && inSight(z, b) && dashOk(z, b)"),
  ("(z === me || b.hp > 0 || !b.chaser || b.chaser === z)", "(z === me || !chDown(b) || !b.chaser || b.chaser === z)"),
  ("if (d <= bd && (z === me || b.hp <= 0 || (crowd.get(b) || 0) < CROWD_MAX))", "if (d <= bd && (z === me || chDown(b) || (crowd.get(b) || 0) < CROWD_MAX))"),
  ("if (z.pick && z.pick.hp > 0) crowd.set(", "if (z.pick && !chDown(z.pick)) crowd.set("),
  ("me.mut && aimed.hp <= 0 && chMeYield(aimed)) ? aimed : ready;", "me.mut && chDown(aimed) && chMeYield(aimed)) ? aimed : ready;"),
  ("if (prey && !t && prey.hp <= 0) claimPrey(z, prey);", "if (prey && !t && chDown(prey)) claimPrey(z, prey);"),
  ("        else if (go && go.hp > 0) fight(z, go, dt);", "        else if (go && !chDown(go)) fight(z, go, dt);   /* c283 */"),
  # 물기 시작하면 체력 0으로 (이후는 원래 감염 흐름 그대로)
  ("    t.state = 'held';\n", "    t.state = 'held';\n    if (t.hp > 0) t.hp = 0;   // c283: 틀니로 덮친 사람 — 물리는 순간 쓰러진다\n"),
  # 설명
  ("teeth: (n) => `감염 시간 -${10 * (1 + n)}%`,", "teeth: (n) => `감염 시간 -${10 * (1 + n)}% · 체력 ${5 * (1 + n)}% 이하면 덮침`,"),
  ("teeth: '나와 동료들이 인간을 좀비로 만드는 시간이 줄어듭니다. 회복하는 체력의 총량은 그대로입니다. 강화하면 더 빨라집니다.',", "teeth: '나와 동료들이 인간을 좀비로 만드는 시간이 줄어들고, 체력이 조금 남은 인간도 바로 덮칠 수 있습니다. 강화하면 더 빨라지고 더 많이 남아도 덮칩니다.',"),
  # MAX — 끝까지 강화하면 별 대신
  ("  const starTag = (n) => n ? ` <span style=\"color:#ffd34d;letter-spacing:-1px\">${chStars(n)}</span>` : '';",
   "  const chStarsK = (k, n) => CHAPTER && n >= chLvMax(k) ? 'MAX' : chStars(n);   // c283: 끝까지 강화 = 노란 MAX\n  const starTag = (n, k) => n ? ` <span style=\"color:#ffd34d;letter-spacing:-1px\">${k ? chStarsK(k, n) : chStars(n)}</span>` : '';"),
  ("return `지금${starTag(n)}${max ? ' (최대)' : ''}: ${statLine(kind, n)}` + (max ? '' : `<br>다음 강화${starTag(n + 1)}: ${statLine(kind, n + 1)}`); };",
   "return `지금${starTag(n, kind)}${max ? ' (최대)' : ''}: ${statLine(kind, n)}` + (max ? '' : `<br>다음 강화${starTag(n + 1, kind)}: ${statLine(kind, n + 1)}`); };"),
  ("text-shadow:0 2px 6px rgba(0, 0, 0, 0.7)\">${chStars(max ? n : n + 1)}</div>", "text-shadow:0 2px 6px rgba(0, 0, 0, 0.7)\">${chStarsK(kind, max ? n : n + 1)}</div>"),
  ("(max ? `지금${starTag(n)} (최대): ${statLine(kind, n)}` : `지금${starTag(n)}: ${statLine(kind, n)}<br>강화 뒤${starTag(n + 1)}: ${statLine(kind, n + 1)}`)",
   "(max ? `지금${starTag(n, kind)} (최대): ${statLine(kind, n)}` : `지금${starTag(n, kind)}: ${statLine(kind, n)}<br>강화 뒤${starTag(n + 1, kind)}: ${statLine(kind, n + 1)}`)"),
  ('color:#ffd34d">${max ? \'MAX\' : chStars(n + 1)}', 'color:#ffd34d">${max ? \'MAX\' : chStarsK(k, n + 1)}', 2),
  ('color:#ffd34d">${has ? chStars(n + 1) : \'NEW\'}', 'color:#ffd34d">${has ? chStarsK(k, n + 1) : \'NEW\'}'),
  ("const st = CHAPTER ? chStars(n) :", "const st = CHAPTER ? (n >= chLvMax(kd[els.indexOf(el)]) ? '<span style=\"color:#ffd34d;font-weight:900;letter-spacing:0\">MAX</span>' : chStars(n)) :   /* c283 */"),
]
