# c408: 깨어 있는 사람은 다른 단락에 있어도 빼지 않는다 — 전 규칙(c54)대로 스스로 다시 잠든 사람만 뺀다
#   c405는 '할 일 없는' 깨어 있는 사람도 뺐는데, 그러면 한 번 싸운 이동 경찰(출동 경찰)이 다음 사건 호출을 못 받아 추격이 줄었다
src = open('c407.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  const chBodyDormable = (b) => b.kind === 'safe' ? !(b.knockT > 0) : b.kind === 'citizen' && (b.sleep || chSecIdle(b));",
    "  const chBodyDormable = (b) => b.kind === 'safe' ? !(b.knockT > 0) : b.kind === 'citizen' && !!b.sleep;   /* c408: 자고 있는 사람만 — 깨어 있는 사람(이동 경찰·출동 경찰 포함)은 전 규칙대로 스스로 다시 잠들 때까지 그대로 돈다. 이동 경찰은 한 번 깨면 안 자니까 끝까지 사건 호출을 받는다 */")
rep("  //   빼지 않는 것: 나·동료 · 싸우거나 쫓거나 도망치는 중인 사람 · 사건 자리로 가는 출동 경찰 · 달리는 경찰차 · 보스 · 드론. 다시 채우기·경보·출동 시계는 그대로 돈다",
    "  //   빼지 않는 것: 나·동료 · 깨어 있는 사람 전부 (c408 — 자고 있는 사람만 뺀다) · 달리는 경찰차 · 사람이 다시 탈 차 · 보스 · 드론. 다시 채우기·경보·출동 시계는 그대로 돈다")
open('c408_patch.py', 'w').write("# c408: 깨어 있는 사람은 빼지 않는다 (출동 경찰 추격 되돌림)\nC408_R = " + repr(R) + "\n")
print(len(R), 'entries')
