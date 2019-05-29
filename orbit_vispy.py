import numpy as np
import sys
from graphics import OrbitalGraphics, STTransform

from sim.body import Body, KEY
from sim.simulation import Simulation


# -- Calculation Functions --
M_EARTH = 5.972e24  # kg
R_EARTH = 6.5e6  # m
M_SUN = 1.989e30  # kg


g = OrbitalGraphics()
b = [
    Body(5, np.array([[50, 0.],[0., 10.], [0., 0.]])),
    #Body(M_EARTH, np.array([[ R_EARTH + 408.*1e3 , 0.],[0., 7660.], [0., 0.]])),
    #Body(M_SUN, np.array([[0., 0.],[0., 0.], [0., 0.]]), lock=True)
Body(5e13, np.array([[0., 0.],[0., 0.], [0., 0.]]), lock=True)
]
s = Simulation(np.array(0.1), np.array(95*60*4), b)

if __name__ == '__main__' and sys.flags.interactive == 0:
    MAX = 10000
    tracking = np.zeros((MAX, 3))
    for i in range(0, MAX):
        s.frame()
        tracking[i, 0] = b[0].history[i-1][KEY.POS, 0]
        tracking[i, 1] = b[0].history[i-1][KEY.POS, 1]
        tracking[i, 2] = 0
        if i % 3 == 0:
            g.earth_transform = STTransform(translate=[b[0].state[0, 0], b[0].state[0, 1], 0])
            g.trails.set_data(tracking[0:i+1], edge_color=None, face_color=(1, 1, 1, .5), size=5)
            g.sun.transform = STTransform(translate=[b[1].state[0, 0], b[1].state[0, 1], 0])
            print(np.linalg.norm(b[0].state[KEY.VEL]), b[0].state[KEY.ACC])
            g.draw()
