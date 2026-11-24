# c422: 무기 갈림길 — 흰 ★6 다음 강화(7번째)에서 카드 2장 중 하나를 고르고 빨간 별(1~6)이 붙는다. 빨간 ★6 = MAX.
#        흰 ★6 뒤로 원래 수치는 멈추고 고른 길 능력만 오른다. 지금은 산성 자폭 스위치만 (끈적 산성 · 분열 산성)
#        + 드론을 부수면 경험치 1 (적이 죽을 때 경험치)
src = open('c421.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# 갈림길 표 · 최대 단계
rep("  const chLvMax = (k) => k === 'bag' ? 3 : /* c198: 빠루도 5번 (+120%) */ ITEM[k] && !ITEM[k].passive ? 6 : 5;",
    """  const CH_BRANCH = {                          // c422: 무기 갈림길 — 흰 ★6 다음 강화에서 둘 중 하나 (빨간 별 r = 1~6)
    bomb: [
      { id: 'sticky', name: '끈적 산성', desc: '자폭 산성을 맞은 적이 느려집니다.', line: (r) => `산성 맞은 적 이동 속도 -${15 * r}%`, short: ['둔화', (r) => `-${15 * r}%`] },
      { id: 'split', name: '분열 산성', desc: '자폭 산성을 뒤집어쓴 적이 그 상태로 쓰러지면, 감염시키지 않아도 그 즉시 새끼 좀비 2마리로 변합니다.', line: (r) => `새끼 좀비 2마리로 변할 확률 ${15 * r}%`, short: ['분열', (r) => `${15 * r}%`] },
    ],
  };
  const chBr = {};                             // c422: 무기마다 고른 길 (id)
  const chBrR = (k, id) => CHAPTER && chBr[k] === id ? Math.max(0, lv(k) - 6) : 0;   // 그 길의 빨간 별 수 (안 골랐으면 0)
  const chLvB = (k) => Math.min(6, lv(k));     // c422: 원래 수치는 흰 ★6에서 멈춘다
  const chStickyK = () => 1 - 0.15 * chBrR('bomb', 'sticky');   // 끈적 산성 — 15%씩 느리게 (90%까지)
  const chLvMax = (k) => k === 'bag' ? 3 : /* c198: 빠루도 5번 (+120%) */ ITEM[k] && !ITEM[k].passive ? (CH_BRANCH[k] ? 12 : 6)   /* c422: 갈림길이 있는 무기는 빨간 ★6까지 */ : 5;""")
rep("  const chStarsK = (k, n) => CHAPTER && n >= chLvMax(k) ? 'MAX' : chStars(n);",
    "  const chStarsK = (k, n) => CHAPTER && n >= chLvMax(k) ? 'MAX' : CHAPTER && n > 6 ? `<span style=\"color:#ff3b30\">${'★'.repeat(n - 6)}</span>` : chStars(n);   /* c422: 흰 ★6 다음은 빨간 별 */")
rep("? '<span style=\"color:#ffd34d;font-weight:900;letter-spacing:0\">MAX</span>' : chStars(n)) :", "? '<span style=\"color:#ffd34d;font-weight:900;letter-spacing:0\">MAX</span>' : chStarsK(kd[els.indexOf(el)], n)) :   /* c422 */")
rep("for (const k of Object.keys(ilv)) delete ilv[k];", "for (const k of Object.keys(ilv)) delete ilv[k]; for (const k of Object.keys(chBr)) delete chBr[k];   /* c422 */")
# 수치 줄 · 카드 짧은 수치: 흰 ★6 뒤는 원래 수치(★6) + 고른 길
rep("    blood: (n) => `내 최대 체력 +${12 * (1 + n)}%`,\n  };", "    blood: (n) => `내 최대 체력 +${12 * (1 + n)}%`,\n  };\n  for (const k of Object.keys(CH_BRANCH)) { const f = CH_STAT[k]; CH_STAT[k] = (n) => { if (n <= 6) return f(n); const B = CH_BRANCH[k].find((b) => b.id === chBr[k]); return f(6) + ' · ' + (B ? `${B.name}: ${B.line(n - 6)}` : '갈림길 — 둘 중 하나 선택'); }; }   // c422")
i = src.index("    shoes: ['이동', (n) => `+${5 * (1 + n)}%`], paras"); j = src.index("\n  };\n", i)
R.append((src[i:j + 5], src[i:j + 5] + "\n  for (const k of Object.keys(CH_BRANCH)) { const S = CH_SHORT[k], f = S[1]; S[1] = (n) => { if (n <= 6) return f(n); const B = CH_BRANCH[k].find((b) => b.id === chBr[k]); return B ? B.short[0] + ' ' + B.short[1](n - 6) : '갈림길'; }; }   // c422"))
# 원래 수치는 ★6에서 멈춘다 (자폭 범위 · 산성 시간)
rep("const R = 1.5 + lv('bomb');", "const R = 1.5 + chLvB('bomb');   /* c422 */")
rep("(4 + 2 * lv('bomb'))", "(4 + 2 * chLvB('bomb'))", 3)
# 갈림길 고르기 — 7번째 강화가 되는 순간 (어느 길로 강화했든) 획득창처럼 바로 뜬다
rep("  function chItemChanged(kind) {", "  function chItemChanged(kind) {\n    if (CHAPTER && CH_BRANCH[kind] && lv(kind) > 6 && !chBr[kind] && !pendingAward.includes('br:' + kind)) pendingAward.push('br:' + kind);   // c422: 갈림길 고르기")
rep("(e.k === 'mut:hydra' || e.k === 'mut:armor' || e.k === 'mut:zombie') chShowMut(e.k.slice(4));", "(e.k.startsWith('br:')) chBranchPick(e.k.slice(3)); else if (e.k === 'mut:hydra' || e.k === 'mut:armor' || e.k === 'mut:zombie') chShowMut(e.k.slice(4));", 2)
rep("  function chPickWin(ov, k) {", """  function chBranchPick(k) {                   // c422: 갈림길 — 카드 2장 중 하나 (전직처럼). 고르면 빨간 ★1의 능력이 바로 붙는다
    acqOpen = true; paused = true; stopInput();
    const ov = document.createElement('div'); ov.id = 'pick';
    ov.innerHTML = `<div class="hd">${ITEM[k].name} 갈림길</div><div class="sub">둘 중 하나를 선택하세요</div><div class="cards" style="flex-wrap:wrap;justify-content:center">` +
      CH_BRANCH[k].map((B) => `<div class="card" data-k="${B.id}" style="min-height:178px;padding-top:8px"><div style="height:14px;font:900 12px/14px var(--font);color:#ff3b30">★</div>` +
        `<div class="ic" style="margin-top:4px">${ITEM[k].icon}</div><div class="nm" style="margin-top:8px">${B.name}</div><div class="ds" style="margin-top:8px">${B.desc}</div><div class="vl">${B.line(1)}</div></div>`).join('') + `</div>`;
    stage.appendChild(ov); chFitNames(ov);
    const block = (e) => { e.stopPropagation(); e.preventDefault(); };
    ov.addEventListener('pointermove', block); ov.addEventListener('pointerup', block);
    ov.addEventListener('pointerdown', (e) => {
      block(e); if (ov.dataset.done) return;
      const card = e.target.closest('.card'); if (!card) return;
      chPickWin(ov, card.dataset.k); chBr[k] = card.dataset.k; chItemChanged(k); chPopBtn(k);
      chPickClose(ov, () => { acqOpen = false; });
    });
  }
  function chPickWin(ov, k) {""")
# 끈적 산성 — 사람 이동 · 장갑차 · 드론
rep("const gk = (b.goo && !CHAPTER ? 0.56 : 1)   /* c421 */", "const gk = (b.goo && !CHAPTER ? 0.56 : 1)   /* c421 */ * (CHAPTER && b.goo ? chStickyK() : 1)   /* c422: 끈적 산성 */")
rep("CAR_SPEED * 0.9) /* c421: 산성 둔화 없음 */;", "CAR_SPEED * 0.9) /* c421: 산성 둔화 없음 */ * (car.goo ? chStickyK() : 1)   /* c422: 끈적 산성 */;")
rep("const sp = CH_DRONE_SPEED * dt,", "const sp = CH_DRONE_SPEED * dt * (d.goo > 0 ? chStickyK() : 1)   /* c422: 끈적 산성 */,")
# 분열 산성 — 자폭 산성이 묻은 채 체력이 0이 되면 (체력이 있던 적) 확률로 그 즉시 새끼 좀비 2마리
rep("      if (!c.goo || c.kind !== 'citizen') continue;\n", "      if (!c.goo || c.kind !== 'citizen') continue;\n      if (CHAPTER && c.maxHp > 0 && c.hp <= 0 && !c.brSplitT && c.state !== 'held') { c.brSplitT = 1; const p = 0.15 * chBrR('bomb', 'split'); if (p && Math.random() < p) { chSplitAcid(c); continue; } }   // c422: 분열 산성 (쓰러진 순간 한 번만 굴린다)\n")
rep("  function chMini(c) {", """  function chSplitAcid(t) {                    // c422: 분열 산성 — 그 인간은 죽고 새끼 좀비 2마리 (경험치 1 · 사건 하나는 감염과 같다)
    for (const z of bodies) if (z.target === t && z.mode === 'pounce') { z.mode = 'free'; z.target = null; }
    t.marked = false; const x = t.foot.x, zz = t.foot.z;
    makeZombie(t); chMini(t); t.hp = t.maxHp = t.maxHp / 3; if (t.hpBar) t.hpDisp = t.hp;
    chParasite(t);
    for (let i = 0; i < 10; i++) { const g = i / 10 * Math.PI * 2; puff(x, 0.3, zz, 0x7ed321, 0.3, 0.8, 0.45, Math.cos(g) * 2, 0.3, Math.sin(g) * 2, 0.85); }
    gainXp(); callPolice(t.foot);
  }
  function chMini(c) {""")
# 드론을 부수면 경험치 1 (적이 죽을 때 경험치)
rep("    if (d.dead) return; d.dead = true;\n", "    if (d.dead) return; d.dead = true;\n    if (CHAPTER && isZombie(me)) gainXp();   // c422: 기계도 부수면 경험치 1\n")
open('c422_patch.py', 'w').write("# c422: 무기 갈림길 (자폭 스위치) · 드론 경험치\nC422_R = " + repr(R) + "\n")
print(len(R))
