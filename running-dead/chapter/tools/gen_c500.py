import pathlib
s = pathlib.Path('c499.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("""    for (const P of CH_MAP.passPts) {                                     // c4: 길목 — 그 자리를 밝혔으면 양쪽 화살표
      if (!P.found && explored[Math.floor((P.z - MM.z0) / MM_CELL) * mmW + Math.floor((P.x - MM.x0) / MM_CELL)]) P.found = true;
      if (P.found) g.drawImage(CH_ICON[P.dir === 'h' ? 'passH' : 'passV'], X(P.x) - sz2 / 2, Z(P.z) - sz2 / 2, sz2, sz2);
    }""", """    CH_MAP.passPts.forEach((P, i) => {                                    // c500: 건널목 — 양쪽 입구에 노란 화살표 (들어가는 쪽을 가리킨다) · 밝힌 입구만
      const Q = CH_MAP.passes2 && CH_MAP.passes2[i], ex = (x, z) => explored[Math.floor((z - MM.z0) / MM_CELL) * mmW + Math.floor((x - MM.x0) / MM_CELL)];
      if (!Q) { if (!P.found && ex(P.x, P.z)) P.found = true; if (P.found) g.drawImage(CH_ICON[P.dir === 'h' ? 'passH' : 'passV'], X(P.x) - sz2 / 2, Z(P.z) - sz2 / 2, sz2, sz2); return; }   // c4 (끝점이 없는 맵)
      for (const [ax, az, bx, bz, k] of [[Q.ax, Q.az, Q.bx, Q.bz, 'fa'], [Q.bx, Q.bz, Q.ax, Q.az, 'fb']]) {
        if (!P[k] && ex(ax, az)) P[k] = true; if (!P[k]) continue;
        const cx = X(ax), cz = Z(az), dx = X(bx) - cx, dz = Z(bz) - cz, l = Math.hypot(dx, dz) || 1, ux = dx / l, uz = dz / l, r = sz2 * 0.6;
        g.beginPath(); g.moveTo(cx + ux * r, cz + uz * r); g.lineTo(cx - ux * r * 0.55 - uz * r * 0.8, cz - uz * r * 0.55 + ux * r * 0.8); g.lineTo(cx - ux * r * 0.55 + uz * r * 0.8, cz - uz * r * 0.55 - ux * r * 0.8); g.closePath();
        g.fillStyle = '#ffd34d'; g.fill(); g.lineWidth = 1.2 * u; g.strokeStyle = 'rgba(0, 0, 0, 0.85)'; g.stroke();
      }
    });""")
rep("if (CHAPTER) for (const P of CH_MAP.passPts) P.found = false;", "if (CHAPTER) for (const P of CH_MAP.passPts) P.found = P.fa = P.fb = false;   /* c500 */")
pathlib.Path('c500_patch.py').write_text('C500_R = ' + repr(R) + '\n')
