import pathlib
s = pathlib.Path('c507.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1. 옛 버전 유전자 옮겨오기 없앰 — 본편 저장은 한 번 깨끗이 새로 시작 (v2)
rep("    if (!o.mig) { o.mig = 1; try { o.genes += +localStorage.getItem('rd_genes') || 0; localStorage.removeItem('rd_genes'); } catch (e) {} } return o; })();",
    "    if (!o.v2) { o = { genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1 }; }   // c508: 옛 버전에서 옮겨온 유전자까지 한 번 깨끗이\n    try { localStorage.removeItem('rd_genes'); } catch (e) {} return o; })();")
rep("localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1 }));", "localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1 }));")
# 2. 판 안 왼쪽 위 유전자 = 이번 판에서 얻은 것 (0부터)
rep("  chGeneEl.innerHTML = CH_GENE_SVG + '<span>' + chGenes + '</span>';", "  chGeneEl.innerHTML = CH_GENE_SVG + '<span>0</span>';   // c508: 이번 판에서 얻은 유전자")
rep("CH_SV.genes += n; chSave(); chGeneEl.lastChild.textContent = chGenes; }", "CH_SV.genes += n; chSave(); chGeneEl.lastChild.textContent = chRunGenes; }")
pathlib.Path('c508_patch.py').write_text('C508_R = ' + repr(R) + '\n')
print(len(R))
