# c124: 레벨업 — 아직 없는 도구(쓰는 아이템)는 안 나온다. 가진 도구의 강화만 나온다 (장비는 그대로)
C124_R = [
 ("    return CH_ITEMS.filter((k) => !(chHas(k) && lv(k) >= chLvMax(k)));", "    return CH_ITEMS.filter((k) => !(chHas(k) && lv(k) >= chLvMax(k)) && (ITEM[k].passive || chHas(k)));   /* c124: 도구의 첫 등장은 레벨업에 없다 */"),
]
