# c271: 도트 숫자 — 1.5배 크게 · 수명의 80%까지는 또렷하게, 마지막 20% 동안만 사라진다
C271_R = [
 ("f.s.material.map = chDotTex(n); f.s.scale.set(1.0, 0.5, 1); f.fixedScale = true; f.peak = true;", "f.s.material.map = chDotTex(n); f.s.scale.set(1.5, 0.75, 1); f.fixedScale = true; f.late = true;   /* c271: 1.5배 · 끝 20%만 사라짐 */"),
 ("f.s.material.opacity = f.blink ? f.op : f.peak ?", "f.s.material.opacity = f.late ? f.op * (u < 0.8 ? 1 : (1 - u) / 0.2) : f.blink ? f.op : f.peak ?"),
]
