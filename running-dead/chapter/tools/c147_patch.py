# c147: 내가 조이스틱으로 움직이는 동안에는 사물(문·차·금고·길거리 사물)을 치지 않는다 — 동료는 그대로 가면서 친다
C147_R = [
 ("    if (CHAPTER && z.mode === 'free') chMoveHit(z, dt);", "    if (CHAPTER && z.mode === 'free' && !(z === me && touching)) chMoveHit(z, dt);   /* c147: 나는 조이스틱을 잡고 있는 동안 사물을 안 친다 */"),
]
