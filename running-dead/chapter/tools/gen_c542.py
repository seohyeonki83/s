import pathlib
s = pathlib.Path('c541.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep('<div class="ttl"></div>', '<div class="ttl"><span class="vr">${((document.getElementById(\'ver\') || {}).textContent || \'\').match(/c\\d+/) || \'\'}</span></div>')   # c542: 버전 조그맣게
rep("#outg .ttl{", "#outg .vr{font-size:11px;font-weight:700;color:rgba(255,255,255,0.35);letter-spacing:0}\n#outg .ttl{")
pathlib.Path('c542_patch.py').write_text('C542_R = ' + repr(R) + '\n')
print(len(R))
