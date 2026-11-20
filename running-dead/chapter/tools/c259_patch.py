# c259: 새 장비 '산성 강도' — 산성 피해(자폭 스위치 · 산성 폭발 · 보스 포함)의 도트에 처음 +1, 강화마다 +1 (최대 +6)
C259_R = [
 ("    acid: svgI(", "    acidp: svgI('<path d=\"M10 3C7.5 7.2 4.5 10 4.5 13.5a5.5 5.5 0 0 0 11 0C15.5 10 12.5 7.2 10 3z\" fill=\"#7ed321\"/><rect x=\"17\" y=\"5\" width=\"2.6\" height=\"9\" rx=\"1\" fill=\"#ff5a3c\"/><rect x=\"13.8\" y=\"8.2\" width=\"9\" height=\"2.6\" rx=\"1\" fill=\"#ff5a3c\"/>'),   /* c259 */\n    acid: svgI("),
 ("teeth: { icon: IC.teeth, name: '틀니', passive: true },", "teeth: { icon: IC.teeth, name: '틀니', passive: true }, acidp: { icon: IC.acidp, name: '산성 강도', passive: true },   /* c259 */"),
 ("    acid: ['동료들이 산성피를 뿌리며 전사합니다', ", "    acidp: ['산성 피해를 입은 적의 도트 데미지가 늘어납니다', '강화 시 더 늘어납니다.'],   /* c259 */\n    acid: ['동료들이 산성피를 뿌리며 전사합니다', "),
 ("    acid: (n) => `범위 = 근접 거리", "    acidp: (n) => `산성 도트 +${1 + n} (0.5초마다)`,   /* c259 */\n    acid: (n) => `범위 = 근접 거리"),
 ("acid: ['산성', (n) => `${3 + n}초`],", "acid: ['산성', (n) => `${3 + n}초`], acidp: ['도트', (n) => `+${1 + n}`],"),
 ("acid: '동료들이 산성피를 뿌리며 전사합니다', catalyst", "acid: '동료들이 산성피를 뿌리며 전사합니다', acidp: '산성 피해를 입은 적의 도트 데미지 증가', catalyst"),
 ("'revive', 'teeth', 'acid'];", "'revive', 'teeth', 'acid', 'acidp'];   /* c259: 산성 강도 */"),
 ("parcel: ['bomb', 'taser', 'book', 'bag', 'crowbar', 'absorb', 'vest', 'shoes']", "parcel: ['bomb', 'taser', 'book', 'bag', 'crowbar', 'absorb', 'vest', 'shoes', 'acidp']"),
 # 피해
 ("      c.hp = Math.max(0, c.hp - 2);   /* c123: 도트 2 */", "      c.hp = Math.max(0, c.hp - 2 - chAcidB());   /* c123: 도트 2 · c259: + 산성 강도 */"),
 ("if (car.goo && (car.gooT += dt) >= 0.5) { car.gooT -= 0.5; if (o && o.hp > 2) o.hp -= 2; }", "if (car.goo && (car.gooT += dt) >= 0.5) { car.gooT -= 0.5; const gd = 2 + chAcidB(); if (o && o.hp > gd) o.hp -= gd; }   // c259"),
 ("      e.acidT -= 0.5; const d = e.acid.length;", "      e.acidT -= 0.5; const d = e.acid.length * (1 + chAcidB());   // c259: 겹마다 1 + 산성 강도"),
 ("  function chAcidOn(e, T) {", "  const chAcidB = () => owned.acidp ? 1 + lv('acidp') : 0;   // c259: 산성 강도 — 도트에 더하는 값\n  function chAcidOn(e, T) {"),
]
