import pathlib
s = pathlib.Path('c496.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("(kind === 'bag' && chCanDis(kind) ? chTwoOk : tapOk)(ov, max ? '확인' : '강화', () => {", "(kind === 'bag' && chCanDis(kind) ? chTwoOk : tapOk)(ov, max ? '확인' : kind === 'bag' ? '획득' : '강화', () => {   /* c497: 가방은 획득 */")
rep("`지금${starTag(n, kind)}: ${statLine(kind, n)}<br>강화 뒤${starTag(n + 1, kind)}: ${statLine(kind, n + 1)}`", "`지금${starTag(n, kind)}: ${statLine(kind, n)}<br>${kind === 'bag' ? '획득 뒤' : '강화 뒤'}${starTag(n + 1, kind)}: ${statLine(kind, n + 1)}`")
rep("<div class=\"ds\" style=\"margin-top:8px\">${has ? '강화' : CH_BRIEF[k]}</div>", "<div class=\"ds\" style=\"margin-top:8px\">${has ? (k === 'bag' ? '하나 더 획득' : '강화') : CH_BRIEF[k]}</div>")
pathlib.Path('c497_patch.py').write_text('C497_R = ' + repr(R) + '\n')
rep("<div class=\"t\">${d.name} ${max ? '(이미 최대 강화)' : '강화'}</div>", "<div class=\"t\">${d.name} ${max ? (kind === 'bag' ? '(이미 최대)' : '(이미 최대 강화)') : kind === 'bag' ? '획득' : '강화'}</div>")
pathlib.Path('c497_patch.py').write_text('C497_R = ' + repr(R) + '\n')
