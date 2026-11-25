# c452: 감염 시간 — 나 10% 짧게 · 동료 15% 짧게 (회복량은 그대로)
src = open('c451.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    z.biteT = z.biteLen = (z === me ? INFECT / MY_INFECT : INFECT) * biteK() * (z.mut ? 0.5 : 1);", "    z.biteT = z.biteLen = (z === me ? INFECT / MY_INFECT : INFECT) * biteK() * (z.mut ? 0.5 : 1) * (CHAPTER ? (z === me ? 0.9 : 0.85) : 1);   /* c452: 나 10% · 동료 15% 짧게 */")
rep("  const myBiteLen = (n = up.bite) => INFECT / MY_INFECT * biteK(n);", "  const myBiteLen = (n = up.bite) => INFECT / MY_INFECT * biteK(n) * (CHAPTER ? 0.9 : 1);   /* c452 */")
open('c452_patch.py', 'w').write("# c452: 감염 시간\nC452_R = " + repr(R) + "\n")
