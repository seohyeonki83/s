# c193: 건물 지붕은 한 번 열리면(좀비가 들어가거나 열린 문 너머로 보면) 그 판 내내 열려 있다 — 랜드마크 · 집 · 창고 다. 미니맵 아이콘은 그대로 (금고를 깨면 X)
C193_R = [
 ("      B.open = B.tkCut || eyeSp.has(B) || B.doors.some(doorSeen);   /* c154 */", "      B.open = B.everOpen || B.tkCut || eyeSp.has(B) || B.doors.some(doorSeen);   /* c154 */ if (CHAPTER && B.open) B.everOpen = true;   /* c193: 한 번 열리면 계속 */"),
 ("chBTdone = false; chSf.wn = 0;   /* c166 · c168 */", "chBTdone = false; chSf.wn = 0; for (const B of buildings) B.everOpen = false;   /* c166 · c168 · c193 */"),
]
