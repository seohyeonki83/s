# c251: 테이저건 — 쿨타임 30% 늘림 · 장탄 = 처음 1 → 강화 1번 2 → 강화 2번부터 3 (최대 3)
C251_R = [
 ("  const itemMax = (k) => k === 'mutate' ? CH_WV('mutN', lv('mutate')) : ITEM[k].max;", "  const itemMax = (k) => k === 'mutate' ? CH_WV('mutN', lv('mutate')) : CHAPTER && k === 'taser' ? Math.min(3, 1 + lv('taser'))   /* c251: 1 · 2 · 3 */ : ITEM[k].max;"),
 ("ITEM[k].reload * (k === 'taser' ? 1.1 : 1))", "ITEM[k].reload * (k === 'taser' ? 1.1 * (CHAPTER ? 1.3 : 1) : 1))   /* c251: 테이저 쿨타임 30% 늘림 */"),
 ("    taser: (n) => `한 번에 ${CH_WV('taserN', n)}명 · ${CH_WV('taserT', n)}초 감전`,", "    taser: (n) => `한 번에 ${CH_WV('taserN', n)}명 · ${CH_WV('taserT', n)}초 감전 · 장탄 ${Math.min(3, 1 + n)}`,   /* c251 */"),
]
