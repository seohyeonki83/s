import pathlib
s = pathlib.Path('c581.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("c.baseCol = 0x7a1f94;", "c.baseCol = 0x5c1470;   /* c582: 더 어두운 보라 */")
rep("sg: { col: '#7a1f94',", "sg: { col: '#8a2aa8',")   # 소개 글씨는 읽히게 조금 밝게
pathlib.Path('c582_patch.py').write_text('C582_R = ' + repr(R) + '\n')
print(len(R))
