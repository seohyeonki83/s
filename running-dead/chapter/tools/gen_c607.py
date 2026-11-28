import pathlib
s = pathlib.Path('c606.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_GOO_DOT = 2;", "  const CH_GOO_DOT = 4;   /* c607: 자폭 스위치 도트 기본 2 → 4 */\n  const CH_ACID_DOT = 1;   // c607: 산성피 도트 기본 2 → 1 (터지는 순간 피해는 그대로)")
rep("e.acidT -= CH_DOT_T; const d = (1 * HPK + chAcidB()) * CH_UPK.atk;", "e.acidT -= CH_DOT_T; const d = (CH_ACID_DOT + chAcidB()) * CH_UPK.atk;   /* c607 */")
rep("d.acidT -= CH_DOT_T; const n = (1 * HPK + chAcidB()) * CH_UPK.atk;", "d.acidT -= CH_DOT_T; const n = (CH_ACID_DOT + chAcidB()) * CH_UPK.atk;   /* c607 */")
pathlib.Path('c607_patch.py').write_text('C607_R = ' + repr(R) + '\n')
print(len(R))
