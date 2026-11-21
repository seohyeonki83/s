# c275: 방 벽도 부서진다 · 철창(사각형 전체)만 안 부서진다
C275_R = []
C275_R.append(("for (const q of out) { const sd", "for (const q of out) { if (chOnJail(q)) { q.noBrk = true; continue; }   /* c275: 철창에 붙은 바깥벽 토막은 안 부서진다 */ const sd"))
C275_R.append(("    const LP = (hs.length", """    const jailS = chRooms.filter((R) => R.type === 'jail').flatMap((J) => J.walls);   // c275: 철창 네 변
    const chOnJail = (q, tol = 1e-6) => jailS.some((s) => { const hz = q[1] === q[3]; if ((s[1] === s[3]) !== hz) return false; const A = hz ? 0 : 1; if (Math.abs(s[1 - A] - q[1 - A]) > tol) return false;
      return Math.min(Math.max(s[A], s[2 + A]), Math.max(q[A], q[2 + A])) - Math.max(Math.min(s[A], s[2 + A]), Math.min(q[A], q[2 + A])) > 0.05; });
    const LP = (hs.length"""))
C275_R.append(("    const keep = walls.filter((w) => !old.has(w)); walls.length = 0;", """    for (const R of chRooms) {                // c275: 방 안쪽 벽도 토막으로 (체력은 그 건물 벽과 같다) — 철창과 철창에 맞붙은 벽(0.3칸 안)은 뺀다
      const P = R.parent; if (R.type === 'jail' || !CH_WALL_T[P.type]) continue;
      const out = [], pcs = [];
      for (const w of R.walls) {
        const hz = w[1] === w[3], edge = hz ? (Math.abs(w[1] - P.z0) < 1e-6 || Math.abs(w[1] - P.z1) < 1e-6) : (Math.abs(w[0] - P.x0) < 1e-6 || Math.abs(w[0] - P.x1) < 1e-6);
        if (edge || chOnJail(w, 0.3)) { out.push(w); continue; }   // 바깥벽 쪽은 건물 벽 토막이 부서질 때 같이 뚫린다
        old.add(w);
        const x0 = Math.min(w[0], w[2]) - 0.06, x1 = Math.max(w[0], w[2]) + 0.06, z0 = Math.min(w[1], w[3]) - 0.06, z1 = Math.max(w[1], w[3]) + 0.06;
        R.inner = R.inner.filter((m) => { const on = m.position.x > x0 && m.position.x < x1 && m.position.z > z0 && m.position.z < z1; if (on) scene.remove(m); return !on; });
        const [ax, az, bx, bz] = w, n = Math.max(1, Math.round(sl(w) / LP));
        for (let i = 0; i < n; i++) { const q = [ax + (bx - ax) * i / n, az + (bz - az) * i / n, ax + (bx - ax) * (i + 1) / n, az + (bz - az) * (i + 1) / n]; out.push(q); pcs.push(q); add.push(q); }
      }
      if (!pcs.length) continue;
      R.walls = out; R.wos = []; R.faces = {}; chWallBs.push(R);
      for (const q of pcs) {
        q.m = flat(Math.abs(q[2] - q[0]) + WALL, Math.abs(q[3] - q[1]) + WALL, (q[0] + q[2]) / 2, (q[1] + q[3]) / 2, wallMat, -0.505); q.m.visible = false; R.inner.push(q.m);
        const sd = q[1] === q[3] ? (Math.abs(q[1] - R.z0) < 1e-6 ? 'n' : 's') : (Math.abs(q[0] - R.x0) < 1e-6 ? 'w' : 'e'), F = R.faces[sd] || (R.faces[sd] = { wHit: new Map(), wN: 0, wNF: -1, meT: -9 });
        const o = { F, kind: 'obj', type: 'wall', B: R, seg: q, foot: new THREE.Vector3((q[0] + q[2]) / 2, 0, (q[1] + q[3]) / 2), hp: 1, maxHp: 1, dead: false, off: false, k: CH_WALL_T[P.type] }; q.wo = o; R.wos.push(o); chWallObjs.push(o);
      }
    }
    const keep = walls.filter((w) => !old.has(w)); walls.length = 0;"""))
# 방 벽은 그 방 안 · 그 건물 복도에서 친다. 건물 바깥벽은 그 건물 방 안에서도 친다
C275_R.append(("if (z.space && z.space !== B) continue;", "if (B.parent ? z.space !== B && z.space !== B.parent : z.space && z.space !== B && z.space.parent !== B) continue;   /* c275 */"))
# 뚫린 방 벽 = 방문 (길 찾기)
C275_R.append(("""      B.doors.push(L);
    }
    B.tkCut = true;""", """      if (!(B.rooms || []).some((R) => L.cx > R.x0 - 0.05 && L.cx < R.x1 + 0.05 && L.cz > R.z0 - 0.05 && L.cz < R.z1 + 0.05)) B.doors.push(L);   // c275: 방에 붙은 자리면 방의 쪽문이 된다 (아래)
    } else {                                  // c275: 방 벽이 뚫리면 방문처럼 드나든다 — 안쪽 벽 = 복도로, 바깥벽 쪽 = 밖으로
      const side = hz ? (Math.abs(az - B.z0) < Math.abs(az - B.z1) ? 'n' : 's') : (Math.abs(ax - B.x0) < Math.abs(ax - B.x1) ? 'w' : 'e');
      const nx = side === 'e' ? 1 : side === 'w' ? -1 : 0, nz = side === 's' ? 1 : side === 'n' ? -1 : 0;
      L = { side, cx: hz ? (h0 + h1) / 2 : ax, cz: hz ? az : (h0 + h1) / 2, nx, nz, tx: -nz, tz: nx, w: h1 - h0, hole: true, ext: !!edge, out: edge ? undefined : P };
      B.doors.push(L);
    }
    B.tkCut = true;"""))
C275_R.append(("""    dust(hx, hzz, 26, 2.4); debris(hx, hzz, 30, [0x2b2b2b, 0x3a3a3a, 0x555555], 0.45, 7);
  }""", """    dust(hx, hzz, 26, 2.4); debris(hx, hzz, 30, [0x2b2b2b, 0x3a3a3a, 0x555555], 0.45, 7);
    return L;
  }"""))
C275_R.append(("chWallBreak(B, q, c);", "const L0 = chWallBreak(B, q, c);"))
C275_R.append(("L = B.doors[B.doors.length - 1];", "L = L0;   /* c275 */"))
C275_R.append(("if (B.rooms) for (const R of B.rooms) for (const rs of R.walls.slice()) {", "for (const R of B.rooms || (B.parent ? B.parent.rooms.filter((Q) => Q !== B) : [])) if (R.type !== 'jail') for (const rs of R.walls.slice()) {   /* c275: 방 벽이면 붙어 있는 옆방 벽도 */"))
C275_R.append(("""    o.foot.set((s[0] + s[2]) / 2, 0, (s[1] + s[3]) / 2);
    if (o.warp) chWallWarp(o, true);""", """    o.foot.set((s[0] + s[2]) / 2, 0, (s[1] + s[3]) / 2);
    if (o.B.parent) { o.B.inner = o.B.inner.filter((m) => m.parent); o.B.inner.push(s.m); s.m.visible = !!o.B.parent.open; }   // c275: 방 벽 그림은 건물 지붕이 열렸을 때만
    if (o.warp) chWallWarp(o, true);"""))
# 철창은 전차도 못 뚫는다
C275_R.append(("if (B.type === 'hill' || car.x < B.x0 - R", "if (B.type === 'hill' || B.type === 'jail' || car.x < B.x0 - R"))
C275_R.append(("""      for (const sg of B.walls) {
        if (!chSegBox(""", """      for (const sg of B.walls) {
        if (sg.noBrk) continue;   // c275
        if (!chSegBox("""))
# 짧은 방 벽(문 옆)이 뚫려 몸이 못 지나가면 붙어 있는 방문도 같이 부서진다 · 0.3칸 안에 나란한 옆방 벽도 같이 뚫린다
C275_R.append(("      if (hz ? Math.abs(rs[1] - q[1]) > 1e-6 : Math.abs(rs[0] - q[0]) > 1e-6) continue;", "      if (hz ? Math.abs(rs[1] - q[1]) > (B.parent ? 0.3 : 1e-6) : Math.abs(rs[0] - q[0]) > (B.parent ? 0.3 : 1e-6)) continue;   /* c275: 붙은 옆방 벽은 조금 떨어져 있어도 */"))
C275_R.append(("    rebuildSight(B); B.navDirty = true; visDirty = true;\n    for (const R of B.rooms ||", """    if (B.parent && hi - lo < 1.8) for (const D of B.locks) {   // c275: 문 옆 짧은 방 벽 — 구멍이 좁으면 붙은 방문도 부서진다
      const d = D.obj; if (!d || d.dead || d.off) continue; const s = d.seg;
      if ((s[1] === s[3]) !== hz || Math.abs(s[1 - A] - q[1 - A]) > 1e-6 || Math.max(s[A], s[2 + A]) < lo - 0.05 || Math.min(s[A], s[2 + A]) > hi + 0.05) continue;
      breakObj(d);
      lo = Math.min(lo, s[A], s[2 + A]); hi = Math.max(hi, s[A], s[2 + A]);   // 구멍과 문 자리를 한 구멍으로 (길 찾기가 좁은 쪽으로 가지 않게)
      if (L) { L.w = hi - lo; if (hz) L.cx = (lo + hi) / 2; else L.cz = (lo + hi) / 2; }
      if (hz) c.x = (lo + hi) / 2; else c.z = (lo + hi) / 2; c.hw = (hi - lo) / 2;
    }
    rebuildSight(B); B.navDirty = true; visDirty = true;
    for (const R of B.rooms ||"""))
