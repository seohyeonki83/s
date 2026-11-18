# c135: 길거리 노랑 · 주황 20% 줄임 · 나와 동료 공격력 15% 올림 (사물 체력은 그대로 — 사물도 15% 빨리 부서진다)
C135_R = [
 ("- Math.round(CH_GANG / 5); k < nY; k++)", "- Math.round(CH_GANG / 5), nY2 = chRoundP(nY * 0.8); k < nY2; k++)   /* c135: 혼자 다니는 노랑 20% 줄임 */"),
 ("      if (t === 'vig' && Math.random() < 0.19) return;", "      if ((t === 'guard' || t === 'attacker') && Math.random() < 0.2) return;   // c135: 무리 속 노랑 · 주황 다섯에 하나는 안 나온다\n      if (t === 'vig' && Math.random() < 0.19) return;"),
 ("for (let k = N(a, b); k > 0; k--) list.push(type); }", "for (let k = N(a, b); k > 0; k--) if (!((type === 'guard' || type === 'attacker') && Math.random() < 0.2)) list.push(type); }   /* c135: 포인트의 노랑 · 주황도 20% 줄임 */"),
 ("    if (TEST_MAP && !CHAPTER && v === me) dmg = 0;   // v396", "    if (CHAPTER && a && (a === me || a.kind === 'ally') && (!a.splashing || a === me)) dmg *= 1.15;   // c135: 나와 동료 공격력 15% 올림 (덩치의 범위 공격은 본 공격에서 이미 올랐다)\n    if (TEST_MAP && !CHAPTER && v === me) dmg = 0;   // v396"),
 ("ex[i].push(Math.random() < 0.68 ? '' : 'guard'); }", "{ const q = Math.random() < 0.68 ? '' : 'guard'; if (!(q === 'guard' && Math.random() < 0.2)) ex[i].push(q); } }   /* c135: 포인트에 덧붙는 노랑도 20% 줄임 */"),
]
