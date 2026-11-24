# c424: 장비 배지 — 더 촘촘하게 (지름 36 → 32px, 좌우 40 → 35px, 위아래 48 → 41px, 모든 줄 3개씩). 14개 다 가지면 7줄 → 5줄
src = open('c423.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("      const row = i < 3 ? 0 : 1 + Math.floor((i - 3) / 2), col = i < 3 ? i : (i - 3) % 2;   // c37: 첫 줄 3개, 그 위로 2개씩",
    "      const row = Math.floor(i / 3), col = i % 3;   // c424: 모든 줄 3개씩   // c37: 첫 줄 3개, 그 위로 2개씩")
rep("      el.style.left = `calc(max(16px, env(safe-area-inset-left, 0px)) + ${col * 40}px)`;\n      el.style.bottom = `calc(6px + env(safe-area-inset-bottom, 0px) + ${row * 48}px)`;\n      el.style.width = el.style.height = '36px';",
    "      el.style.left = `calc(max(16px, env(safe-area-inset-left, 0px)) + ${col * 35}px)`;\n      el.style.bottom = `calc(6px + env(safe-area-inset-bottom, 0px) + ${row * 41}px)`;\n      el.style.width = el.style.height = '32px'; el.style.borderWidth = '2px';   /* c424: 촘촘하게 */\n      { const ic = el.querySelector('.ic'); if (ic) ic.style.transform = 'scale(0.88)'; const pc = el.querySelector('.pc'); if (pc) { pc.style.fontSize = '9px'; pc.style.marginTop = '0'; } }")
open('c424_patch.py', 'w').write("# c424: 장비 배지 촘촘하게\nC424_R = " + repr(R) + "\n")
