import pathlib, json
s = pathlib.Path('c516.mjs').read_text()
IMG = json.loads(pathlib.Path('boss_img.json').read_text())
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
def between(a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

OUT = r"""  // ── c517: 아웃게임 — 가로로 미는 지도 · 깃발 · 스테이지 상세 창 (난이도 탭 · 클리어 조건 · 보스 · 보상 · 서브 미션 · 시작하기) · 성장 · 설정 ──
  const CH_LVN = ['수상함', '경계', '비상', '팬데믹', '총동원령', '계엄', '데프콘', '전면전', '대재앙', '종말'];
  const CH_MIS_T = { e: [[3, 6], 30], n: [[4, 7], 50], h: [[5, 8], 70] };   // 서브 미션 (임시) — [경보 단계, 분] · 동료 수
  const CH_MIX_T = { e: 5, n: 4, h: 3 };
  const CH_CLR_G = { e: 300, n: 300, h: 1000 };
  const CH_BOSS_IMG = __BOSSIMG__;
  const CH_STG_INFO = {
    1: { nm: '외곽 도시', ds: '감염이 처음 번진 조용한 도시. 아직은 경찰뿐이지만 곧 특공대가 온다.', boss: ['군인차 부대', '군인차 3대가 함께 온다. 차마다 사각 로봇 2 · 군인 3, 드론 8대가 붙어 있다가 차가 서면 날아오른다.', 'convoy'] },
    2: { nm: '공단 지구', ds: '공장과 창고가 늘어선 지구. 적이 20% 더 단단하고 세다.', boss: ['불도저 2대', '벽을 부수며 밀고 들어온다. 가끔 돌진하고, 치이면 크게 다친다.', 'dozer'] },
    3: { nm: '국경 요새', ds: '군대가 지키는 마지막 도시. 적이 40% 더 단단하고 세다.', boss: ['장갑차', '불도저 2배 체력 · 밀기 1.5배 · 기관총. 움직임은 불도저와 같다.', 'tank'] },
  };
  const CH_GENE_I = (w = 16) => `<svg viewBox="0 0 24 24" width="${w}" height="${w}" style="vertical-align:-3px"><path d="M7 2c0 6 10 6 10 10S7 16 7 22" fill="none" stroke="#7fe3ff" stroke-width="2.6" stroke-linecap="round"/><path d="M17 2c0 6-10 6-10 10s10 4 10 10" fill="none" stroke="#c78bff" stroke-width="2.6" stroke-linecap="round"/><path d="M9 7h6M8 12h8M9 17h6" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/></svg>`;
  const chClrText = (d) => d === 'e' ? '특공대 3번을 모두 물리치기 (120 · 265 · 405초에 온다)' : d === 'n' ? '특공대 4번을 모두 물리치기 (네 번째는 550초 · 저격수 3 · 군인 8)' : '550초에 오는 보스와 호위를 모두 물리치기';
  const chMisTxt = (d, i) => { const M = CH_MIS_T[d]; return i ? `동료 ${M[1]}마리 모으기` : `${M[0][1]}분 안에 경보 '${CH_LVN[M[0][0] - 1]}' 도달`; };
  const chLockWhy = (st, d) => d === 'e' ? `스테이지 ${st - 1}을 클리어하면 열려` : d === 'n' ? '쉬움을 클리어하면 열려' : '보통을 클리어하면 열려';
  function chOutgame(go, tut) {
    const ov = document.createElement('div'); ov.id = 'outg';
    const st = document.createElement('style');
    st.textContent = `
#outg{position:fixed;inset:0;z-index:1000;background:#0d1117;color:#fff;font-family:system-ui,-apple-system,sans-serif;display:flex;flex-direction:column;-webkit-user-select:none;user-select:none}
#outg button{font:inherit;color:inherit;border:none;background:none;touch-action:manipulation;cursor:pointer}
#outg .top{display:flex;align-items:center;gap:8px;padding:calc(10px + env(safe-area-inset-top,0px)) 16px 10px;background:linear-gradient(#0d1117,rgba(13,17,23,0.85));z-index:2}
#outg .gp{display:flex;align-items:center;gap:6px;background:#1b2330;border:2px solid #2d3a4d;border-radius:20px;padding:5px 12px 5px 8px;font-weight:900;font-size:17px}
#outg .ttl{flex:1;text-align:center;font-weight:900;font-size:18px;letter-spacing:1px;color:#e8d8ff}
#outg .tb{width:44px;height:40px;border-radius:12px;background:#1b2330;border:2px solid #2d3a4d;font-size:19px;display:flex;align-items:center;justify-content:center}
#outg .map{flex:1;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none}
#outg .map::-webkit-scrollbar{display:none}
#outg .in{position:relative;height:100%;aspect-ratio:2.4/1;min-width:900px}
#outg .in svg{position:absolute;inset:0;width:100%;height:100%}
#outg .nd{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:3px}
#outg .fl{width:58px;height:58px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ff8a5c,#c4302b);border:3px solid #ffe2a8;box-shadow:0 4px 0 #6d1a16,0 6px 14px rgba(0,0,0,0.6);font-weight:900;font-size:24px;display:flex;align-items:center;justify-content:center;text-shadow:0 2px 2px rgba(0,0,0,0.5)}
#outg .nd.lk .fl{background:radial-gradient(circle at 35% 30%,#7d8796,#4a525e);border-color:#9aa3b0;box-shadow:0 4px 0 #2a3038,0 6px 14px rgba(0,0,0,0.6);font-size:20px}
#outg .nd.soon .fl{background:#2a313b;border:3px dashed #59636f;box-shadow:none;font-size:13px;color:#8a93a3;width:50px;height:50px}
#outg .nd.cur .fl{animation:ogp 1.2s ease-in-out infinite}
@keyframes ogp{50%{transform:scale(1.08)}}
#outg .nm{font-weight:900;font-size:13px;background:rgba(0,0,0,0.6);padding:2px 8px;border-radius:8px;white-space:nowrap}
#outg .sr{display:flex;gap:1px;font-size:15px;line-height:1}
#outg .sr i{font-style:normal;color:#3d4450}#outg .sr i.on{color:#ffd34d;text-shadow:0 0 6px rgba(255,200,60,0.7)}
#outg .md{font-size:11px;font-weight:800;color:#bcd;background:rgba(0,0,0,0.5);padding:1px 6px;border-radius:6px}
#outg .hint{position:absolute;bottom:calc(10px + env(safe-area-inset-bottom,0px));left:0;right:0;text-align:center;font-size:12px;color:rgba(255,255,255,0.55);pointer-events:none}
#outg .bd{position:absolute;inset:0;background:rgba(0,0,0,0.55);z-index:5;display:flex;align-items:flex-end;justify-content:center}
#outg .sh{width:100%;max-width:520px;max-height:90%;overflow-y:auto;-webkit-overflow-scrolling:touch;background:#161c25;border-radius:20px 20px 0 0;border-top:3px solid #3a4a62;padding:16px 16px calc(16px + env(safe-area-inset-bottom,0px));box-sizing:border-box}
#outg .sh .hd{display:flex;align-items:flex-start;gap:10px}
#outg .sh .hd .t1{font-size:12px;font-weight:800;color:#ff9b6b}
#outg .sh .hd .t2{font-size:22px;font-weight:900}
#outg .sh .x{margin-left:auto;width:36px;height:36px;border-radius:10px;background:#252e3b;font-size:18px}
#outg .sh .ds{font-size:13px;color:#aab4c3;margin:6px 0 12px;line-height:1.45}
#outg .tabs{display:flex;gap:6px;margin-bottom:12px}
#outg .tabs button{flex:1;padding:10px 0;border-radius:12px;background:#222a36;border:2px solid #2d3a4d;font-weight:900;font-size:15px;color:#9aa6b8}
#outg .tabs button.sel{background:#2f6fe0;border-color:#7fb0ff;color:#fff}
#outg .tabs button.sel.h{background:#b3261e;border-color:#ff8a80}
#outg .tabs small{display:block;font-size:11px;font-weight:800;margin-top:2px;color:#ffd34d}
#outg .cd{background:#1e2530;border:2px solid #2a3442;border-radius:14px;padding:10px 12px;margin-bottom:8px}
#outg .cd .k{font-size:11px;font-weight:900;color:#8fa0b8;letter-spacing:1px;margin-bottom:5px}
#outg .cd .v{font-size:15px;font-weight:800;line-height:1.4}
#outg .bs img{width:100%;border-radius:10px;display:block;margin-bottom:8px;border:2px solid #3a2020}
#outg .bs .bn{font-size:17px;font-weight:900;color:#ff8a80}
#outg .bs .bt{font-size:13px;color:#c9d1dc;line-height:1.45;margin-top:2px}
#outg .rw{display:flex;align-items:center;gap:10px;font-weight:800;font-size:14px;padding:4px 0}
#outg .rw .gi{display:flex;align-items:center;gap:4px;background:#11161e;border-radius:10px;padding:4px 9px;font-size:16px;font-weight:900;min-width:62px;justify-content:center}
#outg .rw .lb{flex:1;line-height:1.3}
#outg .rw .lb small{display:block;font-size:11px;color:#8fa0b8;font-weight:700}
#outg .rw.got{opacity:0.5}
#outg .rw .ck{width:22px;height:22px;border-radius:6px;border:2px solid #4a5668;display:flex;align-items:center;justify-content:center;font-size:14px;flex:none}
#outg .rw .ck.on{background:#2e9e5b;border-color:#5fd38f}
#outg .go{width:100%;margin-top:6px;padding:15px 0;border-radius:16px;background:linear-gradient(#ffb547,#f07b12);box-shadow:0 4px 0 #8a4205;font-size:20px;font-weight:900;color:#2b1400}
#outg .go:disabled{background:#3a4250;box-shadow:0 4px 0 #20262f;color:#8a93a3;font-size:15px}
#outg .ug{display:flex;align-items:center;gap:12px;background:#1e2530;border:2px solid #2a3442;border-radius:14px;padding:12px;margin-bottom:8px}
#outg .ug .ic{width:46px;height:46px;border-radius:12px;background:#11161e;display:flex;align-items:center;justify-content:center;font-size:24px;flex:none}
#outg .ug .tx{flex:1}#outg .ug .n1{font-weight:900;font-size:16px}#outg .ug .n2{font-size:12px;color:#8fa0b8;font-weight:700;margin-top:2px}
#outg .ug .pc{font-size:22px;font-weight:900;color:#7fe3ff;min-width:56px;text-align:right}
#outg .ub{padding:10px 12px;border-radius:12px;background:#2f6fe0;font-weight:900;font-size:14px;display:flex;align-items:center;gap:4px;white-space:nowrap}
#outg .ub:disabled{background:#3a4250;color:#8a93a3}
#outg .sb{width:100%;padding:13px 0;border-radius:14px;background:#2a3340;font-weight:900;font-size:16px;margin-bottom:8px}
#outg .sb.rst{background:transparent;border:1px solid #3a4250;color:#8a93a3;font-size:13px;padding:8px 0}
#outg .sb.rst.on{background:#c62828;color:#fff;border-color:#c62828}
`;
    document.head.appendChild(st);
    const cleared = (k) => !!CH_SV.clr[k];
    const stars = (n) => ['e', 'n', 'h'].map((d) => `<i class="${cleared(n + d) ? 'on' : ''}">★</i>`).join('');
    const medals = (n) => ['e', 'n', 'h'].reduce((a, d) => a + (CH_SV.sub[n + d + '0'] ? 1 : 0) + (CH_SV.sub[n + d + '1'] ? 1 : 0), 0);
    const NODES = [[8, 64], [25, 38], [42, 62], [59, 36], [75, 60], [91, 40]];   // 깃발 자리 (% · 가로 · 세로)
    let curN = 1; for (const n of [1, 2, 3]) if (chUnlocked(n, 'e')) curN = n;
    const path = () => { let d = `M ${NODES[0][0] * 24} ${NODES[0][1] * 10}`; for (let i = 1; i < NODES.length; i++) { const [ax, ay] = NODES[i - 1], [bx, by] = NODES[i], mx = (ax + bx) / 2 * 24; d += ` C ${mx} ${ay * 10}, ${mx} ${by * 10}, ${bx * 24} ${by * 10}`; } return d; };
    const mapSvg = `<svg viewBox="0 0 2400 1000" preserveAspectRatio="none">
<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16324a"/><stop offset="1" stop-color="#0f2236"/></linearGradient>
<linearGradient id="land" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4b6b3f"/><stop offset="0.5" stop-color="#5d7a46"/><stop offset="1" stop-color="#6b6a45"/></linearGradient></defs>
<rect width="2400" height="1000" fill="url(#sea)"/>
<g stroke="#1d4363" stroke-width="3" fill="none" opacity="0.6"><path d="M0 120 q60 -14 120 0 t120 0 t120 0"/><path d="M1900 930 q60 -14 120 0 t120 0 t120 0"/><path d="M700 960 q60 -14 120 0 t120 0"/></g>
<path d="M-20 260 C 120 130, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170 L 2420 860 C 2240 930, 2060 880, 1880 920 S 1520 960, 1380 900 S 1060 950, 900 900 S 560 960, 400 910 S 120 930, -20 880 Z" fill="url(#land)" stroke="#2b3f25" stroke-width="10"/>
<path d="M-20 260 C 120 130, 330 170, 470 120 S 760 60, 900 140 S 1180 90, 1330 130 S 1640 60, 1800 120 S 2160 90, 2420 170" fill="none" stroke="#d8c48a" stroke-width="6" opacity="0.35"/>
<path d="M300 140 C 340 330, 520 420, 470 600 S 640 820, 700 930" fill="none" stroke="#2a5878" stroke-width="22" stroke-linecap="round"/><path d="M300 140 C 340 330, 520 420, 470 600 S 640 820, 700 930" fill="none" stroke="#3b7aa3" stroke-width="10" stroke-linecap="round"/>
<path d="M1540 120 C 1500 300, 1640 420, 1600 560 S 1700 780, 1680 930" fill="none" stroke="#2a5878" stroke-width="18" stroke-linecap="round"/><path d="M1540 120 C 1500 300, 1640 420, 1600 560 S 1700 780, 1680 930" fill="none" stroke="#3b7aa3" stroke-width="8" stroke-linecap="round"/>
<g fill="#7a7466" stroke="#4d483d" stroke-width="5">${[[760, 250], [830, 300], [700, 320], [1200, 760], [1280, 720], [1360, 780], [2050, 700], [2130, 740], [1960, 760], [1100, 230], [2250, 300]].map(([x, y]) => `<path d="M${x - 60} ${y + 50} L${x} ${y - 55} L${x + 60} ${y + 50} Z"/>`).join('')}</g>
<g fill="#ece7da" opacity="0.85">${[[760, 250], [830, 300], [700, 320], [1200, 760], [1280, 720], [1360, 780], [2050, 700], [2130, 740], [1960, 760], [1100, 230], [2250, 300]].map(([x, y]) => `<path d="M${x - 20} ${y - 18} L${x} ${y - 55} L${x + 20} ${y - 18} Z"/>`).join('')}</g>
<g fill="#3a5a2e">${[[140, 420], [180, 460], [110, 480], [620, 760], [660, 800], [960, 520], [1000, 560], [1440, 330], [1480, 300], [1830, 440], [1870, 480], [2300, 560], [2260, 600], [380, 820]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="34"/>`).join('')}</g>
<path d="${path()}" fill="none" stroke="#2b2316" stroke-width="30" stroke-linecap="round" opacity="0.55"/>
<path d="${path()}" fill="none" stroke="#e8d7a6" stroke-width="12" stroke-linecap="round" stroke-dasharray="26 22"/>
${[[1, 192, 640], [2, 600, 380], [3, 1008, 620]].map(([n, x, y]) => `<g fill="#cfc6b4" stroke="#5a5244" stroke-width="4" opacity="0.9">${[[-70, -40, 36, 50], [-30, -70, 40, 80], [16, -50, 34, 60], [56, -30, 30, 40]].map(([dx, dy, w, h]) => `<rect x="${x + dx}" y="${y + dy - 60}" width="${w}" height="${h}"/>`).join('')}</g>`).join('')}
</svg>`;
    const draw = () => {
      let h = `<div class="top"><div class="gp">${CH_GENE_I(20)}<span>${CH_SV.genes}</span></div><div class="ttl">러닝데드</div><button class="tb" data-ug="1" aria-label="성장">💪</button><button class="tb" data-set="1" aria-label="설정">⚙️</button></div><div class="map"><div class="in">${mapSvg}`;
      NODES.forEach(([x, y], i) => {
        const n = i + 1;
        if (n > 3) { h += `<div class="nd soon" style="left:${x}%;top:${y}%"><div class="fl">준비 중</div></div>`; return; }
        const ok = chUnlocked(n, 'e');
        h += `<button class="nd ${ok ? '' : 'lk'} ${n === curN ? 'cur' : ''}" data-st="${n}" style="left:${x}%;top:${y}%"><div class="fl">${ok ? n : '🔒'}</div><div class="nm">${CH_STG_INFO[n].nm}</div><div class="sr">${stars(n)}</div><div class="md">🎖 ${medals(n)}/6</div></button>`;
      });
      h += `</div></div><div class="hint">← 지도를 밀어서 둘러보기 →</div>`;
      ov.innerHTML = h;
      const m = ov.querySelector('.map'), nd = ov.querySelector(`.nd[data-st="${curN}"]`); if (m && nd) requestAnimationFrame(() => { m.scrollLeft = Math.max(0, nd.offsetLeft - m.clientWidth / 2); });
    };
    let sheet = null;
    const closeSheet = () => { if (sheet) { sheet.remove(); sheet = null; } };
    const openSheet = (inner, onClick) => { closeSheet(); sheet = document.createElement('div'); sheet.className = 'bd'; sheet.innerHTML = `<div class="sh">${inner}</div>`; ov.appendChild(sheet);
      sheet.addEventListener('click', (e) => { if (e.target === sheet) { closeSheet(); return; } const b = e.target.closest('button'); if (!b || b.disabled) return; if (b.classList.contains('x')) { closeSheet(); return; } onClick(b); }); };
    const stageSheet = (n, d) => {
      const I = CH_STG_INFO[n], key = n + d, ok = chUnlocked(n, d);
      const tab = (q) => { const okq = chUnlocked(n, q); return `<button data-d="${q}" class="${q === d ? 'sel' : ''} ${q}">${okq ? '' : '🔒 '}${CH_DIF_NM[q]}<small>${cleared(n + q) ? '★ 클리어' : '&nbsp;'}</small></button>`; };
      let h = `<div class="hd"><div><div class="t1">스테이지 ${n}</div><div class="t2">${I.nm}</div></div><button class="x">✕</button></div><div class="ds">${I.ds}</div><div class="tabs">${['e', 'n', 'h'].map(tab).join('')}</div>`;
      h += `<div class="cd"><div class="k">클리어 조건</div><div class="v">${chClrText(d)}</div></div>`;
      if (d === 'h') h += `<div class="cd bs"><div class="k">보스</div><img src="${CH_BOSS_IMG[I.boss[2]]}" alt=""><div class="bn">${I.boss[0]}</div><div class="bt">${I.boss[1]}<br>보스가 살아 있는 동안 15초마다 군인 2명이 더 온다.</div></div>`;
      h += `<div class="cd"><div class="k">적</div><div class="v" style="font-size:14px">${n > 1 ? `모든 적 체력 · 공격력 +${(n - 1) * 20}%<br>` : ''}샷건 · 사각 로봇 섞임 · 건널목 터렛: 경보 '${CH_LVN[CH_MIX_T[d] - 1]}'부터</div></div>`;
      const g = CH_CLR_G[d], got = cleared(key);
      h += `<div class="cd"><div class="k">보상</div><div class="rw ${got ? 'got' : ''}"><div class="gi">${CH_GENE_I()}${g}</div><div class="lb">${CH_DIF_NM[d]} 첫 클리어${got ? ' · 받음 ✓' : ''}<small>처음 한 번만</small></div></div><div class="rw"><div class="gi">${CH_GENE_I()}1</div><div class="lb">적 하나 없앨 때마다<small>죽어도 남는다</small></div></div></div>`;
      h += `<div class="cd"><div class="k">서브 미션 · 클리어해야 받는다</div>${[0, 1].map((i) => { const dn = !!CH_SV.sub[key + i]; return `<div class="rw ${dn ? 'got' : ''}"><div class="ck ${dn ? 'on' : ''}">${dn ? '✓' : ''}</div><div class="lb">${chMisTxt(d, i)}</div><div class="gi">${CH_GENE_I()}100</div></div>`; }).join('')}</div>`;
      h += ok ? `<button class="go" data-go="1">시작하기</button>` : `<button class="go" disabled>🔒 ${chLockWhy(n, d)}</button>`;
      openSheet(h, (b) => { if (b.dataset.d) stageSheet(n, b.dataset.d); else if (b.dataset.go) { CH_UPK.hp = 1 + 0.01 * CH_SV.up.hp; CH_UPK.ahp = 1 + 0.01 * CH_SV.up.ahp; CH_UPK.atk = 1 + 0.01 * CH_SV.up.atk; ov.remove(); go(n, d); } });
      const t = sheet.querySelector('.sh'); if (t) t.scrollTop = 0;
    };
    const upSheet = () => {
      const row = (k, ic, nm, ds) => { const v = CH_SV.up[k]; return `<div class="ug"><div class="ic">${ic}</div><div class="tx"><div class="n1">${nm}</div><div class="n2">${ds}</div></div><div class="pc">+${v}%</div><button class="ub" data-up="${k}" ${CH_SV.genes < CH_UP_COST ? 'disabled' : ''}>+1% ${CH_GENE_I(14)}${CH_UP_COST}</button></div>`; };
      openSheet(`<div class="hd"><div><div class="t1">유전자로 강해지기</div><div class="t2">성장</div></div><button class="x">✕</button></div><div class="ds">한 번 누를 때마다 기본값의 1%씩 오른다. 끝없이 올릴 수 있다.<br>보유 유전자 ${CH_GENE_I(14)} <b>${CH_SV.genes}</b></div>` +
        row('hp', '❤️', '내 체력', '내 최대 체력 · 혈액팩 회복량') + row('ahp', '🧟', '동료 체력', '동료 좀비 최대 체력') + row('atk', '⚔️', '공격력', '나 · 동료 · 덩치 · 히드라 · 산성 · 끈끈이 피해'),
        (b) => { if (b.dataset.up && CH_SV.genes >= CH_UP_COST) { CH_SV.genes -= CH_UP_COST; CH_SV.up[b.dataset.up]++; chSave(); draw(); upSheet(); } });
    };
    const setSheet = () => {
      openSheet(`<div class="hd"><div><div class="t2">설정</div></div><button class="x">✕</button></div><div style="height:12px"></div><button class="sb" data-tut="1">튜토리얼 다시 하기<br><small style="font-size:11px;color:#8fa0b8">처치 유전자만 받는다</small></button><div style="height:18px"></div><button class="sb rst" data-rst="1">초기화 (모든 기록 삭제)</button>`,
        (b) => {
          if (b.dataset.tut) { ov.remove(); tut(); return; }
          if (b.dataset.rst) {
            if (!b.classList.contains('on')) { b.classList.add('on'); b.textContent = '정말 초기화? 한 번 더 누르기'; setTimeout(() => { if (b.isConnected) { b.classList.remove('on'); b.textContent = '초기화 (모든 기록 삭제)'; } }, 3000); return; }
            try { localStorage.removeItem('rd_genes'); localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1 })); window.name = ''; } catch (e) {}
            location.reload();
          }
        });
    };
    ov.addEventListener('click', (e) => {
      if (sheet && sheet.contains(e.target)) return;
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.ug) { upSheet(); return; }
      if (b.dataset.set) { setSheet(); return; }
      if (b.dataset.st) { const n = +b.dataset.st; if (!chUnlocked(n, 'e')) { b.animate([{ transform: 'translate(-50%,-50%)' }, { transform: 'translate(-46%,-50%)' }, { transform: 'translate(-54%,-50%)' }, { transform: 'translate(-50%,-50%)' }], { duration: 250 }); return; }
        const d = ['h', 'n', 'e'].find((q) => chUnlocked(n, q) && !cleared(n + q)) || ['h', 'n', 'e'].find((q) => chUnlocked(n, q)); stageSheet(n, d); }
    });
    draw(); document.body.appendChild(ov);
  }
""".replace('__BOSSIMG__', json.dumps(IMG))

old_out = between("  function chOutgame(go, tut) {", "  const CH_PICK = window.__map ||")
rep(old_out, OUT)
rep("""    try { window.name = ''; } catch (e) {}
    if (!CH_SV.tut) { res('t'); return; }
    chOutgame((st, d) => { CH_STG = st; CH_DIF = d; res('m'); }, () => res('t'));""",
"""    let nm = ''; try { nm = window.name || ''; window.name = ''; } catch (e) {}
    if (!CH_SV.tut || nm === 'rd-run:t') { res('t'); return; }
    if (nm.startsWith('rd-run:')) { const [, a, b] = nm.split(':'); if (+a >= 1 && +a <= 3 && CH_DIF_NM[b] && chUnlocked(+a, b)) { CH_STG = +a; CH_DIF = b; res('m'); return; } }   // c517: 결과 창 '다시 하기'
    chOutgame((st, d) => { CH_STG = st; CH_DIF = d; res('m'); }, () => res('t'));""")
rep("  const CH_MIS = (CH_RUN ? { e: [[3, 6], 30], n: [[4, 7], 50], h: [[5, 8], 70] }[CH_DIF] : [[3, 6], 30]);", "  const CH_MIS = CH_MIS_T[CH_RUN ? CH_DIF : 'e'];   // c517: 표는 위 (아웃게임과 같은 것)")

# 결과 창
old_res = between("  function chRunResult(win) {", "  function chMadRoll0(c) {")
NEWRES = r"""  function chRunResult(win) {                 // c505 · c517: 클리어 · 실패 — 보상 정산 (아이콘 줄) → 지도로 · 다시 하기
    if (chRunOver) return; chRunOver = true; paused = true; stopInput();
    const R = []; let add = 0;
    if (CH_TUT) { if (win && !CH_SV.tut) { add += 100; R.push(['🎓', '튜토리얼 첫 클리어', 100, true]); } if (win) CH_SV.tut = true; }
    else if (CH_RUN && win) {
      const key = CH_STG + CH_DIF;
      if (!CH_SV.clr[key]) { const g = CH_CLR_G[CH_DIF]; add += g; R.push(['★', CH_DIF_NM[CH_DIF] + ' 첫 클리어', g, true]); CH_SV.clr[key] = 1; } else R.push(['★', CH_DIF_NM[CH_DIF] + ' 클리어 (이미 받음)', 0, false]);
      chMis.forEach((m, i) => { const k = key + i; if (m.done && !CH_SV.sub[k]) { add += 100; R.push(['🎖', '서브 미션 ' + (i + 1), 100, true]); CH_SV.sub[k] = 1; } });
    }
    CH_SV.genes += add; chSave();
    const G = CH_GENE_I(16);
    const ov = document.createElement('div'); ov.id = 'rres';
    ov.style.cssText = 'position:absolute;inset:0;z-index:70;background:rgba(8,10,14,0.94);color:#fff;font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:20px;box-sizing:border-box';
    const row = (ic, nm, g, nw) => `<div style="display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:12px;background:${nw ? '#22303f' : '#1a2029'};margin-top:6px"><span style="width:26px;text-align:center;font-size:18px">${ic}</span><span style="flex:1;font:800 14px system-ui">${nm}${nw ? ' <b style="color:#ffd34d;font-size:11px">NEW</b>' : ''}</span><span style="display:flex;align-items:center;gap:4px;font:900 16px system-ui">${G}${g}</span></div>`;
    let h = `<div style="font:900 40px system-ui;color:${win ? '#ffd34d' : '#ff5a5a'};text-shadow:0 0 18px ${win ? 'rgba(255,200,60,0.6)' : 'rgba(255,60,60,0.5)'}">${win ? '클리어!' : '실패'}</div><div style="font:800 14px system-ui;color:#9aa6b8">${CH_TUT ? '튜토리얼' : '스테이지 ' + CH_STG + ' · ' + CH_STG_INFO[CH_STG].nm + ' · ' + CH_DIF_NM[CH_DIF]}</div>`;
    h += `<div style="width:min(340px,88vw);margin-top:10px">` + row('🧟', '적 처치 · 감염', chRunGenes, false) + R.map(([ic, nm, g, nw]) => row(ic, nm, g, nw)).join('');
    if (CH_RUN) h += `<div style="margin-top:12px;font:900 11px system-ui;color:#8fa0b8;letter-spacing:1px">서브 미션${win ? '' : ' · 클리어해야 받는다'}</div>` + [0, 1].map((i) => `<div style="display:flex;align-items:center;gap:8px;margin-top:5px;font:700 13px system-ui;color:${chMis[i].done ? '#fff' : '#8a93a3'}"><span style="width:20px;height:20px;border-radius:6px;border:2px solid ${chMis[i].done ? '#5fd38f' : '#4a5668'};background:${chMis[i].done ? '#2e9e5b' : 'transparent'};display:flex;align-items:center;justify-content:center;font-size:12px">${chMis[i].done ? '✓' : ''}</span>${chMisTxt(CH_DIF, i)}</div>`).join('');
    h += `<div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid #3a4250;margin-top:14px;padding-top:10px;font:900 15px system-ui"><span>보유 유전자</span><span style="display:flex;align-items:center;gap:5px">${G}${CH_SV.genes}</span></div></div>`;
    h += `<div style="display:flex;gap:10px;margin-top:16px;width:min(340px,88vw)"><button data-a="map" style="flex:1;font:900 17px system-ui;color:#fff;background:#2a3340;border:none;border-radius:14px;padding:13px 0">지도로</button><button data-a="again" style="flex:1;font:900 17px system-ui;color:#2b1400;background:linear-gradient(#ffb547,#f07b12);border:none;border-radius:14px;padding:13px 0">다시 하기</button></div>`;
    ov.innerHTML = h; stage.appendChild(ov);
    ov.addEventListener('pointerdown', (e) => e.stopPropagation());   // 조이스틱이 손가락을 가져가지 않게
    ov.addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; try { window.name = b.dataset.a === 'again' ? (CH_TUT ? 'rd-run:t' : 'rd-run:' + CH_STG + ':' + CH_DIF) : ''; } catch (er) {} location.reload(); });
  }
"""
rep(old_res, NEWRES)

# 시작 목표 창 — 본편은 클리어 조건 + 서브 미션
rep("(CH_TUT ? '이곳을 탈출하십시오' : '모든 경찰서를 파괴해라') + '</div><div class=\"g3\">' + stations.map(() => '<span>!</span>').join('') + '</div>",
    "(CH_TUT ? '이곳을 탈출하십시오' : CH_RUN ? (CH_DIF === 'h' ? CH_STG_INFO[CH_STG].boss[0] + ' 물리치기' : '특공대 ' + (CH_DIF === 'e' ? 3 : 4) + '번 물리치기') : '모든 경찰서를 파괴해라') + '</div>' + (CH_RUN ? '<div class=\"g4\">' + chClrText(CH_DIF) + '<div class=\"g5\">서브 미션</div>' + [0, 1].map((i) => '<div>· ' + chMisTxt(CH_DIF, i) + '</div>').join('') + '</div>' : '') + '<div class=\"g3\">' + (CH_RUN ? [] : stations).map(() => '<span>!</span>').join('') + '</div>")
rep("  function showGoal() {", """  if (CHAPTER) { const st = document.createElement('style'); st.textContent = '#goal .g4{margin:12px auto 0;width:min(330px,86vw);font:800 14px/1.5 system-ui,sans-serif;color:#e8ecf2;background:rgba(10,14,20,0.75);border:1px solid rgba(255,255,255,0.15);border-radius:12px;padding:10px 12px;text-align:left;text-shadow:none}#goal .g5{margin-top:8px;font:900 11px system-ui;color:#ffd34d;letter-spacing:1px}#goal .g2{font-size:28px!important}'; document.head.appendChild(st); }   // c517
  function showGoal() {""")
rep("for (const k of ['citizen', 'guard', 'attacker', 'police', 'station', 'soldier', 'sniper']) tutSeen[k] = true; }", "for (const k of ['citizen', 'guard', 'attacker', 'police', 'station', 'soldier', 'sniper']) tutSeen[k] = true; }\n    if (CH_RUN) goalShown = false;   // c517: 본편은 판마다 목표 창 (클리어 조건 · 서브 미션)")
rep("'#stars .obj{margin-top:26px;font:800 11px/1.2 system-ui,sans-serif;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,0.9);white-space:nowrap}' +",
    "'#stars .obj{display:inline-block;margin-top:5px;padding:4px 10px;border-radius:10px;background:rgba(8,12,18,0.55);font:800 12px/1.35 system-ui,sans-serif;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,0.9);white-space:nowrap}#stars .obj:empty{display:none}#stars .obj .cd{font-size:11px;color:#ffd34d}#stars .obj .cd .bosscd{color:#ff6b6b}#stars .obj .cd .bosscd i{font-style:normal}' +   /* c517: 목표 + 카운트다운 = 한 상자 */")
rep("    const t = chObjText(); if (o.textContent !== t) o.textContent = t;", "    const t = chObjText() + (chSf.cdS ? '<div class=\"cd\">' + chSf.cdS + '</div>' : ''); if (o.dataset.t !== t) { o.dataset.t = t; o.innerHTML = t; }   // c517: 카운트다운도 같은 상자 안")
rep("    if (s !== chSf.shown) { chSf.shown = s; chSfEl.innerHTML = s; chSfEl.style.display = s ? 'block' : 'none'; }", "    if (CH_RUN) { chSf.cdS = s; if (chSf.shown !== '') { chSf.shown = ''; chSfEl.style.display = 'none'; } }   // c517: 본편 — 카운트다운은 목표 상자 안에\n    else if (s !== chSf.shown) { chSf.shown = s; chSfEl.innerHTML = s; chSfEl.style.display = s ? 'block' : 'none'; }")
pathlib.Path('c517_patch.py').write_text('C517_R = ' + repr(R) + '\n')
print(len(R))
