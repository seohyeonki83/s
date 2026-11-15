# c94: 집 문 폭을 3분의 1 줄인다 (3.4 → 2.27칸. 정문·쪽문 모두, 차고는 그대로)
C94_R = [
 ("return { side, cx: nx > 0 ? B.x1 : nx < 0 ? B.x0 : s.x, cz: nz > 0 ? B.z1 : nz < 0 ? B.z0 : s.z, nx, nz, tx: -nz, tz: nx }; };",
  "return { side, cx: nx > 0 ? B.x1 : nx < 0 ? B.x0 : s.x, cz: nz > 0 ? B.z1 : nz < 0 ? B.z0 : s.z, nx, nz, tx: -nz, tz: nx, w: CHAPTER && B.type === 'house' && !B.garage ? DOOR * 2 / 3 : undefined }; };   /* c94: 집 문은 폭 3분의 2 */"),
 ("flat(L.nz ? DOOR + WALL : WALL, L.nz ? WALL : DOOR + WALL,", "flat(L.nz ? LW + WALL : WALL, L.nz ? WALL : LW + WALL,"),
]
