import pathlib
s = pathlib.Path('c508.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
line = [l for l in s.split('\n') if l.startswith("    if (starSlots().length !== STAR_MAX || starsEl.dataset.m !== (sk ? 'k' : 'e'))")][0]
rep(line, """    if (CHAPTER) {   // c509: 위 = 지금 단계 이름 · 가운데 = 느낌표 5개 (게이지 칸 끝마다 하나) · 아래 = 5칸 게이지 (6단계부터 새 게이지 · 해골)
      if (starSlots().length !== STAR_MAX || starsEl.dataset.m !== (sk ? 'k' : 'e')) { starsEl.dataset.m = sk ? 'k' : 'e';
        starsEl.innerHTML = '<i class="lv"></i><div class="alr">' + (sk ? '<span class="s sk">☠</span>' : '<span class="s">!</span>').repeat(STAR_MAX) + '</div><div class="ag">' + '<b><u></u></b>'.repeat(5) + '</div><div class="obj"></div>'; }
    } else
""" + line)
rep("    if (CHAPTER && !starsEl.querySelector('.ag')) { const g = document.createElement('div'); g.className = 'ag'; g.innerHTML = '<i></i>'; starsEl.appendChild(g); const o = document.createElement('div'); o.className = 'obj'; starsEl.appendChild(o); }   // c505: 경보 게이지 · 목표",
    "    if (CHAPTER) chAlHud();   // c509")
old_css_start = "st.textContent = '#stars{pointer-events:auto!important;cursor:pointer}#stars .ag{width:150px;height:6px;margin:3px auto 0;border-radius:3px;background:rgba(255,255,255,0.18);overflow:hidden}#stars .ag i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffb84d,#ff4a3a)}"
rep(old_css_start, "st.textContent = '#stars{pointer-events:auto!important;cursor:pointer}#stars .lv{display:block;margin:0 0 1px;min-height:13px;font:800 12px/13px system-ui,sans-serif;color:#e2c2fb}' +\n      '#stars .alr{display:flex;width:164px;margin:0 auto}#stars .alr .s{flex:1;width:auto;text-align:right;padding-right:1px;font-size:20px;line-height:20px;box-sizing:border-box}#stars .alr .s.sk{color:#ff2a2a;font-size:15px}' +\n      '#stars .ag{display:flex;gap:2px;width:164px;height:6px;margin:2px auto 0}#stars .ag b{flex:1;height:100%;border-radius:2px;background:rgba(255,255,255,0.18);overflow:hidden}#stars .ag u{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffb84d,#ff4a3a)}#stars[data-m=\"k\"] .ag u{background:linear-gradient(90deg,#ff4a3a,#b00000)}' +\n      '")
rep("""    const g = starsEl.querySelector('.ag i'), o = starsEl.querySelector('.obj'); if (!g || !o) return;
    const b0 = chAL >= 5 ? 5 : 0; let f = 0; for (let L = b0; L < b0 + 5; L++) f += chAlFill(L); const w = Math.round(f / 5 * 1000) / 10 + '%';
    if (g.style.width !== w) g.style.width = w;
    const t = chObjText();""", """    const o = starsEl.querySelector('.obj'); if (!o) return;
    const t = chObjText();""")
rep("  function chObjHud() {", """  function chAlHud() {                         // c509: 5칸 게이지 — 칸마다 한 단계, 칸이 차면 그 끝 느낌표에 불
    const U = starsEl.querySelectorAll('.ag u'); if (U.length !== 5) return;
    const b0 = starsEl.dataset.m === 'k' ? 5 : 0;
    for (let k = 0; k < 5; k++) { const w = Math.round(chAlFill(b0 + k) * 1000) / 10 + '%'; if (U[k].style.width !== w) U[k].style.width = w; }
  }
  function chObjHud() {""")
rep("    if (CH_TUT) return;   // c293: 튜토리얼은 특공대·보스 없음", "    if (CHAPTER) chAlHud();   // c509\n    if (CH_TUT) return;   // c293: 튜토리얼은 특공대·보스 없음")
pathlib.Path('c509_patch.py').write_text('C509_R = ' + repr(R) + '\n')
print(len(R))
