# c148: 사물(길거리·건물 안의 둥근 사물)에는 체력바를 안 띄운다 — 금고·문·차는 그대로
C148_R = [
 ("barUp = b === me || b.hp < b.maxHp;", "barUp = b === me || (b.hp < b.maxHp && !(CHAPTER && b.prop));   /* c148: 사물은 체력바 없음 */"),
]
