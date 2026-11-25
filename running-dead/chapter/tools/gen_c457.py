import pathlib
s = pathlib.Path('c456.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("(chSf.n >= 4 ? 'sfpopb' : 'sfpop')", "(chSf.n >= 3 ? 'sfpopb' : 'sfpop')")
rep("s = chSf.n < 4 ? (chSf.n === 0 ?", "s = chSf.n < 3 ? (chSf.n === 0 ?")
rep("if (chSf.n <= 4) chQueueTeam(chSf.n - 1);", "if (chSf.n <= 3) chQueueTeam(chSf.n - 1);   /* c457: 특공대 3차례 → 4번째가 보스 */")
rep("chSf.n = 4; chSf.T = chSfAt(5) - 0.05;", "chSf.n = 3; chSf.T = chSfAt(4) - 0.05;")
rep("if (i < 4) {   // c250", "if (i < 3) {   // c457: 3차례 · c250")
rep("const P = [[['W', [S_, G_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]]]][i];",
    "const P = [[['W', [S_, G_, G_, G_]]], [['W', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, S_, G_, G_, G_, G_]]]][i];   /* c457: 4번째를 2 · 3번째에 나눔 — 저1군3 · 저3군8 · 저4군10 */")
pathlib.Path('c457_patch.py').write_text('C457_R = ' + repr(R) + '\n')
