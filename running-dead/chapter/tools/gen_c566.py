import pathlib
s = pathlib.Path('c565.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const needXp = (L) => CHAPTER ? Math.round(15 + 0.1 * L * L) :", "const needXp = (L) => CHAPTER ? Math.max(1, Math.round(15 + 0.1 * L * L - 10 * Math.exp(-L / 5))) :   /* c566: 첫 레벨업 5명 — 빼는 양이 레벨마다 줄어 Lv20쯤 원래 곡선과 같아진다 */")
pathlib.Path('c566_patch.py').write_text('C566_R = ' + repr(R) + '\n')
print(len(R))
