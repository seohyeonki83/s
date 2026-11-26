import pathlib
s = pathlib.Path('c486.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("dmg: z === me ? zDamage(z) : zDamage(z) * 4", "dmg: z === me ? zDamage(z) : zDamage(z) * 40 / (ALLY_DAMAGE * 1.15 * 1.1 * 1.07 * 1.03)   /* c487: 동료 히드라 침 = 40 (챕터 동료 배율을 곱한 뒤 · 촉매제는 그 위에) */")
pathlib.Path('c487_patch.py').write_text('C487_R = ' + repr(R) + '\n')
