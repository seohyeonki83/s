import pathlib
s = pathlib.Path('c458.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("if (i < 3) {   // c457: 3차례 · c250", "if (i < 4) {   // c459: 3 = 보스 뒤 100초마다 오는 팀 · c457: 3차례 · c250")
rep("['C', [S_, S_, G_, G_, G_, G_]]]][i];", "['C', [S_, S_, G_, G_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]]][i];   /* c459: 보스 뒤 반복 팀 저2군6 */")
rep("      const T = chTanks.find((t) => !t.wreck) || chTanks[0];   // c454",
    "      chSf.T += dt; while (chSf.T >= chSfAt(chSf.n + 1)) { chSf.n++; chQueueTeam(3); }   // c459: 보스 뒤 100초마다 (650 · 750 · …) — 보스전 중에도 · 끝난 뒤에도\n      const T = chTanks.find((t) => !t.wreck) || chTanks[0];   // c454")
rep("    if (s !== chSf.shown) { chSf.shown = s;",
    "    if (chSf.on && chSf.boss) s = '다음 특공대 출동까지 ' + Math.max(0, Math.ceil(chSfAt(chSf.n + 1) - chSf.T)) + '초';   // c459\n    if (s !== chSf.shown) { chSf.shown = s;")
pathlib.Path('c459_patch.py').write_text('C459_R = ' + repr(R) + '\n')
