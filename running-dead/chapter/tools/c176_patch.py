# c176: 보스 뒤 출동은 군인 2명만 (저격수 없음) · 장갑차를 호위하는 거리 = 저격수와 같은 근접·지배 거리 + 장갑차 몸통 반 길이(2.1칸)
C176_R = [
 ("comp: chSf.wn % 3 === 0 ? [S_, G_] : [G_, G_]", "comp: [G_, G_]   /* c176: 군인만 */"),
 ("<= GUARD_DOMAIN * (m.tank ? CH_TK_ESC : 1)) c.recall = false;", "<= GUARD_DOMAIN + (m.tank ? chTkR() : 0)) c.recall = false;"),
 ("const ek = m.tank ? CH_TK_ESC : 1; let tx = m.foot.x + Math.cos(c.slotA) * GUARD_NEAR * ek * c.slotK, tz = m.foot.z + Math.sin(c.slotA) * GUARD_NEAR * ek * c.slotK;",
  "const ek = m.tank ? chTkR() : 0; let tx = m.foot.x + Math.cos(c.slotA) * (GUARD_NEAR * c.slotK + ek), tz = m.foot.z + Math.sin(c.slotA) * (GUARD_NEAR * c.slotK + ek);   /* c176: 장갑차면 몸통만큼 바깥 */"),
 ("const lim = (c.inRange ? GUARD_DOMAIN_FIGHT : GUARD_DOMAIN) * (m.tank ? CH_TK_ESC : 1);", "const lim = (c.inRange ? GUARD_DOMAIN_FIGHT : GUARD_DOMAIN) + (m.tank ? chTkR() : 0);   /* c176 */"),
 ("  let chTkMark = false;\n", "  let chTkMark = false;\n  const chTkR = () => CAR_L * CH_TK_K / 2;   // c176: 장갑차 몸통 반 길이 (호위 거리에 더한다)\n"),
 ("c.slotA = Math.random() * Math.PI * 2; c.slotK = rand(0.85, 1); }\n    return T;", "c.slotA = Math.random() * Math.PI * 2; c.slotK = rand(0.5, 1); }   /* c176: 저격수 호위와 같은 자리 폭 */\n    return T;"),
]
