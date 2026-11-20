# c227: 무기 버튼 옆 돋보기 — 버튼 가운데 높이에 정확히 맞추고(가로 정렬) 오른쪽으로 4px 더
C227_R = [
 ("  .item .mag, .pbadge .mag { position: absolute; right: -19px; bottom: -6px;", "  .item .mag, .pbadge .mag { position: absolute; right: -23px; top: 50%; bottom: auto; transform: translateY(-50%);   /* c227 */"),
 ("  .pbadge .mag { right: -13px; bottom: -11px;", "  .pbadge .mag { right: -13px; top: auto; transform: none; bottom: -11px;"),
]
