# c134: 장갑차 돌진 때 게임이 멈추던 것 고침 — 무는 중이라 그 자리에 붙어 있던(fixed) 좀비·사람을 사물로 잘못 보고 부숴서 오류가 났다. 사물(금고 종류)만 깔아뭉갠다
C134_R = [
 ("if (car.tank && (b.fixed || b.prop || b.kind === 'safe')) { chTankCrush(car, b, fx, fz, rx, rz); continue; }", "if (car.tank && b.kind === 'safe') { chTankCrush(car, b, fx, fz, rx, rz); continue; }   /* c134: 사물·금고만 (무는 중인 몸은 사물이 아니다) */"),
]
