# c412: 작은 좀비 색을 더 밝게 (동료 색에서 흰색 쪽으로 40% → 70%)
src = open('c411.mjs').read()
n = src.count("0xb9c8f9"); assert n >= 1
R = [("0xb9c8f9", "0xdce4fc", n)] if n != 1 else [("0xb9c8f9", "0xdce4fc")]
open('c412_patch.py', 'w').write("# c412: 작은 좀비 색 더 밝게\nC412_R = " + repr(R) + "\n")
