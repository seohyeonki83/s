# c449: 덩치 · 히드라(변이) 동료를 얻으면 — 멈추고 카메라가 그 동료로 가서 비춘 뒤 획득창 · 확인을 누르면 카메라가 나에게 돌아온다 (튜토리얼 '발견'과 같은 느낌)
src = open('c448.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    if (b.prop === 'hvat' || b.prop === 'avat') pendingAward.push(b.prop === 'avat' ? 'mut:armor' : 'mut:hydra');", "    if (b.prop === 'hvat' || b.prop === 'avat') { pendingAward.push(b.prop === 'avat' ? 'mut:armor' : 'mut:hydra'); chMutFoc.push(c); }   // c449: 카메라가 비출 동료")
rep("    mutate(b, t); pendingAward.push('mut:' + t);", "    mutate(b, t); pendingAward.push('mut:' + t); chMutFoc.push(b);   /* c449 */")
rep("  function chShowMut(type) {                  // c316: 덩치·히드라 동료를 얻었다 — 무기 획득창과 같은 창 (사용자 문구 그대로)\n    acqOpen = true; paused = true; stopInput();\n", """  const chMutFoc = [];                         // c449: 동료 획득창마다 비출 동료 (덩치 · 히드라)
  function chShowMut(type) {                  // c316: 덩치·히드라 동료를 얻었다 — 무기 획득창과 같은 창 (사용자 문구 그대로)
    acqOpen = true; paused = true; stopInput();
    if (CHAPTER && type !== 'zombie') { const b = chMutFoc.shift(); if (b && bodies.includes(b) && !chMutPanned) {   // c449: 먼저 카메라가 그 동료로 가서 비춘다
      const P = new THREE.Vector3(b.foot.x, 0, b.foot.z).addScaledVector(UP, b.halfH || RADIUS), [sx, sy] = viewCenter(), o = centerOn(P.x, P.y, P.z, sx, sy);
      chMutPanned = true; panCam(o.x, o.z, () => { hiOn(b.mesh); setTimeout(() => { hiOff(); chShowMut(type); }, 1100); }); return; } }
    const back = chMutPanned; chMutPanned = false;
""")
rep("      setTimeout(() => { ov.remove(); acqOpen = false; paused = false; last = 0; }, 260);\n    });\n  }\n  function showAward(kind) {", "      setTimeout(() => { ov.remove(); if (back) panCam(0, 0, () => { acqOpen = false; paused = false; last = 0; }); else { acqOpen = false; paused = false; last = 0; } }, 260);   // c449: 확인 → 카메라가 나에게 돌아온 뒤 다시 움직인다\n    });\n  }\n  let chMutPanned = false;\n  function showAward(kind) {")
open('c449_patch.py', 'w').write("# c449: 변이 동료 획득 — 카메라로 비추기\nC449_R = " + repr(R) + "\n")
