import pathlib
s = pathlib.Path('c461.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
old = "const P = [[['W', [S_, G_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]]][i];"
rep(old, """const CR = [null, [S_, G_, G_], [S_, G_, G_, G_, G_], [S_, G_, G_, G_, G_]][i];   // c462: 차에 탈 사람 (2팀 저1군2 · 3팀 저1군4)
      let P = [['W', i ? [S_, G_, G_] : [S_, G_, G_, G_]]];
      if (CR) {   // c462: 군인차 1대 또는 2대 (반반) · 사람은 랜덤으로 나눠 탄다 · 저격수는 맨 앞
        const L = CR.slice(); for (let k = L.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [L[k], L[j]] = [L[j], L[k]]; }
        const cut = Math.random() < 0.5 ? 0 : 1 + Math.floor(Math.random() * (L.length - 1)), C = cut ? [L.slice(0, cut), L.slice(cut)] : [L];
        for (const c of C) { c.sort((a, b) => (b === S_) - (a === S_)); P.push(['C', c]); }
      }""")
pathlib.Path('c462_patch.py').write_text('C462_R = ' + repr(R) + '\n')
