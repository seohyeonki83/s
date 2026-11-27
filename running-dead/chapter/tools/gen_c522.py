import pathlib
s = pathlib.Path('c521.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_UPK = { hp: 1 + 0.01 * CH_SV.up.hp, ahp: 1 + 0.01 * CH_SV.up.ahp, atk: 1 + 0.01 * CH_SV.up.atk };", "  const CH_UP_K = 0.005;   // c522: 성장 1 = 기본값의 0.5% (유전자 100)\n  const CH_UPK = { hp: 1 + CH_UP_K * CH_SV.up.hp, ahp: 1 + CH_UP_K * CH_SV.up.ahp, atk: 1 + CH_UP_K * CH_SV.up.atk };")
rep("CH_UPK.hp = 1 + 0.01 * CH_SV.up.hp; CH_UPK.ahp = 1 + 0.01 * CH_SV.up.ahp; CH_UPK.atk = 1 + 0.01 * CH_SV.up.atk;", "CH_UPK.hp = 1 + CH_UP_K * CH_SV.up.hp; CH_UPK.ahp = 1 + CH_UP_K * CH_SV.up.ahp; CH_UPK.atk = 1 + CH_UP_K * CH_SV.up.atk;")
rep("const CH_UP_COST = 100;   // 성장 1포인트 = 유전자 100 · 기본값의 1%", "const CH_UP_COST = 100;   // 성장 1 = 유전자 100 · 기본값의 0.5% (c522)")
rep("<div class=\"pc\">+${v}%</div><button class=\"ub\" data-up=\"${k}\" ${CH_SV.genes < CH_UP_COST ? 'disabled' : ''}>+1% ${CH_GENE_I(14)}${CH_UP_COST}",
    "<div class=\"pc\">${v}</div><button class=\"ub\" data-up=\"${k}\" ${CH_SV.genes < CH_UP_COST ? 'disabled' : ''}>+1 ${CH_GENE_I(14)}${CH_UP_COST}")   # c522: 숫자로 (0부터)
rep("한 번 누를 때마다 기본값의 1%씩 오른다. 끝없이 올릴 수 있다.", "능력 1 = 기본값의 0.5%. 0부터 시작하고 끝없이 올릴 수 있다.")
rep("const CH_SK = CH_RUN ? 1 + 0.3 * (CH_STG - 1) : 1;", "const CH_SK = CH_RUN ? 1 + 0.2 * (CH_STG - 1) : 1;   /* c522: 다시 +20%씩 (1.0 · 1.2 · 1.4) */")
rep("+${(n - 1) * 30}%", "+${(n - 1) * 20}%")
rep("적이 30% 더 단단하고 세다.", "적이 20% 더 단단하고 세다.")
rep("적이 60% 더 단단하고 세다.", "적이 40% 더 단단하고 세다.")
pathlib.Path('c522_patch.py').write_text('C522_R = ' + repr(R) + '\n')
print(len(R))
