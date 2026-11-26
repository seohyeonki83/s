import pathlib
s = pathlib.Path('c505.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1. 특공대 · 보스 부대는 안 잔다
rep("    return b.state === 'normal' && !(b.police && !b.post) && ", "    return b.state === 'normal' && !b.sfw && !b.tkU && !b.cvy && !(b.police && !b.post) && ")
# 2. 보스 드론은 드론 상한 8대에 안 센다
rep("i < N && chDrones.length < CH_DRONE_MAX; i++) {", "i < N && chDrones.filter((d) => !d.cvy).length < CH_DRONE_MAX; i++) {   /* c506: 보스 드론 제외 */")
# 3. 보스 공격력도 스테이지 강화 (장갑차 · 불도저 기관총 — 밀기는 c505에서 이미)
rep("(a.kind === 'citizen' || a.kind === 'drone')) dmg *= CH_SK;", "(a.kind === 'citizen' || a.kind === 'drone' || a.kind === 'tank')) dmg *= CH_SK;   /* c506: 보스 공격도 */")
rep("if (chDroneOn && !chDrones.some((d) => !d.dead) && (chDroneT += dt)", "if (chDroneOn && !chDrones.some((d) => !d.dead && !d.cvy) && (chDroneT += dt)")   # c506: 보스 드론이 살아 있어도 주기는 흐른다
pathlib.Path('c506_patch.py').write_text('C506_R = ' + repr(R) + '\n')
print(len(R))
