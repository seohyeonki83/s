import pathlib, sys
base = sys.argv[1]
HOOK = r"""window.__rd = { 
  PREP: (nE, nA) => {
    for (const c of bodies.slice()) if (c.kind === 'citizen' && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 25) chBTgone(c);
    const T = ['police', 'soldier', 'attacker', 'guard', 'sniper']; let made = 0, al = 0; chNoMix = true;
    for (let k = 0; k < 6000 && (made < nE || al < nA); k++) {
      const ally = al < nA && (made >= nE || k % 2), a = Math.random() * 6.283, r = ally ? rand(1.2, 3) : rand(3.5, 8), x = me.foot.x + Math.cos(a) * r, z = me.foot.z + Math.sin(a) * r;
      if (spaceOf(x, z) || !freeSpot(x, z, null) || bodies.some((o) => Math.hypot(o.foot.x - x, o.foot.z - z) < 0.9) || fireBlocked(me.foot.x, me.foot.z, x, z)) continue;
      if (ally) { const c = addCitizen(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, ''); c.met = true; makeZombie(c); al++; }
      else { const c = addCitizen(x, z, { x0: x - 3, z0: z - 3, x1: x + 3, z1: z + 3 }, T[made % T.length]); c.met = true; c.disc = true; c.etT = true; made++; }
    }
    chNoMix = false; me.hp = me.maxHp = 1e9; return { made, al, space: me.space };
  },
  SET: (k, n, br) => { chETSet(k, n, br); for (const it of items) it.off = false; },
  USE: (k) => useItem(k),
  EN: () => { const E = bodies.filter((b) => b.etT); return { n: E.length, hp: Math.round(E.reduce((s, b) => s + Math.max(0, b.hp), 0)), stun: E.filter((b) => b.stunT > 0).length, goo: E.filter((b) => b.goo).length, lured: E.filter((b) => b.state === 'lured').length, down: E.filter((b) => !(b.hp > 0)).length }; },
  MUT: () => ({ allies: zombies.filter((z) => z !== me).length, mut: zombies.filter((z) => z !== me && z.mut).length, me: me.mut || null }),
  ME: () => [Math.round(me.foot.x), Math.round(me.foot.z), me.space ? 1 : 0],
  get me() { return me; },"""
for v in sys.argv[2:]:
    s = pathlib.Path(f'var/{base}{v}.html').read_text()
    s = s.replace("window.__rd = { get me() { return me; },", HOOK)
    pathlib.Path(f'var/{base}{v}C.html').write_text(s)
