# c179: 장갑차 몸통 = 모서리를 살짝 깎은 팔각형 · 길이 조금 더 짧게 (원래 길이의 85% → 78%) · 출동해서 올 때(눈에 띄기 전) 속도 = 경찰차 최고 속도의 90%
C179_R = [
 ("CH_TK_KL = MIL_K * 2 * 0.8 * 0.85,", "CH_TK_KL = MIL_K * 2 * 0.8 * 0.78,   /* c179: 78% */"),
 ("K[0].scale.x = 0.85;   /* c177 */", """K[0].geometry = (() => { const L = CAR_L * 0.78, W = CAR_W, c = 0.16, s = new THREE.Shape(); s.moveTo(-L / 2 + c, -W / 2); s.lineTo(L / 2 - c, -W / 2); s.lineTo(L / 2, -W / 2 + c); s.lineTo(L / 2, W / 2 - c); s.lineTo(L / 2 - c, W / 2); s.lineTo(-L / 2 + c, W / 2); s.lineTo(-L / 2, W / 2 - c); s.lineTo(-L / 2, -W / 2 + c); s.closePath(); return new THREE.ShapeGeometry(s).rotateX(-Math.PI / 2); })();   /* c179: 모서리를 깎은 팔각형 */"""),
 ("PlaneGeometry(CAR_L * 0.96 * 0.85, 0.13)", "PlaneGeometry(CAR_L * 0.78 - 0.36, 0.13)   /* c179: 깎은 모서리 안쪽까지 */"),
 ("const spd = CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / (car.tkSeen ? 2 : 1) * (car.goo ? 0.8 : 1);", "const spd = (car.tkSeen ? CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / 2 : CAR_SPEED * 0.9) * (car.goo ? 0.8 : 1);   /* c179: 눈에 띄기 전 = 경찰차의 90% */"),
]
