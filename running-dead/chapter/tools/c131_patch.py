# c131: 길거리를 배회하는 빨강 · 경찰 10% 줄임 (없앤다)
C131_R = [
 ("    G.types.forEach((t, i) => {\n      let x = p[0], z = p[1];", "    G.types.forEach((t, i) => {\n      if (t === 'vig' && Math.random() < 0.1) return;   // c131: 길거리 빨강 열에 하나는 안 나온다\n      let x = p[0], z = p[1];"),
 ("k < Math.round(CH_COPS * CH_ONE_K * 0.8); k++)", "k < Math.round(CH_COPS * CH_ONE_K * 0.8 * 0.9); k++)   /* c131: 10% 더 줄임 */"),
]
