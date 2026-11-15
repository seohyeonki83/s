# c119: 건물 찾기 격자 — 좌표가 숫자가 아닐 때(NaN)도 멈추지 않고 '밖'으로 본다 (c114의 허점)
C119_R = [
 ("if (c < 0 || r < 0 || c >= chSpW || r >= chSpH) return null;", "if (!(c >= 0 && r >= 0 && c < chSpW && r < chSpH)) return null;   /* c119: NaN도 걸러낸다 */"),
]
