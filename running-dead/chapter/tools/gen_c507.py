import pathlib
s = pathlib.Path('c506.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("      h += `<button class=\"og-tut\" data-tut=\"1\">튜토리얼 다시 하기</button>`;",
    "      h += `<button class=\"og-tut\" data-tut=\"1\">튜토리얼 다시 하기</button><div style=\"text-align:center;margin-top:28px\"><button class=\"og-rst\" data-rst=\"1\">초기화</button></div>`;   // c507")
rep("#outg .og-tut{width:100%;margin-top:14px;background:#3a4250}';", "#outg .og-tut{width:100%;margin-top:14px;background:#3a4250}#outg .og-rst{font-size:11px;font-weight:700;padding:4px 10px;border-radius:8px;background:transparent;color:#6b7482;border:1px solid #3a4250}#outg .og-rst.on{color:#fff;background:#c62828;border-color:#c62828}';")
rep("      if (b.dataset.tut) { ov.remove(); tut(); return; }", """      if (b.dataset.tut) { ov.remove(); tut(); return; }
      if (b.dataset.rst) {   // c507: 초기화 — 한 번 누르면 확인, 3초 안에 한 번 더 누르면 전부 지운다
        if (!b.classList.contains('on')) { b.classList.add('on'); b.textContent = '정말 초기화? 한 번 더 누르기'; setTimeout(() => { if (b.isConnected) { b.classList.remove('on'); b.textContent = '초기화'; } }, 3000); return; }
        try { localStorage.removeItem('rd_genes'); localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1 })); window.name = ''; } catch (e) {}
        location.reload(); return;
      }""")
pathlib.Path('c507_patch.py').write_text('C507_R = ' + repr(R) + '\n')
print(len(R))
