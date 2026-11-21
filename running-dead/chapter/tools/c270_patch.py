# c270: 보스 감전 시간 = 다른 적과 같다 (3분의 1 → 그대로)
C270_R = [
 ("if (c.tank) { c.stunT = CH_WV('taserT', lv('taser')) / 3;", "if (c.tank) { c.stunT = CH_WV('taserT', lv('taser'));   /* c270: 보스도 같다 */"),
]
