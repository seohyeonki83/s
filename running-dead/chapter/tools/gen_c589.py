import pathlib
s = pathlib.Path('c588.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("new THREE.PlaneGeometry(0.34, 0.09).translate(0.3 + 0.17, 0, 0), p = new THREE.PlaneGeometry(0.16, 0.16).translate(0.66, 0, 0);",
    "new THREE.PlaneGeometry(0.24, 0.09).translate(0.3 + 0.12, 0, 0), p = new THREE.PlaneGeometry(0.16, 0.16).translate(0.54, 0, 0);   /* c589: 받침판 0.12 안쪽으로 */")
pathlib.Path('c589_patch.py').write_text('C589_R = ' + repr(R) + '\n')
print(len(R))
