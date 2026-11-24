# c419: 드론 주기 2배 · 한 번에 2배
C419_R = [('CH_DRONE_EVERY = 40,', 'CH_DRONE_EVERY = 80,   /* c419: 40 → 80초 (주기 2배) */'), ('N = stars <= 3 ? 1 : stars === 4 ? 2 : 3; i < N', 'N = (stars <= 3 ? 1 : stars === 4 ? 2 : 3) * 2   /* c419: 한 번에 2배 */; i < N')]
