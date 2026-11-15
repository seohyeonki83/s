# c82: 건물 안 사물 25% 더 줄임 · 길거리 하양 20% 늘림 · 노랑 전체 10% 늘림 · 주차된 차 20% 더 줄임 · 주차된 차의 10%는 오토바이
C82_R = [
  # ── 사물: 놓기로 한 것의 5분의 1을 빼던 것 (c73) → 0.8 × 0.75 = 0.6만 남긴다 ──
  ("want = Math.round(P.length / 5)", "want = Math.round(P.length * (1 - 0.8 * 0.75))   /* c82: 25% 더 줄임 */"),
  # ── 사람 ──
  ("    const whiteOut = Math.round((CH_WHITE_OUT + houseOut) * 1.15 * CH_ONE_K);",
   "    const whiteOut = Math.round((CH_WHITE_OUT + houseOut) * 1.15 * CH_ONE_K * 1.2);   /* c82: 길거리 하양 20% 더 */"),
  ("for (let k = 0; k < Math.round(CH_YELLOW_OUT * CH_ONE_K); k++)",
   "for (let k = 0, nY = Math.round((CH_YELLOW_OUT * CH_ONE_K + Math.round(CH_GANG / 5)) * CH_YELLOW_UP) - Math.round(CH_GANG / 5); k < nY; k++)   /* c82: 길거리 노랑(혼자 다니는 노랑 + 무리에 섞인 노랑) 10% 더 — 늘어난 몫은 혼자 다니는 노랑으로 */"),
  ("if (type === 'vig') k = chRedN(k);",
   "if (type === 'guard') { const q = k * CH_YELLOW_UP; k = Math.floor(q) + (Math.random() < q - Math.floor(q) ? 1 : 0); }   /* c82: 건물 안 노랑 10% 더 (열 번에 한 번꼴로 한 명 더) */ if (type === 'vig') k = chRedN(k);"),
  ("  const CH_WHITE_GANG = 0.5;", "  const CH_YELLOW_UP = 1.1;                      // c82: 노랑 10% 더 (안·밖 모두)\n  const CH_WHITE_GANG = 0.5;"),
  # ── 주차된 차: 5분의 1을 빼던 것 (c73) → 0.8 × 0.8 = 0.64만 남긴다. 남은 민간 차의 10%는 오토바이로 바꾼다 ──
  ("      for (let i = 0, n = Math.min(pool.length, Math.round(all.length / 5)); i < n; i++) { const c = pool[i]; if (c.tag) chDeco.n[c.tag]--; chTrGone(c); }",
   "      const nCut = Math.min(pool.length, Math.round(all.length * (1 - 0.8 * 0.8)));   // c82: 20% 더 줄임\n"
   "      for (let i = 0; i < nCut; i++) { const c = pool[i]; if (c.tag) chDeco.n[c.tag]--; chTrGone(c); }\n"
   "      const rest = pool.slice(nCut);           // c82: 남은 민간 차 열 대에 한 대는 오토바이 (같은 자리 · 무게는 차와 같고 크기만 작다)\n"
   "      for (let i = 0, n = Math.round((all.length - nCut) * 0.1); i < n && i < rest.length; i++) { const c = rest[i], x = c.x, z = c.z, h = c.h, tag = c.tag; chTrGone(c); chDecoCar('moto', x, z, h).tag = tag; }"),
  ("    ambul:   { name: '구급차', kl: 1.3, kw: 1.3, hp: 1.3, mass: 1.4, col: [0xf6f6f4] },\n",
   "    ambul:   { name: '구급차', kl: 1.3, kw: 1.3, hp: 1.3, mass: 1.4, col: [0xf6f6f4] },\n"
   "    moto:    { name: '오토바이', kl: 0.68, kw: 0.6, hp: 1.0, mass: 1.0, col: [0xd42a1e, 0x1e6fd4, 0x2b2c31, 0xe0b23c, 0x2f8a4a, 0xf0f0ee] },   // c82: 서 있기만 한다 — 무게·체력은 세단과 같고 크기만 작다\n"),
  ("    rr(2, 4, 252, 120, type === 'truck' || type === 'fire' || type === 'cash' || type === 'parcel' ? 10 : 24, '#0c0c0e');",
   "    if (type !== 'moto') rr(2, 4, 252, 120, type === 'truck' || type === 'fire' || type === 'cash' || type === 'parcel' ? 10 : 24, '#0c0c0e');"),
  ("    if (type === 'truck') {\n",
   "    if (type === 'moto') {                    // c82: 오토바이 — 바퀴 둘 · 몸통 · 연료통 · 안장 · 핸들 (바탕은 비운다)\n"
   "      rr(4, 32, 82, 64, 22, '#101013'); rr(174, 36, 78, 56, 22, '#101013');\n"
   "      rr(50, 22, 152, 84, 30, mix(col, 0)); rr(118, 32, 64, 64, 22, mix(col, 0.24)); rr(56, 34, 60, 60, 20, '#1b1b1f');\n"
   "      g.fillStyle = '#2c2c33'; g.fillRect(180, 4, 14, 120); rr(171, 0, 32, 20, 8, '#4a4a54'); rr(171, 108, 32, 20, 8, '#4a4a54');\n"
   "      rr(240, 50, 14, 28, 5, '#fff4b8'); rr(2, 54, 8, 20, 3, '#d02222');\n"
   "    } else if (type === 'truck') {\n"),
]
