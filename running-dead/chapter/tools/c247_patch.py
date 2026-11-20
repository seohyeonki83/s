# c247: 랜드마크 사수 경찰차 — 문이 부서질 때가 아니라 좀비(나·동료)가 그 건물 안으로 들어오는 순간 출동 (두 번째 출동은 그대로)
C247_R = [
 ("""    for (const o of objs) {                   // ① 랜드마크 사수 — c54: 바깥문(정문·쪽문·방 쪽문)이 부서지면 한 번. 방문(안쪽 문)은 아니다
      if (o.type !== 'door' || !o.dead || (o.B.parent && !o.L.ext)) continue;
      const B = o.B.parent || o.B;
      if (!CH_LM.has(B.type) || B.called) continue;
      B.called = 1; B.gate = o.L; chGuardCar(B);
    }""",
  """    for (const z of zombies) {                // ① 랜드마크 사수 — c247: 좀비가 그 건물(방 포함) 안에 들어오는 순간 한 번
      const S = z.space; if (!S) continue;
      const B = S.parent || S;
      if (B.called || !CH_LM.has(B.type)) continue;
      let g = null, gd = Infinity;               // 차가 갈 자리 = 그 좀비와 가장 가까운 출입구 (뚫린 벽·열린 문·잠긴 문)
      for (const D of B.doors.concat(B.locks)) { const d = Math.hypot(D.cx - z.foot.x, D.cz - z.foot.z); if (d < gd) { gd = d; g = D; } }
      B.called = 1; B.gate = g || B.front; if (B.gate) chGuardCar(B);
    }"""),
]
