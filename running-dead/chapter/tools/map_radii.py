# 사물 부딪힘 반지름 (map_deco.py · draw_deco.py · 게임의 CH_PROP와 같게)
PR = dict(chair=.34, box=.4, crate=.48, ammo=.48, drum=.4, plant=.3, vending=.55, atm=.48, cart=.4, exting=.22, hose=.48,
          bench=.5, lamp=.14, tlight=.14, bin=.28, dumpster=.6, booth=.5, hydrant=.2, mailbox=.16, postbox=.3, cone=.18, barrier=.5, flag=.12, board=.45, planter=.34, bike=.45,
          parasol=.6, freezer=.55, claw=.5, bookdrop=.4, wheelchair=.36, gurney=.55, sbag=.55, tires=.42, pump=.36, gsign=.2, pillar=.2, statue=.7, fountain=1.35, hoop=.22, amp=.34,
          busstop=.7, excavator=1.0, pile=.8, mixer=.5, toilet=.5, csign=.4, bags=.34)
# 그림 크기 [폭, 높이] — 세워 놓은 그림이라 키 큰 것은 바로 뒤(북쪽)의 사물을 가린다 (map_deco.py가 가려지는 자리를 피할 때 쓴다. 게임의 CH_PROP와 같게)
WH = dict(pillar=(0.4, 2.4), pump=(0.75, 1.5), gsign=(1, 3), tires=(0.85, 1), bin=(0.6, 0.8), drum=(0.78, 1.05), cone=(0.42, 0.6), fountain=(1.6, 1.9), bench=(1.5, 0.8), lamp=(0.7, 2.6),
          vending=(1.15, 1.9), booth=(0.95, 2), amp=(0.7, 0.8), statue=(1.5, 2.6), hoop=(1.7, 3), excavator=(2.8, 1.9), pile=(1.9, 1.1), mixer=(1.2, 1.2), toilet=(0.95, 1.9), csign=(1.2, 1.2),
          flag=(0.9, 3), sbag=(1.3, 0.8), ammo=(1.05, 0.7), crate=(1, 0.85), hydrant=(0.45, 0.7), hose=(0.95, 1.05), exting=(0.45, 0.85), box=(0.85, 0.75), cart=(0.9, 0.9), dumpster=(1.5, 1.15),
          bike=(1.3, 0.85), atm=(0.95, 1.6), planter=(0.7, 0.85), wheelchair=(0.85, 0.95), gurney=(1.5, 0.8), parasol=(1.6, 1.9), freezer=(1.3, 0.85), claw=(0.95, 1.75), bookdrop=(0.8, 1.15),
          board=(1.1, 1.5), barrier=(1.3, 0.85), mailbox=(0.4, 0.95), bags=(0.8, 0.6), tlight=(0.6, 2.4), busstop=(2.2, 1.9), postbox=(0.6, 1.15))
