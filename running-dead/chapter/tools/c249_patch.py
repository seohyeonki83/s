# c249: 특공대 1~4차 전체 양 4분의 1 줄임 (33명 → 25명) — 1차 4 · 2차 5 · 3차 7 · 4차 9 (보스전은 그대로)
C249_R = [
 ("const sq = i === 0 ? [[S_, G_, G_, G_, G_]] : i === 1 ? [[S_, G_, G_, G_], [S_, G_, G_]] : [[S_, G_, G_], [S_, G_, G_], [S_, G_, G_]];   /* c223 */",
  "const sq = i === 0 ? [[S_, G_, G_, G_]] : i === 1 ? [[S_, G_, G_], [S_, G_]] : [[S_, G_, G_], [S_, G_], [S_, G_]];   /* c249: 4분의 1 줄임 */"),
 ("teamWait.push({ car: [S_, G_, G_, S_, G_, G_], t: 0, seg, hold: true }, { car: [S_, G_, G_, S_, G_, G_], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });",
  "teamWait.push({ car: [S_, G_, G_, S_, G_], t: 0, seg, hold: true }, { car: [S_, G_, S_, G_], t: rand(0, 5), seg: chTeamSeg2(seg), hold: true });   /* c249 */"),
]
