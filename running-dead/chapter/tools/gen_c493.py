import pathlib
s = pathlib.Path('c492.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("      deaths = Math.max(deaths, STAR_AT[1]); stars = Math.max(stars, 2);   // 난리남", "      { const A = bodies.filter((q) => q.kind === 'ally'); for (const q of A.slice(0, 2)) mutate(q, 'armor'); }   // c493: 보스 테스트 — 덩치 2마리 (영구)\n      deaths = Math.max(deaths, STAR_AT[1]); stars = Math.max(stars, 2);   // 난리남")
rep("['k', '보스 테스트', '큰 맵 · 동료 70 · 무적 · 바로 보스 출동']", "['k', '보스 테스트', '큰 맵 · 동료 70 · 덩치 2 · 무적 · 바로 불도저 2대']")
pathlib.Path('c493_patch.py').write_text('C493_R = ' + repr(R) + '\n')
