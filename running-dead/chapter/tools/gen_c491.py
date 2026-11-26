import pathlib
s = pathlib.Path('c490.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("car.hpK *= 0.8 * 0.8 * 0.75   /* c490: 25% 더 */", "car.hpK *= 0.8 * 0.8 * 0.75 * 0.85   /* c491: 15% 더 · c490: 25% 더 */")
rep("(tkD ? (0.5 + Math.max(0, car.tkM)) * 0.9 * 0.85 * 0.98 : 1);", "(tkD ? (0.5 + Math.max(0, car.tkM)) * 0.9 * 0.85 * 0.98 : 1) * (CHAPTER && car.dozer ? 0.85 : 1);   /* c491: 불도저 밀어붙이는 피해 15% 줄임 */")
pathlib.Path('c491_patch.py').write_text('C491_R = ' + repr(R) + '\n')
