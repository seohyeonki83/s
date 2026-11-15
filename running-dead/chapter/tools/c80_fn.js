  // ── c80: 수송차 (물음표) · 운전자 성격과 패닉 ──
  //   차가 생길 때 30대 중 1대는 수송차 — 현금 수송차(현금) · 구급차(주사·바이러스 등 의료 5종) · 택배차(나머지 8종). 싣는 가짓수에 비례해 나오므로, 수송차 하나를 부수면 14종이 같은 확률로 나온다.
  //   수송차는 위에 물음표가 뜬다 (금고와 같은 노란 물음표). 부수면 실은 것 하나가 그 자리에 떨어지고, 랜드마크 문이 부서졌을 때처럼 사수 경찰차 1대가 그 자리로 온다.
  //   운전자: 조심형(지금까지의 운전 — 가운데 좀비 앞에 서고, 맞으면 얼어붙었다가 내린다) · 가속형(서 있다가 냅다 밟는다 — 좀비도 사람도 안 가린다) ·
  //           비비기형(물러났다가 옆으로 다시 들이민다) · 돌진형(좀비를 아예 신경 안 쓴다 — 현금 수송차는 늘 이쪽). 패닉 중엔 더 밟는다 (1.3~1.6배).
  const CH_LOOT_P = 1 / 30;
  const CH_LOOT_CAR = { cash: ['cash'], ambul: ['mutate', 'awaken', 'catalyst', 'rage', 'blood'], parcel: ['bomb', 'taser', 'book', 'bag', 'crowbar', 'absorb', 'vest', 'shoes'] };
  const CH_LOOT_N = Object.values(CH_LOOT_CAR).reduce((a, l) => a + l.length, 0);
  const chLootType = () => { let r = Math.random() * CH_LOOT_N; for (const k in CH_LOOT_CAR) if ((r -= CH_LOOT_CAR[k].length) < 0) return k; return 'parcel'; };
  const chLootRoll = () => { let r = Math.random() * CH_LOOT_N / CH_LOOT_P; if (r >= CH_LOOT_N) return null; for (const k in CH_LOOT_CAR) if ((r -= CH_LOOT_CAR[k].length) < 0) return k; return 'parcel'; };   // 한 번의 추첨으로: 30분의 1 안에서 가짓수대로 (1 : 5 : 8)
  const CH_TR_FAST = 1.25;                     // 기본 속도 = 지금 속도(최저) ~ 그 1.25배, 차마다 다르다
  const CH_DRV_RAM = 10 / 3, CH_DRV_K = (100 - CH_DRV_RAM) / 90;   // 돌진형은 3분의 1로 (10% → 3.33%) — 줄어든 몫은 나머지 셋이 원래 비율대로 나눠 갖는다. 현금 수송차는 늘 돌진형
  const CH_DRV = [['calm', 40 * CH_DRV_K], ['floor', 25 * CH_DRV_K], ['wiggle', 25 * CH_DRV_K], ['ram', CH_DRV_RAM]];
  const CH_TR_LIFE = [40, 80], CH_TR_LIFE_LOOT = 3;   // 이만큼(초) 돌아다닌 차는 내 눈 밖에서 구역을 떠나고, 곧 새 차가 들어온다 (지나가는 차들) · 수송차는 3배 오래 돈다 (쫓아가 세울 틈)
  const CH_TR_RAGE_MAX = 1.15;                // 밟아도 경찰차 최고 속도의 1.15배까지
  function chTrDriver(car, loot) {             // 갓 생긴 차에 운전자 성격을 붙인다 (수송차면 물음표도)
    const T = car.tr, F = window.__trForce || null;
    let drv = 'calm'; { let r = Math.random() * 100; for (const [k, w] of CH_DRV) if ((r -= w) < 0) { drv = k; break; } }
    if (loot === 'cash') drv = 'ram';
    if (F && F.drv) drv = F.drv;
    T.drv = drv; T.panicT = 0; T.pk = rand(1.3, 1.6); T.spdK = 1; T.rage = false; T.wig = null; T.wigN = 0; T.wigMax = 2 + Math.floor(Math.random() * 3); T.nerve = rand(0.4, 1.5); T.nerveT = 0; T.wv = 0; T.wvT = 0; T.seenHit = 0; T.smT = 0;
    T.life = rand(CH_TR_LIFE[0], CH_TR_LIFE[1]) * (loot ? CH_TR_LIFE_LOOT : 1); T.lifeT = 0;
    T.exitDmg = drv === 'calm' ? rand(0.1, 0.3) : drv === 'ram' ? rand(0.4, 0.65) : rand(0.2, 0.45);
    if (loot) {
      car.loot = loot;
      const q = new THREE.Sprite(new THREE.SpriteMaterial({ map: SAFE_Q, transparent: true, depthTest: false, depthWrite: false }));
      q.renderOrder = UI - 1; q.scale.set(2.7 / car.kl, 1.35, 1); q.position.set(0, 1.6, 0); car.g.add(q); car.qm = q;
    }
  }
  function chTrPanic(T, sec) { if (T.drv !== 'calm') T.panicT = Math.max(T.panicT, sec); }
  function chLootDrop(car) {                   // 수송차가 부서졌다 → 실은 것 하나가 그 자리에 떨어지고 (금고와 같다) 경찰이 출동한다
    if (car.looted) return; car.looted = true; if (car.qm) car.qm.visible = false;
    const mine = CH_LOOT_CAR[car.loot].filter((k) => !chFull(k)), rest = CH_ITEMS.filter((k) => !chFull(k)), pool = mine.length ? mine : rest;   // 끝까지 올린 아이템은 안 나온다 — 그 차 몫이 다 찼으면 남은 것 중에서
    if (pool.length) { car.lootGot = pool[Math.floor(Math.random() * pool.length)]; dropPickup(car.lootGot, car.x, car.z, null); }
    chCarRobbed(car);
  }
  function chCarRobbed(car) {                  // 털린 수송차 자리로 사수 경찰차 1대 — 랜드마크 문이 부서졌을 때와 똑같다 (구역 가장자리 안 보이는 곳에서 나와 도로를 무시하고 온다 · 오다가 좀비를 보면 서서 내린다 · 닿으면 서서 그 둘레를 지킨다)
    const zi = chZoneAt(car.x, car.z), G = { x0: car.x - 1, z0: car.z - 1, x1: car.x + 1, z1: car.z + 1, doors: [], zone: zi, robbed: true }, p = chEdgeSpot(zi);
    addCar(p.x, p.z, Math.atan2(car.z - p.z, car.x - p.x), new THREE.Vector2(car.x, car.z), 2 + Math.floor(Math.random() * 2));
    cars[cars.length - 1].guard = G; chRobbed++;
  }
  let chRobbed = 0;
  function chTrBehind(car, fx, fz) {           // 바로 뒤가 막혔나 (후진할 때) — 다른 차 · 건물 · 강 · 지도 밖
    const L = CAR_L * ckl(car), px = car.x - fx * (L / 2 + 0.7), pz = car.z - fz * (L / 2 + 0.7);
    if (px < MM.x0 + 1 || px > MM.x1 - 1 || pz < MM.z0 + 1 || pz > MM.z1 - 1 || spaceOf(px, pz) || chNearRiver(px, pz, 0.4)) return true;
    for (const c of cars) { if (c === car || c.wreck) continue; if (Math.hypot(c.x - px, c.z - pz) < CAR_L * ckl(c) / 2 + 0.5) return true; }
    return false;
  }
  function chTrSmoke(car, T, dt) {             // 밟는 차 — 뒤에서 연기 (내 둘레에서만)
    if ((T.smT -= dt) > 0) return; T.smT = 0.13;
    if (Math.abs(car.x - me.foot.x) > 14 || Math.abs(car.z - me.foot.z) > 14) return;
    const fx = Math.cos(car.h), fz = Math.sin(car.h), L = CAR_L * ckl(car);
    puff(car.x - fx * L / 2 + rand(-0.2, 0.2), 0.2, car.z - fz * L / 2 + rand(-0.2, 0.2), 0x9a9a96, 0.35, rand(1.0, 1.4), rand(0.4, 0.6), -fx * 0.6, rand(0.2, 0.4), -fz * 0.6, 0.38);
  }
