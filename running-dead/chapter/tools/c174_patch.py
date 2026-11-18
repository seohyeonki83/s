# c174: 장갑차 돌진 — 속도 30% 빠르게 (경찰차의 1.2배 → 1.56배) · 시간 30% 짧게 (1.5초 → 1.05초). 거리는 둘을 곱한 만큼 (11.3칸 → 10.3칸)
C174_R = [
 ("car.tkPh = 'dash'; car.tkPhT = 1.5;", "car.tkPh = 'dash'; car.tkPhT = 1.05;   /* c174 */"),
 ("car.tkLeft = CAR_SPEED * 1.2 * 1.5;", "car.tkLeft = CAR_SPEED * 1.56 * 1.05;   /* c174 */"),
 ("const V = CAR_SPEED * 1.2 * Math.max(0, car.tkM);", "const V = CAR_SPEED * 1.56 * Math.max(0, car.tkM);   /* c174: 30% 빠르게 */"),
 ("car.tkPhT <= -1.5 ||", "car.tkPhT <= -1.05 ||"),
]
