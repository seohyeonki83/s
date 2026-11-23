# c407: 본 맵 테스트(둘러보기 — 속도 3배 · 이동만 · 적이 나를 못 본다) + 미니맵 원형 · 확대 되돌림
src = open('c406.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# ── 1. 본 맵 테스트 ('w') — 맵은 본 맵과 같은 방식으로 새로 만든다 ──
rep("['m', '본 맵', '그룹 9개 · 단락 36개 · 시작할 때마다 새로']", "['m', '본 맵', '그룹 9개 · 단락 36개 · 시작할 때마다 새로'], ['w', '본 맵 테스트', '둘러보기 · 속도 3배 · 이동만 · 적이 나를 못 봄']")
rep("  const CH_MAIN = CH_PICK === 'm', CH_BASE = CH_PICK === 'p',", "  const CH_TOUR = CH_PICK === 'w', CH_MAIN = CH_PICK === 'm' || CH_TOUR, CH_BASE = CH_PICK === 'p',   /* c407: 본 맵 테스트 = 본 맵 + 둘러보기 */")
rep("CH_TUT ? '튜토리얼 1' : CH_MAIN ? '본 맵' : CH_BASE", "CH_TUT ? '튜토리얼 1' : CH_TOUR ? '본 맵 테스트' : CH_MAIN ? '본 맵' : CH_BASE")
rep("    me.speed = MY_SPEED;                     // 이동 속도 (동료와 같다)", "    me.speed = MY_SPEED * (CH_TOUR ? 3 : 1);   /* c407: 본 맵 테스트는 3배 */                     // 이동 속도 (동료와 같다)")
rep("    if (CHAPTER && z.bombing) { chBombStep(z, dt); return; }   // c272: 자폭 돌진 중\n",
    "    if (CHAPTER && z.bombing) { chBombStep(z, dt); return; }   // c272: 자폭 돌진 중\n"
    "    if (CH_TOUR && z === me) { const on = pid !== null; steer(z.vel, wantV.set(on ? move.x * z.speed : 0, on ? move.y * z.speed : 0), ACCEL * 3 * dt); z.pick = null; z.aim = null; z.engaging = null; return; }   // c407: 본 맵 테스트 — 나는 이동만 한다 (공격·덮치기·물기 없음)\n")
rep("  const sees = (c, z) => z && isZombie(z) && (z.space === c.space", "  const sees = (c, z) => z && isZombie(z) && !(CH_TOUR && z === me) && (z.space === c.space")   # 본 맵 테스트: 사람은 나를 못 본다
rep("    for (const z of nearIn(zCells, c.foot.x, c.foot.z, c.sight, seBuf)) {   // 둘레 칸의 좀비만 (v177)\n      if (!isZombie(z)) continue;", "    for (const z of nearIn(zCells, c.foot.x, c.foot.z, c.sight, seBuf)) {   // 둘레 칸의 좀비만 (v177)\n      if (!isZombie(z) || (CH_TOUR && z === me)) continue;   /* c407: 본 맵 테스트 — 나를 못 본다 */")
rep("for (const z of nearIn(zCells, c.foot.x, c.foot.z, ER, evBuf)) if (isZombie(z) && z.space === c.space", "for (const z of nearIn(zCells, c.foot.x, c.foot.z, ER, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && z.space === c.space")
rep("for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && z.space === c.space", "for (const z of nearIn(zCells, c.foot.x, c.foot.z, er, evBuf)) if (isZombie(z) && !(CH_TOUR && z === me) && z.space === c.space")
rep("      if (z.space || !isZombie(z) || (z.trHit === car && z.trHitT > clock)) continue;", "      if (z.space || !isZombie(z) || (CH_TOUR && z === me) || (z.trHit === car && z.trHitT > clock)) continue;")
rep("    if (CH_BT && z === me) { me.hp = me.maxHp; return; }   // c166: 보스 테스트 — 나는 무적", "    if ((CH_BT || CH_TOUR) && z === me) { me.hp = me.maxHp; return; }   // c166: 보스 테스트 — 나는 무적 · c407: 본 맵 테스트도")
rep("    if (CHAPTER) chSecTick(dt);   // c405: 내가 있는 단락만 돌린다\n", "    if (CHAPTER) chSecTick(dt);   // c405: 내가 있는 단락만 돌린다\n    if (CH_TOUR && isZombie(me)) me.hp = me.maxHp;   // c407: 본 맵 테스트 — 체력은 늘 가득\n")
rep("  function chEmptySlots() {\n", "  function chEmptySlots() {\n    if (CH_TOUR) return;   // c407: 본 맵 테스트 — 무기 칸 없음\n")
# ── 2. 미니맵: 확대를 되돌리고 (전에 지도 전체를 비추던 배율 그대로), 모양은 원 ──
rep("전에 지도 전체를 비추던 배율보다 1.25배 확대 = 비추는 폭이 80%.", "배율은 전에 지도 전체를 비추던 그대로 (c407: 1.25배 확대를 되돌렸다 — 20% 더 넓게 비춘다) · 모양은 원.")
rep("const MM_SIDE = 88, MM_ZOOM = 1.25,", "const MM_SIDE = 88, MM_ZOOM = 1,")
rep("  mmEl.style.width = MM_SW + 'px'; mmEl.style.height = MM_SH + 'px'; if (CH_TUT) mmEl.style.display = 'none';",
    "  mmEl.style.width = MM_SW + 'px'; mmEl.style.height = MM_SH + 'px'; if (CHAPTER) { mmEl.style.borderRadius = '50%'; mmEl.style.outline = 'none'; mmEl.style.boxShadow = '0 0 0 1px rgba(255, 255, 255, 0.25)'; }   /* c407: 원 (테두리는 그림자로 — 둥글게 따라간다) */ if (CH_TUT) mmEl.style.display = 'none';")
rep("S.transform = ''; S.zIndex = ''; S.borderRadius = ''; S.boxShadow = '';", "S.transform = ''; S.zIndex = ''; S.borderRadius = CHAPTER ? '50%' : ''; S.boxShadow = CHAPTER ? '0 0 0 1px rgba(255, 255, 255, 0.25)' : ''; S.outline = CHAPTER ? 'none' : '';")
rep("S.zIndex = '15'; S.borderRadius = '12px'; S.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.65)';", "S.zIndex = '15'; S.borderRadius = '12px'; S.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.65)'; S.outline = '';")
open('c407_patch.py', 'w').write("# c407: 본 맵 테스트(둘러보기) + 미니맵 원형 · 확대 되돌림\nC407_R = " + repr(R) + "\n")
print(len(R), 'entries')
