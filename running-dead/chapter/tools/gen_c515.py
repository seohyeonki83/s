import pathlib
s = pathlib.Path('c514.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
# 1. 저장 한 번 더 완전히 초기화 (v3)
rep("    if (!o.v2) { o = { genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1 }; }", "    if (!o.v3) { o = { genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1 }; }   // c515: 한 번 더 전부 초기화")
rep("tut: false, mig: 1, v2: 1 }));", "tut: false, mig: 1, v2: 1, v3: 1 }));")
# 2. 일시정지 버튼 보이게 (미니맵 바로 밑) · 되감기 버튼은 없앰
rep("const el = document.getElementById(id); el.style.bottom = 'auto'; if (CHAPTER) el.style.opacity = '0';", "const el = document.getElementById(id); el.style.bottom = 'auto'; if (CHAPTER && id === 'reset') el.style.display = 'none';   /* c515: 일시정지는 보이게 · 되감기는 없앰 */")
# 3. 일시정지 창에 '나가기' — 포기하고 아웃게임으로
rep("    ov.innerHTML = '<div class=\"t\">일시정지</div>';\n    openMenu(ov, '계속');",
    """    ov.innerHTML = '<div class="t">일시정지</div>';
    if (CHAPTER) {   // c515: 나가기 — 포기하고 아웃게임으로 (그동안 얻은 유전자는 이미 저장돼 있다)
      ov.style.flexDirection = 'column'; ov.style.alignItems = 'center';
      const q = document.createElement('button'); q.type = 'button'; q.textContent = '나가기';
      q.style.cssText = 'margin-top:28px;font:900 17px system-ui,sans-serif;color:#fff;background:#c62828;border:none;border-radius:14px;padding:11px 34px;touch-action:manipulation';
      q.addEventListener('pointerdown', (e) => e.stopPropagation());
      q.addEventListener('click', (e) => { e.stopPropagation(); chRunOver = true; try { window.name = ''; } catch (er) {} location.reload(); });
      ov.appendChild(q);
    }
    openMenu(ov, '계속');""")
pathlib.Path('c515_patch.py').write_text('C515_R = ' + repr(R) + '\n')
print(len(R))
