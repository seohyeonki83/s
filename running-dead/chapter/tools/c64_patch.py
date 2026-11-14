# c64: 경찰 출동 간격 20% 단축 · 근접 거리 안의 적이 사물보다 먼저 (나·동료) · 맞으면 2초 사물 무시는 나도
C64_FN = r"""  // ── c64: 근접 거리 안에 적(사람)이 있으면 사물(문·차·바리케이트·금고)보다 그 적을 먼저 친다 — 나도 동료도 ──
  function chWallCut(ax, az, bx, bz) {         // c64: 두 점을 잇는 선이 살아 있는 바리케이트 줄의 조각(바리케이트·경찰차)을 지나나
    const mx = (ax + bx) / 2, mz = (az + bz) / 2, hl = Math.hypot(bx - ax, bz - az) / 2;
    for (const c of cars) {
      if (!c.wall || c.wreck) continue;
      const hu = CAR_L * ck(c) / 2, hv = CAR_W * ck(c) / 2 * (c.barr ? CH_BARR_W : 1), far = hl + hu + hv;
      if (Math.abs(mx - c.x) > far || Math.abs(mz - c.z) > far) continue;
      const fx = Math.cos(c.h), fz = Math.sin(c.h), px = ax - c.x, pz = az - c.z, qx = bx - ax, qz = bz - az;
      const u0 = px * fx + pz * fz, v0 = -px * fz + pz * fx, du = qx * fx + qz * fz, dv = -qx * fz + qz * fx;
      let t0 = 0, t1 = 1, hit = true;
      for (let k = 0; k < 2 && hit; k++) {
        const p = k ? v0 : u0, d = k ? dv : du, h = k ? hv : hu;
        if (Math.abs(d) < 1e-9) { if (Math.abs(p) > h) hit = false; continue; }
        let a = (-h - p) / d, e = (h - p) / d; if (a > e) { const s = a; a = e; e = s; }
        if (a > t0) t0 = a; if (e < t1) t1 = e; if (t0 > t1) hit = false;
      }
      if (hit) return true;
    }
    return false;
  }
  const chAdjBuf = [];
  function chAdjFoe(z) {                        // 근접 거리 안에서 가장 가까운, 아직 체력이 남은 사람 (같은 공간). 3명 제한과 상관없이
    let best = null, bd = Infinity;
    for (const c of nearIn(cCells, z.foot.x, z.foot.z, MELEE + 1.2, chAdjBuf)) {
      if (c.kind !== 'citizen' || !(c.hp > 0) || c.space !== z.space || c.marked || chWallCut(z.foot.x, z.foot.z, c.foot.x, c.foot.z)) continue;   // 바리케이트 너머는 빼고
      const d = Math.hypot(c.foot.x - z.foot.x, c.foot.z - z.foot.z);
      if (d <= MELEE + Math.max(0, (z.r || BODY) - BODY) + Math.max(0, (c.r || BODY) - BODY) && d < bd) { bd = d; best = c; }
    }
    return best;
  }
"""
C64_R = [
  ("    chDispT = 32 - 3 * (stars - 1);", "    chDispT = (32 - 3 * (stars - 1)) * 0.8;   // c64: 20% 더 짧게 (25.6 · 23.2 · 20.8 · 18.4 · 16초)"),
  ("if (CHAPTER && a && a.kind === 'citizen' && v.kind === 'ally' && !v.dead) v.objOff = clock + 2;", "if (CHAPTER && a && a.kind === 'citizen' && (v.kind === 'ally' || v === me) && !v.dead) v.objOff = clock + 2;   /* c64: 나도 */"),
  ("const go = t || prey;", "const adj = CHAPTER ? chAdjFoe(z) : null, go = t || prey || adj;   /* c64: 3명 제한에 걸렸어도 근접 거리 안의 적은 친다 */"),
  ("const noObj = CHAPTER && z !== me && z.objOff > clock;   /* c58 */", "const noObj = CHAPTER && ((z.objOff > clock && go && !chWallCut(z.foot.x, z.foot.z, go.foot.x, go.foot.z)) || !!adj);   /* c58 · c64: 맞은 지 2초 안(나도)이고 쫓을 사람이 있으면 · 근접 거리 안에 적이 있으면 사물·금고는 안 노린다 (사람이 바리케이트 너머뿐이면 바리케이트를 친다) */"),
  ("  function showDud() {", C64_FN + "  function showDud() {"),
]
