import pathlib
s = pathlib.Path('c566.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("CH_SV.up[b.dataset.up]++; chSave(); draw(); upSheet(); }", "CH_SV.up[b.dataset.up]++; chSave(); { const m = ov.querySelector('.map'); draw(m ? m.scrollLeft : 0); } upSheet(); }   /* c567: 다시 그려도 지도는 보던 자리 그대로 */")
pathlib.Path('c567_patch.py').write_text('C567_R = ' + repr(R) + '\n')
print(len(R))
