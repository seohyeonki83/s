import pathlib
s = pathlib.Path('c532.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 체크박스: 메달 표시 빼고 3칸 크게
rep('<div class="md">🎖 ${medals(n)}/6</div>', '')
rep("#outg .cb{width:17px;height:17px;border-radius:5px;", "#outg .cbx{gap:5px!important;margin-top:2px}#outg .cb{width:24px;height:24px;border-radius:6px;font-size:16px!important;")
# 특공대 · 보스 출동 — 게임을 멈추고 강하게
rep("""    squadAnim = true;
    const el = document.createElement('div'); el.className = 'rank squad';
    el.innerHTML = CHAPTER && chBanner.shift() === 'boss' ? '<div class="rbox"><div class="rt">보스 출동</div></div>' : '<div class="rbox"><div class="rt">특공대 출동</div></div>';
    stage.appendChild(el);""", """    squadAnim = true;
    const boss = CHAPTER && chBanner.shift() === 'boss';
    const el = document.createElement('div'); el.className = CHAPTER ? 'sqx' + (boss ? ' boss' : '') : 'rank squad';
    if (CHAPTER) {   // c533: 출동 연출 — 게임이 멈추고 화면 전체 경보 (빨간 번쩍임 · 경고 띠 · 글씨가 쾅 · 흔들림)
      if (!document.getElementById('sqxst')) { const st = document.createElement('style'); st.id = 'sqxst'; st.textContent = '.sqx{position:absolute;inset:0;z-index:30;pointer-events:none;overflow:hidden;font-family:system-ui,sans-serif}.sqx .fl{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(255,40,40,0) 30%,rgba(200,0,0,0.75) 100%)}.sqx .dk{position:absolute;inset:0;background:rgba(0,0,0,0.45)}.sqx .tp{position:absolute;left:-20%;right:-20%;height:34px;background:repeating-linear-gradient(-45deg,#111 0 22px,#ffcc00 22px 44px);box-shadow:0 0 18px rgba(0,0,0,0.7)}.sqx .t1{top:calc(30% - 70px);transform:rotate(-4deg)}.sqx .t2{top:calc(30% + 96px);transform:rotate(-4deg)}.sqx .tx{position:absolute;left:0;right:0;top:30%;text-align:center}.sqx .tx b{display:block;font:900 54px/1.05 system-ui,sans-serif;color:#ff3b30;letter-spacing:3px;text-shadow:0 0 22px rgba(255,40,40,0.95),0 4px 0 #3a0000,0 0 2px #fff}.sqx .tx i{display:block;margin-top:8px;font:800 17px system-ui,sans-serif;font-style:normal;color:#fff;text-shadow:0 2px 6px #000}.sqx.boss .tx b{font-size:64px;color:#ff2a2a}'; document.head.appendChild(st); }
      el.innerHTML = `<div class="dk"></div><div class="fl"></div><div class="tp t1"></div><div class="tp t2"></div><div class="tx"><b>${boss ? '보스 출동' : '특공대 출동'}</b><i>${boss ? (CH_RUN && CH_STG_INFO[CH_STG] ? CH_STG_INFO[CH_STG].boss[0] + '가 온다' : '보스가 온다') : '특공대가 이쪽으로 온다'}</i></div>`;
      const wasP = paused; paused = true; stopInput(); el.dataset.wp = wasP ? '1' : '';
      const D = boss ? 2800 : 2200;
      el.querySelector('.fl').animate([{ opacity: 0 }, { opacity: 1 }, { opacity: 0.25 }, { opacity: 1 }, { opacity: 0.25 }, { opacity: 1 }, { opacity: 0.2 }, { opacity: 0 }], { duration: D, fill: 'forwards' });
      el.querySelector('.dk').animate([{ opacity: 0 }, { opacity: 1, offset: 0.1 }, { opacity: 1, offset: 0.85 }, { opacity: 0 }], { duration: D, fill: 'forwards' });
      for (const [q, dx] of [['.t1', -1], ['.t2', 1]]) el.querySelector(q).animate([{ transform: `rotate(-4deg) translateX(${dx * 120}%)` }, { transform: 'rotate(-4deg) translateX(0)', offset: 0.15 }, { transform: `rotate(-4deg) translateX(${-dx * 8}%)`, offset: 0.85 }, { transform: `rotate(-4deg) translateX(${-dx * 120}%)` }], { duration: D, easing: 'ease-in-out', fill: 'forwards' });
      el.querySelector('.tx').animate([{ transform: 'scale(3)', opacity: 0 }, { transform: 'scale(0.92)', opacity: 1, offset: 0.12 }, { transform: 'scale(1.04)', offset: 0.18 }, { transform: 'scale(1)', offset: 0.25 }, { transform: 'scale(1)', opacity: 1, offset: 0.85 }, { transform: 'scale(1.3)', opacity: 0 }], { duration: D, easing: 'ease-out', fill: 'forwards' });
      stage.animate([{ transform: 'translate(0,0)' }, { transform: 'translate(-10px,7px)', offset: 0.13 }, { transform: 'translate(9px,-8px)', offset: 0.16 }, { transform: 'translate(-7px,-5px)', offset: 0.19 }, { transform: 'translate(5px,6px)', offset: 0.22 }, { transform: 'translate(0,0)', offset: 0.26 }, { transform: 'translate(0,0)' }], { duration: D });
      if (navigator.vibrate) try { navigator.vibrate(boss ? [80, 60, 80, 60, 120] : [70, 50, 70]); } catch (e) {}
      setTimeout(() => { if (!el.dataset.wp && !acqOpen && !lvOpen && !menuOv) { paused = false; last = 0; } }, D);
    } else el.innerHTML = '<div class="rbox"><div class="rt">특공대 출동</div></div>';
    stage.appendChild(el);""")
pathlib.Path('c533_patch.py').write_text('C533_R = ' + repr(R) + '\n')
print(len(R))
