# c138: 현금을 알아채는 거리 = 누구나 같은 값 (기준 시야 7.2칸 × 현금 배수). 저격수도, 시야가 늘거나 줄어든 순간에도 똑같다
C138_R = [
 ("chSight0(c) * cashK()", "SIGHT * cashK()", 3),
 ("if (bd <= c.sense * cashK()) enterLured(c);", "if (bd <= SENSE * cashK()) enterLured(c);   /* c138: 바로 홀리는 거리도 기준 인지거리(3.6칸)로 통일 */"),
]
