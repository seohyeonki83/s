# c266: 도트 숫자를 맨 위에 (모든 체력바·내 UI보다 위)
C266_R = [
 ("f.s.material.map = chDotTex(n); f.s.scale.set(1.0, 0.5, 1); f.fixedScale = true; f.peak = true; f.s.renderOrder = UI - 1;", "f.s.material.map = chDotTex(n); f.s.scale.set(1.0, 0.5, 1); f.fixedScale = true; f.peak = true; f.s.renderOrder = UI_ME + 90;   /* c266: 맨 위 */"),
]
