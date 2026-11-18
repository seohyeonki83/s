# c186: 나 — 문 · 금고도 사람과 같은 순위 (닿는 거리 안에 있으면 사람과 견줘 더 가까운 쪽을 친다). 노릴 사람이 저격수면 저격수가 먼저 · 덮칠 사람이 있으면 덮치기가 먼저
C186_R = [
 ("        if (CHAPTER && z === me && !ob && !t && go && go.kind === 'citizen' && chTier(go) === 0 && !(z.objOff > clock)) { const d = nearObj(z); if (d && d.type === 'door') ob = d; }",
  "        if (CHAPTER && z === me && !t && go && go.kind === 'citizen' && !go.sniper) { if (!ob) { const d = nearObj(z); if (d && d.type === 'door') ob = d; } if (!sf) sf = nearSafe(z); }   // c186: 나 — 문·금고 = 사람과 같은 순위 (저격수만 먼저)"),
]
