# c289: 튜토리얼 1 — 실험실 (작은 박스 안에서 시작 → 박스 벽을 부수고 → 사물 많은 실험실 → 오른쪽 위 문 → 긴 복도). 클리어 없음
C289_R = [
  ("[['b', '큰 맵',", "[['t', '튜토리얼 1', '실험실 · 박스 안에서 시작'], ['b', '큰 맵',"),
  ("const CH_SMALL = CH_PICK === 's', CH_BT = CH_PICK === 'k';", "const CH_SMALL = CH_PICK === 's', CH_BT = CH_PICK === 'k', CH_TUT = CH_PICK === 't';   // c289: 튜토리얼 1"),
  ("CH_SMALL ? '작은 맵' : CH_BT ? '보스 테스트' : '큰 맵'", "CH_TUT ? '튜토리얼 1' : CH_SMALL ? '작은 맵' : CH_BT ? '보스 테스트' : '큰 맵'"),
  ("  const BUILDINGS = CHAPTER ? CH_MAP.b :", """  const CH_TUTT = new Set(['lab', 'labc']);   // c289: 튜토리얼 건물 (실험실 · 복도) — 금고·사람·자동 사물·랜덤 문 없음
  const TUT_B = CH_TUT ? (() => {             // c289: 큰 맵 남쪽 바깥 — 마을에서 아무도 오지 않는 자리
    const cz = CH_MAP.mm.z1 + 58, W = 18, D = 13, x0 = -W / 2, z0 = cz - D / 2, z1 = cz + D / 2, BS = MELEE * 2, doorX = W / 2 - 2.6, CL = 28, CW = 4.4, n = CH_MAP.b.length;
    return [
      { x: 0, z: cz, w: W, d: D, doors: [], locks: ['n'], at: { n: doorX }, kinds: {}, local: 900, block: -1, t: 'lab', zone: 0 },                 // 실험실 — 가로로 살짝 긴 방 · 문은 위쪽 벽 오른쪽 끝
      { x: x0 + BS / 2, z: z1 - BS / 2, w: BS, d: BS, doors: [], locks: [], kinds: {}, local: 901, block: -1, t: 'box', zone: 0, parent: n, room: { doors: [] } },   // 박스 — 실험실 왼쪽 아래 구석 · 한 변 = 내 공격 거리의 2배
      { x: doorX, z: z0 - CL / 2, w: CW, d: CL, doors: [], open: ['s'], locks: [], kinds: {}, local: 902, block: -1, t: 'labc', zone: 0 },        // 긴 복도 — 실험실 문에서 위로
    ];
  })() : [];
  const BUILDINGS = CHAPTER ? (CH_TUT ? CH_MAP.b.concat(TUT_B) : CH_MAP.b) :"""),
  ("return { side, cx: nx > 0 ? B.x1 : nx < 0 ? B.x0 : s.x, cz: nz > 0 ? B.z1 : nz < 0 ? B.z0 : s.z,", "return { side, cx: nx > 0 ? B.x1 : nx < 0 ? B.x0 : (s.at && s.at[side] !== undefined ? s.at[side] : s.x), cz: nz > 0 ? B.z1 : nz < 0 ? B.z0 : (s.at && s.at[side] !== undefined ? s.at[side] : s.z),   /* c289: at = 문 자리 */", 2),
  ("    store: { name: '창고', col: '#7d6e5a', roof: 0x34302a },\n  };", "    store: { name: '창고', col: '#7d6e5a', roof: 0x34302a },\n    lab: { name: '실험실', col: '#4f9d93', roof: 0x1d2b2a }, labc: { name: '복도', col: '#4f9d93', roof: 0x1d2b2a },   // c289\n  };"),
  ("      if (B.type === 'house' || B.parent) return;\n      B.sign =", "      if (B.type === 'house' || B.parent || CH_TUTT.has(B.type)) return;   /* c289 */\n      B.sign ="),
  ("if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5;", "if (CHAPTER && CH_LM.has(B.type)) o.hp = o.maxHp = o.maxHp * 1.5; if (CHAPTER && B.type === 'lab') o.hp = o.maxHp = MY_DAMAGE * 3.5;   /* c289: 실험실 문 = 집 문 */"),
  ("if (B.type === 'hill' || B.parent || CH_LM.has(B.type)) continue;", "if (B.type === 'hill' || B.parent || CH_LM.has(B.type) || CH_TUTT.has(B.type)) continue;"),
  ("      if (B.type === 'hill' || B.parent || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;", "      if (B.type === 'hill' || B.parent || CH_TUTT.has(B.type) || (B.type === 'house' && Math.random() >= CH_HOUSE_SAFE)) continue;   /* c289 */"),
  ("    if (W < 1.6 || H < 1.6 || type === 'jail') return;", "    if (W < 1.6 || H < 1.6 || type === 'jail' || type === 'box' || CH_TUTT.has(type)) return;   /* c289: 튜토리얼은 정해 둔 사물만 */"),
  ("      const P = R.parent; if (R.type === 'jail' || !CH_WALL_T[P.type]) continue;", "      const P = R.parent, kW = R.type === 'box' ? CH_WALL_T.house : CH_WALL_T[P.type]; if (R.type === 'jail' || !kW) continue;   /* c289: 박스 벽 = 집 벽 체력 */"),
  ("dead: false, off: false, k: CH_WALL_T[P.type] }; q.wo = o; R.wos.push(o);", "dead: false, off: false, k: kW }; q.wo = o; R.wos.push(o);"),
  ("      chFurnPlan = null;\n    }", """      chFurnPlan = null;
    }
    if (CH_TUT) chTutFurn();   // c289"""),
  ("  function chFurnOne(S) {", """  function chTutFurn() {                     // c289: 실험실 사물 — 박스 둘레와 문 앞만 비우고 빽빽하게
    const L = buildings.find((B) => B.type === 'lab'), x0 = L.x0, z0 = L.z0, x1 = L.x1, z1 = L.z1;
    for (const [x, z] of [[-2.9, 3.2], [0.3, 3.2], [-2.9, 7.0], [0.3, 7.0]]) chAddSlab('table', x0 + 9 + x, z0 + z, 0, L);   // 실험대 두 줄
    const P = [['pc', 3.2, 0.95], ['pc', 6.0, 0.95], ['pc', 12.0, 0.95], ['chair', 3.2, 2.0], ['chair', 6.0, 2.0], ['chair', 12.0, 2.0],   // 위쪽 벽: 컴퓨터 책상 (문 앞은 비움)
      ['cabinet', 0.6, 0.7], ['plant', 0.5, 2.3], ['cabinet', 9.2, 0.6],
      ['chair', 5.4, 2.6], ['chair', 7.8, 2.6], ['chair', 9.9, 2.6], ['chair', 5.4, 4.6], ['chair', 7.8, 4.6], ['chair', 9.9, 4.6],   // 실험대 둘레 의자
      ['chair', 5.4, 6.4], ['chair', 7.8, 6.4], ['chair', 9.9, 6.4], ['chair', 5.4, 8.4], ['chair', 9.9, 8.4],
      ['locker', 17.3, 4.2], ['locker', 17.3, 5.2], ['locker', 17.3, 6.2], ['cabinet', 17.3, 7.6], ['drum', 17.2, 9.1],   // 오른쪽 벽: 사물함·약품장
      ['crate', 16.0, 12.0], ['crate', 14.9, 12.1], ['drum', 16.9, 10.6], ['box', 13.7, 11.4], ['box', 15.6, 10.7], ['box', 12.6, 12.2],   // 오른쪽 아래: 상자·드럼
      ['cabinet', 9.0, 12.3], ['cabinet', 10.1, 12.3], ['plant', 7.4, 12.3], ['box', 11.2, 10.6], ['chair', 8.2, 10.6],   // 아래쪽 벽
      ['box', 4.9, 9.2], ['crate', 4.6, 7.6], ['drum', 0.7, 5.0], ['box', 0.6, 6.3], ['plant', 1.7, 4.3], ['chair', 2.6, 6.0],   // 왼쪽 (박스 위)
      ['box', 14.2, 3.8], ['crate', 12.9, 5.4], ['chair', 14.0, 7.9], ['box', 12.6, 8.8]];
    for (const [t, x, z] of P) { const p = chAddProp(t, x0 + x, z0 + z); p.space = L; }
  }
  function chFurnOne(S) {"""),
  ("me.foot.set(st[0], 0, st[1]); } me.space = null;", "me.foot.set(st[0], 0, st[1]); } me.space = null; if (CH_TUT) { const X = buildings.find((B) => B.type === 'box'); me.foot.set((X.x0 + X.x1) / 2, 0, (X.z0 + X.z1) / 2); me.px = me.foot.x; me.pz = me.foot.z; me.space = X; }   /* c289: 박스 한가운데서 시작 */"),
]
C289_R.append(("      const r = b.r || BODY;\n      if (b.foot.x < MM.x0 + r) {", "      const r = b.r || BODY;\n      if (!(CH_TUT && b.foot.z > MM.z1 + 20)) {   // c289: 튜토리얼 구역(지도 남쪽 바깥)은 지도 경계에 안 묶인다\n      if (b.foot.x < MM.x0 + r) {"))
C289_R.append(("else if (b.foot.z > MM.z1 - r) { b.foot.z = MM.z1 - r; if (b.vel.y > 0) b.vel.y = 0; }\n", "else if (b.foot.z > MM.z1 - r) { b.foot.z = MM.z1 - r; if (b.vel.y > 0) b.vel.y = 0; }\n      }\n"))
