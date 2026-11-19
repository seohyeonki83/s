# c207: 벽 체력바 없음 · 데미지 30% 이상이면 벽 그림이 살짝 뒤틀리고 60% 이상이면 조금 더 (그림만 — 부서지기 전까진 못 지나가고 시야도 막힌다)
C207_R = [
 (" if (!v.hpBar) { addHpBar(v, hpFoeMat); v.hpDisp = v.hp; } }   // c200", " }   // c200 · c207: 벽은 체력바 없음"),
 ("    if (v.kind === 'obj') { if (!v.dead) { v.hp = Math.max(0, v.hp - dmg);",
  "    if (v.kind === 'obj') { if (!v.dead) { v.hp = Math.max(0, v.hp - dmg); if (v.type === 'wall') chWallWarp(v);"),
 ("  function chWallRedraw(o) {",
  """  function chWallWarp(o, force) {              // c207: 데미지 30% 이상 = 살짝 뒤틀림 · 60% 이상 = 조금 더 (그림만)
    const st = o.hp <= o.maxHp * 0.4 ? 2 : o.hp <= o.maxHp * 0.7 ? 1 : 0;
    if (st === (o.warp || 0) && !force) return;
    o.warp = st; const m = o.seg.m; if (!m) return;
    if (o.wS === undefined) { o.wS = Math.random() < 0.5 ? -1 : 1; o.wP = Math.random() < 0.5 ? -1 : 1; }
    const s = o.seg, hz = s[1] === s[3], px = (s[0] + s[2]) / 2, pz = (s[1] + s[3]) / 2, off = [0, 0.03, 0.07][st] * o.wP;
    m.rotation.y = [0, 0.045, 0.11][st] * o.wS;
    m.position.x = px + (hz ? 0 : off); m.position.z = pz + (hz ? off : 0);
  }
  function chWallRedraw(o) {"""),
 # 깎인 토막을 다시 그릴 때 뒤틀림 유지
 ("    o.foot.set((s[0] + s[2]) / 2, 0, (s[1] + s[3]) / 2);\n  }",
  "    o.foot.set((s[0] + s[2]) / 2, 0, (s[1] + s[3]) / 2);\n    if (o.warp) chWallWarp(o, true);\n  }"),
 # 새 판: 반듯하게
 ("o.hpDisp = o.hp; o.hotF = undefined; if (o.hpBar) o.hpBar.visible = false; }", "o.hpDisp = o.hp; o.hotF = undefined; if (o.hpBar) o.hpBar.visible = false; chWallWarp(o, true); }   /* c207 */"),
]
