# c212: ① 랜드마크 방의 바깥 쪽문 자리(마트·군부대)를 벽 토막이 덮던 버그 (c203) — 면을 다시 나눌 때 그 자리도 비운다
#        ② 벽이 맞을 때마다 빨갛게 번쩍 (나·동료 모두)
C212_R = [
 ("const gapsOf = (sd) => [...B.doors, ...B.locks.filter((L) => !L.merged)]", "const gapsOf = (sd) => [...B.doors, ...B.locks.filter((L) => !L.merged), ...(B.rooms || []).flatMap((Q) => Q.locks.filter((L) => L.ext))]   /* c212: 방 바깥 쪽문 자리도 */"),
 ("if (v.type === 'wall') chWallWarp(v);", "if (v.type === 'wall') { chWallWarp(v); chWallFlash(v); }"),
 ("  function chWallWarp(o, force) {",
  """  const chWallRedMat = flatMat(0xd42a1e), chWallFl = new Set();
  function chWallFlash(o) { const m = o.seg.m; if (!m || o.dead) return; m.material = chWallRedMat; o.flT = clock + 0.12; chWallFl.add(o); }   // c212: 맞으면 빨갛게 번쩍
  function chWallFlashTick() { for (const o of chWallFl) if (o.dead || clock >= o.flT || clock < o.flT - 1) { if (o.seg.m) o.seg.m.material = wallMat; chWallFl.delete(o); } }
  function chWallWarp(o, force) {"""),
 ("  function drawObjBars(dt) {", "  function drawObjBars(dt) {\n    if (CHAPTER) chWallFlashTick();   // c212"),
]
