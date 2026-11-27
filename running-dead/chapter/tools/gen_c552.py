import pathlib
s = pathlib.Path('c551.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep('<button class="sb rst" data-rst="1">초기화 (모든 기록 삭제)</button>`,',
    '<button class="sb rst" data-rst="1">초기화 (모든 기록 삭제)</button><div style="height:8px"></div><button class="sb rst" data-rst="2">튜토리얼 클리어 상태로 초기화</button>`,   /* c552 */')
rep("""            if (!b.classList.contains('on')) { b.classList.add('on'); b.textContent = '정말 초기화? 한 번 더 누르기'; setTimeout(() => { if (b.isConnected) { b.classList.remove('on'); b.textContent = '초기화 (모든 기록 삭제)'; } }, 3000); return; }
            try { localStorage.removeItem('rd_genes'); localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1, v4: 1 })); window.name = ''; } catch (e) {}""",
"""            const t2 = b.dataset.rst === '2', lab = t2 ? '튜토리얼 클리어 상태로 초기화' : '초기화 (모든 기록 삭제)';   /* c552: 튜토리얼만 깬 상태 — 보상 500 + 시민 30명 몫 30 */
            if (!b.classList.contains('on')) { b.classList.add('on'); b.textContent = '정말 초기화? 한 번 더 누르기'; setTimeout(() => { if (b.isConnected) { b.classList.remove('on'); b.textContent = lab; } }, 3000); return; }
            try { localStorage.removeItem('rd_genes'); localStorage.setItem('rd_save_v1', JSON.stringify({ genes: t2 ? 530 : 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: t2, mig: 1, v2: 1, v3: 1, v4: 1 })); window.name = ''; } catch (e) {}""")
pathlib.Path('c552_patch.py').write_text('C552_R = ' + repr(R) + '\n')
print(len(R))
