# c291: 탐험 안개 — 칸 한가운데 대신 '칸에서 나에게 가장 가까운 점'으로 보고 벽 뒤 0.25칸까지 연다 (벽 선이 처음부터 깔끔하게) · 안개는 몸 그림 아래로
C291_R = [
  ("          const cx = F.x0 + (i + 0.5) * F.cs, dx = cx - ex, dz = cz - ez, d = Math.hypot(dx, dz); if (d > R) continue;\n          const pl = d > 0.4 ? 0.4 / d : 0; if (blocked(ex, ez, cx - dx * pl, cz - dz * pl)) continue;   // 벽 바로 뒤 0.4칸까지는 밝힌다 (벽 선이 다 보이게)",
   "          const cx = F.x0 + (i + 0.5) * F.cs, hc = F.cs / 2, nx = Math.max(cx - hc, Math.min(cx + hc, ex)), nz = Math.max(cz - hc, Math.min(cz + hc, ez));   // c291: 칸에서 나에게 가장 가까운 점\n          const dx = nx - ex, dz = nz - ez, d = Math.hypot(dx, dz); if (d > R) continue;\n          const pl = d > 0.25 ? 0.25 / d : 0; if (blocked(ex, ez, nx - dx * pl, nz - dz * pl)) continue;   // 벽 바로 뒤 0.25칸까지는 밝힌다 (벽 그림 두께만큼)"),
  ("m.renderOrder = 50; scene.add(m);   // 거의 맨 위 — 안 본 곳은 사람·사물까지 다 가린다", "m.renderOrder = -0.4; scene.add(m);   // c291: 벽 그림 위 · 몸 그림 아래 (안 본 곳의 사람·사물은 원래 시야 밖이라 숨겨진다)"),
]
C291_R.append(("  function chFogTick(eyes) {", "  window.__fog = () => chFog;   // 테스트용\n  function chFogTick(eyes) {"))
