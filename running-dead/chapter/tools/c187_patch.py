# c187: 나 — 금고 · 문을 치기 시작하면 사람 타겟처럼 붙잡는다 (다른 적이 와도 안 옮겨 간다. 저격수만 예외). 처음 고를 때는 겉면까지 거리로 사람과 견준다
C187_R = [
 ("        if (ob && (forced || !go || objGap(ob, z) < Math.hypot(go.foot.x - z.foot.x, go.foot.z - z.foot.z) - RADIUS) && (!sf || objGap(ob, z) < Math.hypot(sf.foot.x - z.foot.x, sf.foot.z - z.foot.z) - sf.r)) fightObj(z, ob, dt);",
  "        const meLk = CHAPTER && z === me && !(go && go.sniper) ? z.meLock : null;   // c187: 나 — 치던 금고·문은 붙잡는다 (저격수만 예외)\n"
  "        if (ob && (forced || meLk === ob || !go || objGap(ob, z) < Math.hypot(go.foot.x - z.foot.x, go.foot.z - z.foot.z) - RADIUS) && (meLk === ob || !sf || objGap(ob, z) < Math.hypot(sf.foot.x - z.foot.x, sf.foot.z - z.foot.z) - sf.r)) { fightObj(z, ob, dt); if (CHAPTER && z === me) z.meLock = ob.type === 'door' ? ob : null; }"),
 ("        else if (sf && (!go || Math.hypot(sf.foot.x - z.foot.x, sf.foot.z - z.foot.z) < Math.hypot(go.foot.x - z.foot.x, go.foot.z - z.foot.z))) fight(z, sf, dt);",
  "        else if (sf && (meLk === sf || !go || Math.hypot(sf.foot.x - z.foot.x, sf.foot.z - z.foot.z) - (CHAPTER && z === me ? sf.r : 0) < Math.hypot(go.foot.x - z.foot.x, go.foot.z - z.foot.z) - (CHAPTER && z === me ? RADIUS : 0))) { fight(z, sf, dt); if (CHAPTER && z === me) z.meLock = sf; }   /* c187: 겉면까지 거리로 견준다 · 붙잡는다 */"),
]
