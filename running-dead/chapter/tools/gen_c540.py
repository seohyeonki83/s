import pathlib
s = pathlib.Path('c539.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1. 목표 창 — 튜토리얼 '생체 실험실을 탈출하라' · 맵마다 이야기 한 단락
rep("(CH_TUT ? '탈출하기' :", "(CH_TUT ? '생체 실험실을 탈출하라' :")
rep("<div class=\"k\">목표</div><div class=\"v\">탈출하기</div>", "<div class=\"k\">목표</div><div class=\"v\">생체 실험실을 탈출하라</div>")
rep("+ '</div>' + (CH_RUN ? '<div class=\"g4\">", "+ '</div>' + (CH_TUT || CH_RUN ? '<div class=\"g6\">' + chStory() + '</div>' : '') + (CH_RUN ? '<div class=\"g4\">")
rep("#goal .g5{margin-top:8px;font:900 11px system-ui;color:#ffd34d;letter-spacing:1px}", "#goal .g5{margin-top:8px;font:900 11px system-ui;color:#ffd34d;letter-spacing:1px}#goal .g6{margin:12px auto 0;width:min(320px,84vw);font:600 14px/1.6 system-ui,sans-serif;color:#e9e2f5;text-shadow:0 2px 6px rgba(0,0,0,0.95);word-break:keep-all}")
rep("  function showGoal() {", """  function chStory() {                          // c540: 맵마다 이야기 한 단락
    if (CH_TUT) return '차가운 수조 속에서 눈을 떴다. 몸이 예전 같지 않다. 나를 이렇게 만든 건 저 흰 가운의 인간들이다. 문을 부수고, 길을 막는 자는 모두 물어뜯어라. 이곳을 빠져나가는 것, 그게 복수의 시작이다.';
    return { 1: '실험실을 빠져나온 감염은 조용한 도시로 번지기 시작했다. 도시를 지키려 특공대가 몰려온다. 그들마저 우리 무리로 만들어라.',
      2: '공장과 창고 너머로 감염이 퍼지자 군은 중장비를 앞세웠다. 벽을 밀고 들어오는 강철을 무너뜨리고 이 지구를 삼켜라.',
      3: '모든 병력은 북쪽 군사기지에서 나온다. 검문소를 넘어 기지 한가운데까지 밀고 들어가라. 그곳이 무너지면 군은 머리를 잃는다.',
      4: '마지막 방어선, 국경 요새. 장갑차가 길을 막고 서 있다. 이곳만 넘으면 더는 우리를 막을 것이 없다.' }[CH_STG] || '';
  }
  function showGoal() {""")
# 2. 튜토리얼 첫 하양 — 첫 방 문(보물상자)에서 가장 먼 복도 끝으로 (상자 깨기 전엔 안 보이게)
rep("man(C1, '', (C1.x0 + C1.x1) / 2, (C1.z0 + C1.z1) / 2);", "{ const D = L.locks[0], pts = [[C1.x0 + 0.9, C1.z0 + 0.9], [C1.x1 - 0.9, C1.z0 + 0.9], [C1.x0 + 0.9, C1.z1 - 0.9], [C1.x1 - 0.9, C1.z1 - 0.9]].sort((a, b) => Math.hypot(b[0] - D.cx, b[1] - D.cz) - Math.hypot(a[0] - D.cx, a[1] - D.cz)); const w1 = man(C1, '', pts[0][0], pts[0][1]); w1.area = { x0: pts[0][0] - 0.6, z0: pts[0][1] - 0.6, x1: pts[0][0] + 0.6, z1: pts[0][1] + 0.6 }; }   /* c540: 복도 맨 끝으로 */")
# 3. Type B 북쪽 구역 — 가로 2/3 · 세로 1.3배 · 막사 좁게 · 막사 지나 한참 뒤에 바리케이트
rep("const NS = Math.round(Math.sqrt(0.7 * SRC[2].w * SRC[2].h));", "const NS0 = Math.sqrt(0.7 * SRC[2].w * SRC[2].h), NW = Math.round(NS0 * 2 / 3), NH = Math.round(NS0 * 1.3);   // c540: 가로 3분의 2 · 세로 1.3배")
rep("const W = big.W, N = { custom: true, si: -1, W: NS, H: NS, g: 0 };", "const W = big.W, N = { custom: true, si: -1, W: NW, H: NH, g: 0 };")
rep("N.x0 = (W - NS) * (0.2 + 0.6 * rnd()); N.z0 = 0; N.x1 = N.x0 + NS; N.z1 = NS;", "N.x0 = (W - NW) * (0.2 + 0.6 * rnd()); N.z0 = 0; N.x1 = N.x0 + NW; N.z1 = NH;")
rep("for (const [sx, row] of [[-1, 0], [1, 0], [-1, 1], [1, 1]]) { const w = 8, d = 5.5, x = sx < 0 ? N.x0 + 2 + w / 2 : N.x1 - 2 - w / 2, z = N.z0 + 25.4 + row * 7.2;",
    "for (const [sx, row] of [[-1, 0], [1, 0], [-1, 1], [1, 1]]) { const w = 5.5, d = 5, x = sx < 0 ? N.x0 + 1.5 + w / 2 : N.x1 - 1.5 - w / 2, z = N.z1 - 5.5 - (1 - row) * 7.6;   /* c540: 막사 = 남쪽 입구 양옆 (좁게) */")
rep("const ck = { x: u + M.passW / 2 * 1.5 + 1.6, z: N.z1 - 1.6,", "const ck = { x: u + M.passW / 2 * 1.5 + 1.6, z: N.z1 - 1.2,")
rep("for (const dx of [-12, -4, 4, 12]) {", "for (const dx of [-8.4, -2.8, 2.8, 8.4]) {   /* c540: 좁아진 마당 */")
pathlib.Path('c540_patch.py').write_text('C540_R = ' + repr(R) + '\n')
print(len(R))
