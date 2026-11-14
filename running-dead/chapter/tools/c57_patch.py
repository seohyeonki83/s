# c57: 변이(각성)한 나는 덮치기 맨 끝 — 덮칠 동료가 있으면 나는 안 덮친다
C57_FN = r"""  // c57: 변이(각성)한 나는 덮치기 맨 끝 — 체력 0인 사람을 덮칠 동료가 있으면 나는 거리와 상관없이 그 사람을 안 노린다 (달려들지도, 덮치지도 않는다).
  //   덮칠 동료 = ① 그 사람을 찜하고 달려오는 동료 (나보다 멀리 있어도), ② 자기 덮침 거리 안에 있는 한가한 동료 (변이 동료 포함 — 다른 사람을 덮치려는 중이면 빼고), ③ 그 사람을 타겟으로 잡고 오는 동료
  //   그런 동료가 정말 없을 때만 내가 덮친다. 내 덮침 거리 안에 있는데 3초가 지나도록 아무도 안 덮치면 (찜한 동료가 막혀서 못 올 때) 그때도 내가 덮친다
  const CH_YIELD_MAX = 3;
  function chAllyTakes(t) {
    const c = t.chaser;
    if (c && c !== me && !c.dead && c.claim === t && c.mode === 'free') return true;
    for (const o of zombies) {
      if (o === me || o.mode !== 'free' || o.knockT > 0) continue;
      if (!o.mut && !o.recall && o.pick === t) return true;   // ③ 이 사람을 노리고 오는 중 (곧 찜한다 — 방금 체력이 0이 된 사람도 놓치지 않게)
      if (Math.hypot(t.foot.x - o.foot.x, t.foot.z - o.foot.z) > o.attack || !stillPounceable(o, t)) continue;
      if (o.pcand && o.pcand !== t && stillPounceable(o, o.pcand)) continue;   // 다른 사람을 덮치려는 중
      return true;
    }
    return false;
  }
  function chMeYield(t) {
    if (!chAllyTakes(t)) return false;
    if (t.space !== me.space || Math.hypot(t.foot.x - me.foot.x, t.foot.z - me.foot.z) > me.attack) return true;   // 내가 아직 못 덮치는 자리 — 그냥 양보 (시간은 안 센다)
    if (!(clock - t.yLast < 0.5)) t.yAt = clock;   // 양보하기 시작한 때 (0.5초 넘게 끊겼으면 새로 센다)
    t.yLast = clock;
    return clock - t.yAt < CH_YIELD_MAX;
  }
"""
C57_R = [
  # 나의 타겟 고르기·덮치기 가능·습격 모두 huntable을 거친다 — 변이한 나는 동료가 덮칠 사람(체력 0)을 타겟에서 뺀다
  ("(b.space === z.space || (linked(z.space, b.space) && zSeen(b)));   // v296: 다른 공간도 좀비 편이 보고 있으면",
   "(b.space === z.space || (linked(z.space, b.space) && zSeen(b))) && !(CHAPTER && z === me && me.mut && b.hp <= 0 && chMeYield(b));   /* c57: 변이한 나는 덮치기 맨 끝 */   // v296: 다른 공간도 좀비 편이 보고 있으면"),
  # 손을 떼기 직전에 빨간 테두리가 떠 있던 사람도 같은 규칙
  ("        const t = aimed && aimed.kind === 'citizen' && !aimed.marked && aimed.space === z.space ? aimed : ready;",
   "        const t = aimed && aimed.kind === 'citizen' && !aimed.marked && aimed.space === z.space && !(CHAPTER && z === me && me.mut && aimed.hp <= 0 && chMeYield(aimed)) ? aimed : ready;   /* c57 */"),
  ("  function pounceYield(z, t) {                // v416:", C57_FN + "  function pounceYield(z, t) {                // v416:"),
  ("zombify: makeZombie, slotOf, pop: () => chPop,", "zombify: makeZombie, slotOf, pop: () => chPop, awaken: awakenMe,"),
]
