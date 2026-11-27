import pathlib
s = pathlib.Path('c547.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_PICK = window.__map || await new Promise((res) => {", r"""  function chLoadShow() {                       // c548: 맵을 만드는 동안 — 검은 화면 + '인간 세계에 침투 중...'
    if (document.getElementById('ldx')) return;
    const st = document.createElement('style'); st.textContent = '#ldx{position:fixed;inset:0;z-index:2000;background:#000;display:flex;align-items:center;justify-content:center;font:800 18px system-ui,-apple-system,sans-serif;color:#cfc6dd;letter-spacing:2px}#ldx i{font-style:normal;display:inline-block;width:1.6em;text-align:left}#ldx i::after{content:"";animation:ldxd 1.2s steps(4) infinite}@keyframes ldxd{0%{content:""}25%{content:"."}50%{content:".."}75%{content:"..."}}'; document.head.appendChild(st);
    const d = document.createElement('div'); d.id = 'ldx'; d.innerHTML = '인간 세계에 침투 중<i></i>'; document.body.appendChild(d);
  }
  const CH_PICK = window.__map || await new Promise((res0) => {
    const res = (v) => { chLoadShow(); setTimeout(() => res0(v), 80); };   // c548: 로딩 화면이 먼저 그려지고 나서 맵을 만든다""")
rep("    window.__rdReady = true;", "    window.__rdReady = true;\n    { const l = document.getElementById('ldx'); if (l) { l.style.transition = 'opacity 0.35s'; l.style.opacity = '0'; setTimeout(() => l.remove(), 400); } }   // c548")
pathlib.Path('c548_patch.py').write_text('C548_R = ' + repr(R) + '\n')
print(len(R))
