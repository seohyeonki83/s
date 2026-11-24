# c431: 테이저건 갈림길 — 전이 감전 / 전기폭탄
#  · 전이 감전: 내가 쏜 적(숙주)의 감전 +0.3초씩 (빨간 ★6 = 5.3초). 숙주가 감전된 동안 0.8초마다 둘레(공격 거리 1.7칸 × 1 → 2)의 적이 0.2초 감전 (잔류제 영향 없음, 다시 번지지 않음)
#  · 전기폭탄: 쏘는 대신 나를 중심으로 360° 전기 파장 — 범위 = 내 시야 7.2칸 × 빨간 별 ÷ 6, 안의 모든 적(드론 · 보스 포함) 3.5초 감전 (잔류제 영향)
src = open('c430.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    mutate: [   // c430: 동료 변이 좀비", """    taser: [   // c431
      { id: 'chain', nm: '전이 감전', name: '전이 감전', desc: '감전된 적이 더 오래 감전되고, 그 적 둘레의 적들도 0.8초마다 0.2초씩 감전됩니다.', line: (r) => `감전 ${(3.5 + 0.3 * r).toFixed(1)}초 · 둘레 ${(MELEE * (1 + 0.2 * (r - 1))).toFixed(1)}칸 안 적 0.8초마다 0.2초 감전`, short: ['전이', (r) => `${(MELEE * (1 + 0.2 * (r - 1))).toFixed(1)}칸`] },
      { id: 'bomb', nm: '전기폭탄', name: '전기폭탄', desc: '나를 중심으로 전기 파장이 퍼져, 범위 안의 모든 적(드론 · 보스 포함)을 3.5초 동안 감전시킵니다.', line: (r) => `범위 ${(SIGHT * r / 6).toFixed(1)}칸 · 감전 3.5초`, short: ['범위', (r) => `${(SIGHT * r / 6).toFixed(1)}칸`] },
    ],
    mutate: [   // c430: 동료 변이 좀비""")
rep("for (const k of Object.keys(CH_BRANCH)) chBrLook(k);   /* c427 */ chAbsK = null;   /* c430 */", "for (const k of Object.keys(CH_BRANCH)) chBrLook(k);   /* c427 */ chAbsK = null;   /* c430 */ chChainL.length = 0;   /* c431 */")
rep("CH_WV('taserT', lv('taser')) * chLingK();", "chTaserT(c);   /* c431 */", 3)
rep("    if (kind === 'taser') {                   // 내 인지거리 안 적 1명", "    if (kind === 'taser' && CHAPTER && chBr.taser === 'bomb') chEBomb();   // c431: 전기폭탄 — 쏘는 대신 파장\n    else if (kind === 'taser') {                   // 내 인지거리 안 적 1명")
rep("  function itemsTick(dt) {\n", "  function itemsTick(dt) {\n    if (CHAPTER && chChainL.length) chChainTick(dt);   // c431\n")
rep("  function chMutLook(z) {", """  const chChainL = [], chChBuf = [];           // c431: 전이 감전 숙주 {e, t: 남은 감전, k: 다음 번개까지, r: 빨간 별}
  function chTaserT(e) {                       // c431: 테이저 감전 시간 (전이 감전이면 +0.3초씩 · 숙주로 등록)
    const r = chBrR('taser', 'chain'), T = (CH_WV('taserT', lv('taser')) + 0.3 * r) * chLingK();
    if (r) chChainL.push({ e, t: T, k: 0.8, r });
    return T;
  }
  function chChainTick(dt) {                   // c431: 숙주가 감전된 동안 0.8초마다 둘레 적 0.2초 감전 (잔류제 영향 없음 · 다시 번지지 않음)
    for (let i = chChainL.length - 1; i >= 0; i--) {
      const H = chChainL[i], e = H.e, gone = e.drone ? e.dead : e.tank ? e.wreck : e.kind !== 'citizen' || !bodies.includes(e);
      if (gone || (H.t -= dt) <= 0) { chChainL.splice(i, 1); continue; }
      if ((H.k -= dt) > 0) continue; H.k = 0.8;
      const x = e.foot ? e.foot.x : e.x, z = e.foot ? e.foot.z : e.z, Rr = MELEE * (1 + 0.2 * (H.r - 1));
      const zap = (tx, tz) => { const f = puff(tx, 0.7, tz, 0xfff27a, 0.5, 0.15, 0.18, 0, 0.4, 0, 1); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; };
      zap(x, z);
      for (const c of nearIn(cCells, x, z, Rr, chChBuf)) { if (c === e || c.kind !== 'citizen' || c.space !== (e.space ?? null) || Math.hypot(c.foot.x - x, c.foot.z - z) > Rr) continue; c.stunT = Math.max(c.stunT || 0, 0.2); c.vel.set(0, 0); c.lungeT = -1; zap(c.foot.x, c.foot.z); }
      for (const d of chDrones) { if (d === e || d.dead || Math.hypot(d.x - x, d.z - z) > Rr + d.r) continue; d.stunT = Math.max(d.stunT || 0, 0.2); zap(d.x, d.z); }
      const T = chTank; if (T && T !== e && !T.wreck && Math.hypot(T.x - x, T.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) { T.stunT = Math.max(T.stunT || 0, 0.2); T.vx = T.vz = 0; zap(T.x, T.z); }
    }
  }
  function chEBomb() {                         // c431: 전기폭탄 — 나를 중심으로 360° 파장, 범위 안 모든 적 3.5초 감전 (잔류제 영향)
    const r = chBrR('taser', 'bomb'), Rr = SIGHT * r / 6, T = 3.5 * chLingK(), x = me.foot.x, z = me.foot.z;
    const f = puff(x, 0.4, z, 0xfff27a, 0.6, Rr * 2.2, 0.35, 0, 0, 0, 0.55); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.6; f.peak = true;
    const g = puff(x, 0.5, z, 0xffffff, 0.4, Rr * 1.2, 0.18, 0, 0, 0, 0.8); g.s.material.map = flashTex; g.s.renderOrder = UI - 0.55; g.peak = true;
    for (const c of bodies) { if (c.kind !== 'citizen' || c.state === 'held') continue; if ((c.space !== me.space && !linked(c.space, me.space)) || Math.hypot(c.foot.x - x, c.foot.z - z) > Rr || fireBlocked(x, z, c.foot.x, c.foot.z)) continue; c.stunT = Math.max(c.stunT || 0, T); c.vel.set(0, 0); zaps.push({ to: c, t: 0.3 }); }
    for (const d of chDrones) { if (d.dead || Math.hypot(d.x - x, d.z - z) > Rr + d.r) continue; d.stunT = Math.max(d.stunT || 0, T); zaps.push({ to: d, t: 0.3 }); }
    const tk = chTank; if (tk && !tk.wreck && Math.hypot(tk.x - x, tk.z - z) - CAR_L * CH_TK_KL / 2 <= Rr) { tk.stunT = Math.max(tk.stunT || 0, T); tk.vx = tk.vz = 0; zaps.push({ to: tk, t: 0.3 }); }
  }
  function chMutLook(z) {""")
open('c431_patch.py', 'w').write("# c431: 테이저건 갈림길\nC431_R = " + repr(R) + "\n")
print(len(R))
