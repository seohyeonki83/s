# c278: 카드 글이 넘치지 않게 — 한 줄 설명을 2줄 안으로 · 긴 이름은 글자를 줄여 한 줄로
C278_R = [
  ("vest: '총격 피해 감소 · 충격에 밀리지 않음', shoes:", "vest: '총격 피해·밀림 감소', shoes:"),
  ("teeth: '나와 동료들이 인간을 더 빠르게 좀비로 만듭니다', acid: '동료들이 산성피를 뿌리며 전사합니다', acidp: '산성 피해를 입은 적의 도트 데미지 증가',",
   "teeth: '나와 동료들의 감염 속도 증가', acid: '동료가 죽으면 산성피', acidp: '산성 도트 데미지 증가',"),
  ("rage: '동료들의 공격 속도와 이동 속도 증가',", "rage: '동료들의 공격·이동 속도 증가',"),
  ("ov.querySelector('.ok').classList.remove('ready');\n  }", "ov.querySelector('.ok').classList.remove('ready');\n    chFitNames(ov);\n  }\n  function chFitNames(ov) { for (const e of ov.querySelectorAll('.card .nm')) { e.style.whiteSpace = 'nowrap'; let f = 15; while (e.scrollWidth > e.clientWidth + 1 && f > 11) e.style.fontSize = (--f) + 'px'; } }   // c278: 긴 이름은 글자를 줄여 한 줄로"),
  ("`</div>`;   /* c274: 확인 버튼 없음 */\n    stage.appendChild(ov);", "`</div>`;   /* c274: 확인 버튼 없음 */\n    stage.appendChild(ov); chFitNames(ov);"),
  ("    stage.appendChild(ov);\n    let chosen = null;", "    stage.appendChild(ov); if (CHAPTER) chFitNames(ov);\n    let chosen = null;", 2),
]
C278_R.append(("vest: ['총격', (n) => `-${10 * (1 + n)}% · 밀림 -${2 + 2.5 * n}`]", "vest: ['총격', (n) => `-${10 * (1 + n)}%`]   /* c278: 카드는 총격만 (밀림은 설명 칸에) */"))
