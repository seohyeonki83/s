# c241: 덩치의 사물 피해 3배 → 2배
C241_R = [
 ("    if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= 3;", "    if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= 2;   /* c241: 3 → 2배 */"),
]
