import pathlib
s = pathlib.Path('c522.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
L = s.split('\n')
i = next(k for k, l in enumerate(L) if l.startswith('  const CH_STG_INFO = {'))
old = '\n'.join(L[i:i + 5])
rep(old, """  const CH_STG_INFO = {   // c523: 설명은 짧고 직관적으로 (내부 수치 없음)
    1: { nm: '외곽 도시', ds: '감염이 처음 번진 조용한 도시.', boss: ['군인차 부대', '드론을 싣고 오는 군인차 3대', 'convoy'] },
    2: { nm: '공단 지구', ds: '공장과 창고가 늘어선 지구.', boss: ['불도저 2대', '벽을 부수며 돌진하는 불도저', 'dozer'] },
    3: { nm: '국경 요새', ds: '군대가 지키는 마지막 도시.', boss: ['장갑차', '기관총을 쏘며 밀고 오는 장갑차', 'tank'] },
  };""")
rep("const chClrText = (d) => d === 'e' ? '특공대 3번을 모두 물리치기 (120 · 265 · 405초에 온다)' : d === 'n' ? '특공대 4번을 모두 물리치기 (네 번째는 550초 · 저격수 3 · 군인 8)' : '550초에 오는 보스와 호위를 모두 물리치기';",
    "const chClrText = (d) => d === 'e' ? '특공대 3번 물리치기' : d === 'n' ? '특공대 4번 물리치기' : '보스 물리치기';")
rep("<div class=\"bt\">${I.boss[1]}<br>보스가 살아 있는 동안 15초마다 군인 2명이 더 온다.</div>", "<div class=\"bbt\">${I.boss[1]}</div>")
rep("#outg .bs .bt{", "#outg .bs .bbt{")   # c523: 아래 버튼 칸(.bt)과 이름이 겹쳐 보스 설명이 화면 아래로 튀던 것
rep("h += `<div class=\"cd\"><div class=\"k\">적</div><div class=\"v\" style=\"font-size:14px\">${n > 1 ? `모든 적 체력 · 공격력 +${(n - 1) * 20}%<br>` : ''}샷건 · 사각 로봇 섞임 · 건널목 터렛: 경보 '${CH_LVN[CH_MIX_T[d] - 1]}'부터</div></div>`;",
    "{ const dg = n + { e: 0, n: 1, h: 2 }[d]; h += `<div class=\"cd\"><div class=\"k\">위험도</div><div class=\"v\" style=\"font-size:20px;letter-spacing:2px\">${[1, 2, 3, 4, 5].map((k) => `<span style=\"color:${k <= dg ? '#ff5a5a' : '#3d4450'}\">☠</span>`).join('')}</div></div>`; }   // c523: 수치 대신 위험도 해골")
rep("${CH_DIF_NM[d]} 첫 클리어${got ? ' · 받음 ✓' : ''}<small>처음 한 번만</small></div></div><div class=\"rw\"><div class=\"gi\">${CH_GENE_I()}1</div><div class=\"lb\">적 하나 없앨 때마다<small>죽어도 남는다</small></div></div></div>`;",
    "첫 클리어${got ? ' · 받음 ✓' : ''}</div></div></div>`;")
rep("<div class=\"k\">서브 미션 · 클리어해야 받는다</div>", "<div class=\"k\">서브 미션</div>")
rep("<div class=\"tx\"><div class=\"n1\">${nm}</div><div class=\"n2\">${ds}</div></div>", "<div class=\"tx\"><div class=\"n1\">${nm}</div></div>")
rep("<div class=\"t1\">유전자로 강해지기</div><div class=\"t2\">성장</div></div><button class=\"x\">✕</button></div><div class=\"ds\">능력 1 = 기본값의 0.5%. 0부터 시작하고 끝없이 올릴 수 있다.<br>보유 유전자 ${CH_GENE_I(14)} <b>${CH_SV.genes}</b></div>`",
    "<div class=\"t2\">성장</div></div><button class=\"x\">✕</button></div><div class=\"ds\">${CH_GENE_I(14)} <b>${CH_SV.genes}</b></div>`")
rep("<div class=\"ds\">실험실 수조에서 깨어난 첫 좀비. 동료를 모으고 길을 막는 사람들을 물리치며 연구소를 빠져나가라.</div>", "<div class=\"ds\">실험실에서 깨어난 첫 좀비.</div>")
rep("'<div class=\"g4\">' + chClrText(CH_DIF) + '<div class=\"g5\">서브 미션</div>'", "'<div class=\"g4\"><div class=\"g5\" style=\"margin-top:0\">서브 미션</div>'")
rep("<div class=\"lb\">첫 클리어 · 받음 ✓<small>처음 한 번만</small></div></div><div class=\"rw\"><div class=\"gi\">${CH_GENE_I()}1</div><div class=\"lb\">적 하나 없앨 때마다<small>다시 해도 받는다</small></div></div></div>`", "<div class=\"lb\">첫 클리어 · 받음 ✓</div></div></div>`")
pathlib.Path('c523_patch.py').write_text('C523_R = ' + repr(R) + '\n')
print(len(R))
