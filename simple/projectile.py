import math
from enum import Enum

import numpy as np
from matplotlib import pyplot as plt

if False:
    import warnings
    warnings.filterwarnings("error")


class CalcMode(Enum):
    STD = 0
    AVG = 1


MODE = CalcMode.AVG


T_STEP = np.array(0.1)  # sec
T_MAX = np.array(3)  # sec
T_ITER = math.floor(T_MAX / T_STEP)  # number of iterations based on time designation


# -- MODEL --:
history = np.ndarray((T_ITER, 3, 2))

INIT_FRAME = np.array(
    [
        np.array([0., 0.]),  # Position from origin (m)
        np.array([10., 10.]),  # Velocity (m/s)
        np.array([0., -9.8])  # Acceleration (m/s^2)
    ]
)
history[0] = INIT_FRAME

for istep in range(1, T_ITER):
    t = T_ITER * istep  # (sec) Time at step

    if MODE == CalcMode.STD:
        history[istep] = history[istep - 1]  # Copy previous state
        step = history[istep-1, 1:3] * T_STEP  # Calculate delta for pos, vel
        history[istep, 0:2] += step  # Add pos, vel delta
    elif MODE == CalcMode.AVG:
        vp = history[istep-1, 1] + history[istep-1, 2] * T_STEP
        xp = history[istep-1, 0] + ((vp + history[istep-1, 1])/2)*T_STEP
        history[istep] = np.array([xp, vp, history[istep-1, 2]])


# STATS:
try:
    ground = np.where(history[:, 0, 1] <= 0)[0][1]
except IndexError:
    print("Projectile did not reach ground!")
    raise

# -- CALCULATED --:
calculated = np.ndarray((T_ITER, 3, 2))
for istep in range(0, T_ITER):
    t = T_STEP * istep  # (sec) Time at step
    x = np.array([
        t*INIT_FRAME[1,0],  # horizontal
        t*INIT_FRAME[1,1] + (INIT_FRAME[2,1]*(t**2)/2)  # vertical
    ])
    v = np.array([
        INIT_FRAME[1,0],  # horizontal
        INIT_FRAME[1,1] + (INIT_FRAME[2,1]*t)
    ])
    a = INIT_FRAME[2]
    calculated[istep] = np.array([x,v,a])

# #PRINT:
print("Max Height: {:.2f}m".format(np.max(history[:, 0, 1])))
print("Range: {:.2f}m".format(history[ground, 0, 0]))

# PLOTTING:
plt.figure(1)

plt.subplot(211)

#plt.plot(history[:, 0, 1])  # y pos vs. time
#plt.plot(calculated[:, 0, 1], c='r', linestyle='dashed')  # y pos vs. time CALCULATED

plt.plot(*history[:, 0, :].T)  # y pos vs. time
plt.plot(*calculated[:, 0, :].T, c='r', linestyle='dashed')  # y pos vs. time CALCULATED

plt.subplot(212)

plt.plot(history[:, 0, 1]-calculated[:, 0, 1])  # y pos difference vs time

plt.show()
