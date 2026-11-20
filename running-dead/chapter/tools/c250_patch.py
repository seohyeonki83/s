# c250: 특공대 1~4차 구성 (걸어서 W · 군인차 C)
#   1차: W 저격수1+군인3 · 2차: W 저격수1+군인2, C 저격수1+군인2 · 3차: W 저격수1+군인2, C 저격수1+군인2, C 군인2 · 4차: W 저격수1+군인2, C 저격수1+군인3, C 저격수1+군인3
C250_R = [
 ("""    if (i < 3) { const sq = i === 0 ? [[S_, G_, G_, G_]] : i === 1 ? [[S_, G_, G_], [S_, G_]] : [[S_, G_, G_], [S_, G_], [S_, G_]];   /* c249: 4분의 1 줄임 */
      sq.forEach((c, k) => teamWait.push({ comp: c, t: k * 3, first: false, seg, hold: true })); return; }
    if (i < 5) { teamWait.push({ car: [S_, G_, G_, S_, G_], t: 0, seg, hold: true }, { car: [S_, G_, S_, G_], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });   /* c249 */ return; }""",
  """    if (i < 4) {   // c250: 차례마다 [걸어서 'W' | 군인차 'C', 구성]
      const P = [[['W', [S_, G_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_]], ['C', [G_, G_]]], [['W', [S_, G_, G_]], ['C', [S_, G_, G_, G_]], ['C', [S_, G_, G_, G_]]]][i];
      P.forEach(([m, c], k) => teamWait.push(m === 'W' ? { comp: c, t: k * 3, first: false, seg, hold: true } : { car: c, t: k * 3, seg: k ? chTeamSeg2(seg) : seg, hold: true }));
      return;
    }"""),
]
