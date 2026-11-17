# c127: 카운트다운이 가운데 크게 떠 있는 동안은 뒤에 검은 판 — 제자리에 박힐 때 사라진다
C127_R = [
 ("position:absolute;left:0;right:0;top:calc(66px + env(safe-area-inset-top, 0px));z-index:4;pointer-events:none;text-align:center;",
  "position:absolute;left:0;right:0;width:fit-content;margin:0 auto;padding:6px 12px;border-radius:9px;white-space:nowrap;top:calc(60px + env(safe-area-inset-top, 0px));z-index:4;pointer-events:none;text-align:center;"),
 ("chSfEl.style.animation = (chSf.n >= 4 ? 'sfpopb' : 'sfpop') + ' 1.9s ease-in-out';", "chSfEl.style.animation = (chSf.n >= 4 ? 'sfpopb' : 'sfpop') + ' 1.9s ease-in-out, sfplate 1.9s ease-in-out';"),
 ("' @keyframes sfpopb {", "' @keyframes sfplate { 0% { background: rgba(0,0,0,0.85); } 62% { background: rgba(0,0,0,0.85); } 100% { background: rgba(0,0,0,0); } } @keyframes sfpopb {"),
 ("translateY(30vh) scale(2.3)", "translateY(30vh) scale(1.9)", 3),   # 좁은 화면(390)에서도 안 잘리게
]
