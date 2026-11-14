# c56: 검은 테두리는 변이한 나만 · 다시 채우기 틱
C56_FN = r"""  function chMeRing(on) {                      // c56: 내가 변이했을 때만 검은 테두리 — 변이한 동료들 사이에서 나를 알아보게
    if (me.ring) { me.mesh.remove(me.ring); me.ring = null; }
    if (!on) return;
    const ring = new THREE.Mesh(new THREE.RingGeometry(RADIUS * 0.84, RADIUS, 48), new THREE.MeshBasicMaterial({ color: 0x0b0b0d, transparent: true, depthTest: false, depthWrite: false }));
    ring.position.z = 0.003; me.mesh.add(ring); me.ring = ring;
  }
"""
C56_R = [
  ("    me.mut = type; me.mutT = sec;", "    if (CHAPTER) chMeRing(true);   // c56\n    me.mut = type; me.mutT = sec;"),
  ("    if (z === me) { me.mut = null; me.mesh.material.color.setHex(COLOR.me);", "    if (z === me) { if (CHAPTER) chMeRing(false); me.mut = null; me.mesh.material.color.setHex(COLOR.me);"),
  ("    if (CHAPTER) chDispatchTick(dt);   // c46", "    if (CHAPTER) chDispatchTick(dt);   // c46\n    if (CHAPTER) chRespawnTick(dt);   // c56: 사람·무리 다시 채우기 · 집 점령 표시"),
  ("zombify: makeZombie, slotOf,", "zombify: makeZombie, slotOf, pop: () => chPop,"),
  ("  function showDud() {", C56_FN + "  function showDud() {"),
]
