# c396: 레벨업 = 15 + 0.1 × 레벨² (제곱 곡선)
C396_R = [('const needXp = (L) => Math.round(5 * Math.pow(1.13, L));', 'const needXp = (L) => CHAPTER ? Math.round(15 + 0.1 * L * L) : Math.round(5 * Math.pow(1.13, L));   /* c396: 제곱 곡선 — 처음 15명, 레벨마다 0.1 × 레벨²만큼 더 (레벨 20까지 548명 · 30까지 1307명 · 50까지 4795명) */')]
