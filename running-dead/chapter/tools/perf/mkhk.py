import pathlib, sys
HOOK = r"""window.__rd = {
  HK: () => {
    const out = { maxHp: {}, frac: {}, abs: {} };
    const at = (dx, dz) => [me.foot.x + dx, me.foot.z + dz];
    const mk = (t, dx) => { const [x, z] = at(dx, 2); chNoMix = true; const c = addCitizen(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, t === 'red' ? 'attacker' : t === 'sg' ? 'police' : t === 'robot' ? 'soldier' : t); chNoMix = false; if (t === 'red') chVig(c); if (t === 'sg') chMakeSg(c); if (t === 'robot') chMakeRobot(c); c.met = true; c.disc = true; return c; };
    const ally = (dx) => { const [x, z] = at(dx, -2); const c = addCitizen(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, ''); c.met = true; makeZombie(c); return c; };
    out.maxHp.me = me.maxHp;
    const A = ally(0), AR = ally(1.5); mutate(AR, 'armor'); const AH = ally(3); mutate(AH, 'hydra');
    out.maxHp.ally = A.maxHp; out.maxHp.armor = AR.maxHp; out.maxHp.hydra = AH.maxHp;
    const T = {}; for (const t of ['guard', 'attacker', 'red', 'police', 'sg', 'sniper', 'soldier', 'robot']) { T[t] = mk(t, Object.keys(T).length * 1.3 - 5); out.maxHp[t] = T[t].maxHp; }
    out.maxHp.car = (cars.find((c) => c.obj && !c.wall) || {}).obj?.maxHp; out.maxHp.door = (objs.find((o) => o.type === 'door') || {}).maxHp; out.maxHp.safe = SAFE_HP; out.maxHp.droneHP = CH_DRONE_HP; out.maxHp.cap = CH_HP_CAP;
    const fr = (v, fn) => { v.hp = v.maxHp; const h0 = v.hp; fn(); const d = h0 - v.hp; v.hp = v.maxHp; return { d: +d.toFixed(3), f: +(d / v.maxHp).toFixed(5) }; };
    const P = T.police;
    out.frac.me_vs_police = fr(P, () => landHit(me, P, zDamage(me)));
    out.frac.ally_vs_police = fr(P, () => landHit(A, P, zDamage(A)));
    out.frac.armor_vs_police = fr(P, () => landHit(AR, P, zDamage(AR)));
    out.frac.org_vs_ally = fr(A, () => landHit(T.attacker, A, CH_DMG_ORG));
    out.frac.red_vs_ally = fr(A, () => landHit(T.red, A, CH_DMG_RED));
    out.frac.yel_vs_ally = fr(A, () => landHit(T.guard, A, CH_DMG_YEL));
    out.frac.police_vs_ally = fr(A, () => shoot(P, A));
    out.frac.police_vs_me = fr(me, () => shoot(P, me));
    out.frac.sniper_vs_me = fr(me, () => shoot(T.sniper, me));
    out.frac.soldier_vs_ally = fr(A, () => shoot(T.soldier, A));
    out.frac.sg_vs_ally = fr(A, () => landHit(T.sg, A, CH_DMG_PO / 5));
    out.frac.drone_vs_me = fr(me, () => landHit({ kind: 'drone', drone: true, foot: me.foot }, me, CH_DRONE_DMG / 3));
    out.frac.goo_vs_police = fr(P, () => { gooOn(P); P.gooT = 0.999; gooTick(0.002); });
    out.frac.acid_vs_police = fr(P, () => { chAcidOn(P, 3); P.acidT = 0.999; chAcidTick(0.002); });
    out.abs.acidHit = chAcidHit(); out.abs.carHit = CAR_HIT_DMG;
    return out;
  },
  get me() { return me; },"""
for f in sys.argv[1:]:
    p = pathlib.Path(f'var/{f}.html'); s = p.read_text()
    s = s.replace("window.__rd = { get me() { return me; },", HOOK)
    pathlib.Path(f'var/{f}H.html').write_text(s)
