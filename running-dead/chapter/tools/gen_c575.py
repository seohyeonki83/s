import pathlib
s = pathlib.Path('c574.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    station: { col: '#b44ee6', name: '경찰서', say: '깝치면 개털림' },",
    """    station: { col: '#b44ee6', name: '경찰서', say: '깝치면 개털림' },
    sg: { col: '#7a1f94', name: '샷건 경찰', say: '가까이 다가와 부채꼴로 쏘고<br>맞은 좀비를 밀어냅니다.' },   /* c575: 챕터 첫 발견 소개 */
    robot: { col: '#2f5a1a', name: '사각 로봇', say: '단단한 로봇입니다.<br>감염되지 않고 부서지면 터집니다.' },
    turret: { col: '#8a93a3', name: '터렛', say: '건널목을 지키는 고정 포대입니다.<br>한 번에 8발 · 부서지면 터집니다.' },
    drone: { col: '#7fe3ff', name: '드론', say: '하늘에서 기관총을 쏩니다.' },
    red: { col: '#ff4a3d', name: '자경단', say: '몽둥이로 때려 밀어냅니다.' },
    pink: { col: '#ff5fa8', name: '변이 인간', say: '감염시키면 변이 동료가 됩니다.' },""")
rep("  function checkTut() {                       // 처음으로 내 시야에 들어온 종류 → 소개 줄 세우기\n",
    """  let chTutClk = -9;
  function chTutAdd(k, item) { tutSeen[k] = true; CH_SV.seen[k] = 1; chSave(); tutQueue.push(Object.assign({ k }, item)); }
  function checkTut() {                       // 처음으로 내 시야에 들어온 종류 → 소개 줄 세우기
    if (CH_RUN) {   /* c575: 챕터 — 적 종류마다 처음 발견(나 + 동료 시야)하면 카메라가 가서 한 번 소개 (보스 빼고 · 기록에 남아 다시 안 나온다) */
      if (clock - chTutClk < 0.2 || !isZombie(me)) return; chTutClk = clock; const SV = CH_SV.seen = CH_SV.seen || {};   // 판 시작에 '본 것'으로 찍어 두는 기본 종류도 챕터에선 저장 기록만 본다
      for (const b of bodies) {
        if (b.kind !== 'citizen' || b.bBoss || b.dead) continue;
        const k = b.turret ? 'turret' : b.robot ? 'robot' : b.sg ? 'sg' : b.sniper ? 'sniper' : b.soldier ? 'soldier' : b.police ? 'police' : b.boss ? 'pink' : b.vig ? 'red' : b.attacker ? 'attacker' : b.guard ? 'guard' : 'citizen';
        if (SV[k] || !(iSee(b) || zSeen(b))) continue;
        chTutAdd(k, { x: b.foot.x, z: b.foot.z, b });
      }
      if (!SV.drone) for (const d of chDrones) if (!d.dead && (iSee(d) || zSeen(d))) { chTutAdd('drone', { x: d.foot.x, z: d.foot.z, b: { foot: d.foot, halfH: d.h, mesh: d.s } }); break; }
      return;
    }
""")
rep("    police: { col: '#8e24aa', name: CHAPTER ? '경찰' : '짭새', say: '건법 씀' },", "    police: { col: '#8e24aa', name: CHAPTER ? '경찰' : '짭새', say: CHAPTER ? '총을 쏘는 경찰입니다.' : '건법 씀' },")
rep("    guard: { col: CHAPTER ? '#ffcf33' : '#ff8c1a', name: CHAPTER ? '강한 인간' : '헬창', say: '깝침' },", "    guard: { col: CHAPTER ? '#ffcf33' : '#ff8c1a', name: CHAPTER ? '강한 인간' : '헬창', say: CHAPTER ? '체력이 높은 인간입니다.' : '깝침' },")
rep("    attacker: { col: CHAPTER ? '#ff8c1a' : '#c62828', name: CHAPTER ? '위협적인 인간' : '만두귀', say: '좀 침' },", "    attacker: { col: CHAPTER ? '#ff8c1a' : '#c62828', name: CHAPTER ? '위협적인 인간' : '만두귀', say: CHAPTER ? '보자마자 덤벼듭니다.' : '좀 침' },")
rep("    sniper: { col: '#ff2a2a', name: '저격수', say: '발빠른 저격수<br>제거 1순위' },", "    sniper: { col: '#ff2a2a', name: '저격수', say: CHAPTER ? '멀리서 강하게 쏘고 밀어냅니다.<br>제거 1순위' : '발빠른 저격수<br>제거 1순위' },")
pathlib.Path('c575_patch.py').write_text('C575_R = ' + repr(R) + '\n')
print(len(R))
