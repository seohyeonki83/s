# c450: 덩치가 건물·사물(벽 · 문 · 차 · 금고 · 길거리 사물)에 주는 피해 배율 2배 → 1.4배 (30% 줄임 · 괴물 · 흡수도 같다)
src = open('c449.mjs').read()
a = "if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= 2;"
assert src.count(a) == 1
R = [(a, "if ((v.kind === 'obj' || v.kind === 'safe') && a.mut === 'armor') dmg *= CHAPTER ? 1.4 : 2;   /* c450: 2 → 1.4배 (30% 줄임) */")]
open('c450_patch.py', 'w').write("# c450: 덩치 사물 피해 30% 줄임\nC450_R = " + repr(R) + "\n")
