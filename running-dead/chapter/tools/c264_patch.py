# c264: 주황·빨강 경계 = 경찰과 같다 — 시야에 들어오면 바로 덤비던 것(c68)을 빼고, 경찰과 같은 경계 시간(시민의 3분의 1, 수상함 전엔 5배) 뒤에 덤빈다
C264_R = [
 ("    else if (near <= c.sight && CHAPTER && c.attacker && !c.boss && c.hp > 0) enterFight(c, nearZ, true);   // c68: 주황·빨강 — 시야에 들어오면 경계 없이 바로 덤빈다\n", ""),
 ("* (c.soft ? CH_SOFT_ALERT : 1) * (CHAPTER && stars < 1 ? 5 : 1); }", "* (c.soft && !(CHAPTER && c.attacker) ? CH_SOFT_ALERT : 1) * (CHAPTER && stars < 1 ? 5 : 1); }   /* c264: 주황도 경찰과 같은 경계 시간 */"),
]
