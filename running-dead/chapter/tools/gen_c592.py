import pathlib
s = pathlib.Path('c591.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
L = s.split('\n')
def line_starting(pfx):
    m = [l for l in L if l.startswith(pfx)]; assert len(m) == 1, (pfx, len(m)); return m[0]

# ── 저장: 성장 새로 시작 · 특성 기록
rep("    if (!o.u2) { for (const k of ['hp', 'ahp', 'atk']) o.up[k] = (o.up[k] || 0) * 2; o.u2 = 1; }",
    "    if (!o.u2) { for (const k of ['hp', 'ahp', 'atk']) o.up[k] = (o.up[k] || 0) * 2; o.u2 = 1; }\n    if (!o.u3) { o.up = { hp: 0, ahp: 0, atk: 0 }; o.tr = {}; o.u3 = 1; }   /* c592: 성장 개편 — 성장 기록 새로 시작 (유전자 · 클리어 기록은 그대로) */ o.tr = o.tr || {};")
# ── 성장 수치: 1포인트 = 유전자 10 · 10포인트(게이지 1개) = 표시 +1 = +0.5% · 특성 포인트 1
rep(line_starting("  const CH_UP_COST = 50;"), "  const CH_UP_COST = 10;   /* c592: 1포인트 = 유전자 10 */")
rep(line_starting("  const CH_UP_K = 0.0025;"), "  const CH_UP_K = 0.005;   /* c592: 게이지 1개(10포인트) = +0.5% */")
rep(line_starting("  const CH_UPK = { hp: 1 + CH_UP_K * CH_SV.up.hp,"),
    """  const chUpLv = (k) => Math.floor((CH_SV.up[k] || 0) / 10);   // c592: 채운 게이지 수 (표시 = 100 + 이것)
  const CH_UPK = { hp: 1 + CH_UP_K * chUpLv('hp'), ahp: 1 + CH_UP_K * chUpLv('ahp'), atk: 1 + CH_UP_K * chUpLv('atk') };
  // ── c592: 특성 — 게이지 1개 = 특성 포인트 1 · 단계마다 비용 2배 (1 · 2 · 4 …) · 최대 10단계
  const chTrait = (k) => (CH_SV.tr || {})[k] || 0;
  const chTrCost = (lv) => Math.pow(2, lv);   // lv → lv+1 비용
  const chTpAll = () => chUpLv('hp') + chUpLv('ahp') + chUpLv('atk');
  const chTpLeft = () => chTpAll() - Object.values(CH_SV.tr || {}).reduce((n, lv) => n + Math.pow(2, lv) - 1, 0);
  const chMutK = () => 1 + 0.02 * chTrait('mut');            // 돌연변이 — 괴물 추가분 +2%씩
  const chStrB = () => 0.15 * chTrait('str');                // 괴력 — 내 미는 힘 +0.15씩
  const chLureK = (c) => { const r0 = c.military ? 8 : c.police ? 5 : 0, r = Math.max(0, r0 - 0.2 * chTrait('cash')); return (10 - r) / 10; };   // 현금 — 유혹 저항력 (군인·저격수 8 · 경찰 5) −0.2씩
  let chTzHit = false;   // 테이저 피해 중 (흡혈 안 함)
  const CH_TRD = [
    { k: 'start', ic: '🧟', nm: '시작 동료', fx: (L) => { const n = Math.floor(L / 2), m = L % 2; return L ? '판 시작 시 ' + [n ? '일반 좀비 ' + n : '', m ? '새끼 좀비 1' : ''].filter(Boolean).join(' + ') : '없음'; } },
    { k: 'leech', ic: '🩸', nm: '흡혈', fx: (L) => `때릴 때마다 최대 체력의 ${(0.1 * L).toFixed(1)}% 회복` },
    { k: 'bat', ic: '⚡', nm: '배터리 강화', fx: (L) => L ? `테이저 피해 = 내 한 대의 ${Math.round((1 / 3 + 2 / 3 * (L - 1) / 9) * 100)}%` : '테이저 피해 없음' },
    { k: 'bomb', ic: '💥', nm: '자폭 스위치 폭발력 강화', fx: (L) => `자폭 범위 +${(0.17 * L).toFixed(2)}칸` },
    { k: 'cash', ic: '💵', nm: '현금 강화', fx: (L) => `유혹 저항력 -${(0.2 * L).toFixed(1)} · 군인 ${Math.round((10 - (8 - 0.2 * L)) * 10)}% · 경찰 ${Math.round((10 - (5 - 0.2 * L)) * 10)}%` },
    { k: 'mut', ic: '🦠', nm: '돌연변이', fx: (L) => `괴물 추가 능력 +${2 * L}% (스플래시 · 미는 힘 · 사거리)` },
    { k: 'str', ic: '🦾', nm: '괴력', fx: (L) => `내 미는 힘 +${(0.15 * L).toFixed(2)}` },
  ];""")
rep("CH_UPK.hp = 1 + CH_UP_K * CH_SV.up.hp; CH_UPK.ahp = 1 + CH_UP_K * CH_SV.up.ahp; CH_UPK.atk = 1 + CH_UP_K * CH_SV.up.atk;",
    "CH_UPK.hp = 1 + CH_UP_K * chUpLv('hp'); CH_UPK.ahp = 1 + CH_UP_K * chUpLv('ahp'); CH_UPK.atk = 1 + CH_UP_K * chUpLv('atk');   /* c592 */")
# ── 성장 창 (100부터 · 10칸 게이지 · 꽉 차면 팡) + 특성 창
i0 = s.index("    const upSheet = () => {"); i1 = s.index("    const tutSheet = () => {")
rep(s[i0:i1], r"""    const upSheet = (pop) => {   // c592: 성장 — 표시 100부터 · 클릭 1번 = 유전자 10 · 10칸 게이지가 꽉 차면 +1 (팡) · 특성 포인트 +1
      const row = (k, ic, nm) => { const v = CH_SV.up[k] || 0, lvN = Math.floor(v / 10), f = pop === k ? 10 : v % 10;
        return `<div class="ug${pop === k ? ' pop' : ''}" data-row="${k}"><div class="ic">${ic}</div><div class="tx"><div class="n1">${nm}</div><div class="gg">${Array.from({ length: 10 }, (_, i) => `<i class="${i < f ? 'on' : ''}"></i>`).join('')}</div></div><div class="pc">${100 + lvN}${pop === k ? '<b class="ufl">+1</b>' : ''}</div><button class="ub" data-up="${k}" ${CH_SV.genes < CH_UP_COST ? 'disabled' : ''}>+ ${CH_GENE_I(14)}${CH_UP_COST}</button></div>`; };
      openSheet(`<div class="hd"><div><div class="t2">성장</div></div><button class="x">✕</button></div><div class="ds">${CH_GENE_I(14)} <b>${CH_SV.genes}</b> · 특성 포인트 <b class="tpn">${chTpLeft()}</b></div>` +
        row('hp', '❤️', '내 체력') + row('ahp', '🧟', '동료 체력') + row('atk', '⚔️', '공격력') + `<div class="gh">10번 채우면 +1 (능력 +0.5%) · 특성 포인트 +1</div>`,
        (b) => { if (b.dataset.up && CH_SV.genes >= CH_UP_COST) { const k = b.dataset.up; CH_SV.genes -= CH_UP_COST; CH_SV.up[k] = (CH_SV.up[k] || 0) + 1; chSave(); { const m = ov.querySelector('.map'); draw(m ? m.scrollLeft : 0); }   /* c567: 지도는 보던 자리 그대로 */
          const full = CH_SV.up[k] % 10 === 0; upSheet(full ? k : null); if (full) { const sh0 = sheet; setTimeout(() => { if (sheet === sh0 && sheet && sheet.querySelector('.ug.pop')) upSheet(); }, 700); } } });
    };
    const trSheet = (pop) => {   // c592: 특성 — 특성 포인트로 올린다 · 단계마다 비용 2배 · 최대 10단계
      const tp = chTpLeft();
      const row = (D) => { const L = chTrait(D.k), mx = L >= 10, c = chTrCost(L);
        return `<div class="tr${pop === D.k ? ' pop' : ''}"><div class="ic">${D.ic}</div><div class="tx"><div class="n1">${D.nm} <span class="lv">${L}/10</span></div><div class="dt">${Array.from({ length: 10 }, (_, i) => `<i class="${i < L ? 'on' : ''}"></i>`).join('')}</div><div class="n2">${L ? '지금: ' + D.fx(L) : '아직 없음'}</div>${mx ? '' : `<div class="n3">다음: ${D.fx(L + 1)}</div>`}</div>${mx ? '<div class="mx">MAX</div>' : `<button class="ub" data-tr="${D.k}" ${tp < c ? 'disabled' : ''}>✦${c}</button>`}</div>`; };
      openSheet(`<div class="hd"><div><div class="t2">특성</div></div><button class="x">✕</button></div><div class="ds">특성 포인트 <b class="tpn">✦ ${tp}</b> · 성장 게이지 1개 = 1포인트</div>` + CH_TRD.map(row).join(''),
        (b) => { const k = b.dataset.tr; if (!k) return; const L = chTrait(k); if (L >= 10 || chTpLeft() < chTrCost(L)) return; CH_SV.tr[k] = L + 1; chSave(); { const m = ov.querySelector('.map'); draw(m ? m.scrollLeft : 0); } trSheet(k); });
      const t = sheet && sheet.querySelector('.sh'); if (t && pop) { const el = t.querySelector('.tr.pop'); if (el) el.scrollIntoView({ block: 'nearest' }); }
    };
""")
rep("<div class=\"bt\"><button class=\"ugb\" data-ug=\"1\"><span class=\"i\">💪</span>성장</button></div>",
    "<div class=\"bt\"><button class=\"ugb\" data-ug=\"1\"><span class=\"i\">💪</span>성장</button><button class=\"ugb trb\" data-trs=\"1\"><span class=\"i\">✦</span>특성${chTpLeft() > 0 ? `<span class=\"bd2\">${chTpLeft()}</span>` : ''}</button></div>")
rep("      if (b.dataset.ug) { upSheet(); return; }", "      if (b.dataset.ug) { upSheet(); return; }\n      if (b.dataset.trs) { trSheet(); return; }   /* c592 */")
rep("#outg .ub:disabled{background:#3a4250;color:#8a93a3}", """#outg .ub:disabled{background:#3a4250;color:#8a93a3}
#outg .bt{gap:10px}#outg .bt .ugb{width:min(170px,43vw);position:relative}#outg .ugb.trb{background:linear-gradient(#b36bff,#7a35d0);box-shadow:0 4px 0 #4a1d85}
#outg .ugb .bd2{position:absolute;top:-8px;right:-6px;min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:#ff3b5c;color:#fff;font-size:13px;line-height:22px;box-shadow:0 2px 4px rgba(0,0,0,.4)}
#outg .ug{position:relative}#outg .ug .gg{display:flex;gap:3px;margin-top:7px}#outg .ug .gg i{flex:1;height:9px;border-radius:3px;background:#11161e;border:1px solid #2a3442}#outg .ug .gg i.on{background:#7fe3ff;border-color:#7fe3ff;box-shadow:0 0 6px rgba(127,227,255,.6)}
#outg .ug.pop{animation:ugflash .7s ease-out}#outg .ug.pop .gg i{background:#fff;border-color:#fff;box-shadow:0 0 10px #7fe3ff}#outg .ug.pop .pc{animation:ugpop .7s ease-out}
#outg .ug .pc{position:relative}#outg .ug .ufl{position:absolute;right:0;top:-6px;font-size:18px;color:#ffe066;text-shadow:0 0 8px rgba(255,200,60,.8);animation:ugfl .8s ease-out forwards}
@keyframes ugpop{0%{transform:scale(1)}30%{transform:scale(1.7);color:#fff;text-shadow:0 0 16px #7fe3ff}100%{transform:scale(1)}}
@keyframes ugflash{0%{border-color:#2a3442}25%{border-color:#7fe3ff;box-shadow:0 0 18px rgba(127,227,255,.55)}100%{border-color:#2a3442}}
@keyframes ugfl{0%{opacity:0;transform:translateY(8px)}20%{opacity:1}100%{opacity:0;transform:translateY(-26px)}}
#outg .gh{font-size:12px;color:#8fa0b8;text-align:center;margin:4px 0 2px}
#outg .tr{display:flex;align-items:center;gap:12px;background:#1e2530;border:2px solid #2a3442;border-radius:14px;padding:12px;margin-bottom:8px}
#outg .tr .ic{width:46px;height:46px;border-radius:12px;background:#11161e;display:flex;align-items:center;justify-content:center;font-size:24px;flex:none}
#outg .tr .tx{flex:1;min-width:0}#outg .tr .n1{font-weight:900;font-size:15px}#outg .tr .lv{font-size:12px;color:#c79bff;font-weight:900;margin-left:4px}
#outg .tr .dt{display:flex;gap:3px;margin:6px 0 5px}#outg .tr .dt i{width:12px;height:12px;border-radius:50%;background:#11161e;border:1px solid #3a4250}#outg .tr .dt i.on{background:#c79bff;border-color:#c79bff;box-shadow:0 0 5px rgba(199,155,255,.7)}
#outg .tr .n2{font-size:12px;color:#d9e1ec;font-weight:700}#outg .tr .n3{font-size:12px;color:#8fa0b8;font-weight:700;margin-top:2px}
#outg .tr .ub{background:#7a35d0}#outg .tr .ub:disabled{background:#3a4250;color:#8a93a3}#outg .tr .mx{font-weight:900;color:#c79bff;font-size:14px}
#outg .tr.pop{animation:trflash .7s ease-out}@keyframes trflash{0%{border-color:#2a3442}25%{border-color:#c79bff;box-shadow:0 0 18px rgba(199,155,255,.6)}100%{border-color:#2a3442}}""")

# ── 특성 효과
rep("    if (CHAPTER && a && a.mini) dmg /= 3;", "    if (CHAPTER && a && a.mini) dmg /= 3;\n    if (CHAPTER && a === me && !a.splashing && !chTzHit && v && v.kind === 'citizen' && !v.robot && v.hp > 0 && chTrait('leech') && me.hp > 0) me.hp = Math.min(me.maxHp, me.hp + me.maxHp * 0.001 * chTrait('leech'));   /* c592: 흡혈 — 사람을 때릴 때마다 (한 번에 한 번) */")
rep("      for (const { c } of hit) { if (chRedR('taser'))", "      for (const { c } of hit) { if (chTaserDmg(c)) { zaps.push({ to: c, t: 0.45 }); continue; }   /* c592: 배터리 강화 — 맞는 순간 피해 (기계는 터진다) */ if (chRedR('taser'))")
rep("  function chSplitAcid(t) {", """  function chTaserDmg(c) {   // c592: 배터리 강화 — 내 한 대의 1/3(1단계) ~ 100%(10단계). 기계가 터지면 true
    const L = chTrait('bat'); if (!CHAPTER || !L || c.tank) return false;
    const dmg = zDamage(me) * (1 / 3 + 2 / 3 * (L - 1) / 9);
    if (c.drone) { chDroneDmg(c, dmg); return !!c.dead; }
    if (c.kind !== 'citizen' || c.hp <= 0) return false;
    chTzHit = true; landHit(me, c, dmg); chTzHit = false;
    if (c.robot && c.hp <= 0) { if (c.kind === 'citizen') chRobotDie(c); return true; }
    return false;
  }
  function chStartAllies() {   // c592: 시작 동료 — 일반 좀비 (단계 ÷ 2) · 홀수 단계면 새끼 좀비 1
    const L = chTrait('start'); if (!L) return; const n = Math.floor(L / 2), m = L % 2;
    for (let i = 0; i < n + m; i++) for (let t = 0; t < 40; t++) {
      const a = (i / (n + m)) * Math.PI * 2 + rand(-0.4, 0.4) + t * 0.3, r = 1.3 + t * 0.06, x = me.foot.x + Math.cos(a) * r, z = me.foot.z + Math.sin(a) * r;
      if (spaceOf(x, z) !== me.space || !freeSpot(x, z, null) || blocked(me.foot.x, me.foot.z, x, z)) continue;
      chExact = true; const c = chPut(x, z, { x0: x - 1, z0: z - 1, x1: x + 1, z1: z + 1 }, '', me.space); chExact = false;
      makeZombie(c); if (i >= n) { chMini(c); c.hp = c.maxHp = c.maxHp / 3; if (c.hpBar) c.hpDisp = c.hp; } break;
    }
  }
  function chSplitAcid(t) {""")
rep("    const R = 1.7 + 0.5 * chLvB('bomb');", "    const R = 1.7 + 0.5 * chLvB('bomb') + 0.17 * chTrait('bomb');   /* c592: 자폭 스위치 폭발력 강화 */")
rep("터지는 범위 ${+(1.7 + 0.5 * Math.min(5, n)).toFixed(1)}칸", "터지는 범위 ${+(1.7 + 0.5 * Math.min(5, n) + 0.17 * chTrait('bomb')).toFixed(1)}칸")
rep("bomb: ['', (n) => `${+(1.7 + 0.5 * Math.min(5, n)).toFixed(1)}칸·", "bomb: ['', (n) => `${+(1.7 + 0.5 * Math.min(5, n) + 0.17 * chTrait('bomb')).toFixed(1)}칸·")
rep("(c.military ? 0.2 : c.police ? 0.5 : 1)", "chLureK(c)   /* c592: 현금 강화 — 유혹 저항력 */")
rep("return (7 + (B && B.id === 'monster' ? 7 * B.r / 5 : 0))", "return (7 + (B && B.id === 'monster' ? 7 * B.r / 5 * chMutK() : 0) + (z === me ? chStrB() : 0))   /* c592: 돌연변이 · 괴력 */")
rep("return B && B.id === 'monster' ? 1 + B.r / 5 : 1;", "return B && B.id === 'monster' ? 1 + B.r / 5 * chMutK() : 1;   /* c592: 돌연변이 */")
rep("return B && B.id === 'monster' ? 0.5 + 0.25 * (B.r - 1) : 0;", "return B && B.id === 'monster' ? (0.5 + 0.25 * (B.r - 1)) * chMutK() : 0;   /* c592: 돌연변이 */")
rep("    me.force = CHAPTER ? CH_MY_FORCE : MY_FORCE;   /* c376: 평소 나 7 */", "    me.force = CHAPTER ? CH_MY_FORCE + chStrB() : MY_FORCE;   /* c592: 괴력 */   /* c376: 평소 나 7 */")
rep("me.mesh.scale.setScalar(1); me.force = CHAPTER ? CH_MY_FORCE : MY_FORCE;", "me.mesh.scale.setScalar(1); me.force = CHAPTER ? CH_MY_FORCE + chStrB() : MY_FORCE;   /* c592: 괴력 */")
rep("chStartW = { x: me.foot.x, z: me.foot.z, n: 1 + Math.floor(Math.random() * 2), tries: 0 };", "chStartW = { x: me.foot.x, z: me.foot.z, n: 1 + Math.floor(Math.random() * 2), tries: 0 }; if (CH_RUN) chStartAllies();   /* c592: 시작 동료 */")
pathlib.Path('c592_patch.py').write_text('C592_R = ' + repr(R) + '\n')
print(len(R))
