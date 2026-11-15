# c105: 덩치 좀비 무게(미는 힘) +2 — 동료 덩치도, 덩치가 된 나도 (10.4 → 12.4)
C105_R = [
 ("z.force = MY_FORCE * 1.3;", "z.force = MY_FORCE * 1.3 + (CHAPTER ? 2 : 0);   /* c105: +2 (10.4 → 12.4) */"),
 ("me.force = MY_FORCE * 1.3; }", "me.force = MY_FORCE * 1.3 + (CHAPTER ? 2 : 0); }   /* c105 */"),
]
