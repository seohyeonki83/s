import pathlib
s = pathlib.Path('c498.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("mmEl.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); mmBig = !mmBig; mmLayout(); });",
    "mmEl.addEventListener('pointerdown', (e) => { e.stopPropagation(); e.preventDefault(); mmBig = !mmBig;\n      if (mmBig && !paused) { paused = true; mmPaused = true; stopInput(); } else if (!mmBig && mmPaused) { mmPaused = false; paused = false; last = 0; }   // c499: 큰 지도를 연 동안 일시정지\n      mmLayout(); });")
rep("  let mmBig = false;", "  let mmBig = false, mmPaused = false;   // c499")
pathlib.Path('c499_patch.py').write_text('C499_R = ' + repr(R) + '\n')
