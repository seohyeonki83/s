# c145: 나만 — 문을 치는 거리 1.5배 · 문의 우선순위 = 하양과 같다 (하양보다 문이 가까우면 문을 친다) · 못 부수던 길거리 사물(동상·분수·굴착기·간이 화장실 …)도 부술 수 있다
C145_R = [
 ("function chObjLim(z, o) { return (o.type === 'door' || o.type === 'car') && z !== me && hotObj(o) ? 4 * MELEE : chReach(z); }", "function chObjLim(z, o) { return (o.type === 'door' || o.type === 'car') && z !== me && hotObj(o) ? 4 * MELEE : z === me && o.type === 'door' ? chReach(z) * 1.5 : chReach(z); }   /* c145: 나는 문을 1.5배 거리에서 친다 */"),
 ("const o = nearObj(z); if (o && objGap(o, z) <= chReach(z)) return o;", "const o = nearObj(z); if (o && objGap(o, z) <= (z === me ? chObjLim(z, o) : chReach(z))) return o;"),
 ("        let ob = forced || (!t && !noObj && !(CHAPTER && go) ? nearObj(z) : null);\n", "        let ob = forced || (!t && !noObj && !(CHAPTER && go) ? nearObj(z) : null);\n        if (CHAPTER && z === me && !ob && !t && go && go.kind === 'citizen' && chTier(go) === 0 && !(z.objOff > clock)) { const d = nearObj(z); if (d && d.type === 'door') ob = d; }   // c145: 나 — 문은 하양과 같은 순위 (노릴 사람이 하양이면 더 가까운 쪽을 친다)\n"),
 ("      if (b.inv) b.hp = b.maxHp = 1e12;\n", "      /* c145: 박힌 큰 사물도 부술 수 있다 (체력 = 9대짜리 사물). 차는 전처럼 막힌다 */\n"),
 ("if (!S && p.out && !p.sleep && !p.inv) chOutGridAdd(p);", "if (!S && p.out && !p.sleep) chOutGridAdd(p);"),
]
