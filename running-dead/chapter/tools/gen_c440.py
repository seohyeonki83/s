# c440: 갈림길을 고른 무기는 카드 분위기도 바뀐다 (테두리 · 빛 · 배경이 그 길 색) · 변이 주사 · 각성 주사 — 괴물(빨강) / 흡수(하늘색) 아이콘 · 버튼 색
src = open('c439.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  IC.blood = svgI(", """  IC.mutMon = svgI('<rect x="9" y="2" width="6" height="2" rx="1" fill="#cfd6e3"/><rect x="11" y="4" width="2" height="3" fill="#cfd6e3"/><rect x="8" y="7" width="8" height="11" rx="1.5" fill="#f3d9d9"/><rect x="9.5" y="10" width="5" height="7" rx="1" fill="#e0242a"/><rect x="11.3" y="18" width="1.4" height="4" fill="#9aa4b5"/>');   /* c440: 변이 주사 — 괴물 (빨강) */
  IC.mutAbs = svgI('<rect x="9" y="2" width="6" height="2" rx="1" fill="#cfd6e3"/><rect x="11" y="4" width="2" height="3" fill="#cfd6e3"/><rect x="8" y="7" width="8" height="11" rx="1.5" fill="#dcf3fb"/><rect x="9.5" y="10" width="5" height="7" rx="1" fill="#26b8e8"/><rect x="11.3" y="18" width="1.4" height="4" fill="#9aa4b5"/>');   /* c440: 변이 주사 — 흡수 (하늘색) */
  IC.awkMon = svgI('<rect x="9" y="2" width="6" height="2" rx="1" fill="#cfd6e3"/><rect x="11" y="4" width="2" height="3" fill="#cfd6e3"/><rect x="7" y="7" width="10" height="13" rx="2" fill="#3a1010" stroke="#ff2a2a" stroke-width="1.4"/><path d="M13 9 9.5 14h2.5l-1 4 4-5.5h-2.6z" fill="#ff5a5a"/>');   /* c440: 각성 주사 — 괴물 */
  IC.awkAbs = svgI('<rect x="9" y="2" width="6" height="2" rx="1" fill="#cfd6e3"/><rect x="11" y="4" width="2" height="3" fill="#cfd6e3"/><rect x="7" y="7" width="10" height="13" rx="2" fill="#0f2a36" stroke="#3ad6ff" stroke-width="1.4"/><path d="M13 9 9.5 14h2.5l-1 4 4-5.5h-2.6z" fill="#8fe9ff"/>');   /* c440: 각성 주사 — 흡수 */
  IC.blood = svgI(""")
rep("      { id: 'monster', name: '괴물 좀비', desc: '변이한 동료가 괴물이 됩니다.", "      { id: 'monster', icon: IC.mutMon, col: '#ff3b3b', name: '괴물 좀비', desc: '변이한 동료가 괴물이 됩니다.")
rep("      { id: 'absorb', name: '흡수 좀비', desc: '변이한 동료가", "      { id: 'absorb', icon: IC.mutAbs, col: '#3ad6ff', name: '흡수 좀비', desc: '변이한 동료가")
rep("      { id: 'monster', name: '괴물 좀비', desc: '각성한 내가 괴물이 됩니다.", "      { id: 'monster', icon: IC.awkMon, col: '#ff3b3b', name: '괴물 좀비', desc: '각성한 내가 괴물이 됩니다.")
rep("      { id: 'absorb', name: '흡수 좀비', desc: '각성한 내가", "      { id: 'absorb', icon: IC.awkAbs, col: '#3ad6ff', name: '흡수 좀비', desc: '각성한 내가")
rep("      { id: 'chain', nm: '전이 감전', name:", "      { id: 'chain', nm: '전이 감전', col: '#ffe14a', name:")
rep("      { id: 'bomb', nm: '전기폭탄', name:", "      { id: 'bomb', nm: '전기폭탄', col: '#fff27a', name:")
rep('class="card" data-k="${k}" style="min-height:158px;padding-top:8px', 'class="card" data-k="${k}" style="min-height:158px;padding-top:8px${chBrCard(k)}', 3)
rep("  function chBrLook(k) {", """  function chBrCard(k) {                       // c440: 갈림길을 고른 무기 카드 — 그 길 색으로 테두리 · 빛 · 배경
    const B = CHAPTER && CH_BRANCH[k] && CH_BRANCH[k].find((b) => b.id === chBr[k]); if (!B || !B.col) return '';
    return `;border-color:${B.col};box-shadow:0 0 16px ${B.col}99, inset 0 0 22px ${B.col}40;background:linear-gradient(180deg, ${B.col}38, rgba(20,20,28,0.92) 70%)`;
  }
  function chBrLook(k) {""")
rep("CH_BRANCH[k].map((B) => `<div class=\"card\" data-k=\"${B.id}\" style=\"min-height:178px;padding-top:8px\">", "CH_BRANCH[k].map((B) => `<div class=\"card\" data-k=\"${B.id}\" style=\"min-height:178px;padding-top:8px${B.col ? `;border-color:${B.col};box-shadow:0 0 16px ${B.col}99;background:linear-gradient(180deg, ${B.col}38, rgba(20,20,28,0.92) 70%)` : ''}\">")
open('c440_patch.py', 'w').write("# c440: 갈림길 카드 색 · 변이·각성 아이콘\nC440_R = " + repr(R) + "\n")
print(len(R))
