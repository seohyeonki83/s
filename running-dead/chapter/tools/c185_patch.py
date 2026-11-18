# c185: 첫 카운트다운은 '특공대 도착까지' · 보스 체력 10% 줄임 · 보스 체력바 = 내 체력바만큼 굵게, 내 체력바보다 위에 그린다
C185_R = [
 ("s = chSf.n < 4 ? '다음 특공대 출동까지 ' + left + '초'", "s = chSf.n < 4 ? (chSf.n === 0 ? '특공대 도착까지 ' : '다음 특공대 출동까지 ') + left + '초'"),
 ("car.hpK = 10 * 0.95 * 3;", "car.hpK = 10 * 0.95 * 3 * 0.9;   /* c185: 10% 줄임 */"),
 ("chCarObj(car, false); car.obj.oneBar = true;", "chCarObj(car, false); car.obj.oneBar = true; car.obj.hpBar.scale.y = 3 * 0.7; for (const m of car.obj.hpBar.children) m.renderOrder += UI_ME + 60 - UI;   // c185: 내 체력바만큼 굵게 · 내 것보다 위"),
]
