# c78: 사람은 평소엔 도로로 다니지 않는다 (배회 목표·활동 자리는 도로 밖 · 자리 옮기기는 도로로 나뉜 같은 칸 안에서만).
#      도망·경계·싸움·추격 중인 사람은 차를 안 본다 — 도로로 뛰어들고, 민간 차가 미리 서 주지 않으며, 치이면 좀비처럼 날아가고 체력이 깎인다
C78_FN = r"""  // ── c78: 사람과 도로 ──
  const chOnRoad = (x, z, m = 0) => CH_MAP.roads.some(([a, b, c, d]) => x > a - m && x < c + m && z > b - m && z < d + m);
  function chBlockOf(x, z) {                   // 도로로 나뉜 칸 — 같은 칸 안에서는 도로를 안 건너고 다닐 수 있다
    const zi = chZoneOf(x, z), G = (chRoadG || (chRoadG = chRoadGraphs()))[zi]; let i = 0, j = 0;
    for (const l of G.V) if (x > l.c) i++;
    for (const l of G.H) if (z > l.c) j++;
    return zi * 100 + i * 10 + j;
  }
  function chBlind(c) {                        // 차를 안 보는 사람 — 경계·도망·싸움 중이거나, 사건 자리로 뛰어가거나 나를 쫓는 경찰·군인 (건널목 수비대·자리 지키는 경찰은 빼고)
    if (c.kind !== 'citizen' || c.sleep) return false;
    if (c.state === 'alert' || c.state === 'panic' || c.state === 'fight') return true;
    return !!c.police && c.state === 'normal' && !c.gar && ((c.calls && c.calls.length > 0) || (!c.station && !c.post));
  }
  function chSideArea(x, z) {                  // 도로 위 자리에서 가장 가까운 길가(도로 밖 빈자리) 둘레의 활동 영역 — 차에서 내린 사람이 진정한 뒤 머물 곳
    const zi = chZoneOf(x, z);
    for (let r = 1.5; r <= 9; r += 1.5) for (let k = 0; k < 12; k++) {
      const a = (k + Math.random()) / 12 * Math.PI * 2, px = x + Math.cos(a) * r, pz = z + Math.sin(a) * r;
      if (px < MM.x0 + 3 || px > MM.x1 - 3 || pz < MM.z0 + 3 || pz > MM.z1 - 3 || chZoneOf(px, pz) !== zi || spaceOf(px, pz) || !freeSpot(px, pz, null) || chNearRiver(px, pz, AREA / 2 + 1) || chOnRoad(px, pz, 1.2)) continue;
      return chRoamArea(px, pz);
    }
    return square(x, z);
  }
"""
C78_R = [
  # 배회 목표는 도로 밖 (가장자리에서 0.45칸 넘게) — 20번 중 18번까지만 따진다 (자리가 온통 도로면 어쩔 수 없다)
  ("freeSpot(g.x, g.y, null) && !(CHAPTER && chOnCar(g.x, g.y))) break;",
   "freeSpot(g.x, g.y, null) && !(CHAPTER && (chOnCar(g.x, g.y) || (n < 18 && chOnRoad(g.x, g.y, 0.45))))) break;   /* c78 */"),
  # 길거리 사람이 놓이는 자리 · 다시 채워지는 자리 · 무리 한 명 한 명
  ("      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null)) continue;",
   "      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null) || chOnRoad(x, z, 1.2)) continue;   /* c78: 도로 밖 */"),
  ("    const ok = (x, z, strict) => !spaceOf(x, z) && !chNearRiver(x, z, AREA / 2 + 1) && freeSpot(x, z, null) &&",
   "    const ok = (x, z, strict) => !spaceOf(x, z) && !chNearRiver(x, z, AREA / 2 + 1) && freeSpot(x, z, null) && !chOnRoad(x, z, 1.2) &&"),
  ("      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null) || Math.hypot(x - me.foot.x, z - me.foot.z) < 14) continue;",
   "      if (spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null) || chOnRoad(x, z, 1.2) || Math.hypot(x - me.foot.x, z - me.foot.z) < 14) continue;"),
  ("if (!spaceOf(x, z) && freeSpot(x, z, null) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)) break; }",
   "if (!spaceOf(x, z) && freeSpot(x, z, null) && !(tt < 30 && chOnRoad(x, z, 0.45)) && !bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9)) break; }"),
  # 자리째 옮길 때 — 도로 밖 · 도로를 안 건너는 같은 칸 안에서만
  ("      if (x < MM.x0 + 3 || x > MM.x1 - 3 || z < MM.z0 + 3 || z > MM.z1 - 3 || chZoneOf(x, z) !== rm.zone || spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null)) continue;",
   "      if (x < MM.x0 + 3 || x > MM.x1 - 3 || z < MM.z0 + 3 || z > MM.z1 - 3 || chZoneOf(x, z) !== rm.zone || spaceOf(x, z) || chNearRiver(x, z, AREA / 2 + 1) || !freeSpot(x, z, null)) continue;\n"
   "      if (chOnRoad(x, z, 1.2) || chBlockOf(x, z) !== chBlockOf(rm.ax, rm.az)) continue;   // c78: 도로 밖 · 같은 칸 안에서만 (도로를 건너 옮겨 가지 않는다)"),
  # 차에서 내린 사람 — 진정하면 가장 가까운 길가에서 지낸다
  ("      const c = chPut(x, z, square(x, z), w, null); c.sleep = false; c.met = true; c.tick = 0; c.fromCar = true;",
   "      const c = chPut(x, z, chSideArea(x, z), w, null); c.sleep = false; c.met = true; c.tick = 0; c.fromCar = true;"),
  # 민간 차 — 도망·싸움 중인 사람도 좀비와 같은 좁은 띠로만 본다 (가운데면 서고 옆이면 비켜난다)
  ("      if (lt > 0) zR = true; else zL = true;\n    }\n",
   "      if (lt > 0) zR = true; else zL = true;\n    }\n"
   "    let hMid = false;                          // c78: 차를 안 보는 사람(도망·싸움·추격 중) — 같은 띠로 본다. 평소 상태의 사람은 아래 '앞길'에서 미리 보고 선다\n"
   "    if (!zMid) for (const q of nearIn(cCells, car.x, car.z, car.sight + L, chTrL)) {\n"
   "      if (q.space || !chBlind(q) || (q.trHit === car && q.trHitT > clock)) continue;\n"
   "      const dx = q.foot.x - car.x, dz = q.foot.z - car.z, al = dx * fx + dz * fz - L / 2; if (al <= 0 || al > car.sight) continue;\n"
   "      const lt = -dx * fz + dz * fx; if (Math.abs(lt) > sw) continue;\n"
   "      if (blocked(car.x, car.z, q.foot.x, q.foot.z)) continue;\n"
   "      if (Math.abs(lt) <= sw / 3) { hMid = true; break; }\n"
   "      if (lt > 0) zR = true; else zL = true;\n"
   "    }\n"),
  ("    const halt = zMid || T.hitT > 0;", "    const halt = zMid || hMid || T.hitT > 0;"),
  ("    if (T.mode === 'stop') { if (sp < 0.6 && (T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }",
   "    if (T.mode === 'stop') { if (sp < 0.6 && (zMid || T.hitT > 0) && (T.zT += dt) >= T.exitAt) { chTrExit(car); return; } }   /* c78: 사람 때문에 선 시간은 안 센다 */"),
  ("        if (b.sleep || b.space) continue;\n        const px = b.foot.x - car.x, pz = b.foot.z - car.z, al = px * ux + pz * uz - L / 2 - b.r;",
   "        if (b.sleep || b.space || chBlind(b)) continue;   // c78: 도망·싸움 중인 사람은 미리 못 본다 (띠에 들어와야 본다)\n        const px = b.foot.x - car.x, pz = b.foot.z - car.z, al = px * ux + pz * uz - L / 2 - b.r;"),
  # 치기 — 평소 상태의 사람은 안 친다 (밀어내기만), 차를 안 보는 사람은 좀비처럼 친다
  ("!(car.tr && (!isZombie(b) || (b.trHit === car && b.trHitT > clock)))",
   "!(car.tr && ((!isZombie(b) && !chBlind(b)) || (b.trHit === car && b.trHitT > clock)))"),
  ("  function showDud() {", C78_FN + "  function showDud() {"),
]
