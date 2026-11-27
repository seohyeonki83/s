import pathlib
s = pathlib.Path('c518.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    if (CHAPTER && !CH_ET) chSfTick(dt);   // c463 · c122", "    if (CHAPTER && !CH_ET) chSfTick(dt);   // c463 · c122\n    if (CHAPTER) chChestBlink();   // c519")
rep("  function addSafe(S) {", r"""  let chGlowTex = null;
  function chChestBlink() {                   // c519: 보물상자(금고)가 금빛으로 깜빡인다 — 뒤에 빛 번짐 + 상자도 살짝 밝아졌다 어두워졌다
    const k = 0.5 + 0.5 * Math.sin(clock * 5.5);   // 약 0.9초에 한 번
    for (const b of bodies) {
      if (b.kind !== 'safe' || b.dead || !b.mesh || b.mesh.material.map !== chestTex) continue;   // 보물상자 그림인 것만
      if (!b.glow) {
        if (!chGlowTex) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'), gr = g.createRadialGradient(64, 64, 6, 64, 64, 64); gr.addColorStop(0, 'rgba(255,236,120,1)'); gr.addColorStop(0.5, 'rgba(255,190,30,0.75)'); gr.addColorStop(1, 'rgba(255,150,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); chGlowTex = new THREE.CanvasTexture(c); }
        b.glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: chGlowTex, transparent: true, depthTest: false, depthWrite: false}));
        b.glow.renderOrder = (b.mesh.renderOrder || 0) - 0.01; b.glow.scale.set(3.4, 3.4, 1); b.mesh.add(b.glow);
      }
      b.glow.material.opacity = 0.15 + 0.85 * k; const sc = 3.2 + 1.4 * k; b.glow.scale.set(sc, sc, 1);
      b.mesh.material.color.setScalar(0.85 + 0.15 * k); b.mesh.scale.setScalar(0.7 * (1 + 0.08 * k));
    }
  }
  function addSafe(S) {""")
pathlib.Path('c519_patch.py').write_text('C519_R = ' + repr(R) + '\n')
print(len(R))
