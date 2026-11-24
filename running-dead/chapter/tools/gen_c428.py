# c428: 자폭 스위치 기본 아이콘 원래대로 (갈림길 카드에서만 새 아이콘) · 현금 알아채는 거리는 흰 ★6(18칸)에서 멈춘다 (빨간 별에서 계속 늘던 것)
src = open('c427.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep('<path d="M12 1.5a2 2 0 0 0 0 4z" fill="#a764ff"/><path d="M12 1.5a2 2 0 0 1 0 4z" fill="#ff8fc8"/><circle cx="9" cy="14.5" r="2.4" fill="#e8455a"/>', '<circle cx="12" cy="3.5" r="2" fill="#5fcf3a"/><circle cx="9" cy="14.5" r="2.4" fill="#e8455a"/>')
rep("  const cashK = () => 1.2 + lv('cash') * 1.56 / 7.2;", "  const cashK = () => 1.2 + Math.min(6, lv('cash')) * 1.56 / 7.2;   /* c428: 흰 ★6에서 멈춘다 */")
open('c428_patch.py', 'w').write("# c428: 자폭 기본 아이콘 원래대로 · 현금 거리 ★6에서 멈춤\nC428_R = " + repr(R) + "\n")
