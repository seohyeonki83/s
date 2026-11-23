# c411: 작은 좀비 미는 힘 3분의 1
C411_R = [('function chMini(c) { c.mini = true; c.mesh.scale.setScalar(0.5); if (!c.mut) c.mesh.material.color.setHex(0xb9c8f9); }', 'function chMini(c) { c.mini = true; c.mesh.scale.setScalar(0.5); if (!c.mut) { c.mesh.material.color.setHex(0xb9c8f9); c.force = 1 / 3;   /* c411: 미는 힘 = 보통 좀비의 3분의 1 */ } }')]
