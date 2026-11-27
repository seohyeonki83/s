import pathlib
s = pathlib.Path('c542.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_CLR_G = { e: 300, n: 300, h: 1000 };", "  const CH_CLR_G = { e: 300, n: 400, h: 500 };   /* c543 */\n  const CH_SUB_G = 200;   // c543: 서브 미션 보상")
rep("<div class=\"gi\">${CH_GENE_I()}100</div>", "<div class=\"gi\">${CH_GENE_I()}${CH_SUB_G}</div>")
rep("add += 100; R.push(['🎖', '서브 미션 ' + (i + 1), 100, true]);", "add += CH_SUB_G; R.push(['🎖', '서브 미션 ' + (i + 1), CH_SUB_G, true]);")
pathlib.Path('c543_patch.py').write_text('C543_R = ' + repr(R) + '\n')
print(len(R))
