# c435: 자폭 스위치 — 적을 먼저 고른다. 내 시야 안 적마다 "그 자리에서 터지면 범위 안 점수 합"을 재서 가장 높은 적 (같으면 나와 가까운 적),
#        그 적과 가장 가까운 내 시야 안 동료가 달려든다. 드론 80점 · 보스 80점 (저격수의 2배)
src = open('c434.mjs').read()
R = []
i0 = src.index("  function chBombPick(al, R) {"); i1 = src.index("  function useBomb() {")
R.append((src[i0:i1], """  function chBombPick(al, R) {               // c435: 적을 먼저 고른다 — 내 시야 안 적마다 그 자리에서 터졌을 때 점수 합 (드론 · 보스 = 저격수의 2배 80점), 가장 높은 적 (같으면 나와 가까운 적) → 그 적과 가장 가까운 내 시야 안 동료가 달려든다
    const cand = al.filter((z) => Math.hypot(z.foot.x - me.foot.x, z.foot.z - me.foot.z) <= me.sense);
    if (!cand.length) return false;
    const tk = chTank && !chTank.wreck ? chTank : null, drones = chDroneSeen();
    const score = (x, z, sp) => { let sc = 0;
      for (const c of nearIn(cCells, x, z, R, mutBuf)) { if (c.kind !== 'citizen' || c.space !== sp || Math.hypot(c.foot.x - x, c.foot.z - z) > R) continue; sc += c.boss ? 40 : CH_BOMB_PT[chTier(c)]; }
      if (!sp) { for (const d of chDrones) if (!d.dead && Math.hypot(d.x - x, d.z - z) <= R + d.r) sc += 80; if (tk && Math.hypot(tk.x - x, tk.z - z) <= R + 1.4) sc += 80; }
      return sc; };
    const ts = [];   // 후보 적 {x, z, sp, c (사람) | d (드론) | tk}
    for (const c of bodies) { if (c.kind !== 'citizen' || c.state === 'held') continue; const q = Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z); if (q > me.sense || (c.space !== me.space && !(CHAPTER && linked(c.space, me.space))) || blocked(me.foot.x, me.foot.z, c.foot.x, c.foot.z)) continue; ts.push({ x: c.foot.x, z: c.foot.z, sp: c.space, c, q }); }
    for (const d of drones) ts.push({ x: d.x, z: d.z, sp: null, d, q: Math.hypot(d.x - me.foot.x, d.z - me.foot.z) });
    if (tk) { const q = Math.max(0, Math.hypot(tk.x - me.foot.x, tk.z - me.foot.z) - CAR_L * CH_TK_KL / 2); if (q <= me.sense && !fireBlocked(me.foot.x, me.foot.z, tk.x, tk.z)) ts.push({ x: tk.x, z: tk.z, sp: null, tk, q }); }
    let T = null, bS = -1;
    for (const t of ts) { const sc = score(t.x, t.z, t.sp); if (sc > bS || (sc === bS && t.q < T.q)) { bS = sc; T = t; } }
    if (!T) { const best = cand.reduce((a, z) => Math.hypot(z.foot.x - me.foot.x, z.foot.z - me.foot.z) < Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) ? z : a); chBombCharge(best, R); return true; }   // 적이 없으면 나와 가장 가까운 동료
    const pool = cand.filter((z) => T.d || T.tk ? !z.space : z.space === T.sp), use = pool.length ? pool : cand;
    const best = use.reduce((a, z) => Math.hypot(z.foot.x - T.x, z.foot.z - T.z) < Math.hypot(a.foot.x - T.x, a.foot.z - T.z) ? z : a);
    chBombCharge(best, R); const B = best.bombing; if (!B) return true;
    if (T.c) B.tg = T.c; else if (T.d) B.drone = T.d; else B.drone = { get x() { return tk.x; }, get z() { return tk.z; }, get dead() { return tk.wreck; } };   // 보스 — 드론처럼 그 자리로 뛰어들어 터진다
    return true;
  }
"""))
open('c435_patch.py', 'w').write("# c435: 자폭 — 적 먼저 고르기\nC435_R = " + repr(R) + "\n")
