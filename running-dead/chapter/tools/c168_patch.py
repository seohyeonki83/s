# c168: 장갑차 — 크기 20% 줄임 · 벽 부수는 힘 30% 더 · 보인 뒤 속도 2배 (보통 차의 절반) · 사거리 = 경찰 (7.2칸)
#       보스 뒤 15초 출동 = 군인 2 · 세 번에 한 번은 저격수 1 + 군인 1. 저격수와 따로 온 군인은 장갑차를 호위 · 저격수와 같이 온 군인은 저격수를 (저격수가 죽으면 장갑차)
#       보스 테스트 동료 70명
C168_R = [
 ("CH_TK_K = MIL_K * 2,", "CH_TK_K = MIL_K * 2 * 0.8,   /* c168: 20% 작게 */"),
 ("CH_TK_WALL_T = 2.4,", "CH_TK_WALL_T = 2.4 / 1.3,   /* c168: 벽 부수는 힘 30% 더 */"),
 ("    const R = SIGHT * 1.1; let best = null, bd = R;", "    const R = SIGHT; let best = null, bd = R;   /* c168: 사거리 = 경찰 */"),
 ("/ (car.tkSeen ? 4 : 1) * (car.goo ? 0.8 : 1);", "/ (car.tkSeen ? 2 : 1) * (car.goo ? 0.8 : 1);   /* c168: 보인 뒤 속도 2배 (보통 차의 절반) */"),
 ("teamWait.push({ comp: [S_, G_, G_], t: 0, first: false, seg: teamSeg(), tk: true });", "chSf.wn = (chSf.wn || 0) + 1; teamWait.push({ comp: chSf.wn % 3 === 0 ? [S_, G_] : [G_, G_], t: 0, first: false, seg: teamSeg(), tk: true });   /* c168: 군인 2 · 세 번에 한 번 저격수 1 + 군인 1 */"),
 ("      if (CHAPTER && chTkMark) c.tkU = true;", "      if (CHAPTER && chTkMark) { c.tkU = true; c.tkE = true; }   // c168: 장갑차 호위 (저격수와 같이 온 군인은 저격수 먼저)"),
 ("chBTdone = false;   /* c166 */", "chBTdone = false; chSf.wn = 0;   /* c166 · c168 */"),
 ("for (let i = 0, t = 0; i < 60 && t < 6000; t++) {   // c167: 동료 60명", "for (let i = 0, t = 0; i < 70 && t < 7000; t++) {   // c168: 동료 70명"),
 ("r = 1.2 + Math.random() * 5.0,", "r = 1.2 + Math.random() * 5.5,"),
 ("'큰 맵 · 동료 60 · 무적 · 바로 보스 출동'", "'큰 맵 · 동료 70 · 무적 · 바로 보스 출동'"),
]
