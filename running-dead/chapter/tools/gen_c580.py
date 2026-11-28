import pathlib
# c580: c579 되돌림 — c578과 같은 코드 (c579 바꿈을 거꾸로)
from c579_patch import C579_R
R = [(b, a) for (a, b) in reversed(C579_R)]
pathlib.Path('c580_patch.py').write_text('C580_R = ' + repr(R) + '\n')
print(len(R))
