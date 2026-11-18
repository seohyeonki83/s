# c173: 장갑차는 돌진하는 동안 기관포를 안 쏜다 (후진 중엔 쏜다)
C173_R = [
 ("    if (car.burstN > 0) { if ((car.burstT -= dt) <= 0) chTankBullet(car); }", "    if (car.tkPh === 'dash') car.burstN = 0;   // c173: 돌진 중엔 안 쏜다\n    else if (car.burstN > 0) { if ((car.burstT -= dt) <= 0) chTankBullet(car); }"),
]
