# c404: 미니맵 — 정사각형 · 나를 가운데 두고 따라다닌다 · 지금보다 1.25배 확대 (비추는 폭 80%) · 누르면 지도 전체 (c18 그대로)
src = open('c403.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:80])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  const MM_CW = Math.round((MM.x1 - MM.x0) * MM_S), MM_CH = Math.round((MM.z1 - MM.z0) * MM_S);",
    "  const MM_CW = Math.round((MM.x1 - MM.x0) * MM_S), MM_CH = Math.round((MM.z1 - MM.z0) * MM_S);\n"
    "  // c404: 챕터 미니맵 — 작게 볼 때는 정사각형(88px)에 내 둘레만, 나는 늘 한가운데 (미니맵이 나를 따라다닌다). 전에 지도 전체를 비추던 배율보다 1.25배 확대 = 비추는 폭이 80%.\n"
    "  //   여러 그룹을 이어 붙인 큰 월드는 그룹 하나 크기(mmRef)를 기준 배율로 쓴다. 누르면 지도 전체 (c18)\n"
    "  const MM_SIDE = 88, MM_ZOOM = 1.25, MM_REF_S = CHAPTER && CH_MAP.mmRef ? Math.min(88 / CH_MAP.mmRef.w, 107 / CH_MAP.mmRef.h) : MM_S, MM_VIEW = MM_SIDE / (MM_REF_S * MM_ZOOM);\n"
    "  const MM_SW = CHAPTER ? MM_SIDE : MM_CW, MM_SH = CHAPTER ? MM_SIDE : MM_CH;   // 작게 볼 때 크기\n"
    "  let mmWin = null;                           // 작게 볼 때 비추는 창 {x0, z0, V} (크게 볼 때는 null)")
rep("  mmEl.style.width = MM_CW + 'px'; mmEl.style.height = MM_CH + 'px'; if (CH_TUT) mmEl.style.display = 'none';",
    "  mmEl.style.width = MM_SW + 'px'; mmEl.style.height = MM_SH + 'px'; if (CH_TUT) mmEl.style.display = 'none';")
rep("    el.style.top = `calc(${6 + MM_CH + 6}px + env(safe-area-inset-top, 0px))`;", "    el.style.top = `calc(${6 + MM_SH + 6}px + env(safe-area-inset-top, 0px))`;")
rep("mmEl.width = Math.round(MM_CW * mmDpr); mmEl.height = Math.round(MM_CH * mmDpr);", "mmEl.width = Math.round(MM_SW * mmDpr); mmEl.height = Math.round(MM_SH * mmDpr);", 2)
rep("      S.width = MM_CW + 'px'; S.height = MM_CH + 'px'; S.top = ''; S.left = '';", "      S.width = MM_SW + 'px'; S.height = MM_SH + 'px'; S.top = ''; S.left = '';")
rep("  let chDim = null, chLit = null, chMask = null;", "  let chDim = null, chLit = null, chMask = null, chLayW = null, chLayF = null;   /* c404: 바탕 그림 — 창(작게)용 · 전체(크게)용 따로 */")
a0 = src.index("    const u = W / MM_CW;                       // c18:")
a1 = src.index("    const sz2 = 8 * u, szB = 13.2 * u;")
old = src[a0:a1]
new = (
"    const u = sx / MM_REF_S;                   // c18 · c404: 그림 한 칸 크기 — 지도가 확대된 만큼 아이콘·내 점도 같은 비율로 커진다 (기준 = 전에 지도 전체를 비추던 배율)\n"
"    const win = mmWin, mw = MM.x1 - MM.x0, mh = MM.z1 - MM.z0;\n"
"    const ls = win ? Math.min(sx, Math.sqrt(2.2e6 / (mw * mh))) : sx, lz = win ? ls : sz, lw = win ? Math.max(1, Math.round(mw * ls)) : W, lh = win ? Math.max(1, Math.round(mh * lz)) : H;   // 창으로 볼 때는 지도 전체를 그 배율로 한 번 그려 두고 내 둘레만 잘라 쓴다\n"
"    let L = win ? chLayW : chLayF;\n"
"    if (!L || L.w !== lw || L.h !== lh) {       // c18: 크기가 바뀌면 바탕 그림을 그 크기로 새로 만든다\n"
"      const LX = win ? (x) => (x - MM.x0) * ls : X, LZ = win ? (z) => (z - MM.z0) * lz : Z;\n"
"      L = { w: lw, h: lh, dim: chLayer(lw, lh, LX, LZ, ls, lz, '#303036', '#27272c', '#141417', '#1b1b20', '#1a2a1a', '#14283a', '#3a342c'),     // 안개 속\n"
"        lit: chLayer(lw, lh, LX, LZ, ls, lz, '#9c9ca4', '#85858d', '#3a3a42', '#4c4c56', '#4f7447', '#3d82b6', '#a8957b') };     // 지금 보이는 곳\n"
"      if (win) chLayW = L; else chLayF = L;\n"
"    }\n"
"    chDim = L.dim; chLit = L.lit;\n"
"    if (!chMask || chMask.width !== W || chMask.height !== H) { chMask = document.createElement('canvas'); chMask.width = W; chMask.height = H; }\n"
"    const put = (ctx, img, kx, kz) => {        // 지도 전체 그림(1칸 = kx·kz px)에서 지금 비추는 곳만 옮겨 그린다 — 지도 밖은 비운다\n"
"      if (!win) { ctx.drawImage(img, 0, 0, W, H); return; }\n"
"      const ax = Math.max(win.x0, MM.x0), az = Math.max(win.z0, MM.z0), bx = Math.min(win.x0 + win.V, MM.x1), bz = Math.min(win.z0 + win.V, MM.z1);\n"
"      if (bx <= ax || bz <= az) return;\n"
"      ctx.drawImage(img, (ax - MM.x0) * kx, (az - MM.z0) * kz, (bx - ax) * kx, (bz - az) * kz, X(ax), Z(az), (bx - ax) * sx, (bz - az) * sz);\n"
"    };\n"
"    const g = mmCtx, m = chMask.getContext('2d');\n"
"    g.fillStyle = '#000'; g.fillRect(0, 0, W, H);                         // 못 가 본 곳 = 새까맣게\n"
"    m.globalCompositeOperation = 'source-over'; m.clearRect(0, 0, W, H); put(m, chDim, lw / mw, lh / mh);\n"
"    m.globalCompositeOperation = 'destination-in'; m.imageSmoothingEnabled = true; if (win) put(m, mmFog, 1 / MM_CELL, 1 / MM_CELL); else m.drawImage(mmFog, 0, 0, W, H);   // 가 본 칸만 남긴다\n"
"    g.drawImage(chMask, 0, 0);                                            // 가 본 곳 = 안개\n"
"    g.save(); g.beginPath();\n"
"    for (const z of eyes) { if (!isZombie(z)) continue; const cx = X(z.foot.x), cz = Z(z.foot.z), r = z.sense * sx; if (cx + r < 0 || cx - r > W || cz + r < 0 || cz - r > H) continue; g.moveTo(cx + r, cz); g.arc(cx, cz, r, 0, Math.PI * 2); }\n"
"    g.clip(); put(g, chLit, lw / mw, lh / mh); g.restore();               // 지금 보이는 곳 = 밝게\n"
)
R.append((old, new))
rep("      g.drawImage(CH_ICON[B.done ? 'x' : B.type], Math.max(0, Math.min(W - szB, X((B.x0 + B.x1) / 2) - szB / 2)), Math.max(0, Math.min(H - szB, Z((B.z0 + B.z1) / 2) - szB / 2)), szB, szB);",
    "      if (win) { const ix = X((B.x0 + B.x1) / 2) - szB / 2, iz = Z((B.z0 + B.z1) / 2) - szB / 2; if (ix < W && iz < H && ix > -szB && iz > -szB) g.drawImage(CH_ICON[B.done ? 'x' : B.type], ix, iz, szB, szB); }   /* c404: 창으로 볼 때는 제자리에 (창 밖이면 안 그린다) */\n"
    "      else g.drawImage(CH_ICON[B.done ? 'x' : B.type], Math.max(0, Math.min(W - szB, X((B.x0 + B.x1) / 2) - szB / 2)), Math.max(0, Math.min(H - szB, Z((B.z0 + B.z1) / 2) - szB / 2)), szB, szB);")
rep("    const W = mmEl.width, H = mmEl.height, sx = W / (MM.x1 - MM.x0), sz = H / (MM.z1 - MM.z0);\n    const X = (x) => (x - MM.x0) * sx, Z = (z) => (z - MM.z0) * sz;\n    if (CHAPTER) { chMinimap(eyes, W, H, X, Z, sx, sz); return; }",
    "    const W = mmEl.width, H = mmEl.height;\n"
    "    if (CHAPTER && !mmBig) {                  // c404: 작게 볼 때 = 내 둘레 MM_VIEW칸 네모 (나는 한가운데)\n"
    "      const V = MM_VIEW, wx = me.foot.x - V / 2, wz = me.foot.z - V / 2, k = W / V; mmWin = { x0: wx, z0: wz, V };\n"
    "      chMinimap(eyes, W, H, (x) => (x - wx) * k, (z) => (z - wz) * k, k, k); return;\n"
    "    }\n"
    "    mmWin = null;\n"
    "    const sx = W / (MM.x1 - MM.x0), sz = H / (MM.z1 - MM.z0);\n    const X = (x) => (x - MM.x0) * sx, Z = (z) => (z - MM.z0) * sz;\n    if (CHAPTER) { chMinimap(eyes, W, H, X, Z, sx, sz); return; }")
open('c404_patch.py', 'w').write("# c404: 미니맵 — 정사각형 · 나를 따라다닌다 · 1.25배 확대 (비추는 폭 80%) · 누르면 지도 전체\nC404_R = " + repr(R) + "\n")
print(len(R), 'entries')
