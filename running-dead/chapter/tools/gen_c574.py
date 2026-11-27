import pathlib
s = pathlib.Path('c573.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    for (let i = 0; i < 7; i++) { const a = Math.atan2(uz, ux) + rand(-0.5, 0.5), sp = rand(8, 14); const f = puff(c.foot.x + ux * 0.6, 0.6, c.foot.z + uz * 0.6, 0xffe9a0, 0.18, 0.08, 0.18, Math.cos(a) * sp, 0, Math.sin(a) * sp, 0.9); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; }",
    """    {   /* c574: 샷건 머즐 — 앞쪽 60° 부채꼴로 번쩍 + 산탄이 맞는 범위 끝까지 방사형으로 */
      const a0 = Math.atan2(uz, ux), mx = c.foot.x + ux * 0.55, mz = c.foot.z + uz * 0.55;
      for (let k = -2; k <= 2; k++) { const a = a0 + k * 0.21, d = 0.75 + (2 - Math.abs(k)) * 0.2; const f = puff(mx + Math.cos(a) * d, 0, mz + Math.sin(a) * d, 0xfff23a, 1.05 - Math.abs(k) * 0.12, 0.5, 0.09, 0, 0, 0, 0.85); f.s.material.map = flashTex; f.s.position.addScaledVector(UP, RADIUS); f.s.renderOrder = UI - 0.5; f.peak = true; }   // 부채꼴 섬광
      const life = 0.15, sp = R / life * 1.25;   /* 이펙트 감속(초당 2.5) 만큼 보탠다 */
      for (let i = 0; i < 13; i++) { const a = a0 + (i / 12 - 0.5) * (Math.PI / 3) + rand(-0.04, 0.04), v = sp * rand(0.8, 1.0);   // 산탄 13알 — 부채꼴 끝까지
        for (let j = 0; j < 3; j++) { const f = puff(mx, 0.6, mz, j ? 0xffc864 : 0xfff6c8, j ? 0.16 - j * 0.03 : 0.22, 0.06, life, Math.cos(a) * v, 0, Math.sin(a) * v, j ? 0.7 - j * 0.2 : 1, j * 0.018); f.s.material.map = flashTex; f.s.renderOrder = UI - 0.5; f.peak = true; } }   // 알갱이 + 꼬리 2개
    }""")
pathlib.Path('c574_patch.py').write_text('C574_R = ' + repr(R) + '\n')
print(len(R))
