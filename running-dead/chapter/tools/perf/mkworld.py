# 측정용: 큰 맵 변형(var/perf.html)의 맵 데이터를 이어 붙인 월드로 바꾸고, 구역 4개를 가정한 곳 몇 군데를 일반화한다
import pathlib, sys
src, mapf, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = pathlib.Path(src).read_text()
i0 = s.index('  const CH_MAP = CH_BASE ? ')
i1 = s.index('\n', i0)
L = s[i0:i1]
# 세 번째 최상위 {...} = 큰 맵
depth = 0; spans = []
for i, ch in enumerate(L):
    if ch == '{':
        if depth == 0: st = i
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0: spans.append((st, i + 1))
assert len(spans) == 3, len(spans)
a, b = spans[2]
L2 = L[:a] + pathlib.Path(mapf).read_text() + L[b:]
s = s[:i0] + L2 + s[i1:]
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a)); s = s.replace(a, b)
rep("  const chZoneOf = (x, z) => (x > 0 ? 1 : 0) + (z < CH_MAP.zrMid ? 2 : 0);",
    "  const chZG = (() => { const Z = CH_MAP.zones, mm = CH_MAP.mm, C = 2, W = Math.ceil((mm.x1 - mm.x0) / C) + 1, H = Math.ceil((mm.z1 - mm.z0) / C) + 1, G = new Uint8Array(W * H); for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) { const x = mm.x0 + (i + 0.5) * C, z = mm.z0 + (j + 0.5) * C; let best = 0, bd = 1e18; for (let k = 0; k < Z.length; k++) { const dx = Math.max(Z[k][0] - x, 0, x - Z[k][2]), dz = Math.max(Z[k][1] - z, 0, z - Z[k][3]), d = dx * dx + dz * dz; if (d < bd) { bd = d; best = k; } } G[j * W + i] = best; } return { G, W, H, C, x0: mm.x0, z0: mm.z0 }; })();\n"
    "  const chZoneOf = (x, z) => { const i = Math.max(0, Math.min(chZG.W - 1, Math.floor((x - chZG.x0) / chZG.C))), j = Math.max(0, Math.min(chZG.H - 1, Math.floor((z - chZG.z0) / chZG.C))); return chZG.G[j * chZG.W + i]; };")
rep("s = Math.abs(v ? x : z - CH_MAP.zrMid)", "s = Math.abs((v ? x : z) - P.mid)")
rep("cx: v ? 0 : P.c, cz: v ? P.c : CH_MAP.zrMid", "cx: v ? P.mid : P.c, cz: v ? P.c : P.mid")
rep("CH_SMALL ? small : big;", "CH_SMALL ? small : Math.round(big * CH_POPK);")
pathlib.Path(dst).write_text(s)
print(dst, len(s))
