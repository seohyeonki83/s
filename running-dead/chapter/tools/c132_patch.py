# c132: 길거리 빨강 10%를 한 번 더 하양으로 (남은 빨강의 10% → 합쳐서 19%)
C132_R = [
 ("&& !B && (type === 'vig' || type === 'attacker') && Math.random() < 0.1) { type = ''; wOut = true; }", "&& !B && (type === 'vig' || type === 'attacker') && Math.random() < (type === 'vig' ? 0.19 : 0.1)) { type = ''; wOut = true; }   /* c132: 빨강은 10% 한 번 더 */"),
]
