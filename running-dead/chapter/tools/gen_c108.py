# c108 패치 만들기 — 집 금고 5분의 1 · 사물 하트 20분의 1(체력 30%) · 유전자(재화): 사물 20분의 1로 1~4개 · 시민 한 명 감염마다 1개 · 위에 작은 표시
import pprint
S = open('c107.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))

rep("  const CH_HOUSE_SAFE = 0.05;", "  const CH_HOUSE_SAFE = 0.2;   /* c108: 집 다섯 중 하나에 금고 */")
rep("  const CH_HEART_P = 3 / 50;   // c90: 3배", "  const CH_HEART_P = 1 / 20, CH_GENE_P = 1 / 20;   // c108: 사물이 부서질 때 하트 20분의 1 · 유전자 20분의 1 (어느 사물이든)")
rep("    if (D.store && Math.random() < CH_HEART_P) chHeartDrop(x, z, space);", "    if (Math.random() < CH_HEART_P) chHeartDrop(x, z, space);\n    if (Math.random() < CH_GENE_P) chGeneDrop(x, z, space);   // c108")
rep("    me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.5);\n    for (let i = 0; i < 16; i++)", "    me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.3);   /* c108: 30% */\n    for (let i = 0; i < 16; i++)")
rep("    deaths++;\n", "    deaths++; if (CHAPTER) chGeneAdd(1);   // c108: 시민 한 명마다 유전자 1\n")
rep("      p.s.position.set(p.x, 0, p.z).addScaledVector(UP, 1.0 + Math.sin(p.t * 3) * 0.12);",
    "      if (p.kind === 'gene' && p.t < 0.45) { const k = Math.max(0, p.t / 0.45); p.s.position.set(p.x0 + (p.x - p.x0) * k, 0, p.z0 + (p.z - p.z0) * k).addScaledVector(UP, 0.7 + Math.sin(Math.PI * k) * 1.5); continue; }   // c108: 유전자는 뾰로롱 튀어나와 땅에 떨어진다 (떨어지기 전엔 못 줍는다)\n"
    "      p.s.position.set(p.x, 0, p.z).addScaledVector(UP, (p.kind === 'gene' ? 0.7 : 1.0) + Math.sin(p.t * 3) * 0.12);")
rep("        if (p.kind === 'heart') chHeartEat(); else pendingAward.push(p.kind);", "        if (p.kind === 'heart') chHeartEat(); else if (p.kind === 'gene') chGeneEat(p); else pendingAward.push(p.kind);")
rep("  function showDud() {", r'''  // ── c108: 유전자 (재화) — 시민 한 명을 감염시킬 때마다 1개, 사물이 부서질 때 20분의 1로 1~4개가 땅에 튀어나온다. 모은 수는 위에 작게 보이고 다음 판에도 남는다 ──
  const CH_GENE_SVG = '<svg viewBox="0 0 24 24" width="13" height="13"><path d="M7 2c0 6 10 6 10 10S7 16 7 22" fill="none" stroke="#7fe3ff" stroke-width="2.6" stroke-linecap="round"/><path d="M17 2c0 6-10 6-10 10s10 4 10 10" fill="none" stroke="#c78bff" stroke-width="2.6" stroke-linecap="round"/><path d="M9 5h6M9.5 19h5M8.5 12h7" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round"/></svg>';
  let chGenes = 0; try { chGenes = +localStorage.getItem('rd_genes') || 0; } catch (e) {}
  const chGeneEl = document.createElement('div');
  chGeneEl.id = 'gene';
  chGeneEl.style.cssText = 'position:absolute;left:max(16px, env(safe-area-inset-left, 0px));top:calc(34px + env(safe-area-inset-top, 0px));z-index:4;pointer-events:none;display:flex;align-items:center;gap:3px;font:800 11px/1 system-ui,sans-serif;color:#d8f6ff;text-shadow:0 1px 3px rgba(0,0,0,0.85)';
  chGeneEl.innerHTML = CH_GENE_SVG + '<span>' + chGenes + '</span>';
  stage.appendChild(chGeneEl);
  function chGeneAdd(n) { chGenes += n; chGeneEl.lastChild.textContent = chGenes; try { localStorage.setItem('rd_genes', String(chGenes)); } catch (e) {} }
  let chGeneTex = null;
  function chGeneDrop(x, z, space) {           // 1~4개가 사방으로 튀어나온다 — 하나씩 따로 줍는다
    if (!chGeneTex) chGeneTex = chTexOf(96, 96, (g) => {
      g.lineCap = 'round';
      const strand = (sg, col) => { g.beginPath(); for (let i = 0; i <= 40; i++) { const t = i / 40, y = 10 + t * 76, xx = 48 + sg * Math.sin(t * Math.PI * 2) * 20; if (i) g.lineTo(xx, y); else g.moveTo(xx, y); } g.lineWidth = 15; g.strokeStyle = '#10202c'; g.stroke(); g.lineWidth = 9; g.strokeStyle = col; g.stroke(); };
      g.strokeStyle = '#ffffff'; g.lineWidth = 5; for (const t of [0.12, 0.25, 0.38, 0.62, 0.75, 0.88]) { const y = 10 + t * 76, w = Math.abs(Math.sin(t * Math.PI * 2)) * 20; g.beginPath(); g.moveTo(48 - w, y); g.lineTo(48 + w, y); g.stroke(); }
      strand(1, '#7fe3ff'); strand(-1, '#c78bff');
    });
    const n = 1 + Math.floor(Math.random() * 4), a0 = Math.random() * 6.283;
    for (let i = 0; i < n; i++) {
      const a = a0 + i / n * 6.283 + rand(-0.4, 0.4), r = rand(0.7, 1.3); let tx = x + Math.cos(a) * r, tz = z + Math.sin(a) * r;
      if (spaceOf(tx, tz) !== (space || null) || blocked(x, z, tx, tz)) { tx = x + Math.cos(a) * 0.25; tz = z + Math.sin(a) * 0.25; }   // 벽 너머로는 안 튄다
      const p = { kind: 'gene', x: tx, z: tz, x0: x, z0: z, space, t: -i * 0.06 };
      p.s = new THREE.Sprite(new THREE.SpriteMaterial({ map: chGeneTex, transparent: true, depthTest: false, depthWrite: false })); p.s.renderOrder = UI - 1; p.s.scale.set(0.8, 0.8, 1); p.s.position.set(x, 0.7, z); scene.add(p.s);
      pickups.push(p);
    }
    for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; puff(x, 0.5, z, i % 2 ? 0x7fe3ff : 0xc78bff, 0.35, 1.0, 0.45, Math.cos(a) * 2.2, 0.8, Math.sin(a) * 2.2, 0.8); }
  }
  function chGeneEat(p) { chGeneAdd(1); for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; puff(p.x, 0.7, p.z, 0x9fe8ff, 0.3, 0.9, 0.4, Math.cos(a) * 1.4, 1.0, Math.sin(a) * 1.4, 0.8); } }
  function showDud() {''')
open('c108_patch.py', 'w', encoding='utf8').write('# c108: 집 금고 5분의 1 · 하트 20분의 1(30%) · 유전자 재화 (gen_c108.py가 만든다)\nC108_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
