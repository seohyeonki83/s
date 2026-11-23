// 생성기 시험: node gen9_test.js <첫 씨앗> <개수> [json 저장 경로]
const fs = require('fs');
const M = JSON.parse(fs.readFileSync(__dirname + '/../map_m1.json', 'utf8'));
const src = fs.readFileSync(__dirname + '/gen9.js', 'utf8');
const { chWorldGen } = new Function(src + '\nreturn { chWorldGen };')();
const s0 = +(process.argv[2] || 1), n = +(process.argv[3] || 5);
for (let s = s0; s < s0 + n; s++) {
  const t0 = process.hrtime.bigint(); const W = chWorldGen(M, s); const ms = Number(process.hrtime.bigint() - t0) / 1e6;
  const Z = W.zones, bad = [];
  for (let i = 0; i < Z.length; i++) for (let j = i + 1; j < Z.length; j++) { const a = Z[i], b = Z[j]; if (a[0] < b[2] + 13 - 1e-4 && b[0] < a[2] + 13 - 1e-4 && a[1] < b[3] + 13 - 1e-4 && b[1] < a[3] + 13 - 1e-4) bad.push('zones closer than 13: ' + i + ',' + j); }
  // 물이 단락·다리 틈과 겹치나
  for (const r of W.rivers) for (const z of Z) if (r[0] < z[2] - 1e-6 && r[2] > z[0] + 1e-6 && r[1] < z[3] - 1e-6 && r[3] > z[1] + 1e-6) { bad.push('river overlaps zone'); break; }
  // 건물이 자기 구역 안인가
  for (const b of W.b) { const z = Z[b.zone]; if (b.x - b.w / 2 < z[0] - 0.01 || b.x + b.w / 2 > z[2] + 0.01 || b.z - b.d / 2 < z[1] - 0.01 || b.z + b.d / 2 > z[3] + 0.01) { bad.push('building outside zone ' + b.t); break; } if (b.parent !== undefined) { const P = W.b[b.parent]; if (!P || Math.abs(b.x - P.x) > P.w / 2 || Math.abs(b.z - P.z) > P.d / 2) { bad.push('room outside parent'); break; } } }
  // 면마다 건널목 수 · 간격
  const per = {}; W.passes2.forEach((P) => { for (const [zi, k] of [[P.za, 'a'], [P.zb, 'b']]) { const key = zi + ':' + P.axis + ':' + (k === 'a' ? '+' : '-'); (per[key] = per[key] || []).push(P.c); } });
  let close = 0; for (const k in per) { const a = per[k].sort((p, q) => p - q); for (let i = 1; i < a.length; i++) if (a[i] - a[i - 1] < 14 - 1e-6) close++; }
  const area = W.rivers.reduce((t, r) => t + (r[2] - r[0]) * (r[3] - r[1]), 0), zarea = Z.reduce((t, z) => t + (z[2] - z[0]) * (z[3] - z[1]), 0), tot = (W.mm.x1 - W.mm.x0 + 1) * (W.mm.z1 - W.mm.z0 + 1), sp = W.passes2.reduce((t, P) => t + (P.len - 4.5) * 8, 0);
  console.log('seed', s, '->', W.seed, 'ms', ms.toFixed(1), 'size', (W.mm.x1 - W.mm.x0).toFixed(0) + 'x' + (W.mm.z1 - W.mm.z0).toFixed(0), 'cross', W.passes2.length, 'maxLen', Math.max(...W.passes2.map((P) => P.len - 4.5)).toFixed(1), 'rivers', W.rivers.length, 'b', W.b.length, 'props', W.props.length, 'areaCheck', (area + zarea + sp - tot).toFixed(1), 'tooClose', close, 'bad', JSON.stringify([...new Set(bad)]));
  if (process.argv[4] && s === s0) fs.writeFileSync(process.argv[4], JSON.stringify(W));
}
