# 측정용 변형 — stepWorld 구간마다 걸린 시간을 window.__ph 에 모은다 (게임 동작은 그대로)
import pathlib, sys
src, dst = sys.argv[1], sys.argv[2]
s = pathlib.Path(src).read_text()
def ins_before(anchor, code, cnt=1):
    global s
    assert s.count(anchor) == cnt, (anchor[:60], s.count(anchor))
    s = s.replace(anchor, code + anchor)
def ins_after(anchor, code, cnt=1):
    global s
    assert s.count(anchor) == cnt, (anchor[:60], s.count(anchor))
    s = s.replace(anchor, anchor + code)
HEAD = "  function stepWorld(dt) {\n    clock += dt;\n"
ins_before(HEAD, "  window.__ph = {}; let __pl = null, __pt = 0; function __tk(l) { const t = performance.now(); if (__pl) window.__ph[__pl] = (window.__ph[__pl] || 0) + t - __pt; __pl = l; __pt = t; }\n  window.__pd = {}; let __dl = null, __dt = 0; function __td(l) { const t = performance.now(); if (__dl) window.__pd[__dl] = (window.__pd[__dl] || 0) + t - __dt; __dl = l; __dt = t; }\n")
ins_after(HEAD, "    __tk('01 실제속도');\n")
B = [
 ("    if (CHAPTER && CH_BT) chBossTest(dt);   // c166\n", '02 아이템줍기등'),
 ("    zombies.length = 0;\n", '03 잠깨우기'),
 ("    if (CHAPTER) chSfTick(dt);   // c122\n", '04 부대·영역'),
 ("    for (const b of bodies) {                 // 걸음 전 자리·공간", '05 공간판정'),
 ("    buildGrids();", '06 근처칸'),
 ("    for (const b of bodies) if (isZombie(b)) updateZombie(b, dt);\n", '07 좀비판단'),
 ("    lazyFrame++;\n", '08 사람판단'),
 ("    if (CHAPTER) chBoardTick(dt);", '09 탑승'),
 ("    for (const z of dying) killZombie(z);", '11 차'),
 ("    collide(dt);\n", '12 몸충돌'),
 ("    carCarCollide();", '13 차충돌'),
 ("    for (const b of bodies) if (!b.fixed && !b.sleep && !(b.out && b.foot.x === b.px && b.foot.z === b.pz)) wallCollide(b);", '14 벽충돌'),
 ("    if (CHAPTER) for (const b of bodies) if (!b.fixed && !b.sleep && !(b.out && b.foot.x === b.px && b.foot.z === b.pz)) riverCollide(b);", '15 강충돌'),
 ("    for (const b of bodies) {                 // 지도(미니맵) 밖으로는 못 나간다 (v174)", '16 지도경계'),
 ("    tickItems(dt);", '17 출동등'),
 ("    if (CHAPTER) chFurnTick(dt);", '18 사물'),
 ("    if (CHAPTER) chBarTick(dt);", '19 건널목부대'),
 ("    if (CHAPTER && !CH_TUT) chDroneTick(dt);", '20 드론'),
 ("    if (CHAPTER) { chRespawnTick(dt); if (chStartW) chStartTick(); }", '21 다시채우기'),
 ("    draw(dt);\n    if (CHAPTER) chShadow();", '22 그림준비(draw)'),
 ("    if (CHAPTER) chShadow();                  // c13", '23 산그림자'),
 ("    checkTut();                               // 처음 만난 적 소개 (v202)", '24 이펙트'),
 ("    updateStars();\n    updateMinimap(dt);", '25 경보'),
 ("    updateMinimap(dt);\n    updateCmd(dt);", '26 미니맵'),
 ("    updateCmd(dt);\n    place();", '27 명령·카메라·냄새'),
 ("    if (!window.__noRender) renderer.render(scene, camera);\n  }\n", '28 화면그리기(render)'),
]
for a, l in B: ins_before(a, "    __tk('%s');\n" % l)
ins_after("    if (CHAPTER) chBoardTick(dt);   // c47: 싸움이 끝난 사람은 차로 돌아간다\n", "    __tk('10 이동·타격');\n")
ins_after("    if (!window.__noRender) renderer.render(scene, camera);\n", "    __tk(null);\n")
# draw() 안
D0 = "  function draw(dt) {\n    const eyes = bodies.filter((b) => isZombie(b) || b === me);\n"
ins_after(D0, "    __td('a 눈·탐험안개');\n")
D = [
 ("    if (CHAPTER) { chRoomDraw(); chCanopyDraw(eyes); }   // c53 · c85", 'c 방·지붕막'),
 ("    updateViewRect();\n    drawVision(eyes);", 'd 시야(광선)'),
 ("    drawCars(eyes);\n", 'e 차그림'),
 ("    for (const b of bodies) if (b.tracer) {   // v408", 'f 총알선'),
 ("    for (const b of bodies) {\n      if (b !== me && !onView(b.foot.x, b.foot.z, 1)) {", 'g 몸그림(전체몸)'),
 ("    if (me.aim) { me.aim.mesh.add(aimRing); aimRing.visible = true; }", 'h 조준'),
]
for a, l in D: ins_before(a, "    __td('%s');\n" % l)
# 지붕 줄은 버전마다 앞부분이 달라서 주석으로 찾는다
_i = s.index("// 좀비가 하나라도 들어간 건물만 지붕이 열린다"); _j = s.rindex("\n", 0, _i) + 1; s = s[:_j] + "    __td('b 지붕(건물)');\n" + s[_j:]
ins_after("    drawMyTarget();                           // v288: 내가 노리는 문·경찰차·금고 = 빨강\n", "    __td(null);\n")
# 바깥에서 쓰게
ins_before("  window.__rd = { get me() { return me; }", "  window.__ren = renderer; window.__scene = scene; window.__cam = camera; window.__batch = chBatchBodies;\n  if (typeof chSecs !== 'undefined') window.__secs = () => ({ live: chSecs.filter((S) => S.live).length, of: chSecs.length, dormB: chDormB.length, dormC: chDormC.length, dormO: chDormO.length, cars: cars.length, objs: objs.length, props: chProps.length }); window.__x = { walls, deco: chDecoObjs, reset: () => { chBlk = null; chBlocks = null; chWcGrid = null; }, cf: () => { const t = performance.now(); cfCompute(); return performance.now() - t; }, cfSize: () => [cfW, cfH] };\n")
pathlib.Path(dst).write_text(s)
print(dst)
