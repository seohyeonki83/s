# c426: 배지 줄 원래대로
C426_R = [('      const row = i < 6 ? Math.floor(i / 3) : 2 + Math.floor((i - 6) / 2), col = i < 6 ? i % 3 : (i - 6) % 2;   // c425: 아래 두 줄은 3개씩, 그 위로 2개씩', '      const row = i < 3 ? 0 : 1 + Math.floor((i - 3) / 2), col = i < 3 ? i : (i - 3) % 2;   // c426: 원래대로 — 첫 줄 3개, 그 위로 2개씩')]
