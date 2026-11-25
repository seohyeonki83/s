import pathlib
s = pathlib.Path('c463.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
# 1. 유혹 중인 군인 · 저격수 · 로봇은 안 쏜다
rep("    if (c.military && c.state !== 'fight' && c.state !== 'evade') moveShoot(c, dt, true);",
    "    if (c.state === 'lured') c.burstN = 0;   // c464: 유혹 중엔 연사도 끊는다\n    if (c.military && c.state !== 'fight' && c.state !== 'evade' && c.state !== 'lured') moveShoot(c, dt, true);   /* c464: 끌려가며 쏘던 것 */")
# 2. 전기폭탄 — 나를 중심으로 퍼지는 원형 전기
rep("    const f = puff(x, 0.4, z, 0xfff27a, 0.6, Rr * 2.2, 0.35, 0, 0, 0, 0.55); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.6; f.peak = true;\n    const g = puff(x, 0.5, z, 0xffffff, 0.4, Rr * 1.2, 0.18, 0, 0, 0, 0.8); g.s.material.map = flashTex; g.s.renderOrder = UI - 0.55; g.peak = true;",
    "    const g = puff(x, 0.5, z, 0xffffff, 0.4, 2.2, 0.18, 0, 0, 0, 0.8); g.s.material.map = flashTex; g.s.renderOrder = UI - 0.55; g.peak = true;   // 가운데 작은 번쩍\n    chEBRing(x, z, Rr);   // c464: 원으로 퍼지는 전기")
rep("  function chEBomb() {", r"""  const chEBL = [];                           // c464: 전기폭탄 고리 {x, z, R, t, m: [바깥 노랑, 안쪽 흰 줄]}
  const CH_EB_T = 0.38, CH_EB_F = 0.22, CH_EB_N = 120;
  function chEBRing(x, z, R) {
    const m = [[0xfff27a, 0.32, 0.9], [0xffffff, 0.12, 1]].map(([col, w, op]) => {
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array((CH_EB_N + 1) * 6), 3));
      const idx = []; for (let i = 0; i < CH_EB_N; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } geo.setIndex(idx);
      const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthTest: false, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending }));
      mesh.renderOrder = UI - 0.6; mesh.frustumCulled = false; scene.add(mesh); mesh.userData = { w, op }; return mesh;
    });
    chEBL.push({ x, z, R: Math.max(R, 0.8), t: 0, m, ph: Math.random() * 10 });
  }
  function chEBTick(dt) {
    for (let i = chEBL.length - 1; i >= 0; i--) {
      const E = chEBL[i]; E.t += dt;
      if (E.t >= CH_EB_T + CH_EB_F) { for (const m of E.m) { scene.remove(m); m.geometry.dispose(); m.material.dispose(); } chEBL.splice(i, 1); continue; }
      const k = Math.min(1, E.t / CH_EB_T), r = E.R * (1 - Math.pow(1 - k, 2)), fade = E.t > CH_EB_T ? 1 - (E.t - CH_EB_T) / CH_EB_F : 1, jag = 0.18 + 0.22 * Math.min(1, E.R / 6);
      for (const m of E.m) {
        const P = m.geometry.attributes.position.array, w = m.userData.w;
        for (let j = 0; j <= CH_EB_N; j++) {   // 지그재그 — 프레임마다 새로 (번개처럼 떨린다)
          const a = j / CH_EB_N * Math.PI * 2, n = j % CH_EB_N ? (Math.random() * 2 - 1) * jag * (j % 2 ? 1 : 0.4) : 0, rr = Math.max(0.05, r + n), c = Math.cos(a), sn = Math.sin(a);
          P.set([E.x + c * Math.max(0, rr - w), 0.42, E.z + sn * Math.max(0, rr - w), E.x + c * (rr + w), 0.42, E.z + sn * (rr + w)], j * 6);
        }
        m.geometry.attributes.position.needsUpdate = true; m.material.opacity = m.userData.op * fade;
      }
      if (fade === 1 && Math.random() < dt * 60) { const a = Math.random() * Math.PI * 2; puff(E.x + Math.cos(a) * r, 0.5, E.z + Math.sin(a) * r, 0xfff27a, 0.25, 0.6, 0.18, 0, 0, 0, 0.9).s.material.map = flashTex; }   // 고리 위 불꽃
    }
  }
  function chEBomb() {""")
rep("    if (CHAPTER && chChainL.length) chChainTick(dt);   // c431", "    if (CHAPTER && chChainL.length) chChainTick(dt);   // c431\n    if (chEBL.length) chEBTick(dt);   // c464")
pathlib.Path('c464_patch.py').write_text('C464_R = ' + repr(R) + '\n')
