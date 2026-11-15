# c114: 큰 무리일 때 프레임 드랍 줄이기 (시야 어둠 계산) · 경보단계 조건 20% 앞당김
import pprint
S = open('c113.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
# 시야: 눈(좀비)이 많을수록 붙어 있는 눈을 더 넓게 합친다 (40명까지는 그대로 1칸 · 그 뒤로 60명마다 1칸씩, 많아야 2.6칸). 바깥 눈부터 그리므로 무리 가장자리 시야는 그대로다
rep("    const others = eyes.filter((z) => z !== me).sort((a, b) => far2(b) - far2(a));", "    const others = eyes.filter((z) => z !== me).sort((a, b) => far2(b) - far2(a));\n    const eyeMerge = CHAPTER && eyes.length > 40 ? Math.min(2.6, EYE_MERGE + (eyes.length - 40) / 60) : EYE_MERGE;   // c114")
rep("k.sense >= R - 0.3 && Math.hypot(k.foot.x - x, k.foot.z - y) < EYE_MERGE)) continue;", "k.sense >= R - 0.3 && Math.hypot(k.foot.x - x, k.foot.z - y) < eyeMerge)) continue;")
# 동료마다 걸음마다 차 목록을 전부 훑던 '막힌 차 찾기'(챕터에선 c86부터 안 쓴다)를 건너뛴다
rep("          if (!z.space) for (const OL of (CHAPTER ? chObjLists2 : chObjLists1)", "          if (!z.space && !CHAPTER) for (const OL of (CHAPTER ? chObjLists2 : chObjLists1)")
rep("          if (CHAPTER && z.space && z.space.fs) for (const t of z.space.fs) { if (t.obj.dead) continue; const g = objGap(t.obj, z); if (g <= reach && g < cd) { cd = g; cb = t.obj; } }", "          /* c114: 챕터에선 안 쓴다 (가면서 치기로 바뀌었다) */")
# 동료의 '손 닿는 사물 찾기'는 0.1초쯤 기억해 둔다 (걸음마다 문·차 목록을 다 훑지 않게)
rep("  function nearObj(z) {\n    let best = null, bd = Infinity, any = null, ad = Infinity;", "  function nearObj(z) {\n    if (CHAPTER && z !== me && z.noT > clock) { const o = z.noV; if (!o || (!o.dead && !o.off)) { nearObj.any = o; return o; } }   // c114\n    let best = null, bd = Infinity, any = null, ad = Infinity;")
rep("    nearObj.any = any;  ", "    if (CHAPTER && z !== me) { z.noV = best; z.noT = clock + 0.1 + Math.random() * 0.06; }   // c114\n    nearObj.any = any;  ")
# '이 자리가 어느 건물 안인가'(spaceOf) — 걸음마다 몸마다 건물 70여 채를 다 훑던 것을 4칸 격자로 (그 칸에 걸친 건물만 본다. 결과는 같다)
old = [l for l in S.split('\n') if l.startswith("  const spaceOf = (x, z) => chRooms.find(")][0]
rep(old, """  let chSpG = null, chSpN = -1, chSpW = 0, chSpH = 0, chSpX = 0, chSpZ = 0;   // c114: 건물 찾기 격자 (칸마다 [방들, 건물들] — 원래 목록 순서 그대로)
  function chSpBuild() {
    let x0 = Infinity, z0 = Infinity, x1 = -Infinity, z1 = -Infinity;
    for (const B of buildings) { if (B.x0 < x0) x0 = B.x0; if (B.z0 < z0) z0 = B.z0; if (B.x1 > x1) x1 = B.x1; if (B.z1 > z1) z1 = B.z1; }
    chSpX = x0 - 1; chSpZ = z0 - 1; chSpW = Math.max(1, Math.ceil((x1 - x0 + 2) / 4)); chSpH = Math.max(1, Math.ceil((z1 - z0 + 2) / 4));
    chSpG = Array.from({ length: chSpW * chSpH }, () => [[], []]);
    const put = (B, k) => { for (let r = Math.max(0, Math.floor((B.z0 - chSpZ) / 4)); r <= Math.min(chSpH - 1, Math.floor((B.z1 - chSpZ) / 4)); r++) for (let c = Math.max(0, Math.floor((B.x0 - chSpX) / 4)); c <= Math.min(chSpW - 1, Math.floor((B.x1 - chSpX) / 4)); c++) chSpG[r * chSpW + c][k].push(B); };
    for (const B of chRooms) put(B, 0); for (const B of buildings) put(B, 1);
    chSpN = buildings.length * 1000 + chRooms.length;
  }
  const spaceOf = (x, z) => {
    if (chSpN !== buildings.length * 1000 + chRooms.length) chSpBuild();
    const c = Math.floor((x - chSpX) / 4), r = Math.floor((z - chSpZ) / 4); if (c < 0 || r < 0 || c >= chSpW || r >= chSpH) return null;
    const G = chSpG[r * chSpW + c], A = G[0], B2 = G[1];
    for (let i = 0; i < A.length; i++) if (chIn(A[i], x, z)) return A[i];
    for (let i = 0; i < B2.length; i++) if (chIn(B2[i], x, z)) return B2[i];
    return null;
  };   /* c53: 방이 먼저 */   // 이 자리가 들어 있는 건물 (밖이면 null)""")
# 사람 깨우기·재우기 — 좀비 전부와 거리를 재던 것을 둘레 칸의 좀비하고만 (지난 걸음의 좀비 격자)
rep("        if (hot && (near(b, me) || zombies.some((z) => near(b, z)))) { b.met = true; chWakeUp(b); }", "        if (hot && (near(b, me) || (G_W ? nearIn(zCells, b.foot.x, b.foot.z, CH_MEET, chWkBuf).some((z) => isZombie(z) && near(b, z)) : zombies.some((z) => near(b, z))))) { b.met = true; chWakeUp(b); }   /* c114 */")
rep("          if (far(me) && zombies.every(far)) { b.met = false; b.sleep = true; b.vel.set(0, 0); }", "          if (far(me) && (G_W ? nearIn(zCells, b.foot.x, b.foot.z, CH_SLEEP, chWkBuf).every((z) => !isZombie(z) || far(z)) : zombies.every(far))) { b.met = false; b.sleep = true; b.vel.set(0, 0); }   /* c114 */")
rep("  let G_W = 0, G_H = 0, zCells = [], cCells = [];", "  let G_W = 0, G_H = 0, zCells = [], cCells = []; const chWkBuf = [];")
# 경보단계: 수상함 뒤 조건을 20% 앞당긴다
rep("STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3 * 1.05);", "STAR_AT[i] = Math.round(STAR_AT[i] * 2 * 1.3 * 1.05 * 0.8);   /* c114: 20% 앞당김 → [10, 68, 164, 367, 791] */")
open('c114_patch.py', 'w', encoding='utf8').write('# c114: 큰 무리 시야 계산 줄임 · 경보단계 20% 앞당김 (gen_c114.py가 만든다)\nC114_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
