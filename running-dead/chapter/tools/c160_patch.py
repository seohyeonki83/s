# c160: 동료(얻은 변이 좀비 포함)만 공격력 10% 더 올림 — 나는 그대로
C160_R = [
 ("if (CHAPTER && a && (a === me || a.kind === 'ally') && (!a.splashing || a === me)) dmg *= 1.15;", "if (CHAPTER && a && (a === me || a.kind === 'ally') && (!a.splashing || a === me)) dmg *= a === me ? 1.15 : 1.15 * 1.1;   /* c160: 동료만 10% 더 */"),
]
