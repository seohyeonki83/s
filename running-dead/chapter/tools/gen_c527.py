import pathlib
s = pathlib.Path('c526.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("if (z.mut && z !== me && z.mode === 'free') { mutStep(z, dt); return; }", "if (z.mut && z !== me && z.mode === 'free') { mutStep(z, dt); if (CHAPTER && z.mut === 'armor') chMoveHit(z, dt); return; }   /* c527: 덩치도 가는 길에 몸에 닿은 바리케이트 · 차 · 문 · 사물을 가면서 친다 (밀기만 하던 것) */")
rep("    if (z.knockT > 0) { if (z.bombing) chBombIcon(z); knockStep(z, dt); return; }", "    if (z.knockT > 0) { if (z.bombing) chBombIcon(z); if (CHAPTER && z.atkT > 0) z.atkT -= dt * (z.rage ? 1 + rageK() : 1); knockStep(z, dt); return; }   // c527: 바리케이트를 밀다 튕기는 동안에도 공격 쿨타임은 돈다 (밀기만 하고 못 치던 것)")
a = [l for l in s.split('\n') if "c523: 수치 대신 위험도 해골" in l][0]
rep(a, "      /* c527: 위험도 칸 뺌 */")
pathlib.Path('c527_patch.py').write_text('C527_R = ' + repr(R) + '\n')
print(len(R))
