# c192: 길거리 배회 경찰 — 처음 0 · 수상함 = 기본 · 수상함과 난리남 사이 한가운데 = 기본의 1.5배 (두 번만)
C192_R = [
 ("const k = stars >= 2 ? 1.5 : deaths >= mid ? 1 : stars >= 1 ? 0.5 : 0;", "const k = deaths >= mid ? 1.5 : stars >= 1 ? 1 : 0;   /* c192 */"),
]
