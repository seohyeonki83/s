# c287: 자폭 산성은 무엇으로도 덮이지 않고, 산성 폭발은 자폭 산성이 묻으면 바로 교체된다
C287_R = [
  ("  function chAcidOn(e, T) {                    // c224: 산성 한 겹 (겹마다 따로 시간이 간다)\n", "  function chAcidOn(e, T) {                    // c224: 산성 한 겹 (겹마다 따로 시간이 간다)\n    if (e.goo) return;   // c287: 자폭 산성이 묻어 있으면 산성 폭발은 안 묻는다\n"),
  ("    if (c.goo) return;", "    if (c.acid) c.acid.length = 0;   // c287: 산성 폭발은 자폭 산성으로 교체\n    if (c.goo) return;"),
  ("    if (car.goo) return;", "    if (car.acid) car.acid.length = 0;   // c287\n    if (car.goo) return;"),
]
C287_R.append(("  function chAcidTick(dt) {", "  window.__goo = (c) => gooOn(c); window.__acidOn = (c, T) => chAcidOn(c, T);   // 테스트용\n  function chAcidTick(dt) {"))
