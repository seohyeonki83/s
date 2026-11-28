import pathlib
s = pathlib.Path('c580.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1) 섞임 시작 = 터렛 단계 (쉬움 4 · 보통 3 · 어려움 2) — 샷건 · 사각 같이
rep("const CH_MIXL = CH_RUN ? { e: 5, n: 4, h: 3 }[CH_DIF] : 5;", "const CH_MIXL = CH_RUN ? { e: 4, n: 3, h: 2 }[CH_DIF] : 5;   /* c581: 샷건 · 사각 섞임 + 건널목 터렛 + 출동 25% — 쉬움 팬데믹 · 보통 비상 · 어려움 경계 */")
rep("const CH_MIX_T = { e: 5, n: 4, h: 3 };", "const CH_MIX_T = { e: 4, n: 3, h: 2 };")
# 2) 30% 교체 (확률이 아니라 쌓아서 — 정확히 30%)
rep("    if (CHAPTER && chAL >= CH_MIXL - 1 && !chNoMix)   /* c572: 경찰 → 샷건 섞임은 한 단계 먼저 (쉬움 팬데믹 · 보통 비상 · 어려움 경계) */ { if (type === 'police' && ++chPolN % 3 === 0) chMakeSg(c);   /* c578: 5명 중 1 → 3명 중 1 */ else if (type === 'soldier' && chAL >= CH_MIXL && ++chSolN % 3 === 0) chMakeRobot(c); }",
    "    if (CHAPTER && chAL >= CH_MIXL && !chNoMix)   /* c581: 경찰 30% → 샷건 · 군인 30% → 사각 (같은 단계부터) */ { if (type === 'police' && (chPolN += CH_MIX_K) >= 1) { chPolN -= 1; chMakeSg(c); } else if (type === 'soldier' && (chSolN += CH_MIX_K) >= 1) { chSolN -= 1; chMakeRobot(c); } }")
# 3) 출동 경찰 · 특공대 군인 25% (섞임 시작부터 · 보스 빼고)
rep("  const CH_DISP_N = ", """  const CH_MORE = 1.25, CH_MIX_K = 0.3;   /* c581: 섞임 시작부터 출동 경찰 · 특공대 군인 25% 늘림 · 그중 30% 교체 */
  function chSfMore(groups) {   // c581: 무리들의 군인 수 합을 1.25배로 — 늘어난 군인은 무리마다 돌아가며 붙인다 (저격수 그대로)
    if (!(CHAPTER && chAL >= CH_MIXL)) return;
    const g = groups.reduce((n, L) => n + L.filter((t) => t === 'soldier').length, 0), add = Math.round(g * CH_MORE) - g;
    for (let i = 0; i < add; i++) groups[i % groups.length].push('soldier');
  }
  const CH_DISP_N = """)
rep("const [lo, hi] = CH_DISP_N[Math.min(CH_DISP_N.length, stars) - 1], n = lo + Math.floor(Math.random() * (hi - lo + 1));",
    "const [lo, hi] = CH_DISP_N[Math.min(CH_DISP_N.length, stars) - 1], n0 = (lo + Math.floor(Math.random() * (hi - lo + 1))) * (chAL >= CH_MIXL ? CH_MORE : 1), n = Math.floor(n0) + (Math.random() < n0 % 1 ? 1 : 0);   /* c581 */")
rep("      P.forEach(([m, c], k) => teamWait.push(", "      chSfMore(P.map(([, c]) => c));   /* c581 */\n      P.forEach(([m, c], k) => teamWait.push(")
rep("    if (q < 0.1) { teamWait.push({ car: [S_, G_, G_, G_], t: 0, seg, hold: true }); return; }",
    "    if (q < 0.1) { const C1 = [S_, G_, G_, G_]; chSfMore([C1]); teamWait.push({ car: C1, t: 0, seg, hold: true }); return; }   /* c581 */")
rep("    teamWait.push({ car: L[0], t: 0, seg, hold: true }, { car: L[1], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });",
    "    L[0] = L[0].slice(); L[1] = L[1].slice(); chSfMore(L);   /* c581 */\n    teamWait.push({ car: L[0], t: 0, seg, hold: true }, { car: L[1], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });")
rep("      const c = addCitizen(p.x, p.z, square(p.x, p.z), t); if (car.sfw) c.sfw = car.sfw; if (car.cvy) c.cvy = true;",
    "      chNoMix = !!car.cvy; const c = addCitizen(p.x, p.z, square(p.x, p.z), t); chNoMix = false; if (car.sfw) c.sfw = car.sfw; if (car.cvy) c.cvy = true;   /* c581: 보스 인원은 섞임 없음 */")
# 4~6) 건널목: 경찰 2 → 경찰 2~4 → 군인 2씩 · 터렛 단계 = 기본 + 터렛 · 그 뒤 군인 2 + 사각 1
rep([l for l in s.split('\n') if l.startswith("      const add = s <= 2 ? { police: N(2, 4) } : s < CH_MIXL")][0],
    "      const add = s === 1 ? { police: 2 } : s === 2 ? { police: N(2, 4) } : CHAPTER && s > CH_MIXL ? { soldier: 2, sniper: 1 } : { soldier: 2 };   /* c581: 수상함 경찰 2 · 경계 경찰 2~4 · 그 뒤 군인 2씩 · 터렛 다음 단계부터 군인 2 + 사각 1 */")
# 7) 샷건 넉백: 저격수와 같은 세기 · 끝에서도 50%
rep("      const D = SNIPER_KD * 0.8 * Math.max(0, 1 - e / R);   /* c573: 붙어 있으면 저격수 넉백의 80% */",
    "      const D = SNIPER_KD * (1 - 0.5 * Math.min(1, e / R));   /* c581: 저격수 넉백 — 붙으면 100% · 끝에서 50% */")
# 8) 샷건 이펙트 강화 + 부채꼴 면적
rep("      for (let i = 0; i < 13; i++) {", "      chFanAdd(c.foot.x, c.foot.z, a0, R, c.space);   /* c581: 맞는 범위 부채꼴이 땅에 번쩍 */\n      for (let i = 0; i < 18; i++) {")
rep("const a = a0 + (i / 12 - 0.5) * (Math.PI / 3) + rand(-0.04, 0.04)", "const a = a0 + (i / 17 - 0.5) * (Math.PI / 3) + rand(-0.04, 0.04)")
rep("j ? 0.16 - j * 0.03 : 0.22, 0.06, life,", "j ? 0.22 - j * 0.04 : 0.3, 0.08, life,")
rep("0xfff23a, 1.05 - Math.abs(k) * 0.12, 0.5, 0.09, 0, 0, 0, 0.85);", "0xfff23a, 1.4 - Math.abs(k) * 0.15, 0.6, 0.11, 0, 0, 0, 0.95);")
rep("  const CH_SG_HPK = 450 / 252;", """  const chFans = [];   // c581: 샷건 부채꼴 면적 이펙트
  function chFanAdd(x, z, a0, R, space) {
    const mk = (r, col, op) => { const g = new THREE.CircleGeometry(r, 28, -Math.PI / 6, Math.PI / 3).rotateX(-Math.PI / 2); const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthWrite: false })); m.position.set(x, 0.04, z); m.rotation.y = -a0; m.renderOrder = 4; scene.add(m); return m; };
    chFans.push({ t: 0, life: 0.28, out: mk(R, 0xffb020, 0.42), inn: mk(R * 0.55, 0xfff3a0, 0.6) });
  }
  function chFanTick(dt) {
    for (let i = chFans.length - 1; i >= 0; i--) { const f = chFans[i]; f.t += dt; const u = f.t / f.life;
      if (u >= 1) { for (const m of [f.out, f.inn]) { scene.remove(m); m.geometry.dispose(); m.material.dispose(); } chFans.splice(i, 1); continue; }
      f.out.material.opacity = 0.42 * (1 - u) * (1 - u); f.inn.material.opacity = 0.6 * Math.max(0, 1 - u * 1.8); f.out.material.color.setHex(u < 0.3 ? 0xffd040 : 0xff8a20); }
  }
  const CH_SG_HPK = 450 / 252;""")
rep("    stepFx(dt); stepChips(dt); drawObjBars(dt);", "    stepFx(dt); stepChips(dt); drawObjBars(dt); if (CHAPTER) chFanTick(dt);   /* c581 */")
# 9) 샷건 경찰이 좀비가 되면 샷건을 버린다
rep("    if (b.gooS) { b.mesh.remove(b.gooS); b.gooS = null; } b.goo = false;", "    if (b.gooS) { b.mesh.remove(b.gooS); b.gooS = null; } b.goo = false;\n    if (b.aimGun) { b.mesh.remove(b.aimGun); b.aimGun = null; } if (b.sg) { b.sg = false; b.baseCol = undefined; }   /* c581: 샷건 경찰이 좀비가 되면 샷건은 사라진다 */")
pathlib.Path('c581_patch.py').write_text('C581_R = ' + repr(R) + '\n')
print(len(R))
