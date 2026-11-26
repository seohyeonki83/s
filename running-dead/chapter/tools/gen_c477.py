import pathlib
s = pathlib.Path('c475.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("  const chAcidB = () => owned.acidp ? 1 + lv('acidp') : 0;", "  const chAcidPB = (n) => Math.round(1 + 0.6 * n);   // c477: 산성 강도 +1 · 2 · 2 · 3 · 3 · 4 (★5 = +4)\n  const chAcidB = () => owned.acidp ? chAcidPB(lv('acidp')) : 0;")
rep("    acidp: (n) => `산성 도트 +${1 + n} (1초마다)`,", "    acidp: (n) => `산성 도트 +${chAcidPB(n)} (1초마다)`,   /* c477 */")
rep("acidp: ['도트', (n) => `+${1 + n}`]", "acidp: ['도트', (n) => `+${chAcidPB(n)}`]")
pathlib.Path('c477_patch.py').write_text('C477_R = ' + repr(R) + '\n')
