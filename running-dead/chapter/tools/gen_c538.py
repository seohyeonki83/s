import pathlib
s = pathlib.Path('c537.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1. 기록 전부 리셋 (v4)
rep("    if (!o.v3) { o = { genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1 }; }", "    if (!o.v4) { o = { genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1, v4: 1 }; }   // c538: 챕터 개편 — 기록 전부 초기화")
rep("tut: false, mig: 1, v2: 1, v3: 1 })); window.name", "tut: false, mig: 1, v2: 1, v3: 1, v4: 1 })); window.name")
# 2. 하양 · 노랑 15% 덜 (튜토리얼 빼고 · 건물 안 포함) — 다 깔고 난 뒤 15%를 고르게 뺀다 (다시 채우는 목표 수도 같이 줄인다)
rep("chDecoPlace(); chStartW = {", "chDecoPlace(); if (!CH_TUT) chCull15(); chStartW = {")
rep("  function chPopulate() {", r"""  function chCull15() {                        // c538: 하양('') · 노랑('guard') 15% 빼기
    const L = bodies.filter((b) => b.kind === 'citizen' && !b.police && !b.attacker && !b.robot && !b.boss && !b.fixed && b !== me);
    for (let i = L.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [L[i], L[j]] = [L[j], L[i]]; }
    const cut = new Set(L.slice(0, Math.round(L.length * 0.15)));
    for (const b of cut) {
      for (const o of [b.mesh, b.hpBar, b.icon, b.gauge, b.mark, b.tracer, b.tracer2]) if (o && o.parent) o.parent.remove(o);
      b.kind = 'gone';
      if (chPop) { for (const Z of chPop.one) for (const k of ['', 'guard']) { const P = Z[k], i = P.list.indexOf(b); if (i >= 0) { P.list.splice(i, 1); P.want = Math.max(0, P.want - 1); } }
        for (const G of [...chPop.gangs, ...chPop.wg]) { const i = G.members ? G.members.indexOf(b) : -1; if (i >= 0) { G.members.splice(i, 1); if (G.types && G.types.length > G.members.length) G.types.splice(Math.min(i, G.types.length - 1), 1); } }
        chPop.gangs = chPop.gangs.filter((G) => !G.members || G.members.length); chPop.wg = chPop.wg.filter((G) => !G.members || G.members.length); }
    }
    let w = 0; for (const b of bodies) if (!cut.has(b)) bodies[w++] = b; bodies.length = w;
  }
  function chPopulate() {""")
# 3. 미니맵 목표 — 빨간 해골 · 미니맵 밖이면 테두리에 걸린다 · 아직 안 나온 목표는 없다
rep("    const r = 2.1 * 1.5 * u;   /* c352: 1.5배 */", r"""    if (CH_RUN) {   // c538: 클리어 목표 표시
      const P = chObjPts(), cx = W / 2, cy = H / 2, rr = Math.min(W, H) / 2 - 7 * u;
      for (const [x, z] of P) {
        let px = X(x), py = Z(z);
        if (!mmBig) { const dx = px - cx, dy = py - cy, d = Math.hypot(dx, dy); if (d > rr) { px = cx + dx / d * rr; py = cy + dy / d * rr; } }
        else { px = Math.max(7 * u, Math.min(W - 7 * u, px)); py = Math.max(7 * u, Math.min(H - 7 * u, py)); }
        chSkull(g, px, py, 5.2 * u);
      }
    }
    const r = 2.1 * 1.5 * u;   /* c352: 1.5배 */""")
rep("  function chMinimap(eyes, W, H, X, Z, sx, sz) {", r"""  function chSkull(g, x, y, s) {               // c538: 단순한 빨간 해골
    g.fillStyle = 'rgba(0,0,0,0.75)'; g.beginPath(); g.arc(x, y, s * 1.25, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#ff3030'; g.beginPath(); g.arc(x, y - s * 0.15, s * 0.82, 0, Math.PI * 2); g.fill(); g.fillRect(x - s * 0.48, y + s * 0.3, s * 0.96, s * 0.55);
    g.fillStyle = '#111'; g.beginPath(); g.arc(x - s * 0.33, y - s * 0.12, s * 0.22, 0, Math.PI * 2); g.arc(x + s * 0.33, y - s * 0.12, s * 0.22, 0, Math.PI * 2); g.fill();
    g.fillRect(x - s * 0.05, y + s * 0.38, s * 0.1, s * 0.42); g.fillRect(x - s * 0.3, y + s * 0.38, s * 0.08, s * 0.42); g.fillRect(x + s * 0.22, y + s * 0.38, s * 0.08, s * 0.42);
  }
  function chObjPts() {                         // c538: 지금 미니맵에 보일 클리어 목표들 (특공대 한 명씩 · 보스)
    const P = [];
    if (!CH_RUN || chSf.won) return P;
    if (CH_DIF !== 'h') {
      for (const b of bodies) if (b.kind === 'citizen' && b.sfw && b.sfw <= chSfLast()) P.push([b.foot.x, b.foot.z]);
      for (const c of cars) if (c.sfw && c.sfw <= chSfLast() && !c.wreck && !c.crewOut) P.push([c.x, c.z]);
    } else if (chSf.bossOut) {
      for (const t of chTanks) if (!t.wreck) P.push([t.x, t.z]);
      for (const c of chCvy) if (!c.wreck && !c.crewOut && cars.includes(c)) P.push([c.x, c.z]);
      for (const b of bodies) if (b.kind === 'citizen' && b.cvy) P.push([b.foot.x, b.foot.z]);
      for (const d of chDrones) if (d.cvy && !d.dead) P.push([d.x, d.z]);
    }
    return P;
  }
  function chMinimap(eyes, W, H, X, Z, sx, sz) {""")
pathlib.Path('c538_patch.py').write_text('C538_R = ' + repr(R) + '\n')
print(len(R))
