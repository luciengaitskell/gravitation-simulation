import numpy as np
import sys
from threading import Thread
import time

from vispy import app
from visual.graphics import OrbitalGraphics, STTransform

from sim.body import Body, KEY
from sim.simulation import Simulation


# -- Calculation Variables --
M_EARTH = 5.972e24  # kg
R_EARTH = 6.5e6  # m
M_SUN = 1.989e30  # kg

# -- Graphics Variables --
TIME_WARP = 2  # times realtime

# -- Thread Variables --
T_START = None
running = True

b = [
    Body(10e11, np.array([[40., 0.],[0., 10.], [0., 0.]]), 'green'),  # "EARTH"
    Body(5e13, np.array([[0., 0.],[0., 0.], [0., 0.]]), 'white', lock=False),  # "SUN"
    Body(5e11, np.array([[45., 0.],[0., 5.], [0., 0.]]), 'red', lock=False),  # "OTHER ONE"
    Body(7e11, np.array([[-45., 0.],[0., 5.], [0., 0.]]), 'red', lock=False),  # "OTHER ONE"
    Body(1e11, np.array([[30., 15.],[0., -4.], [0., 0.]]), 'white', lock=False)  # "SECOND"
]
s = Simulation(np.array(0.1), np.array(95*60*4), b)
g = OrbitalGraphics(b)


def simulation():
    global s
    lag = 0
    while running:
        target_delta = (time.time() - T_START) * TIME_WARP
        curr_delta = s.T_STEP * s.i_step

        if curr_delta <= target_delta:
            lag += 1
            s.frame()
            if lag % 5 == 0:
                print("lag: {}".format(lag))
        else:
            lag = 0
            time.sleep(0.05)


_thread_sim = Thread(target=simulation, name="sim-loop")


def vis_update(ev):
    for b_i in range(len(b)):
        g.bodies[b_i].transform = STTransform(translate=[b[b_i].state[0, 0], b[b_i].state[0, 1], 0])
        g.trails[b_i].set_data(b[b_i].tracking[0:s.i_step], edge_color=b[b_i].color, face_color=None, size=5)

    # print(np.linalg.norm(b[0].state[KEY.VEL]), b[0].state[KEY.ACC])


#timer = app.Timer(interval='auto', connect=vis_update)
timer = app.Timer(interval='0.1', connect=vis_update)


if __name__ == '__main__' and sys.flags.interactive == 0:
    T_START = time.time()  # Set simulation start time (for live update)
    _thread_sim.start()  # Start simulation thread
    timer.start()

    try:
        app.run()
    except KeyboardInterrupt:
        running = False
        _thread_sim.join()
