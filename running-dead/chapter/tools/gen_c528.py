import pathlib
s = pathlib.Path('c527.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  function chMadRoll0(c) {", "  function chMadRoll(c) { const ok = chMadRoll0(c); if (ok) chGeneAdd(1); return ok; }   // c505: 오작동 = 적에서 사라짐 · c528: c517에서 결과 창을 바꾸다 같이 지워졌던 것 되살림\n  function chMadRoll0(c) {")
pathlib.Path('c528_patch.py').write_text('C528_R = ' + repr(R) + '\n')
print(len(R))
