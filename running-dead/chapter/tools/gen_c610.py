import pathlib
s = pathlib.Path('c609.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_TP_CLR = 5, CH_TP_SUB = 1;", "  const CH_TP_CLR = 5, CH_TP_SUB = 1;\n  const chTpSub = (n) => CH_TP_SUB * (+n || 1);   // c610: 서브 미션 특성 = 챕터 번호만큼 (1 · 2 · 3 · 4)")
rep("CH_TP_SUB * Object.keys(CH_SV.sub || {}).length;", "Object.keys(CH_SV.sub || {}).reduce((t, k) => t + chTpSub(parseInt(k, 10)), 0);   /* c610 */")
rep("${CH_TP_I(14)}${CH_TP_SUB}", "${CH_TP_I(14)}${chTpSub(n)}")
rep("' · ✦+' + CH_TP_SUB, CH_SUB_G, true]);", "' · ✦+' + chTpSub(CH_STG), CH_SUB_G, true]);")
rep("첫 클리어 5 · 서브 미션 1", "첫 클리어 5 · 서브 미션 챕터 번호만큼")
pathlib.Path('c610_patch.py').write_text('C610_R = ' + repr(R) + '\n')
print(len(R))
