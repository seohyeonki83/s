# c98: 처음 길거리 경찰 5분의 1 줄임 · 노랑의 10%는 하양, 주황의 10%는 노랑, 빨강의 10%는 주황으로
C98_R = [
 ("for (let k = 0; k < Math.round(CH_COPS * CH_ONE_K); k++)", "for (let k = 0; k < Math.round(CH_COPS * CH_ONE_K * 0.8); k++)   /* c98: 길거리 경찰 5분의 1 줄임 */"),
 ("  function chPut(x, z, area, type, B) {\n", "  function chPut(x, z, area, type, B) {\n    if (Math.random() < 0.1) type = type === 'guard' ? '' : type === 'attacker' ? 'guard' : type === 'vig' ? 'attacker' : type;   // c98: 열에 하나는 한 단계 약한 색으로 (노랑 → 하양 · 주황 → 노랑 · 빨강 → 주황)\n"),
]
