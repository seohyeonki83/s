# c146: 적의 공격력 20% 더 올림 (장갑차는 빼고)
C146_R = [
 ("if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15;", "if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= a.kind === 'tank' ? 1.15 : 1.15 * 1.2;   /* c146: 사람·경찰·군인·저격수 20% 더 (합쳐서 1.38배) — 장갑차는 1.15배 그대로 */"),
]
