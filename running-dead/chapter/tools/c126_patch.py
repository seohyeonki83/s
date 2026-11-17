# c126: 특공대 시간표 — 처음 120초, 그 뒤로 5초씩 줄어든다 (120 · 235 · 345 · 450 · 550 보스) · 글자 '다음 특공대 출동까지' · 보스는 경보처럼 세게
C126_R = [
 ("for (let i = 0; i < n; i++) t += 100 - 5 * i; return t; };",
  "for (let i = 0; i < n; i++) t += 120 - 5 * i; return t; };   /* c126: 120초부터 5초씩 → 120 · 235 · 345 · 450 · 550(보스) */\n  { const st = document.createElement('style'); st.textContent = '@keyframes bosscd { 0% { transform: scale(1.22); text-shadow: 0 0 18px #ff2a00, 0 0 40px #ff2a00, 0 2px 4px #000; color: #fff; } 35% { transform: scale(1); color: #ff3a2a; text-shadow: 0 0 8px rgba(255,40,0,0.8), 0 2px 4px #000; } 100% { transform: scale(1); color: #ff3a2a; text-shadow: 0 0 8px rgba(255,40,0,0.8), 0 2px 4px #000; } } .bosscd { display: inline-block; font: 900 19px/1 system-ui, sans-serif; letter-spacing: 0.5px; color: #ff3a2a; animation: bosscd 1s ease-out both; } .bosscd i { font-style: normal; display: inline-block; margin: 0 6px; padding: 1px 7px 2px; border-radius: 5px; background: #ff3a2a; color: #1a0500; text-shadow: none; }'; document.head.appendChild(st); }"),
 ("s = chSf.n < 4 ? '특공대 도착까지 ' + left + '초' : '<b style=\"color:#ff4a3a\">보스</b> 군부대 도착까지 ' + left + '초';",
  "s = chSf.n < 4 ? '다음 특공대 출동까지 ' + left + '초' : '<span class=\"bosscd\"><i>!</i>보스 출동까지 ' + left + '초<i>!</i></span>';   /* c126 */"),
 ("chSfEl.style.animation = 'sfpop 1.9s ease-in-out';", "chSfEl.style.animation = (chSf.n >= 4 ? 'sfpopb' : 'sfpop') + ' 1.9s ease-in-out';   /* c126: 보스 글자는 커서 덜 키운다 */"),
 ("' @keyframes wpnpop {", "' @keyframes sfpopb { 0% { transform: translateY(30vh) scale(1.5); opacity: 0; } 10% { transform: translateY(30vh) scale(1.5); opacity: 1; } 60% { transform: translateY(30vh) scale(1.5); opacity: 1; } 100% { transform: none; opacity: 1; } } @keyframes wpnpop {"),
]
