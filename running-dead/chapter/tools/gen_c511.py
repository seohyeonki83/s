import pathlib
s = pathlib.Path('c510.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("'</div><div class=\"ag\">' + '<b><u></u></b>'.repeat(5) + '</div>", "'</div><div class=\"ag\">' + '<b><u></u></b>'.repeat(sk ? 5 : 4) + '</div>")   # c511: 수상함 앞 칸 없음
rep("""    const U = starsEl.querySelectorAll('.ag u'); if (U.length !== 5) return;
    const b0 = starsEl.dataset.m === 'k' ? 5 : 0;
    for (let k = 0; k < 5; k++) {""", """    const U = starsEl.querySelectorAll('.ag u'); if (!U.length) return;
    const b0 = starsEl.dataset.m === 'k' ? 5 : 1;   // c511: 느낌표 줄은 수상함 앞 칸 없이 4칸 (수상함은 5마리면 바로 불)
    for (let k = 0; k < U.length; k++) {""")
rep("#stars[data-m=\"k\"] .ag u{", "#stars[data-m=\"e\"] .alr .s:first-child{flex:0 0 14px;text-align:center;padding-right:0}#stars[data-m=\"e\"] .ag{padding-left:16px;box-sizing:border-box}#stars[data-m=\"k\"] .ag u{")
pathlib.Path('c511_patch.py').write_text('C511_R = ' + repr(R) + '\n')
print(len(R))
