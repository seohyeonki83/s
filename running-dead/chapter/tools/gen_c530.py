import pathlib
s = pathlib.Path('c529.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("knockStep(z, dt); return; }   // c529: c527의 동료 쿨타임 변경은 되돌림 (동료는 그대로)",
    "if (CHAPTER && z.atkT > 0) z.atkT -= dt * (z.rage ? 1 + rageK() : 1); knockStep(z, dt); return; }   // c530: 다시 넣음 (c527) — 바리케이트를 밀다 몸이 살짝 밀려나는 순간에도 공격 쿨타임은 돈다")
pathlib.Path('c530_patch.py').write_text('C530_R = ' + repr(R) + '\n')
print(len(R))
