# c447: 내 미는 힘 5 · 덩치 7 (덩치가 된 나도 7) · 괴물 덩치 7 → 14 (빨간 별마다 +7/6)
src = open('c446.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("const CH_MY_FORCE = 4;   /* c446: 5 → 4 (덩치가 되면 5) */", "const CH_MY_FORCE = 5;   /* c447: 4 → 5 (덩치가 되면 7) */   /* c446: 5 → 4 (덩치가 되면 5) */")
rep("function chArmF(z) { const B = chMB(z); return 5 + (B && B.id === 'monster' ? 4 * B.r / 6 : 0); }", "function chArmF(z) { const B = chMB(z); return 7 + (B && B.id === 'monster' ? 7 * B.r / 6 : 0); }   /* c447: 기본 7 (괴물 ★6 = 14) */")
rep("(5 + 4 * r / 6).toFixed(1)", "(7 + 7 * r / 6).toFixed(1)", 2)
open('c447_patch.py', 'w').write("# c447: 미는 힘 — 나 5 · 덩치 7 → 14\nC447_R = " + repr(R) + "\n")
