import pathlib
s = pathlib.Path('c602.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
old_desc = pathlib.Path('old_desc.txt').read_text().strip()
rep("fx: (L) => { const L2 = Math.floor(L / 2), n = Math.floor(L2 / 2), m = L2 % 2;", "fx: (L) => { const L2 = Math.ceil(L / 2), n = Math.ceil(L2 / 2), m = L2 % 2 === 0 ? 1 : 0;   /* c603: 일반 1 → 일반 1 + 새끼 1 → 일반 2 … */")
rep("    const L2 = Math.floor(chTrait('start') / 2); if (!L2) return; const n = Math.floor(L2 / 2), m = L2 % 2;", "    const L2 = Math.ceil(chTrait('start') / 2); if (!L2) return; const n = Math.ceil(L2 / 2), m = L2 % 2 === 0 ? 1 : 0;   /* c603: 일반 좀비부터 — 칸마다 일반 1 · 일반 1 + 새끼 1 · 일반 2 … (2단계마다 한 칸) */")
rep(old_desc, "start: '판을 시작할 때 동료 좀비를 데리고 시작합니다. 첫 단계부터 일반 좀비 1마리와 함께 시작하고, 2단계마다 한 칸씩 늘어납니다. 일반 1 → 일반 1 + 새끼 1 → 일반 2 → 일반 2 + 새끼 1 … 순서입니다. 새끼 좀비는 사람을 덮치거나 감염시키지 못하고 때리기만 합니다. 20단계면 일반 좀비 5마리와 새끼 좀비 1마리와 함께 시작합니다.'")
pathlib.Path('c603_patch.py').write_text('C603_R = ' + repr(R) + '\n')
print(len(R))
