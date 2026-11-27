import pathlib
s = pathlib.Path('c525.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  function landHit(a, v, dmg = DAMAGE) {\n", "  function landHit(a, v, dmg = DAMAGE) {\n    if (CHAPTER && v && v.kind === 'citizen' && a && isZombie(a)) v.flT = clock;   // c526: 우리한테 맞으면 움찔 — 제 발로 가는 이동만 0에서 0.15초 동안 회복\n")
rep("b.foot.x += b.vel.x * dt * gk; b.foot.z += b.vel.y * dt * gk; }", "const fl = CH_FLINCH(b); b.foot.x += b.vel.x * dt * gk * fl; b.foot.z += b.vel.y * dt * gk * fl; }")
rep("  const wantV = new THREE.Vector2();", "  const wantV = new THREE.Vector2();\n  const CH_FLINCH_T = 0.15;   // c526: 맞은 순간 이동 0 → 0.15초 동안 원래대로 (밀림 · 넉백은 그대로, 공격도 그대로)\n  const CH_FLINCH = (b) => b.flT === undefined || b.kind !== 'citizen' || b.knockT > 0 || b.pushT > 0 ? 1 : Math.min(1, Math.max(0, (clock - b.flT) / CH_FLINCH_T));")
pathlib.Path('c526_patch.py').write_text('C526_R = ' + repr(R) + '\n')
print(len(R))
