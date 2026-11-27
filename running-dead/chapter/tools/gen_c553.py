import pathlib
s = pathlib.Path('c552.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1) 이야기 글을 한곳에 (로딩 · 아웃게임 · 판 안이 같은 글을 쓴다)
rep("  const CH_GENE_I = (w = 16) =>",
    """  const CH_STORY = { t: '차가운 수조 속에서 눈을 떴다. 몸이 예전 같지 않다. 나를 이렇게 만든 건 저 흰 가운의 인간들이다. 문을 부수고, 길을 막는 자는 모두 물어뜯어라. 이곳을 빠져나가는 것, 그게 복수의 시작이다.',   /* c553 */
    1: '실험실을 빠져나온 감염은 조용한 도시로 번지기 시작했다. 도시를 지키려 특공대가 몰려온다. 그들마저 우리 무리로 만들어라.',
    2: '공장과 창고 너머로 감염이 퍼지자 군은 중장비를 앞세웠다. 벽을 밀고 들어오는 강철을 무너뜨리고 이 지구를 삼켜라.',
    3: '모든 병력은 북쪽 군사기지에서 나온다. 검문소를 넘어 기지 한가운데까지 밀고 들어가라. 그곳이 무너지면 군은 머리를 잃는다.',
    4: '마지막 방어선, 국경 요새. 장갑차가 길을 막고 서 있다. 이곳만 넘으면 더는 우리를 막을 것이 없다.' };
  const CH_GENE_I = (w = 16) =>""")
# 2) 로딩 화면: 이야기 + '침투 중...' → 다 되면 [침투하기]
a = [l for l in s.split('\n') if l.startswith("    const st = document.createElement('style'); st.textContent = '#ldx{")]
assert len(a) == 1
rep("  function chLoadShow() {                       // c548: 맵을 만드는 동안 — 검은 화면 + '인간 세계에 침투 중...'\n    if (document.getElementById('ldx')) return;\n" + a[0] + "\n    const d = document.createElement('div'); d.id = 'ldx'; d.innerHTML = '인간 세계에 침투 중<i></i>'; document.body.appendChild(d);",
    "  let chLdxWait = false;   /* c553: 로딩 화면의 [침투하기]를 누를 때까지 판을 세운다 */\n  function chLoadShow(k) {                       // c548: 맵을 만드는 동안 — 검은 화면 + '인간 세계에 침투 중...'   /* c553: + 그 맵 이야기 · 끝나면 [침투하기] */\n    if (document.getElementById('ldx')) return;\n"
    + a[0].replace("display:flex;align-items:center;justify-content:center;", "display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;")
      .replace("document.head.appendChild(st);", "st.textContent += '#ldx .st{width:min(320px,84vw);font:600 15px/1.75 system-ui,-apple-system,sans-serif;color:#e8e2f0;letter-spacing:0;text-align:left;word-break:keep-all}#ldx .lw{height:52px;display:flex;align-items:center}#ldx .go{font:900 18px system-ui,sans-serif;color:#fff;background:#7a2fb0;border:0;border-radius:14px;padding:14px 46px;letter-spacing:2px;box-shadow:0 4px 14px rgba(160,70,230,0.45);animation:ldxin 0.3s ease-out}@keyframes ldxin{from{opacity:0;transform:scale(0.9)}to{opacity:1;transform:none}}'; document.head.appendChild(st);")
    + "\n    const d = document.createElement('div'); d.id = 'ldx'; d.innerHTML = (CH_STORY[k] ? '<div class=\"st\">' + CH_STORY[k] + '</div>' : '') + '<div class=\"lw\">인간 세계에 침투 중<i></i></div>'; document.body.appendChild(d); chLdxWait = true;")
rep("    const res = (v) => { chLoadShow(); setTimeout(() => res0(v), 80); };",
    "    const res = (v) => { chLoadShow(v === 't' ? 't' : CH_STG); setTimeout(() => res0(v), 80); };")
rep("    { const l = document.getElementById('ldx'); if (l) { l.style.transition = 'opacity 0.35s'; l.style.opacity = '0'; setTimeout(() => l.remove(), 400); } }   // c548",
    """    { const l = document.getElementById('ldx'); if (l) { const w = l.querySelector('.lw'); w.innerHTML = '<button class="go">침투하기</button>';   /* c553: 다 만들었다 → [침투하기] 누르면 들어간다 */
      w.querySelector('.go').addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); if (!chLdxWait) return; chLdxWait = false; l.style.transition = 'opacity 0.35s'; l.style.opacity = '0'; setTimeout(() => l.remove(), 400); }); } }   // c548""")
rep("    if (!goalShown) { if (CH_TUT ?", "    if (!goalShown) { if (chLdxWait) return; if (CH_TUT ?")
# 3) 판 안 목표 창에서는 이야기를 뺀다
rep("(CH_TUT || CH_RUN ? '<div class=\"g6\">' + chStory() + '</div>' : '')", "''   /* c553: 이야기는 로딩 화면으로 */")
# 4) 아웃게임 스테이지 설명 줄 = 이야기
rep('<div class="ds">${I.ds}</div>', '<div class="ds">${CH_STORY[n]}</div>')
rep('<div class="ds">실험실에서 깨어난 첫 좀비.</div>', '<div class="ds">${CH_STORY.t}</div>')
pathlib.Path('c553_patch.py').write_text('C553_R = ' + repr(R) + '\n')
print(len(R))
