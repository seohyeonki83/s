# c139: 무기 5종 수치표를 새로 (0~6단계, 강화 6번까지)
#   테이저건  1명 2초 / 2명 2 / 2명 3 / 3명 3 / 3명 4 / 4명 4 / 5명 5
#   변이 주사 1개 6초 / 1개 9 / 2개 12 / 2개 15 / 3개 18 / 3개 21 / 4개 24
#   각성 주사 최대 5 / 8 / 11 / 14 / 17 / 20 / 23초 (가득 차는 데 늘 25초)
#   자폭      범위 1.5칸 산성 4초 / 2.5·6 / 3.5·8 / 4.5·10 / 5.5·12 / 6.5·14 / 7.5·16 (도트 2)
#   현금      유혹 2초 1대 / 3초 2대 / 4초 3대 / 5초 4대 / 6초 5대 / 6.5초 6대 / 7초 7대 (시간만 저격수·군인 80% · 경찰 50% 짧게)
C139_R = [
 ("  const taserN = (n) => 1 + Math.floor(n / 2),", "  const CH_W = { taserN: [1, 2, 2, 3, 3, 4, 5], taserT: [2, 2, 3, 3, 4, 4, 5], mutN: [1, 1, 2, 2, 3, 3, 4], cashT: [2, 3, 4, 5, 6, 6.5, 7] }, CH_WV = (k, n) => CH_W[k][Math.max(0, Math.min(CH_W[k].length - 1, n))];   // c139: 무기 수치표\n  const taserN = (n) => 1 + Math.floor(n / 2),"),
 ("const chLvMax = (k) => k === 'bag' ? 3 : 5;", "const chLvMax = (k) => k === 'bag' ? 3 : ITEM[k] && !ITEM[k].passive ? 6 : 5;   /* c139: 무기는 6번까지 강화 */"),
 ("'★'.repeat(Math.max(0, Math.min(5, n)))", "'★'.repeat(Math.max(0, Math.min(6, n)))"),
 # 테이저건
 ("const hit = cand.slice(0, 1 + lv('taser'));", "const hit = cand.slice(0, CH_WV('taserN', lv('taser')));"),
 ("c.stunT = STUN_T;   /* c21: 감전은 늘 3초 */", "c.stunT = CH_WV('taserT', lv('taser'));   /* c139 */"),
 # 변이 주사
 ("const MUT_T = () => 10 + 3 * lv('mutate');", "const MUT_T = () => 6 + 3 * lv('mutate');"),
 ("const itemMax = (k) => k === 'mutate' ? 1 + lv('mutate') : ITEM[k].max;", "const itemMax = (k) => k === 'mutate' ? CH_WV('mutN', lv('mutate')) : ITEM[k].max;"),
 # 각성 주사
 ("const chAccMax = () => 10 + 3 * lv('awaken');", "const chAccMax = () => 5 + 3 * lv('awaken');"),
 ("dt * m / (40 * (1 - bookCut()))", "dt * m / (25 * (1 - bookCut()))"),
 # 자폭
 ("const R = ATTACK * (1 + 0.2 * lv('bomb'));", "const R = 1.5 + lv('bomb');   /* c139: 1.5칸에서 강화마다 +1칸 */"),
 ("c.gooLeft = 10 + lv('bomb');", "c.gooLeft = 4 + 2 * lv('bomb');"),
 ("car.gooLeft = 10 + lv('bomb');", "car.gooLeft = 4 + 2 * lv('bomb');"),
 # 현금
 ("const lureHits = () => 2 + 2 * lv('cash');", "const lureHits = () => 1 + lv('cash');"),
 ("if (c.police && (c.lureT = (c.lureT || 0) + dt) >= (c.military ? 0.7 : 1.5)) {", "if ((c.lureT = (c.lureT || 0) + dt) >= CH_WV('cashT', lv('cash')) * (c.military ? 0.2 : c.police ? 0.5 : 1)) {   /* c139: 유혹 시간 — 저격수·군인 80% · 경찰 50% 짧다 */"),
 ("mesh, t: CASH_LIFE, who: new Set() }", "mesh, t: Math.max(CASH_LIFE, CH_WV('cashT', lv('cash')) + 1.5), who: new Set() }"),
 # 글자
 (r"""    bomb: (n) => `터지는 범위 ${(ATTACK * (1 + 0.2 * n)).toFixed(1)}칸 (${n ? '+' + 20 * n + '%' : '덮치는 거리와 같음'})`,""", r"""    bomb: (n) => `터지는 범위 ${1.5 + n}칸 · 산성 ${4 + 2 * n}초`,"""),
 (r"""    mutate: (n) => `주사 ${1 + n}개 · 변이 ${10 + 3 * n}초`,""", r"""    mutate: (n) => `주사 ${CH_WV('mutN', n)}개 · 변이 ${6 + 3 * n}초`,"""),
 (r"""    taser: (n) => `한 번에 ${1 + n}명 · 3초 감전`,""", r"""    taser: (n) => `한 번에 ${CH_WV('taserN', n)}명 · ${CH_WV('taserT', n)}초 감전`,"""),
 (r"""    awaken: (n) => `최대 사용 시간 ${10 + 3 * n}초 · 게이지 충전 속도 ${n ? '+' + 30 * n + '%' : '기본'}`,""", r"""    awaken: (n) => `최대 사용 시간 ${5 + 3 * n}초 · 가득 차는 데 25초`,"""),
 (r"""    cash: (n) => n ? `유혹 강도와 범위 +${n}` : '유혹 강도와 범위 기본',""", r"""    cash: (n) => `유혹 ${CH_WV('cashT', n)}초 · ${1 + n}대 버팀 · 알아채는 거리 ${(7.2 * (1.2 + 0.2 * n)).toFixed(1)}칸`,"""),
 (r"""bomb: ['범위', (n) => n ? `+${20 * n}%` : '기본'], mutate: ['', (n) => `${1 + n}개·${10 + 3 * n}초`], taser: ['대상', (n) => `${1 + n}명`], awaken: ['최대', (n) => `${10 + 3 * n}초`], cash: ['유혹', (n) => n ? `+${n}` : '기본'],""",
  r"""bomb: ['', (n) => `${1.5 + n}칸·${4 + 2 * n}초`], mutate: ['', (n) => `${CH_WV('mutN', n)}개·${6 + 3 * n}초`], taser: ['', (n) => `${CH_WV('taserN', n)}명·${CH_WV('taserT', n)}초`], awaken: ['최대', (n) => `${5 + 3 * n}초`], cash: ['', (n) => `${CH_WV('cashT', n)}초·${1 + n}대`],"""),
 ("taser: ['대상을 3초 동안 감전시킵니다.', '강화 시 감전 대상이 늘어납니다.'],", "taser: ['대상을 감전시켜 멈춥니다.', '강화 시 감전 대상과 시간이 늘어납니다.'],"),
 ("'강화 시 최대 사용 시간과 게이지 충전 속도가 늘어납니다.'", "'강화 시 최대 사용 시간이 늘어납니다.'"),
 ("bomb: ['가장 위험한 적 곁의 동료 하나가 터지며 산성 덩어리를 뿌립니다.', '강화 시 터지는 범위가 넓어집니다.'],", "bomb: ['가장 위험한 적 곁의 동료 하나가 터지며 산성 덩어리를 뿌립니다.', '강화 시 터지는 범위가 넓어지고 산성이 오래갑니다.'],"),
]
