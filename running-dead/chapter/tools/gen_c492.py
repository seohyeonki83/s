import pathlib
s = pathlib.Path('c491.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("if (CHAPTER) { car.dozer = true;", "if (CHAPTER) { car.dozer = true; car.massK = 2;   /* c492: 불도저 무게 반 (40 → 20) */")
pathlib.Path('c492_patch.py').write_text('C492_R = ' + repr(R) + '\n')
