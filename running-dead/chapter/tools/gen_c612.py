import pathlib
s = pathlib.Path('c611.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("dropPickup(pool[Math.floor(Math.random() * pool.length)], x, z, sp); } }   // c505: 저격수 → 장비 하나",
    "dropPickup(pool[Math.floor(Math.random() * pool.length)], x, z, sp); pickups[pickups.length - 1].snip = true; } }   /* c612: 저격수 장비는 거리·벽 상관없이 나한테 날아온다 */   // c505: 저격수 → 장비 하나")
rep("if (!p.mag && d <= CH_MAG_R * (MELEE + Math.max(0, (me.r || BODY) - BODY)) && (chSameSp(me.space, p.space) || !fireBlocked(me.foot.x, me.foot.z, p.x, p.z))) {", "if (!p.mag && (p.snip || (d <= CH_MAG_R * (MELEE + Math.max(0, (me.r || BODY) - BODY)) && (chSameSp(me.space, p.space) || !fireBlocked(me.foot.x, me.foot.z, p.x, p.z))))) {   /* c612: 저격수 장비는 바로 */")
pathlib.Path('c612_patch.py').write_text('C612_R = ' + repr(R) + '\n')
print(len(R))
