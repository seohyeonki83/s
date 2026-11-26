import pathlib, re
s = pathlib.Path('c511.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
L = s.split('\n')
for ln in [2278, 3241, 3344, 3417, 3436, 3444, 3770, 3801, 5916, 8388]:
    line = L[ln - 1]
    new = re.sub(r'\b([a-z]+)\.space !== ([a-z]+)\.space\b', r'!chSameSp(\1.space, \2.space)', line)
    new = re.sub(r'\b([a-z]+)\.space === ([a-z]+)\.space\b', r'chSameSp(\1.space, \2.space)', new)
    assert new != line, ln
    rep(line, new)
rep("  const linked = (a, b) => a === b ||", """  // c512: 벽 없이 통째로 이어진 두 건물(튜토리얼 복도 꺾이는 곳처럼)은 싸울 때 한 공간 — 서로 다른 칸이라 옆에 두고도 못 때리고 맴돌던 것
  let chNbrOk = false;
  function chNbrBuild() {
    chNbrOk = true; const top = buildings.filter((B) => !B.parent && B.walls), E = 0.02;
    const walled = (B, x0, z0, x1, z1) => B.walls.some(([ax, az, bx, bz]) => (ax === bx && x0 === x1 && Math.abs(ax - x0) < E && Math.min(az, bz) <= z0 + E && Math.max(az, bz) >= z0 - E) || (az === bz && z0 === z1 && Math.abs(az - z0) < E && Math.min(ax, bx) <= x0 + E && Math.max(ax, bx) >= x0 - E));
    const locked = (B, x, z) => (B.locks || []).some((K) => K.obj && Math.abs(K.cx - x) < (K.nz ? (K.w || DOOR) / 2 + E : E) && Math.abs(K.cz - z) < (K.nz ? E : (K.w || DOOR) / 2 + E));
    for (let i = 0; i < top.length; i++) for (let j = i + 1; j < top.length; j++) {
      const A = top[i], B = top[j]; let pts = null;
      for (const [P, Q] of [[A, B], [B, A]]) {
        if (Math.abs(P.x1 - Q.x0) < E) { const a = Math.max(P.z0, Q.z0), b = Math.min(P.z1, Q.z1); if (b - a > 1) pts = [0.2, 0.35, 0.5, 0.65, 0.8].map((t) => [P.x1, a + (b - a) * t, P.x1, a + (b - a) * t]); }
        if (Math.abs(P.z1 - Q.z0) < E) { const a = Math.max(P.x0, Q.x0), b = Math.min(P.x1, Q.x1); if (b - a > 1) pts = [0.2, 0.35, 0.5, 0.65, 0.8].map((t) => [a + (b - a) * t, P.z1, a + (b - a) * t, P.z1]); }
      }
      if (!pts || !pts.some(([x, z]) => !walled(A, x, z, x, z) && !walled(B, x, z, x, z) && !locked(A, x, z) && !locked(B, x, z))) continue;
      (A.nbr = A.nbr || new Set()).add(B); (B.nbr = B.nbr || new Set()).add(A);
    }
  }
  function chSameSp(a, b) { if (a === b) return true; if (!CHAPTER || !a || !b || a.parent || b.parent) return false; if (!chNbrOk) chNbrBuild(); return !!(a.nbr && a.nbr.has(b)); }
  const linked = (a, b) => a === b || chSameSp(a, b) ||""")
rep("(b.space === z.space || (linked(z.space, b.space) && zSeen(b)))", "(chSameSp(b.space, z.space) || (linked(z.space, b.space) && zSeen(b)))")
pathlib.Path('c512_patch.py').write_text('C512_R = ' + repr(R) + '\n')
print(len(R))
