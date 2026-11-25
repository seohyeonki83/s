# c445: 내 미는 힘 7 → 5 · 덩치 미는 힘 10 → 5 (덩치가 된 나도 5) · 괴물 덩치만 빨간 별마다 +0.67 (★6 = 9)
src = open('c444.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("const CH_MY_FORCE = 7;", "const CH_MY_FORCE = 5;   /* c445: 7 → 5 */")
rep("function chArmF(z) { const B = chMB(z); return 10 + (B && B.id === 'monster' ? 4 * B.r / 6 : 0); }", "function chArmF(z) { const B = chMB(z); return 5 + (B && B.id === 'monster' ? 4 * B.r / 6 : 0); }   /* c445: 기본 5 (괴물 ★6 = 9) */")
rep("(10 + 4 * r / 6).toFixed(1)", "(5 + 4 * r / 6).toFixed(1)", 2)
open('c445_patch.py', 'w').write("# c445: 미는 힘 — 나 5 · 덩치 5\nC445_R = " + repr(R) + "\n")
