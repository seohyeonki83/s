# c410: 부서진 차(잔해)는 보이기만 한다 — 부딪힘이 없다 (몸 · 차 · 길거리 사물 · 덮치기 가림 · 길 찾기)
src = open('c409.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# 1) 몸과 차: 잔해는 건너뛴다 (밀어내지도, 밀리지도 않는다)
rep("    for (const car of cars) {\n      const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx;\n      for (const b of (CHAPTER && (car.state === 'parked' || car.tr) ? chNearBodies(car) : bodies)) {",
    "    for (const car of cars) {\n      if (car.wreck) { if (car.load) { car.load = 0; car.loadK = 1; } continue; }   // c410: 잔해는 보이기만 한다 — 아무것도 안 막는다\n      const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx;\n      for (const b of (CHAPTER && (car.state === 'parked' || car.tr) ? chNearBodies(car) : bodies)) {")
# 2) 차와 차: 잔해가 낀 쌍은 건너뛴다
rep("      if (act && (B === A || (B.ix < A.ix && live(B)))) continue;   // 둘 다 움직이는 쌍은 한 번만\n",
    "      if (act && (B === A || (B.ix < A.ix && live(B)))) continue;   // 둘 다 움직이는 쌍은 한 번만\n      if (A.wreck || B.wreck) continue;   // c410: 잔해는 차도 그냥 지나간다\n")
# 3) 길거리 사물과 차: 잔해는 건너뛴다
rep("      for (const car of cars) { const dx = p.foot.x - car.x, dz = p.foot.z - car.z; if (dx > 4 || dx < -4 || dz > 4 || dz < -4) continue;\n",
    "      for (const car of cars) { if (car.wreck) continue;   /* c410 */ const dx = p.foot.x - car.x, dz = p.foot.z - car.z; if (dx > 4 || dx < -4 || dz > 4 || dz < -4) continue;\n")
# 4) 덮치기 가림: 잔해는 안 가린다
rep("    for (const car of cars) { if (car.obj && car.obj.dead && !car.wreck) continue; if (box(car)) return true; }",
    "    for (const car of cars) { if (car.wreck || (car.obj && car.obj.dead)) continue;   /* c410: 잔해는 안 가린다 */ if (box(car)) return true; }")
# 5) 길 찾기 · 자리 잡기에 쓰는 차 원: 잔해는 뺀다
rep("    const cs = cars.filter((c) => c.state === 'parked' && !CAR_TEST && !c.wall)   /* v513: 다시 계산 — 사람·차만 쓴다 */",
    "    const cs = cars.filter((c) => c.state === 'parked' && !CAR_TEST && !c.wall && !c.wreck   /* c410 */)   /* v513: 다시 계산 — 사람·차만 쓴다 */")
open('c410_patch.py', 'w').write("# c410: 잔해는 부딪힘이 없다\nC410_R = " + repr(R) + "\n")
print(len(R), 'entries')
