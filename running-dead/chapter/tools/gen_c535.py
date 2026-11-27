import pathlib
s = pathlib.Path('c534.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("<div class=\"fl\">${pre.tut ? '🧪' : '✓'}</div>", "<div class=\"fl\">🧪</div>")   # c535: 깃발 안 큰 체크 없앰
rep("<div class=\"fl\">${!ok ? '🔒' : ['e', 'n', 'h'].some((q) => cleared(n + q)) ? '✓' : n}</div>", "<div class=\"fl\">${!ok ? '🔒' : n}</div>")
rep("if (fl && (anim.t || !['e', 'n', 'h'].some((q) => q !== anim.d && CH_SV.clr[anim.n + q]))) { fl.textContent = '✓';", "if (false) {")
rep("#outg .cbx{gap:5px!important;margin-top:2px}#outg .cb{width:24px;height:24px;border-radius:6px;font-size:16px!important;", "#outg .cbx{gap:6px!important;margin-top:3px}#outg .cb{width:32px;height:32px;border-radius:8px;border-width:3px!important;font-size:21px!important;")   # c535: 체크박스 3칸 크게
pathlib.Path('c535_patch.py').write_text('C535_R = ' + repr(R) + '\n')
print(len(R))
