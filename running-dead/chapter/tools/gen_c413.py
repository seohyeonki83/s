# c413: 이미 가진 가방을 또 얻었을 때(강화 창)도 분해할 수 있다 — 강화할 무기가 있을 때만
src = open('c412.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    mk(label, kind === 'bag' ? '무기 칸이 하나 늘어납니다' : '무기를 사용할 수 있습니다', 'rgba(255,255,255,0.92)', done);",
    "    mk(label, ov.dataset.ds || (kind === 'bag' ? '무기 칸이 하나 늘어납니다' : '무기를 사용할 수 있습니다'), 'rgba(255,255,255,0.92)', done);")
rep("    stage.appendChild(ov);\n    tapOk(ov, max ? '확인' : '강화', () => {",
    "    stage.appendChild(ov); ov.dataset.kind = kind; if (max) ov.dataset.ds = '이미 최대라 더 늘어나지 않습니다';\n    (kind === 'bag' && chCanDis(kind) ? chTwoOk : tapOk)(ov, max ? '확인' : '강화', () => {   // c413: 또 얻은 가방도 분해할 수 있다 (강화할 무기가 있을 때만)")
open('c413_patch.py', 'w').write("# c413: 또 얻은 가방도 분해\nC413_R = " + repr(R) + "\n")
