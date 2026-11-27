import pathlib
s = pathlib.Path('c533.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep(".sqx .dk{position:absolute;inset:0;background:rgba(0,0,0,0.45)}", ".sqx .dk{position:absolute;inset:0;background:rgba(0,0,0,0.7)}.sqx .bd{position:absolute;left:0;right:0;top:calc(30% - 44px);height:150px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,0.92) 22%,rgba(0,0,0,0.92) 78%,rgba(0,0,0,0))}")   # c534: 바탕 더 검게 · 글씨 뒤는 더
rep('el.innerHTML = `<div class="dk"></div><div class="fl"></div>', 'el.innerHTML = `<div class="dk"></div><div class="fl"></div><div class="bd"></div>')
rep("el.querySelector('.dk').animate(", "el.querySelector('.bd').animate([{ opacity: 0 }, { opacity: 1, offset: 0.1 }, { opacity: 1, offset: 0.85 }, { opacity: 0 }], { duration: D, fill: 'forwards' });\n      el.querySelector('.dk').animate(")
pathlib.Path('c534_patch.py').write_text('C534_R = ' + repr(R) + '\n')
print(len(R))
