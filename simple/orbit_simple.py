import math
from enum import Enum

import numpy as np
from matplotlib import pyplot as plt


class KEY:
    POS = 0
    VEL = 1
    ACC = 2


# -- Calculation Functions --
M_EARTH = 5.972e24  # kg
G = 6.67e-11  # m^3 / kg*s^2
R_EARTH = 6.5e6  # m

def accel_from_x(x):
    r = np.linalg.norm(x)
    d = -x/r  # Normalized and inverted x/y direction vector
    a = d * (M_EARTH*G) / r**2  # Scale based on newton's gravitation equation
    return a


# -- Simulation Vars --:
T_STEP = np.array(0.1)  # sec
T_MAX = np.array(95*60*4)  # sec
T_ITER = math.floor(T_MAX / T_STEP)  # number of iterations based on time designation


# -- MODEL --:
history = np.ndarray((T_ITER, 3, 2))

INIT_FRAME = np.array(
    [
        np.array([ R_EARTH + 408.*1e3 , 0.]),  # Position from origin (m)
        np.array([0., 7660.]),  # Velocity (m/s)
        np.array([0., 0.])  # Acceleration (m/s^2)
    ]
)
INIT_FRAME[2] = accel_from_x(INIT_FRAME[0])  # Calculate acceleration at initial position
TOTAL_ENERGY = (1/2 * np.linalg.norm(INIT_FRAME[1])**2) - (G*M_EARTH / np.linalg.norm(INIT_FRAME[0]))

history[0] = INIT_FRAME  # Save initial frame

plt.figure(1)

graph = plt.scatter(0,0,c='red')

plt.xlabel('km')
plt.ylabel('km')
plt.xlim(-1.2*R_EARTH/1e3,1.2*R_EARTH/1e3)
plt.ylim(-1.2*R_EARTH/1e3,1.2*R_EARTH/1e3)
plt.gca().set_aspect('equal')


plt.draw()
#cbar = plt.colorbar(ticks=np.arange(0, T_MAX+0.01, T_MAX/4))
#cbar.set_label("time (sec)")


GRAPHICS_SKIP = 800

try:
    for istep in range(1, T_ITER):
        t = T_STEP * istep  # (sec) Time at step

        last = history[istep-1]

        # Acc from inverse sq law
        ap = last[KEY.ACC]

        for i in range(0, 5):
            vp = last[KEY.VEL] + ap * T_STEP
            xp = last[KEY.POS] + (vp) * T_STEP
            ap = (accel_from_x(xp) + accel_from_x(last[KEY.POS])) / 2

        rad = np.linalg.norm(xp)
        vp_speed = np.linalg.norm(vp)
        ang_momentum = rad * vp_speed

        history[istep] = np.array([xp, vp, ap])

        if (istep) % GRAPHICS_SKIP == 0:
            #plt.scatter(*(xp.reshape(2,1) / 1e3), c=[t], s=0.05)  # y pos vs. x pos
            missing_history = history[istep-GRAPHICS_SKIP:istep, 0, :].T / 1e3
            plt.scatter(*(missing_history), c=np.arange(T_STEP*(istep-GRAPHICS_SKIP), t, T_STEP), s=0.05)  # y pos vs. x pos
            plt.draw()
            plt.pause(0.001)
        #plt.scatter(*(history[:, 0, :].T / 1e3), c=t_seconds, s=0.05)  # y pos vs. x pos
except KeyboardInterrupt:
    pass

# PLOTTING:
plt.figure(2)

ske = 1/2 * (np.linalg.norm(history[:, 1], axis=1)**2)
gpe = -G*M_EARTH / np.linalg.norm(history[:, 0], axis=1)

energy = ske+gpe

t_seconds = np.arange(0, T_MAX, T_STEP)
plt.plot(t_seconds, 100*((energy-TOTAL_ENERGY)/np.abs(TOTAL_ENERGY)))
plt.xlabel('Time (sec)')
plt.ylabel('Total Energy (%)')

plt.show()

