# c411: 작은 좀비(새끼 좀비)의 미는 힘 = 보통 좀비의 3분의 1
src = open('c410.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("function chMini(c) { c.mini = true; c.mesh.scale.setScalar(0.5); if (!c.mut) c.mesh.material.color.setHex(0xb9c8f9); }",
    "function chMini(c) { c.mini = true; c.mesh.scale.setScalar(0.5); if (!c.mut) { c.mesh.material.color.setHex(0xb9c8f9); c.force = 1 / 3;   /* c411: 미는 힘 = 보통 좀비의 3분의 1 */ } }")
open('c411_patch.py', 'w').write("# c411: 작은 좀비 미는 힘 3분의 1\nC411_R = " + repr(R) + "\n")
