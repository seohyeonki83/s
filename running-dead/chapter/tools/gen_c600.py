import pathlib
s = pathlib.Path('c599.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_UP_COST = 10;   /* c592: 1포인트 = 유전자 10 */", "  const CH_UP_COST = 10;   /* c592: 1포인트 = 유전자 10 */\n  const chUpCost = (k) => CH_UP_COST + Math.floor((CH_SV.up[k] || 0) / 10);   // c600: 그 능력이 1 오를 때마다 한 칸 비용 +1 (10 · 11 · 12 …)")
rep("${CH_SV.genes < CH_UP_COST ? 'disabled' : ''}>+ ${CH_GENE_I(14)}${CH_UP_COST}</button>", "${CH_SV.genes < chUpCost(k) ? 'disabled' : ''}>+ ${CH_GENE_I(14)}${chUpCost(k)}</button>")
rep("(b) => { if (b.dataset.up && CH_SV.genes >= CH_UP_COST) { const k = b.dataset.up; CH_SV.genes -= CH_UP_COST;", "(b) => { if (b.dataset.up && CH_SV.genes >= chUpCost(b.dataset.up)) { const k = b.dataset.up; CH_SV.genes -= chUpCost(k);")
pathlib.Path('c600_patch.py').write_text('C600_R = ' + repr(R) + '\n')
print(len(R))
