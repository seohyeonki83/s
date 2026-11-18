# c156: 성능(그리기) — 보통 몸(동료·사람의 맨 원)을 한 번에 묶어 그린다 (InstancedMesh). 그리기 명령이 몸 수만큼에서 한 번으로 준다
#   · 묶는 것: 원 모양 그대로이고 붙은 것(몽둥이·산성·테두리)이 없는 동료·사람. 나·빨강(몽둥이)·산성 묻은 사람·사물·금고는 전처럼 하나씩 그린다
#   · 앞뒤 순서: 묶음 안에서는 전처럼 먼 것부터. 사물이나 하나씩 그리는 몸 바로 옆(겹칠 수 있는 거리)의 몸은 묶지 않고 전처럼 그려서 순서가 안 바뀐다
#   · window.__noBatch = true 면 끈다 (비교용)
JS = r"""  const CH_BATCH_MAX = 1024;
  const chBatch = new THREE.InstancedMesh(circleGeo, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, depthTest: false, depthWrite: false }), CH_BATCH_MAX);
  chBatch.frustumCulled = false; chBatch.renderOrder = -0.01; chBatch.count = 0; chBatch.instanceMatrix.setUsage(THREE.DynamicDrawUsage); scene.add(chBatch);
  const chBM = new THREE.Matrix4(), chBList = [], chBSpec = [], chBFwd = new THREE.Vector3();
  function chBatchBodies() {
    chBList.length = 0; chBSpec.length = 0;
    const off = !!window.__noBatch;
    for (const b of bodies) {
      const m = b.mesh;
      if (!m.visible) { if (m.layers.mask !== 1) m.layers.set(0); continue; }
      if (!off && (b.kind === 'ally' || b.kind === 'citizen') && m.geometry === circleGeo && m.children.length === 0 && m.renderOrder === 0 && m.material.opacity === 1 && !m.material.map) chBList.push(b);
      else { chBSpec.push(b); if (m.layers.mask !== 1) m.layers.set(0); }
    }
    camera.getWorldDirection(chBFwd);
    let n = 0;
    for (let i = 0; i < chBList.length; i++) {
      const b = chBList[i], m = b.mesh; let alone = n < CH_BATCH_MAX;
      if (alone) for (let k = 0; k < chBSpec.length; k++) { const s = chBSpec[k], rd = s.mesh.geometry === circleGeo, lx = rd ? 1.1 * s.mesh.scale.x : 1.0 + (s.r || 0.5), lz = rd ? lx : (s.halfH ? s.halfH * 2 : 1) + 1.0, dx = s.foot.x - b.foot.x, dz = s.foot.z - b.foot.z; if (dx < lx && dx > -lx && dz < lz && dz > -lz) { alone = false; break; } /* 원끼리는 지름만큼, 세워진 사물은 그 키만큼 (화면에서 겹칠 수 있는 거리) */ }
      if (!alone) { if (m.layers.mask !== 1) m.layers.set(0); continue; }
      b.bD = m.position.x * chBFwd.x + m.position.y * chBFwd.y + m.position.z * chBFwd.z;
      chBList[n++] = b;
    }
    chBList.length = n;
    chBList.sort((a, c) => c.bD - a.bD);       // 먼 것부터 (전과 같은 겹침 순서)
    for (let i = 0; i < n; i++) { const m = chBList[i].mesh; chBM.compose(m.position, m.quaternion, m.scale); chBatch.setMatrixAt(i, chBM); chBatch.setColorAt(i, m.material.color); if (m.layers.mask !== 2) m.layers.set(1); }
    chBatch.count = n; chBatch.instanceMatrix.needsUpdate = true; if (chBatch.instanceColor) chBatch.instanceColor.needsUpdate = true;
  }
  window.__ri = renderer.info;
"""
C156_R = [
 ("  const chPf = { on: false, n: 0, w: 0, r: 0, t: 0, base: '' };\n", JS + "  const chPf = { on: false, n: 0, w: 0, r: 0, t: 0, base: '' };\n"),
 ("renderer.render = (sc, cam) => { if (!chPf.on) { rr(sc, cam); return; }", "renderer.render = (sc, cam) => { chBatchBodies(); if (!chPf.on) { rr(sc, cam); return; }"),
]
