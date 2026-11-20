# c267: 경계 시간 — 수상함 전 5~6초 · 수상함 뒤 감염 3명 더(누적 8명)까지 3초 · 그 뒤로 원래대로 (하양·노랑·주황·빨강·경찰 모두)
C267_R = [
 ("  function enterAlert(c) { c.state = 'alert'; c.timer = rand(...ALERT_TIME)", "  function enterAlert(c) { c.state = 'alert'; c.timer = CHAPTER && stars < 1 ? rand(5, 6) : CHAPTER && deaths < STAR_AT[0] + 3 ? 3 : rand(...ALERT_TIME)   /* c267 */"),
 ("* (CHAPTER && stars < 1 ? 5 : 1); }   /* c264: 주황도 경찰과 같은 경계 시간 */", "; }   /* c264: 주황도 경찰과 같은 경계 시간 · c267: 수상함 전·직후는 위 고정 초 */"),
]
