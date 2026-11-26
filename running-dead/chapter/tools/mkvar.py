# 테스트용 변형 — 화면 그리기를 끌 수 있게 하고, 길잡이(chGuide)가 쓰는 시간을 잰다
import pathlib, sys
ver = sys.argv[1]
base = pathlib.Path('/home/user/s/running-dead/chapter/' + ver + '.html').read_text()
R = "    renderer.render(scene, camera);\n  }\n\n  // ── 기술 (v190)"
assert base.count(R) == 1
nr = base.replace(R, "    if (!window.__noRender) renderer.render(scene, camera);\n  }\n  window.__redraw = () => { draw(0); place(); renderer.render(scene, camera); };   // 테스트용: 걸음 없이 다시 그리기만\n\n  // ── 기술 (v190)")
H = "    if (CHAPTER) { const g = chGuide(b, tx, tz); if (g) { tx = g[0]; tz = g[1]; } }"
assert nr.count(H) == 1
prof = nr.replace(H, "    const __t0 = performance.now();\n" + H + "\n    window.__pf = (window.__pf || 0) + performance.now() - __t0; window.__pn = (window.__pn || 0) + 1;")
# 근접 공격이 들어가는 순간을 테스트가 볼 수 있게 (때린 쪽, 맞은 쪽, 범위 공격인지)
M1, M0 = "else landHit(b, b.lungeVictim, ", "{ landHit(b, b.lungeVictim, "
if prof.count(M1) == 1: prof = prof.replace(M1, "else (window.__onMelee && window.__onMelee(b, b.lungeVictim, 0)), landHit(b, b.lungeVictim, ")
else:
    assert prof.count(M0) == 1; prof = prof.replace(M0, "{ (window.__onMelee && window.__onMelee(b, b.lungeVictim, 0)), landHit(b, b.lungeVictim, ")
M2 = "landHit(a, c, (a === me ? ALLY_DAMAGE * (1 + 0.07 * up.arm) * 1.3 * 1.3 * 2 : dmg) * 0.3);"
if prof.count(M2) != 1: M2 = "landHit(a, c, (a === me ? ALLY_DAMAGE * (1 + 0.07 * up.arm) * (CHAPTER ? 3 : 1.3 * 1.3 * 2) : dmg) * (CHAPTER ? 0.5 : 0.3));"   # c378
if prof.count(M2) != 1: M2 = "landHit(a, c, (a === me ? ALLY_DAMAGE * (1 + 0.07 * up.arm) * (CHAPTER ? 3 : 1.3 * 1.3 * 2) : v.kind === 'citizen' ? dmg : zDamage(a)) * (CHAPTER ? (chMonster(a) ? 1 : 0.5) : 0.3));"   # c430
if prof.count(M2) != 1: M2 = M2.replace('(a === me ? ALLY_DAMAGE', '(a === me ? CH_UPK.atk * ALLY_DAMAGE')   # c505
assert prof.count(M2) == 1; prof = prof.replace(M2, "(window.__onMelee && window.__onMelee(a, c, 1)), " + M2)
CAMA = "addScaledVector(BACK, camDist);"
if prof.count(CAMA) == 1: prof = prof.replace(CAMA, "addScaledVector(BACK, camDist * (window.__camK || 1));")   # 화면 캡처용: 카메라를 멀리
MODT = '<script type="module">'
if 'CH_SMALL' in prof:   # c120: 맵 선택 — 시험용은 고르지 않고 바로 (기본 큰 맵 · 작은 맵은 var/<ver>s.html)
    assert prof.count(MODT) == 1
    pathlib.Path('var/' + ver + 's.html').write_text(prof.replace(MODT, '<script>window.__map = "s";</script>\n' + MODT))
    prof = prof.replace(MODT, '<script>window.__map = "b";</script>\n' + MODT)
pathlib.Path('var/' + ver + '.html').write_text(prof)
print('var/' + ver + '.html')
