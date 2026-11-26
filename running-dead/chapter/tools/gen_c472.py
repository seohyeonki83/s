import pathlib, re
s = pathlib.Path('c471.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("c.mesh.material.color.setHex(0xffb6d9);   /* c427: 연분홍 */", "c.mesh.material.color.setHex(0x8cff4a);   /* c472: 밝은 녹색 · c427: 연분홍 */")
line = re.search(r"    parasite: svgI\('[^\n]*", s).group(0)
new = line.replace('#ffa6d2', '#9dff6a').replace('#ffe0ef', '#e4ffd6').replace('#d9478c', '#3fbf2a').replace('#7a2350', '#1f6a17')
rep(line, new + "   /* c472: 분열세포 아이콘 밝은 녹색 */")
pathlib.Path('c472_patch.py').write_text('C472_R = ' + repr(R) + '\n')
