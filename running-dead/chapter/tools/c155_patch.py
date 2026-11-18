# c155: 성능 — 덜 자주 계산하기 (눈에 거의 안 띄는 선에서)
#   ① 동료 시야: 벽까지 거리(광선)는 두 프레임에 한 번만 다시 잰다 — 그 사이 프레임은 지난 값으로 지금 자리에 그린다 (내 시야는 매 프레임. 동료 절반씩 번갈아)
#   ② 동료 대형 자리: 두 걸음에 한 번만 다시 계산 — 그 사이엔 영역 중심에서의 지난 어긋남 그대로 (동료 절반씩 번갈아)
#   ③ 동료가 많을 때(눈 60 넘게) 동료 시야 광선 80 → 60
C155_R = [
 ("      const RAYS = z === me ? VIEW_RAYS : ALLY_RAYS;", "      const RAYS = z === me ? VIEW_RAYS : CHAPTER && eyes.length > 60 ? 60 : ALLY_RAYS;   /* c155 ③ */"),
 ("      rayAngles.length = 0;\n      for (let k = 0; k < RAYS; k++) rayAngles.push(k / RAYS * Math.PI * 2);\n      for (const B of nb) for (const [ex, ez] of B.sightC) {",
  "      const reuse = CHAPTER && z !== me && z.vF === chDrawN - 1 && z.vR === R && (((chDrawN + (z.vK === undefined ? (z.vK = Math.random() < 0.5 ? 0 : 1) : z.vK)) & 1) === 1);   // c155 ①\n"
  "      rayAngles.length = 0;\n"
  "      if (reuse) for (let k = 0; k < z.vN; k++) rayAngles.push(z.vA[k]);\n"
  "      else for (let k = 0; k < RAYS; k++) rayAngles.push(k / RAYS * Math.PI * 2);\n"
  "      if (!reuse) for (const B of nb) for (const [ex, ez] of B.sightC) {"),
 ("      rayAngles.sort((a, b) => a - b);\n      let px = 0, pz = 0, fx = 0, fz = 0;",
  "      if (!reuse) rayAngles.sort((a, b) => a - b);\n"
  "      const keepV = CHAPTER && z !== me && !reuse;\n"
  "      if (keepV) { const L = rayAngles.length; if (!z.vA || z.vA.length < L) { z.vA = new Float64Array(L + 32); z.vD = new Float64Array(L + 32); } for (let k = 0; k < L; k++) z.vA[k] = rayAngles[k]; z.vN = L; z.vF = chDrawN; z.vR = R; }\n"
  "      let px = 0, pz = 0, fx = 0, fz = 0;"),
 ("hit = wallRay(x, y, dx, dz, R, near);", "hit = reuse ? z.vD[i] : keepV ? (z.vD[i] = wallRay(x, y, dx, dz, R, near)) : wallRay(x, y, dx, dz, R, near);"),
 ("  function slotOf(z) {\n    const r = z.slotK * NEAR * armyK;", "  function slotOf(z) {\n    if (CHAPTER && z.slSp === me.space && (z.slF === objFrame || (z.slF === objFrame - 1 && (((objFrame + (z.slK === undefined ? (z.slK = Math.random() < 0.5 ? 0 : 1) : z.slK)) & 1) === 1)))) return slotV.set(areaX() + z.slDX, areaZ() + z.slDY);   // c155 ②\n    const r = z.slotK * NEAR * armyK;"),
 ("      if (d > 1e-6) { x = O.x + dx / d * R; y = O.z + dz / d * R; } else x = O.x + R;\n    }\n    return slotV.set(x, y);\n  }", "      if (d > 1e-6) { x = O.x + dx / d * R; y = O.z + dz / d * R; } else x = O.x + R;\n    }\n    if (CHAPTER) { z.slF = objFrame; z.slSp = me.space; z.slDX = x - areaX(); z.slDY = y - areaZ(); }   // c155 ②\n    return slotV.set(x, y);\n  }"),
]
