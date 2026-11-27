import pathlib
s = pathlib.Path('c575.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("say: '가까이 다가와 부채꼴로 쏘고<br>맞은 좀비를 밀어냅니다.' }", "say: '샷건을 든 경찰입니다.' }   /* c576: 짧게 */")
rep("say: '단단한 로봇입니다.<br>감염되지 않고 부서지면 터집니다.' }", "say: '인간이 다루는 튼튼한 로봇입니다.' }")
rep("say: '건널목을 지키는 고정 포대입니다.<br>한 번에 8발 · 부서지면 터집니다.' }", "say: '건널목을 지키는 고정 포대입니다.' }")
rep("say: '하늘에서 기관총을 쏩니다.' }", "say: '하늘에서 총을 쏘는 드론입니다.' }")
rep("say: CHAPTER ? '총을 쏘는 경찰입니다.' : '건법 씀' }", "say: CHAPTER ? '총을 든 경찰입니다.<br>멀리서 쏩니다.' : '건법 씀' }")
rep("name: '군인', say: '훈련받은 군인입니다.' }", "name: '군인', say: '훈련된 인간입니다.' }")
rep("say: CHAPTER ? '멀리서 강하게 쏘고 밀어냅니다.<br>제거 1순위' : '발빠른 저격수<br>제거 1순위' }", "say: CHAPTER ? '매우 위험한 인간입니다.<br>제거 1순위' : '발빠른 저격수<br>제거 1순위' }")
rep("        if (SV[k] || !(iSee(b) || zSeen(b))) continue;", "        if (SV[k] || k === 'red' || k === 'attacker' || k === 'guard' || !(iSee(b) || zSeen(b))) continue;   /* c576: 빨강 · 주황 · 노랑은 소개 안 함 */")
pathlib.Path('c576_patch.py').write_text('C576_R = ' + repr(R) + '\n')
print(len(R))
