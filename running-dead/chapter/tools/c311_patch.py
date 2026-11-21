# c311: 튜토리얼 바리케이트는 복도 벽 안에 갇힌다 (큰 맵 다리 경계처럼 — 벽은 안 밀린다). 전엔 '건물 밖으로 꺼내기'가 복도 밖으로 튕겨 냈다
C311_R = [("  function carClampB(car) {                   // v463: 건물에 파고든 차를 가장 가까운 벽 밖으로\n",
  """  function carClampB(car) {                   // v463: 건물에 파고든 차를 가장 가까운 벽 밖으로
    if (CHAPTER && car.tutS) {                  // c311: 복도 안 바리케이트 — 거꾸로 그 복도 벽 안쪽으로 (돌아간 만큼의 폭까지)
      const S = car.tutS, c = Math.abs(Math.cos(car.h)), s = Math.abs(Math.sin(car.h)), L = CAR_L * ckl(car), W = CAR_W * ck(car) * (car.barr ? CH_BARR_W : 1), ex = c * L / 2 + s * W / 2, ez = s * L / 2 + c * W / 2;
      car.x = Math.max(S.x0 + ex, Math.min(S.x1 - ex, car.x)); car.z = Math.max(S.z0 + ez, Math.min(S.z1 - ez, car.z));
      return;
    }
""")]
