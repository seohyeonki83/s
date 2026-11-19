# c203: 집 벽 = 면마다 보통 2토막 (집 전체 8토막 안팎) — 쪽문 후보 자리(안 쓰는 잠긴 문, 부술 수 없던 벽)도 벽 토막에 합친다
#   · 토막 길이 = 집 평균 한 변의 절반 · 다른 건물도 같은 길이로 (크면 토막이 많다)
#   · 어그로: 벽을 때리는 동료 1마리당 +20% (그 건물 벽 전부) · 내가 때리는 토막은 문처럼 공격 거리 4배 안 동료를 부른다
C203_R = [
 ("    const LP = hs.length ? hs.reduce((s, B) => s + B.walls.reduce((t, w) => t + sl(w), 0), 0) / hs.length / 8 : 4, old = new Set(), add = [];",
  "    const LP = hs.length ? hs.reduce((s, B) => s + (B.x1 - B.x0 + B.z1 - B.z0) / 2, 0) / hs.length / 2 : 2.2, old = new Set(), add = [];   // c203: 집 한 변의 절반"),
 ("      const out = [];\n      for (const w of B.walls) { old.add(w); const [ax, az, bx, bz] = w, n = Math.max(1, Math.round(sl(w) / LP));",
  """      const out = []; let segs = B.walls;
      if (B.side && B.sideK !== undefined) {   // c203: 쓰는 쪽문(판마다 같은 자리)·정문·열린 자리만 비우고 나머지 면은 통째로
        const cand = B.locks.filter((L) => !L.front), on = (B.block === START_BLOCK && B.local === 0 && cand.find((L) => L.side === 'n')) || cand[B.sideK % cand.length];
        for (const L of cand) if (L !== on) L.merged = true;
        const gapsOf = (sd) => [...B.doors, ...B.locks.filter((L) => !L.merged)].filter((D) => D.side === sd).map((D) => { const h = (D.w || DOOR) / 2, c = sd === 'n' || sd === 's' ? D.cx : D.cz; return [c - h, c + h]; }).sort((a, b) => a[0] - b[0]);
        segs = [];
        for (const [sd, hz, k, lo, hi] of [['n', 1, B.z0, B.x0, B.x1], ['s', 1, B.z1, B.x0, B.x1], ['w', 0, B.x0, B.z0, B.z1], ['e', 0, B.x1, B.z0, B.z1]]) {
          let cur = lo; const mk = (a, b) => { if (b - a > 1e-6) segs.push(hz ? [a, k, b, k] : [k, a, k, b]); };
          for (const [g0, g1] of gapsOf(sd)) { mk(cur, g0); cur = Math.max(cur, g1); }
          mk(cur, hi);
        }
        for (const w of B.walls) old.add(w);
      }
      for (const w of segs) { old.add(w); const [ax, az, bx, bz] = w, n = Math.max(1, Math.round(sl(w) / LP));"""),
 # 합친 쪽문 후보: 새 판마다 벽 선·그림에서 뺀다 (그 자리는 벽 토막이 덮는다)
 ("    for (const B of chWallBs) { B.wHit.clear(); B.wN = 0; }",
  "    for (const B of chWallBs) { B.wHit.clear(); B.wN = 0; for (const L of B.locks) if (L.merged && L.obj) { const o = L.obj, i = walls.indexOf(o.seg), j = B.walls.indexOf(o.seg); if (i >= 0) walls.splice(i, 1); if (j >= 0) B.walls.splice(j, 1); o.off = true; o.mesh.visible = false; if (o.fill) o.fill.visible = false; } }   // c203"),
 # 어그로 20%씩 · 나는 100%
 ("else n++; } B.wN = n; } return B.wN; }", "else if (z !== me) n++; } B.wN = n; } return B.wN; }   /* c203: 동료만 센다 (나는 문처럼 따로) */"),
 ("return chReach(z) * 0.7 * (1 + 0.1 * chWallN(o.B));", "return z !== me && hotObj(o) ? 4 * MELEE : chReach(z) * 0.7 * (1 + 0.2 * chWallN(o.B));   /* c203: 내가 때리는 벽 토막 = 문처럼 공격 거리 4배 안 동료를 부른다 */"),
 ("const lim = chReach(z) * 0.7 * (1 + 0.1 * chWallN(B)), m = lim + 0.5;", "const lim0 = chReach(z) * 0.7 * (1 + 0.2 * chWallN(B)), m = Math.max(lim0, z !== me ? 4 * MELEE : 0) + 0.5;"),
 ("        if (o.dead) continue; const g = objGap(o, z); if (g > lim ||", "        if (o.dead) continue; const lim = z !== me && hotObj(o) ? Math.max(lim0, 4 * MELEE) : lim0, g = objGap(o, z); if (g > lim ||"),
]
