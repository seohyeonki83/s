# c209: 나 — 벽 토막도 금고·문처럼: 쫓는 사람(저격수 빼고)보다 가까우면 친다 · 한 번 치기 시작하면 붙잡고 끝까지
C209_R = [
 ("if (d && d.type === 'door') ob = d;", "if (d && (d.type === 'door' || d.type === 'wall')) ob = d;   /* c209: 벽도 */"),
 ("z.meLock = ob.type === 'door' ? ob : null", "z.meLock = ob.type === 'door' || ob.type === 'wall' ? ob : null   /* c209 */"),
]
