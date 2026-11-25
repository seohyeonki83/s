import pathlib
s = pathlib.Path('c460.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("[['W', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, S_, G_, G_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]]][i];",
    "[['W', [S_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]]][i];   /* c461: 1팀 저1군3 · 2팀 저2군4 · 3팀 저2군6 (보스 뒤 반복도 3팀) */")
pathlib.Path('c461_patch.py').write_text('C461_R = ' + repr(R) + '\n')
