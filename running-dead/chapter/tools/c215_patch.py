# c215: 벽 토막 수 30% 줄임 — 토막 길이 2배 (문 옆 짧은 토막은 1개 아래로 못 줄여서 전체로 약 29%)
C215_R = [
 ("const LP = hs.length ? hs.reduce((s, B) => s + (B.x1 - B.x0 + B.z1 - B.z0) / 2, 0) / hs.length / 2 : 2.2", "const LP = (hs.length ? hs.reduce((s, B) => s + (B.x1 - B.x0 + B.z1 - B.z0) / 2, 0) / hs.length / 2 : 2.2) / 0.5   /* c215: 토막 수 30% 줄임 */"),
]
