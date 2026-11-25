# c450: 덩치 사물 피해 30% 줄임
C450_R = [("if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= 2;", "if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= CHAPTER ? 1.4 : 2;   /* c450: 2 → 1.4배 (30% 줄임) */")]
