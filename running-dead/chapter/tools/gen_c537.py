import pathlib
s = pathlib.Path('c536.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# c537: 지도 왼쪽에 바다를 덧대 — 맨 왼쪽 생체 연구소도 화면 가운데로 올 수 있게
rep("#outg .in{position:relative;height:100%;aspect-ratio:2.4/1;min-width:900px}", "#outg .in{position:relative;height:100%;aspect-ratio:2.4/1;min-width:900px;margin-left:45vw;flex:none}")
rep("#outg .map{flex:1;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none}", "#outg .map{flex:1;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none;display:flex;background:linear-gradient(#16324a,#0f2236)}")
rep("nd.offsetLeft - m.clientWidth / 2", "nd.offsetLeft + nd.offsetParent.offsetLeft - m.clientWidth / 2")
rep("nx.offsetLeft - map.clientWidth / 2", "nx.offsetLeft + nx.offsetParent.offsetLeft - map.clientWidth / 2")
rep("M-20 260 C 120 130, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170 L", "M70 250 C 170 140, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170 L")
rep("M-20 260 C 120 130, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170\" fill=\"none\"", "M70 250 C 170 140, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170\" fill=\"none\"")   # c537: 왼쪽 해안선을 둥글게 (바다 덧댄 쪽)
rep("S 120 930, -20 880 Z", "S 140 930, 80 870 C 10 780, 60 600, 20 480 S 40 300, 70 250 Z")
pathlib.Path('c537_patch.py').write_text('C537_R = ' + repr(R) + '\n')
print(len(R))
