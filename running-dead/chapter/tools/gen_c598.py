import pathlib
s = pathlib.Path('c597.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
i0 = s.index("    const trSheet = (pop) => {"); i1 = s.index("    const tutSheet = () => {")
rep(s[i0:i1], r"""    let trSel = 'start';   // c598: 특성 창 — 고른 탭
    const CH_TR_DESC = {
      start: '판을 시작할 때 동료 좀비를 데리고 시작합니다. 2단계마다 한 칸씩 늘어나며, 새끼 좀비 한 마리가 다음 칸에서 일반 좀비로 자랍니다. 새끼 좀비는 사람을 덮치거나 감염시키지 못하고 때리기만 합니다. 20단계면 일반 좀비 5마리와 함께 시작합니다.',
      leech: '내가 사람을 때릴 때마다 내 최대 체력의 일부를 회복합니다. 범위 공격으로 여러 명을 한꺼번에 때려도 한 번 때릴 때 한 번만 회복합니다. 덮치거나 감염시킬 때는 회복하지 않으며, 사각 로봇 · 터렛 · 드론 같은 기계를 때릴 때도 회복하지 않습니다.',
      bat: '테이저에 맞는 순간 대상이 피해를 입습니다. 피해는 내가 한 번 때리는 피해를 기준으로 하며, 공격력 성장을 그대로 받습니다. 이 피해로 쓰러진 사람은 감전된 채 무방비 상태가 되고, 기계는 그 자리에서 터집니다.',
      bomb: '산성 자폭 스위치가 터지는 범위가 처음부터 넓어집니다. 판 안에서 별로 강화한 범위에 그대로 더해집니다. 범위가 넓어지면 덮는 넓이는 제곱으로 늘어나서, 처음 얻은 자폭 스위치도 바로 쓸모가 생깁니다.',
      cash: '훈련된 인간의 유혹 저항력을 낮춥니다. 저항력이 낮을수록 뿌린 돈에 오래 정신을 팔립니다. 군인 · 저격수의 저항력은 8, 경찰은 5, 일반 인간은 0입니다. 20단계면 저항력이 2 줄어 군인은 40%, 경찰은 70%까지 유혹 시간을 받습니다.',
      mut: '변이한 좀비가 새 능력을 얻습니다. 나(각성) · 동료(변이) · 맵에서 얻은 변이 좀비 모두에 적용되고, 괴물이 되어도 그대로 이어집니다. 덩치: 몸에 닿은 모든 것(적 · 벽 · 문 · 차량 · 바리케이트 · 사물)에 주기적으로 피해를 줍니다. 히드라: 공격을 일정 확률로 피하고 MISS가 뜨며, 넉백도 받지 않습니다.',
      str: '내 미는 힘이 세집니다. 다른 몸을 더 멀리 밀어내고, 밀릴 때는 더 잘 버팁니다. 내가 덩치로 각성해도 그 힘에 그대로 더해집니다.',
    };
    const trSheet = (pop) => {   // c598: 위 = 고른 특성의 자세한 설명 + 강화 버튼 · 아래 = 특성 탭 목록(스크롤, 줄 전체가 탭)
      const tp = chTpLeft(), prev = sheet && sheet.querySelector('.sh'), keep = prev ? prev.scrollTop : 0;
      const D = CH_TRD.find((d) => d.k === trSel) || CH_TRD[0], L = chTrait(D.k), mx = L >= CH_TR_MAX, c = chTrCost(L);
      const dots = (n) => `<div class="dt">${Array.from({ length: CH_TR_MAX }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('')}</div>`;
      const det = `<div class="trd${pop ? ' pop' : ''}"><div class="dh"><div class="ic">${D.ic}</div><div><div class="n1">${D.nm}</div><div class="lv">${L} / ${CH_TR_MAX}단계</div></div></div>${dots(L)}<div class="dd">${CH_TR_DESC[D.k] || ''}</div>` +
        `<div class="de"><div><span>지금</span>${L ? D.fx(L) : '아직 없음'}</div>${mx ? '' : `<div><span>다음</span>${D.fx(L + 1)}</div>`}</div>` +
        (mx ? `<div class="mxb">MAX</div>` : `<button class="up" data-tr="${D.k}" ${tp < c ? 'disabled' : ''}>강화 · ${CH_TP_I(18)} ${c}</button>`) + `</div>`;
      const row = (d) => { const l = chTrait(d.k); return `<button class="trt${d.k === D.k ? ' on' : ''}${pop === d.k ? ' pop' : ''}" data-sel="${d.k}"><span class="ic">${d.ic}</span><span class="tx"><span class="n1">${d.nm}</span>${dots(l)}</span><span class="lv">${l >= CH_TR_MAX ? 'MAX' : l + '/' + CH_TR_MAX}</span></button>`; };
      openSheet(`<div class="hd"><div><div class="t2">특성</div></div><button class="x">✕</button></div><div class="ds"><span class="tpw">${CH_TP_I(16)} 특성 포인트 <b class="tpn">${tp}</b></span> · 성장 게이지 1개 · 첫 클리어 5 · 서브 미션 1</div>` + det + `<div class="trl">${CH_TRD.map(row).join('')}</div>`,
        (b) => { if (b.dataset.sel) { trSel = b.dataset.sel; trSheet(); return; }
          const k = b.dataset.tr; if (!k) return; const l = chTrait(k); if (l >= CH_TR_MAX || chTpLeft() < chTrCost(l)) return; CH_SV.tr[k] = l + 1; chSave(); { const m = ov.querySelector('.map'); draw(m ? m.scrollLeft : 0); } trSheet(k); });
      const t = sheet && sheet.querySelector('.sh'); if (t) t.scrollTop = keep;
    };
""")
rep("#outg .tr{display:flex;", r"""#outg .trd{position:sticky;top:-16px;z-index:2;background:#161c25;margin:0 -16px 8px;padding:10px 16px 12px;border-bottom:2px solid #2a3442}
#outg .trd .dh{display:flex;align-items:center;gap:12px}#outg .trd .ic{width:54px;height:54px;border-radius:14px;background:#11161e;display:flex;align-items:center;justify-content:center;font-size:30px;flex:none;border:2px solid #4a2e7a}
#outg .trd .n1{font-weight:900;font-size:19px}#outg .trd .lv{font-size:13px;color:#c79bff;font-weight:900;margin-top:2px}
#outg .trd .dt{margin:10px 0 8px}#outg .trd .dd{font-size:13.5px;line-height:1.55;color:#d9e1ec;font-weight:600;word-break:keep-all}
#outg .trd .de{margin-top:10px;background:#11161e;border-radius:12px;padding:8px 10px;font-size:13px;font-weight:700;color:#d9e1ec}#outg .trd .de div{display:flex;gap:8px;margin:3px 0}#outg .trd .de span{flex:none;width:30px;color:#8fa0b8;font-weight:900}
#outg .trd .up{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;margin-top:10px;padding:13px 0;border-radius:14px;background:linear-gradient(#b36bff,#7a35d0);box-shadow:0 3px 0 #4a1d85;font-weight:900;font-size:17px;color:#fff}
#outg .trd .up:disabled{background:#3a4250;box-shadow:none;color:#8a93a3}#outg .trd .mxb{margin-top:10px;text-align:center;font-weight:900;color:#c79bff;font-size:16px;padding:10px 0}
#outg .trd.pop .ic{animation:trflash .7s ease-out}
#outg .trl{display:flex;flex-direction:column;gap:6px}
#outg .trt{display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:#1e2530;border:2px solid #2a3442;border-radius:12px;padding:8px 10px;color:#e8ecf2}
#outg .trt.on{border-color:#c79bff;background:#2a2140;box-shadow:0 0 10px rgba(199,155,255,.25)}#outg .trt.pop{animation:trflash .7s ease-out}
#outg .trt .ic{width:36px;height:36px;border-radius:10px;background:#11161e;display:flex;align-items:center;justify-content:center;font-size:20px;flex:none}
#outg .trt .tx{flex:1;min-width:0;display:flex;flex-direction:column}#outg .trt .n1{font-weight:900;font-size:14px}#outg .trt .lv{font-size:12px;color:#c79bff;font-weight:900;flex:none}
#outg .trt .dt,#outg .trd .dt{display:flex;gap:2px}#outg .trt .dt{margin-top:5px}#outg .trt .dt i,#outg .trd .dt i{width:7px;height:8px;border-radius:2px;background:#11161e;border:1px solid #3a4250}#outg .trt .dt i.on,#outg .trd .dt i.on{background:#c79bff;border-color:#c79bff}
#outg .tr{display:flex;""")
pathlib.Path('c598_patch.py').write_text('C598_R = ' + repr(R) + '\n')
print(len(R))
