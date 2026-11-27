import pathlib
s = pathlib.Path('c523.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep('<div class="fl">🧪</div>', '<div class="fl">✓</div>')   # c524: 깬 곳은 체크
rep("<div class=\"fl\">${ok ? n : '🔒'}</div>", "<div class=\"fl\">${!ok ? '🔒' : ['e', 'n', 'h'].some((q) => cleared(n + q)) ? '✓' : n}</div>")   # c524: 깬 스테이지는 번호 대신 체크
rep("#outg .nd.tn .fl{", "#outg .nd.dn .fl{font-size:30px}\n#outg .nd.tn .fl{font-size:30px!important;")
rep("h += `<button class=\"nd ${ok ? '' : 'lk'} ${n === curN ? 'cur' : ''}\"", "h += `<button class=\"nd ${ok ? '' : 'lk'} ${n === curN ? 'cur' : ''} ${['e', 'n', 'h'].some((q) => cleared(n + q)) ? 'dn' : ''}\"")
pathlib.Path('c524_patch.py').write_text('C524_R = ' + repr(R) + '\n')
print(len(R))
