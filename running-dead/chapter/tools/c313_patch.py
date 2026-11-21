# c313: 히드라 속도 = 일반 좀비와 같음 (큰 맵도) · 덩치는 그대로 빠름
C313_R = [
  ("* (me && me.mut ? MUT_SPEED : 1);", "* (me && me.mut === 'armor' ? MUT_SPEED : 1);   /* c313: 히드라는 일반 속도 */"),
  ("    if (key === 'leg') for (const b of bodies) if (isZombie(b)) b.speed = b === me ? meSpeed() : SPEED * legK() * (b.mut ? MUT_SPEED : 1);", "    if (key === 'leg') for (const b of bodies) if (isZombie(b)) b.speed = b === me ? meSpeed() : SPEED * legK() * (b.mut === 'armor' ? MUT_SPEED : 1);   /* c313 */"),
  ("    z.speed = SPEED * legK() * MUT_SPEED;      // v304: 변이 좀비 이동 속도 +25% (덩치·히드라 둘 다)", "    z.speed = SPEED * legK() * (type === 'armor' ? MUT_SPEED : 1);      // v304: 변이 좀비 이동 속도 +25% — c313: 덩치만 (히드라는 일반 좀비와 같다)"),
  ("    if (kind === 'shoes') for (const b of bodies) if (isZombie(b)) b.speed = b === me ? meSpeed() : SPEED * legK() * (b.mut ? MUT_SPEED : 1);", "    if (kind === 'shoes') for (const b of bodies) if (isZombie(b)) b.speed = b === me ? meSpeed() : SPEED * legK() * (b.mut === 'armor' ? MUT_SPEED : 1);   /* c313 */"),
]
