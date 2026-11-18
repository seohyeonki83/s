# c170: 장갑차 포탑(총구)이 쏘는 쪽으로 돌아간다 — 노린 좀비가 없으면 앞을 본다. 총구를 조금 길고 굵게
C170_R = [
 ("const brl = new THREE.Mesh(new THREE.PlaneGeometry(0.72, 0.09).rotateX(-Math.PI / 2), carMat(0x161c0e)); brl.position.set(0.5, 0.003, 0); brl.renderOrder = -0.435;",
  "const brl = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.13).rotateX(-Math.PI / 2), carMat(0x0e1208)); brl.position.set(0.6, 0.003, 0); brl.renderOrder = -0.435;   /* c170: 길고 굵게 */"),
 ("    car.g.add(tur, brl);\n", "    const tg = new THREE.Group(); tg.add(tur, brl); car.g.add(tg); car.tkTur = tg; car.tkAim = 0;   // c170: 포탑 — 돌아간다\n"),
 ("    const car = chTank; if (!car || !car.tracer) return;\n", """    const car = chTank; if (!car || !car.tracer) return;
    if (car.tkTur && !car.wreck) {               // c170: 포탑을 노린 좀비 쪽으로 (초당 약 340도)
      const z = car.burstN > 0 && car.burstZ && isZombie(car.burstZ) ? car.burstZ : car.foe && isZombie(car.foe) ? car.foe : null;
      const want = z ? -(Math.atan2(z.foot.z - car.z, z.foot.x - car.x) - car.h) : 0;
      let d = want - car.tkAim; d = Math.atan2(Math.sin(d), Math.cos(d));
      const st = 6 * dt; car.tkAim += Math.abs(d) <= st ? d : Math.sign(d) * st;
      car.tkTur.rotation.y = car.tkAim;
    }
"""),
]
