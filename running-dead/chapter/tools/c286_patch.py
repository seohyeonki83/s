# c286: 산성은 다시 묻으면 남은 시간과 새 시간 중 긴 쪽 (더하지 않음 · 도트도 한 겹)
C286_R = [
  ("    c.gooLeft = 4 + 2 * lv('bomb');", "    c.gooLeft = Math.max(c.goo ? c.gooLeft : 0, 4 + 2 * lv('bomb'));   // c286: 남은 시간과 새 시간 중 긴 쪽"),
  ("    car.gooLeft = 4 + 2 * lv('bomb');", "    car.gooLeft = Math.max(car.goo ? car.gooLeft : 0, 4 + 2 * lv('bomb'));   // c286"),
]
