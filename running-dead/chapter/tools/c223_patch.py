# c223: 특공대 구성 — 1차: 저격수 1 + 군인 4 (군인 전부 그 저격수 호위) · 2차: (저격수 1 + 군인 3) + (저격수 1 + 군인 2) 분대마다 제 저격수
#   · 3차: (저격수 1 + 군인 2) × 3분대 · 4차: 군인 차 2대, 차마다 저격수 2 + 군인 4 (저격수마다 군인 2)
C223_R = [
 ("""    if (i < 3) { const sq = i === 0 ? [[S_, G_, G_]] : i === 1 ? [[S_, G_, G_, G_]] : [[S_, G_, G_], [S_, G_, G_]];
      sq.forEach((c, k) => teamWait.push({ comp: c, t: k * 3, first: false, seg, hold: true })); return; }
    if (i < 5) { teamWait.push({ car: [S_, G_, G_, G_, S_, G_, G_], t: 0, seg, hold: true }); return; }""",
  """    if (i < 3) { const sq = i === 0 ? [[S_, G_, G_, G_, G_]] : i === 1 ? [[S_, G_, G_, G_], [S_, G_, G_]] : [[S_, G_, G_], [S_, G_, G_], [S_, G_, G_]];   /* c223 */
      sq.forEach((c, k) => teamWait.push({ comp: c, t: k * 3, first: false, seg, hold: true })); return; }
    if (i < 5) { teamWait.push({ car: [S_, G_, G_, S_, G_, G_], t: 0, seg, hold: true }, { car: [S_, G_, G_, S_, G_, G_], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true }); return; }   /* c223: 2대 · 차마다 군인 1명 빼고 */"""),
]
