import pathlib
s = pathlib.Path('c594.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 옛 돌연변이(괴물 추가분) 끄기 — 특성 이름은 그대로, 효과를 새로
rep("  const chMutK = () => 1 + 0.01 * chTrait('mut');   /* c594: 20단계 */", "  const chMutK = () => 1;   /* c595: 옛 돌연변이(괴물 추가분) 없앰 — 새 돌연변이 = 덩치 가시 몸 · 히드라 회피 */\n  const chSpkIv = () => 1.5 - (chTrait('mut') - 1) / 19;   // c595: 덩치 가시 몸 간격 1.5초 → 0.5초\n  const chDodgeP = () => 0.025 * chTrait('mut');            // c595: 히드라 회피 2.5% → 50%")
rep("fx: (L) => `괴물 추가 능력 +${L}% (스플래시 · 미는 힘 · 사거리)` }", "fx: (L) => `덩치: 닿은 적 ${(1.5 - (L - 1) / 19).toFixed(2)}초마다 피해 1 · 히드라: 회피 ${(2.5 * L).toFixed(1)}%` }")
# 회피 — 맞을 때 확률로 피해 · 넉백 없이 MISS
rep("  function landHit(a, v, dmg = DAMAGE) {\n", "  function landHit(a, v, dmg = DAMAGE) {\n    if (CHAPTER && v && v.mut === 'hydra' && isZombie(v) && chTrait('mut') && a && !isZombie(a) && Math.random() < chDodgeP()) { v.missAt = clock; chMissPop(v); return; }   /* c595: 돌연변이 — 히드라 회피 */\n")
rep("  function giveKnock(z, kx, kz, v, T) {       // 방향(kx, kz), 처음 속도 v, 시간 T — 내가 흡수복을 입었으면 깎는다. 밀렸으면 true\n",
    "  function giveKnock(z, kx, kz, v, T) {       // 방향(kx, kz), 처음 속도 v, 시간 T — 내가 흡수복을 입었으면 깎는다. 밀렸으면 true\n    if (z && z.missAt === clock) return false;   // c595: 회피한 공격은 넉백도 없다\n")
# 가시 몸 + MISS 글자
rep("  function gooTick(dt) {\n", r"""  const chMissTex = (() => { const cv = document.createElement('canvas'); cv.width = 160; cv.height = 64; const g = cv.getContext('2d'); g.font = 'italic 900 46px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineWidth = 9; g.strokeStyle = 'rgba(0,0,0,0.8)'; g.strokeText('MISS', 80, 34); g.fillStyle = '#ffffff'; g.fillText('MISS', 80, 34); return new THREE.CanvasTexture(cv); })();
  function chMissPop(v) {   // c595: 회피 — 'MISS'가 떠올랐다 사라진다
    const f = puff(v.foot.x, 1.5, v.foot.z, 0xffffff, 0.5, 0.5, 0.75, 0, 0.9, 0, 1); f.s.material.map = chMissTex; f.s.scale.set(1.9, 0.76, 1); f.fixedScale = true; f.late = true; f.s.renderOrder = UI_ME + 90;
  }
  function chSpikeTick(dt) {   // c595: 돌연변이 — 덩치(나 · 동료 · 맵 변이) 몸에 닿은 적은 간격마다 피해 1 (도트와 같은 셈 · 공격력 성장)
    if (!chTrait('mut')) return; const iv = chSpkIv(), d = 1 * HPK * CH_UPK.atk;
    for (const z of zombies) {
      if (z.mut !== 'armor' || !isZombie(z) || z.dead) continue;
      if ((z.spkT = (z.spkT || 0) + dt) < iv) continue; z.spkT -= iv;
      const R0 = (z.r || BODY) + 0.12;
      for (const c of bodies) {
        if (c.kind !== 'citizen' || c.hp <= 0 || c.space !== z.space) continue;
        const dx = c.foot.x - z.foot.x, dz = c.foot.z - z.foot.z; if (Math.abs(dx) > 3 || Math.abs(dz) > 3 || Math.hypot(dx, dz) > R0 + (c.r || BODY)) continue;
        c.hp = Math.max(0, c.hp - d);
        if (c.hp <= 0 && !c.police && !c.robot && c.state !== 'held') enterPanic(c, null, true);
        if (c.mesh.visible) chDotPop(c.foot.x + 0.6, c.foot.z, Math.max(1, d / HPK));   // 화면에는 1
      }
    }
  }
  function gooTick(dt) {
""")
rep("    gooTick(dt); if (CHAPTER) chAcidTick(dt);", "    gooTick(dt); if (CHAPTER) { chAcidTick(dt); chSpikeTick(dt); }   /* c595 */")
pathlib.Path('c595_patch.py').write_text('C595_R = ' + repr(R) + '\n')
print(len(R))
