import pathlib
s = pathlib.Path('c590.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    if (CHAPTER && CH_SK !== 1 && (v.kind === 'obj' || v.kind === 'safe') && !(v.car && v.car.tank)) dmg /= CH_SK;",
    "    if (CHAPTER && CH_SK !== 1 && (v.kind === 'obj' || v.kind === 'safe') && !(v.car && (v.car.tank || v.car.cvy))) dmg /= CH_SK;   /* c591: 보스 차량(군인차 부대)은 챕터 강화 빼기 */")
rep("const gd = (CH_GOO_DOT + chAcidB()) * CH_UPK.atk;   /* c475 */", "const gd = (CH_GOO_DOT + chAcidB()) * CH_UPK.atk / (CH_SK !== 1 && !car.tank && !car.cvy ? CH_SK : 1);   /* c591: 차량 도트도 챕터 강화 */   /* c475 */")
rep("    if (t === 'armor') b.maxHp = 380 * HPK * 0.9;", "    if (t === 'armor') { b.maxHp = 380 * HPK * 0.9 * CH_UPK.ahp; b.hp = Math.min(b.hp, b.maxHp); }   /* c591: 분홍에서 얻은 덩치도 동료 체력 성장 */")
pathlib.Path('c591_patch.py').write_text('C591_R = ' + repr(R) + '\n')
print(len(R))
