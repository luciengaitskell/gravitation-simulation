import numpy as np
import sys
from graphics import OrbitalGraphics, STTransform

from sim.body import Body, KEY
from sim.simulation import Simulation


# -- Calculation Functions --
M_EARTH = 5.972e24  # kg
R_EARTH = 6.5e6  # m
M_SUN = 1.989e30  # kg


b = [
    Body(10e11, np.array([[40., 0.],[0., 10.], [0., 0.]]), 'green'),  # "EARTH"
    Body(5e13, np.array([[0., 0.],[0., 0.], [0., 0.]]), 'white', lock=False),  # "SUN"
    Body(5e11, np.array([[45., 0.],[0., 5.], [0., 0.]]), 'red', lock=False),  # "OTHER ONE"
    Body(7e11, np.array([[-45., 0.],[0., 5.], [0., 0.]]), 'red', lock=False),  # "OTHER ONE"
    Body(1e11, np.array([[30., 15.],[0., -4.], [0., 0.]]), 'white', lock=False)  # "SECOND"
]
s = Simulation(np.array(0.01), np.array(95*60*4), b)
g = OrbitalGraphics(b)

if __name__ == '__main__' and sys.flags.interactive == 0:
    for i in range(0, s.T_ITER):
        s.frame()
        if i % 30 == 0:
            for b_i in range(len(b)):
                g.bodies[b_i].transform = STTransform(translate=[b[b_i].state[0, 0], b[b_i].state[0, 1], 0])
                g.trails[b_i].set_data(b[b_i].tracking[0:i+1], edge_color=b[b_i].color, face_color=None, size=5)
            print(np.linalg.norm(b[0].state[KEY.VEL]), b[0].state[KEY.ACC])
            g.draw()
