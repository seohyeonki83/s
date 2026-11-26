import pathlib
s = pathlib.Path('c483.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("  const MUT_T = () => 6 + 3 * chLvB('mutate');", "  const CH_MUT_TT = [6, 10, 14, 17, 21, 24];   // c484: 변이 · 각성 시간 (★0~★5, 둘이 같다 — 예전 ★6 끝값 24초를 ★5에, 소수점은 올림)\n  const MUT_T = () => CH_MUT_TT[chLvB('mutate')];")
rep("  const chAccMax = () => 5 + 3 * chLvB('awaken');", "  const chAccMax = () => CH_MUT_TT[chLvB('awaken')];   /* c484 */")
rep("    mutate: (n) => `주사 ${CH_WV('mutN', n)}개 · 변이 ${6 + 3 * n}초`,", "    mutate: (n) => `주사 ${CH_WV('mutN', n)}개 · 변이 ${CH_MUT_TT[Math.min(5, n)]}초`,   /* c484 */")
rep("    awaken: (n) => `최대 사용 시간 ${5 + 3 * n}초 · 가득 차는 데 35초`,", "    awaken: (n) => `최대 사용 시간 ${CH_MUT_TT[Math.min(5, n)]}초 · 가득 차는 데 40초`,   /* c484 */")
rep("mutate: ['', (n) => `${CH_WV('mutN', n)}개·${6 + 3 * n}초`]", "mutate: ['', (n) => `${CH_WV('mutN', n)}개·${CH_MUT_TT[Math.min(5, n)]}초`]")
rep("awaken: ['최대', (n) => `${5 + 3 * n}초`]", "awaken: ['최대', (n) => `${CH_MUT_TT[Math.min(5, n)]}초`]")
pathlib.Path('c484_patch.py').write_text('C484_R = ' + repr(R) + '\n')
