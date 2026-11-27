import pathlib
s = pathlib.Path('c519.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    const NODES = [[8, 64], [25, 38], [42, 62], [59, 36], [75, 60], [91, 40]];   // 깃발 자리 (% · 가로 · 세로)",
    "    const NODES = [[6, 60], [20, 36], [34, 62], [48, 36], [63, 60], [78, 38], [93, 60]];   // c520: 깃발 자리 (% · 가로 · 세로) — 0 = 튜토리얼 (생체 연구소)")
rep("${[[1, 192, 640], [2, 600, 380], [3, 1008, 620]].map(([n, x, y]) =>", "${[1, 2, 3].map((n) => [n, NODES[n][0] * 24, NODES[n][1] * 10]).map(([n, x, y]) =>")
rep("\n</svg>`;\n    const draw = () => {", """
<g stroke="#2f5c54" stroke-width="4"><rect x="${NODES[0][0] * 24 - 80}" y="${NODES[0][1] * 10 - 130}" width="160" height="62" rx="8" fill="#a9d9cc"/><path d="M${NODES[0][0] * 24 - 44} ${NODES[0][1] * 10 - 130} a44 44 0 0 1 88 0 Z" fill="#c6eee3"/><rect x="${NODES[0][0] * 24 - 8}" y="${NODES[0][1] * 10 - 190}" width="16" height="22" fill="#7fb8a8"/></g>
</svg>`;
    const draw = () => {""")
rep('<div class="ttl">러닝데드</div><button class="tb" data-ug="1" aria-label="성장">💪</button>', '<div class="ttl"></div>')
rep("""        const n = i + 1;
        if (n > 3) {""", """        const n = i;
        if (n === 0) { h += `<button class="nd tn" data-tn="1" style="left:${x}%;top:${y}%"><div class="fl">🧪</div><div class="nm">생체 연구소</div><div class="md">✓ 탈출</div></button>`; return; }   // c520: 튜토리얼 = 지도 첫 깃발 (아웃게임에 왔으면 이미 클리어)
        if (n > 3) {""")
rep('<div class="hint">← 지도를 밀어서 둘러보기 →</div>', '<div class="hint">← 지도를 밀어서 둘러보기 →</div><div class="bt"><button class="ugb" data-ug="1"><span class="i">💪</span>성장</button></div>')
rep("#outg .hint{position:absolute;bottom:calc(10px + env(safe-area-inset-bottom,0px));", "#outg .nd.tn .fl{background:radial-gradient(circle at 35% 30%,#7ff0d2,#1f8f78);border-color:#d6fff4;box-shadow:0 4px 0 #0f4a3e,0 6px 14px rgba(0,0,0,0.6);font-size:26px}\n#outg .nd.tn .md{color:#7ff0d2}\n#outg .bt{display:flex;justify-content:center;padding:10px 16px calc(12px + env(safe-area-inset-bottom,0px));background:linear-gradient(rgba(13,17,23,0.85),#0d1117)}\n#outg .ugb{display:flex;align-items:center;justify-content:center;gap:8px;width:min(300px,80vw);padding:14px 0;border-radius:18px;background:linear-gradient(#4f8dff,#2a5fd0);box-shadow:0 4px 0 #173a85;font-size:21px;font-weight:900;color:#fff}\n#outg .ugb .i{font-size:24px}\n#outg .hint{position:absolute;bottom:calc(92px + env(safe-area-inset-bottom,0px));")
rep("      if (b.dataset.set) { setSheet(); return; }", "      if (b.dataset.set) { setSheet(); return; }\n      if (b.dataset.tn) { tutSheet(); return; }")
rep("    const setSheet = () => {", """    const tutSheet = () => {   // c520: 튜토리얼 상세 — 생체 연구소 · 목표 탈출하기
      openSheet(`<div class="hd"><div><div class="t1">튜토리얼</div><div class="t2">생체 연구소</div></div><button class="x">✕</button></div><div class="ds">실험실 수조에서 깨어난 첫 좀비. 동료를 모으고 길을 막는 사람들을 물리치며 연구소를 빠져나가라.</div>` +
        `<div class="cd"><div class="k">목표</div><div class="v">탈출하기</div></div>` +
        `<div class="cd"><div class="k">보상</div><div class="rw got"><div class="gi">${CH_GENE_I()}100</div><div class="lb">첫 클리어 · 받음 ✓<small>처음 한 번만</small></div></div><div class="rw"><div class="gi">${CH_GENE_I()}1</div><div class="lb">적 하나 없앨 때마다<small>다시 해도 받는다</small></div></div></div>` +
        `<button class="go" data-go="1">다시 하기</button>`, (b) => { if (b.dataset.go) { ov.remove(); tut(); } });
    };
    const setSheet = () => {""")
rep('<button class="sb" data-tut="1">튜토리얼 다시 하기<br><small style="font-size:11px;color:#8fa0b8">처치 유전자만 받는다</small></button><div style="height:18px"></div>', '')
rep("'이곳을 탈출하십시오'", "'탈출하기'")
rep("${CH_TUT ? '튜토리얼' : '스테이지 '", "${CH_TUT ? '튜토리얼 · 생체 연구소' : '스테이지 '")
pathlib.Path('c520_patch.py').write_text('C520_R = ' + repr(R) + '\n')
print(len(R))
