# c274: 레벨업 카드 누르면 자세한 설명 · 무기 강화/분해 강화는 확인 없이 바로 · 가방 분해
C274_R = []
OLDLV = """      const card = e.target.closest('.card'), ok = e.target.closest('.ok');
      if (card) { chosen = card.dataset.k; for (const c of ov.querySelectorAll('.card')) c.classList.toggle('on', c === card); ov.querySelector('.ok').classList.add('ready'); return; }
      if (!ok || !chosen) return;
      if (chosen === '__w') { chWupPick(ov); chosen = null; return; }   // c125: 강화할 무기를 고르는 화면으로
      ov.dataset.done = '1';"""
NEWLV = """      const card = e.target.closest('.card'), ok = e.target.closest('.ok');
      if (card && ov.dataset.wup) { const k = card.dataset.k; chPickWin(ov, k); ilv[k] = lv(k) + 1; chItemChanged(k); chPopBtn(k); pendingLv--; lvQueued = Math.max(0, lvQueued - 1); level++; drawLv(); chPickClose(ov, () => { lvOpen = false; }); return; }   // c274: 무기를 누르는 순간 바로 강화 (확인 없음)
      if (card && card.dataset.k === '__w') { chWupPick(ov); ov.dataset.wup = '1'; ov.querySelector('.ok').style.setProperty('display', 'none', 'important'); ov.querySelector('.det')?.classList.remove('on'); chosen = null; return; }   // c274: 무기 강화는 누르자마자 무기 목록 (확인·설명 없음)
      if (card) { chosen = card.dataset.k; for (const c of ov.querySelectorAll('.card')) c.classList.toggle('on', c === card); ov.querySelector('.ok').classList.add('ready'); chDetShow(ov, chosen); return; }   // c274: 자세한 설명이 확인 버튼 위에
      if (!ok || !chosen) return;
      ov.dataset.done = '1'; ov.querySelector('.det')?.classList.remove('on');"""
C274_R.append((OLDLV, NEWLV, 2))   # 테스트맵 showLevelUp에도 같은 줄이 있다 — 설명 칸이 없으면 그냥 넘어간다
C274_R.append(("""      `</div><button class="ok okBtn">확인</button>`;
    stage.appendChild(ov);
    let chosen = null;""", """      `</div><div class="det"></div><button class="ok okBtn">확인</button>`;   /* c274: 설명 칸 */
    stage.appendChild(ov);
    let chosen = null;""", 2))
# 분해 후 강화: 확인 없이 바로
C274_R.append(("""`<div class="vl">${S[0]} ${max ? S[1](n) : S[1](n) + ' → ' + S[1](n + 1)}</div></div>`; }).join('') + `</div><button class="ok okBtn">확인</button>`;
    stage.appendChild(ov);
    let chosen = null; const block = (e) => { e.stopPropagation(); e.preventDefault(); };
    ov.addEventListener('pointermove', block); ov.addEventListener('pointerup', block);
    ov.addEventListener('pointerdown', (e) => {
      block(e); if (ov.dataset.done) return;
      const card = e.target.closest('.card'), ok = e.target.closest('.ok');
      if (card) { chosen = card.dataset.k; for (const c of ov.querySelectorAll('.card')) c.classList.toggle('on', c === card); ov.querySelector('.ok').classList.add('ready'); return; }
      if (!ok || !chosen) return;
      ov.dataset.done = '1';
      for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === chosen ? 'win' : 'gone'); }
      ov.querySelector('.ok').style.opacity = '0';
      ilv[chosen] = lv(chosen) + 1; chItemChanged(chosen);
      const el = (items.find((x) => x.kind === chosen) || {}).el; if (el) { el.classList.remove('pop'); el.getBoundingClientRect(); el.classList.add('pop'); }
      setTimeout(() => { ov.style.opacity = '0'; }, 550);
      setTimeout(() => { ov.remove(); acqOpen = false; paused = false; last = 0; }, 850);
    });
  }""", """`<div class="vl">${S[0]} ${max ? S[1](n) : S[1](n) + ' → ' + S[1](n + 1)}</div></div>`; }).join('') + `</div>`;   /* c274: 확인 버튼 없음 */
    stage.appendChild(ov);
    const block = (e) => { e.stopPropagation(); e.preventDefault(); };
    ov.addEventListener('pointermove', block); ov.addEventListener('pointerup', block);
    ov.addEventListener('pointerdown', (e) => {
      block(e); if (ov.dataset.done) return;
      const card = e.target.closest('.card'); if (!card) return;
      const k = card.dataset.k;   // c274: 누르는 순간 바로 강화
      chPickWin(ov, k); ilv[k] = lv(k) + 1; chItemChanged(k); chPopBtn(k);
      chPickClose(ov, () => { acqOpen = false; });
    });
  }
  function chPickWin(ov, k) {                  // c274: 고른 카드만 커지며 빛나고 나머지는 사라진다
    ov.dataset.done = '1';
    for (const c of ov.querySelectorAll('.card')) { c.classList.remove('on'); c.classList.add(c.dataset.k === k ? 'win' : 'gone'); }
    const ok = ov.querySelector('.ok'); if (ok) ok.style.opacity = '0';
  }
  function chPickClose(ov, fn) { setTimeout(() => { ov.style.opacity = '0'; }, 550); setTimeout(() => { ov.remove(); fn(); paused = false; last = 0; }, 850); }
  function chPopBtn(k) { const el = (items.find((x) => x.kind === k) || {}).el; if (el) { el.classList.remove('pop'); el.getBoundingClientRect(); el.classList.add('pop'); } }
  function chDetShow(ov, k) {                  // c274: 카드를 누르면 확인 버튼 위에 자세한 설명 (검은 반투명 판을 한 겹 더)
    const el = ov.querySelector('.det'); if (!el || !ITEM[k]) return;
    const n = lv(k), now = chHas(k) ? lvText(k) : `획득 시: ${statLine(k, 0)}`;
    el.innerHTML = `<div class="dn"><span class="di">${ITEM[k].icon}</span><span>${ITEM[k].name}</span></div><div class="dt">${CH_DETAIL[k] || ITEM_TEXT[k][0]}</div><div class="dl">${now}</div>`;
    el.classList.add('on'); void n;
  }
  const CH_DETAIL = {                          // c274: 레벨업 카드 자세한 설명 (수치는 아래 '지금 · 다음 강화' 줄에)
    bomb: '가장 위험한 적 곁에 있는 동료 하나에게 산성 표시가 붙고, 그 동료가 가장 가까운 인간에게 빠르게 돌진합니다. 인간에게 닿거나, 4초가 지나거나, 그 동료가 죽으면 터지면서 주변에 산성 덩어리를 뿌립니다. 산성 위에 있는 적은 0.5초마다 도트 피해를 받습니다. 강화하면 터지는 범위가 넓어지고 산성이 더 오래 남습니다.',
    mutate: '가장 가까운 동료 하나에게 주사를 놓아 체력을 가득 채우고 잠시 변이 좀비로 만듭니다. 변이 좀비는 더 세고 더 빠릅니다. 주사는 여러 개를 들고 다니며, 쓴 주사는 쿨타임이 지나면 다시 찹니다. 강화하면 주사를 더 들고 다니고 변이가 더 오래 갑니다.',
    taser: '주변의 적에게 전기를 쏴 감전시킵니다. 감전된 적은 그 시간 동안 멈춥니다. 보스도 똑같이 멈춥니다. 장탄만큼 연달아 쓸 수 있고, 쓴 장탄은 쿨타임이 지나면 다시 찹니다. 강화하면 한 번에 감전시키는 수와 감전 시간, 장탄이 늘어납니다.',
    awaken: '충전된 게이지만큼 내가 변이 좀비로 변합니다. 게이지는 35초에 걸쳐 가득 차고, 쓴 만큼 줄어듭니다. 게이지가 찬 만큼 체력도 회복합니다 (가득이면 20%). 강화하면 한 번에 쓸 수 있는 최대 시간이 늘어납니다.',
    cash: '바닥에 돈다발을 뿌립니다. 돈을 알아챈 인간은 유혹 시간 동안 정신을 못 차리고 돈만 쫓습니다. 유혹 강도만큼 맞을 때까지는 공격을 받아도 정신을 못 차립니다. 경찰이나 군인처럼 훈련된 인간은 유혹에 강합니다. 강화하면 알아채는 거리, 유혹 시간, 유혹 강도가 늘어납니다.',
    book: '내가 가진 모든 무기의 쿨타임이 줄어듭니다. 각성 게이지가 차는 속도도 빨라집니다. 장비(분노 바이러스 등)의 시간에는 영향이 없습니다. 강화하면 쿨타임이 더 줄어듭니다.',
    bag: '쓸 수 있는 무기 칸이 하나 늘어납니다 (최대 5칸). 칸이 꽉 차도 무기는 얻을 수 있지만, 칸이 늘어나야 쓸 수 있습니다. 강화할 때마다 한 칸씩 더 늘어납니다.',
    rage: '30초마다 아직 걸리지 않은 동료 한 명에게 분노 바이러스를 겁니다. 변이한 동료가 1순위이고, 없으면 내 곁의 동료가 걸립니다. 걸린 동료는 살아 있는 동안 공격 속도와 이동 속도가 계속 올라 있습니다 (머리 위 작은 불꽃). 강화하면 이미 걸린 동료까지 모두 더 빨라집니다.',
    crowbar: '내가 문, 벽, 금고, 차, 사물을 때릴 때 주는 피해가 늘어납니다. 동료가 때리는 피해에는 적용되지 않습니다. 강화하면 피해가 더 늘어납니다.',
    vest: '경찰 권총, 군인 소총, 저격수, 보스 기관포처럼 멀리서 날아오는 총격의 피해를 줄입니다. 총에 맞을 때 뒤로 밀리는 힘도 줄여 주고, 버티는 수치보다 약한 충격에는 아예 밀리지 않습니다 (근접 무기 1 · 권총 2 · 군인 3 · 저격수 12). 나에게만 적용됩니다. 강화하면 피해가 더 줄고 더 강한 충격도 버팁니다.',
    shoes: '나와 동료 좀비, 변이한 좀비 모두의 이동 속도가 오릅니다. 도망치는 인간을 더 빨리 따라잡고, 총을 든 적에게서도 더 빨리 빠질 수 있습니다. 강화하면 더 빨라집니다.',
    teeth: '나와 동료들이 인간을 물어 좀비로 만드는 시간이 줄어듭니다. 한 번 감염시킬 때 회복하는 체력의 총량은 그대로이고, 더 짧은 시간에 들어옵니다. 물고 있는 동안 공격받는 시간도 그만큼 줄어듭니다. 강화하면 더 빨라집니다.',
    acid: '동료 좀비나 변이 좀비가 죽는 자리에 산성피가 퍼집니다. 그 안의 적은 0.5초마다 산성 피해를 받습니다 (보스 포함). 산성피가 겹쳐도 피해는 쌓이지 않고 남은 시간만 새로 채워집니다. 강화하면 범위가 넓어지고 더 오래 남습니다.',
    acidp: '모든 산성 피해(산성 폭발의 산성피, 산성 자폭 스위치의 산성 덩어리)가 0.5초마다 주는 도트 데미지가 늘어납니다. 산성 무기나 장비가 없으면 효과가 없습니다. 강화하면 더 늘어납니다.',
    catalyst: '변이한 좀비 모두의 공격력이 오릅니다. 변이 주사를 맞은 동료처럼 변이해 있는 동안 적용됩니다. 강화하면 더 오릅니다.',
    blood: '나의 최대 체력이 늘어납니다. 얻을 때와 강화할 때마다 늘어난 만큼 체력도 함께 찹니다. 동료에게는 적용되지 않습니다.',
    revive: '내가 죽으면 체력이 가득 찬 채로 그 자리에서 되살아납니다. 한 번 쓰면 쿨타임이 지나야 다시 쓸 수 있습니다 (배지에 남은 시간이 나옵니다). 강화하면 쿨타임이 10%씩 줄어듭니다.',
  };
  { const st = document.createElement('style'); st.textContent = '#pick .det { display: none; width: min(356px, calc(100vw - 32px)); margin-top: 16px; padding: 12px 14px 13px; box-sizing: border-box; border-radius: 14px; background: rgba(0, 0, 0, 0.7); color: #fff; text-align: left; word-break: keep-all; } #pick .det.on { display: block; } #pick .det .dn { display: flex; align-items: center; gap: 8px; font: 800 16px/1.2 var(--font); color: #ffd34d; } #pick .det .dn { justify-content: flex-start; } #pick .det .di { flex: none; width: 24px; height: 24px; display: inline-flex; font-size: 22px; line-height: 1; } #pick .det .di > * { width: 100% !important; height: 100% !important; margin: 0 !important; } #pick .det .dt { margin-top: 8px; font: 600 13px/1.55 var(--font); color: rgba(255, 255, 255, 0.92); } #pick .det .dl { margin-top: 9px; font: 700 12px/1.5 var(--font); color: #7fd4ff; }'; document.head.appendChild(st); }"""))
# 가방도 분해
C274_R.append(("(CHAPTER && !d.passive && chCanDis(kind) ? chTwoOk : tapOk)", "(CHAPTER && (!d.passive || kind === 'bag') && chCanDis(kind) ? chTwoOk : tapOk)"))
C274_R.append(("mk(label, '무기를 사용할 수 있습니다',", "mk(label, kind === 'bag' ? '무기 칸이 하나 늘어납니다' : '무기를 사용할 수 있습니다',"))
