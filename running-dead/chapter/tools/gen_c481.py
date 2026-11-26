import pathlib
s = pathlib.Path('c480.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
# 정전기 삭제
rep("    const sr = chRedR('taser'); if (sr) chStatL.push({ e, t: T, r: sr });   // c468: 정전기 숙주", "    // c481: 정전기 삭제 (c468)")
rep("+ (n > 5 ? ` · 정전기 ${(MELEE * chStatK(n - 5)).toFixed(1)}칸` : ''),   /* c468 */", "+ (n > 5 ? ` · 기계 오작동 ${25 + 5 * (n - 6)}%` : ''),   /* c481 */")
# 총 쏘는 인간은 오작동 드론도 쏜다 — 좀비와 드론 중 가까운 쪽
rep("    if (c.state === 'lured') c.burstN = 0;   // c464", r"""    if (CHAPTER && chMadDr.length && c.police && c.state !== 'lured' && c.atkT <= 0 && !c.mad) {   // c481: 오작동 드론 — 총 쏘는 인간은 거리만 보고 가까운 쪽을 쏜다
      let bd = c.sight, d = null; for (const q of chMadDr) { if (q.dead || q.madIn > 0) continue; const k = Math.hypot(q.x - c.foot.x, q.z - c.foot.z); if (k < bd && !fireBlocked(c.foot.x, c.foot.z, q.x, q.z)) { bd = k; d = q; } }
      const zz = d ? nearestZombie(c, c.sight, true) : null;
      if (d && (!zz || Math.hypot(zz.foot.x - c.foot.x, zz.foot.z - c.foot.z) > bd)) {
        const ux = d.x - c.foot.x, uz = d.z - c.foot.z, ul = Math.hypot(ux, uz) || 1;
        c.shotT = 0; c.shotAt = d; c.recoilT = 0; c.recoilX = -ux / ul; c.recoilZ = -uz / ul; c.vel.set(0, 0);
        landHit(c, d, c.sniper ? CH_DMG_SN : c.soldier ? CH_DMG_SO * (c.turret ? 8 : 4) : CH_DMG_PO);
        c.atkT = HIT_EVERY * (c.sniper ? 4 : 1);
      }
    }
    if (c.state === 'lured') c.burstN = 0;   // c464""")
rep("      const d = chMadDr[i];\n", "      const d = chMadDr[i];\n      if (d.dead) { scene.remove(d.madS); chMadDr.splice(i, 1); continue; }   // c481: 인간 총에 맞아 터짐\n")
pathlib.Path('c481_patch.py').write_text('C481_R = ' + repr(R) + '\n')
print(len(R))
