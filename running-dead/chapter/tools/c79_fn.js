  // ── c79: 달리는 차와 몸 — 진짜 물리 ──
  //   처음 부딪힌 순간에만 다친다. 세기는 '차가 그 몸 쪽으로 밀고 드는 빠르기'(닿은 자리의 법선 방향)에 비례 — 정면으로 받으면 세고, 모서리로 스치면 약하다.
  //   마주 달려들던 몸은 더 세게, 같은 쪽으로 가던 몸은 약하게 받힌다. 튕긴 몸은 뜨지 않고 바닥을 미끄러진다 (저격총 넉백과 같다).
  //   무거운 몸(덩치)은 덜 튕기고 차를 더 많이 늦춘다. 그 뒤로는 그냥 밀린다 — 범퍼 앞에 낀 몸은 끌려간다 (같은 차에 다시 다치지 않는다).
  //   앞을 막은 몸들(범퍼에 닿은 몸 + 그 몸에 줄줄이 닿은 몸)의 무게 합만큼 차가 느려지고, 차의 미는 힘을 넘으면 아예 못 간다.
  const CH_PUSH = 8, CH_DRAG = 16, CH_VN_MIN = 0.8, CH_SCRAPE = 0.35;   // 차의 미는 힘 = 보통 몸 8개 × 차 무게 · 막혔을 때 줄어드는 빠르기(초당) · 이보다 느리게 밀고 들면 충돌이 아니다
  let chDt = 1 / 60;
  const chCarW = (b) => b.mut === 'armor' ? MY_FORCE * 1.3 * 2 / 3 : b.mut === 'hydra' ? 2 : 1;   // 차에 대한 몸의 무게 — 보통 1 · 덩치 6.93 · 히드라 2 (나도 같다)
  const chCarM = (car) => car.massK || (car.mil ? 1.6 : 1);
  const chCarCap = (car) => CH_PUSH * chCarM(car) * (car.pushK || 1);
  function chSkid(b, dt) {                     // 바닥에 쓸리는 먼지 — 내 둘레에서만
    if ((b.skidT = (b.skidT || 0) - dt) > 0) return; b.skidT = 0.1;
    if (Math.abs(b.foot.x - me.foot.x) > 13 || Math.abs(b.foot.z - me.foot.z) > 13) return;
    puff(b.foot.x + rand(-0.12, 0.12), 0.16, b.foot.z + rand(-0.12, 0.12), 0xb4ad9f, 0.3, rand(0.75, 1.05), rand(0.35, 0.5), 0, rand(0.15, 0.3), 0, 0.42);
  }
  function chCarHit(car, b, u, v, hu, hv, fx, fz, rx, rz, sp) {   // 달리는 차의 네모 안에 든 몸 — 처음 닿은 순간이면 친다 (튕김 + 데미지 + 차 감속). 아니면 밀리기만 한다
    const same = b.carC === car && clock < b.carCT;                // 이 차와 닿은 지 3초가 안 지났다 = 같은 충돌
    b.carC = car; b.carCT = clock + 3;
    if (same || sp < CH_VN_MIN || b.hitT || b.knockT > 0) return;
    if (car.tr && !isZombie(b) && !chBlind(b)) return;             // 평소 상태의 사람은 민간 차가 안 친다 (미리 보고 선다 — 닿아도 밀어내기만)
    const a = hu - b.r, c = hv - b.r, qu = Math.max(-a, Math.min(a, u)), qv = Math.max(-c, Math.min(c, v));   // 차의 실제 네모에서 그 몸에 가장 가까운 점
    let lu = u - qu, lv = v - qv; const ll = Math.hypot(lu, lv);
    if (ll > 1e-4) { lu /= ll; lv /= ll; } else if (hu - Math.abs(u) < hv - Math.abs(v)) { lu = u < 0 ? -1 : 1; lv = 0; } else { lu = 0; lv = v < 0 ? -1 : 1; }
    const nX = lu * fx + lv * rx, nZ = lu * fz + lv * rz, vcn = car.vx * nX + car.vz * nZ;   // 법선 (차 → 몸) · 차가 그쪽으로 밀고 드는 빠르기
    const rvx = car.vx - b.vel.x, rvz = car.vz - b.vel.y, rn = rvx * nX + rvz * nZ, vn = Math.max(0, rn);   // 둘이 가까워지던 빠르기 (법선 쪽) — 마주 달려들면 크고, 같은 쪽으로 가던 중이면 작다
    const tX = rvx - rn * nX, tZ = rvz - rn * nZ, vt = Math.hypot(tX, tZ);   // 스치는 쪽 (옆구리에 쓸릴 때)
    const ve = Math.min(CAR_SPEED * 1.6, Math.hypot(vn, CH_SCRAPE * vt));    // 충돌 세기 — 정면이면 그대로, 모서리면 조금 덜, 옆구리에 쓸리기만 하면 3분의 1쯤
    if (ve < CH_VN_MIN) return;
    const m = chCarW(b), M = CAR_MASS * chCarM(car), k2 = M / (M + m);
    const kx = nX * vn * KNOCK * k2 + tX * 0.6 * k2, kz = nZ * vn * KNOCK * k2 + tZ * 0.6 * k2;   // 법선 쪽으로 튕기고, 스친 쪽으로는 조금 쓸려 간다
    b.hitT = clock + 1; if (car.tr) { b.trHit = car; b.trHitT = clock + 3; }
    const dmg = CAR_HIT_DMG * ve / CAR_SPEED;
    if (isZombie(b)) { b.hp = Math.max(0, b.hp - dmg); if (b.hp <= 0) b.knockDie = true; }   // 좀비는 죽으면 밀려가서 멈춘 뒤에 사라진다
    else if (b.hp > 0) b.hp = Math.max(0, b.hp - dmg);             // 시민·경찰은 체력이 깎인다 (0이 되면 덮칠 수 있게 된다)
    if (giveKnock(b, kx, kz, Math.hypot(kx, kz), KNOCK_T)) b.knockCar = true;
    else if (b.knockDie) { b.knockDie = false; dying.push(b); }    // 흡수복으로 안 밀렸는데 죽었다
    const dv = 1.1 * ve * m / (M + m) * Math.max(0.25, vcn / sp), ns = Math.max(0, sp - dv);   // 차는 그 몸 무게만큼 운동량을 잃는다 (보통 몸 하나를 정면으로 = 경찰차 최고 속도의 10분의 1)
    car.vx *= ns / sp; car.vz *= ns / sp;
    car.lastHit = clock;
  }
  const chLd = [], chLd2 = [], chLdRow = [];
  function chCarLoad(car, fx, fz) {            // 앞을 막은 몸들의 무게 합 → car.load · 그만큼 느려진 비율 car.loadK (0 = 못 간다)
    const k = car.tr ? 1 : MOVING_K, hu1 = CAR_L * ckl(car) / 2 * k, hv1 = CAR_W * ck(car) / 2 * k, R = hu1 + 4.8;
    nearIn(zCells, car.x, car.z, R, chLd); const n0 = chLd.length; nearIn(cCells, car.x, car.z, R, chLd2); for (let i = 0; i < chLd2.length; i++) chLd[n0 + i] = chLd2[i];
    const row = chLdRow; row.length = 0;
    for (let i = 0, n = n0 + chLd2.length; i < n; i++) { const b = chLd[i];
      if (b.fixed || b.sleep || b.space) continue;
      const dx = b.foot.x - car.x, dz = b.foot.z - car.z, u = dx * fx + dz * fz, v = -dx * fz + dz * fx;
      if (u < hu1 * 0.4 || u > hu1 + 4.2 || Math.abs(v) > hv1 + b.r * 0.6 + 0.35) continue;
      b.ldU = u; b.ldV = v; b.ldOn = false; row.push(b);
    }
    row.sort((p, q) => p.ldU - q.ldU);
    let load = 0;
    for (let i = 0; i < row.length; i++) { const b = row[i];
      if (b.ldU < hu1 + b.r + 0.14 && Math.abs(b.ldV) < hv1 + b.r * 0.6) b.ldOn = true;   // 범퍼에 닿았다
      else for (let j = 0; j < i; j++) { const o = row[j]; if (o.ldOn && Math.hypot(o.ldU - b.ldU, o.ldV - b.ldV) < o.r + b.r + 0.12) { b.ldOn = true; break; } }   // 막고 있는 몸에 닿아 있다 (뒤에서 받치는 몸)
      if (b.ldOn) load += chCarW(b);
    }
    car.load = load; car.loadK = load > 0 ? Math.max(0, 1 - load / chCarCap(car)) : 1;
    if (load > 0) {                            // 미는 힘보다 무거우면 그만큼 느려진다 (운전자가 밟아도 못 넘는다)
      const sp = Math.hypot(car.vx, car.vz), base = car.tr ? car.tr.spd * (car.tr.spdK || 1) : CAR_SPEED * (car.mil ? 2 / 3 : 1), vmax = base * car.loadK;
      if (sp > vmax + 0.02) { const ns = Math.max(vmax, sp - CH_DRAG * chDt); car.vx *= ns / sp; car.vz *= ns / sp; }
    }
  }
