# c308: 겹쳐 놓은 튜토리얼 바리케이트끼리는 서로 밀어내지 않는다 — 밀려난 순간의 빈자리로 좀비가 빠져나가던 문제
C308_R = [("      if ((A.wall && B.state !== 'parked') || (B.wall && A.state !== 'parked')) continue;   // c59: 달리는 경찰차·군인차는 건널목 바리케이트를 그냥 지나간다",
  "      if ((A.wall && B.state !== 'parked') || (B.wall && A.state !== 'parked')) continue;   // c59: 달리는 경찰차·군인차는 건널목 바리케이트를 그냥 지나간다\n      if (A.tutX !== undefined || B.tutX !== undefined) continue;   // c308: 튜토리얼 바리케이트는 제자리 고정 — 서로·다른 차와 밀어내지 않는다")]
C308_R.append(("sh = isZombie(b) && !car.wreck   /* c109: 바리케이트 — 제 힘 그대로 */ ?", "sh = isZombie(b) && !car.wreck && car.tutX === undefined   /* c308: 튜토리얼 바리케이트는 좀비도 못 민다 */   /* c109: 바리케이트 — 제 힘 그대로 */ ?"))
