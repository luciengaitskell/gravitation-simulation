import math
from enum import Enum

import numpy as np
from matplotlib import pyplot as plt


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
T_STEP = np.array(10.)  # sec
T_MAX = np.array(10e2* 95*60)  # sec
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

for istep in range(1, T_ITER):
    t = T_ITER * istep  # (sec) Time at step

    # Velocity   v = u + at
    v_step = history[istep-1, 2] * T_STEP
    vp = history[istep-1, 1] + v_step
    vp_speed = np.linalg.norm(vp)

    # Position based on average velocity from old+new and s1 = s0 + u dt + 1/2 a dt^2
    #   s1 = s0 + (u+v)/2 * dt
    #      = s0 + (2u + a * dt)/2 * dt
    #   s1 = s0 + u * dt + 1/2 * a * dt^2
    xp = history[istep-1, 0] + ((vp + history[istep-1, 1])/2)*T_STEP
    rad = np.linalg.norm(xp)

    # LIMIT velocity, based on conservation of energy;
    ske = 1/2 * vp_speed**2  # Calculate kinetic energy per kg
    gpe = -G*M_EARTH / rad  # Calculate gravitational potential energy per kg

    energy = ske + gpe  # Calculate energy in frame
    energy_clip = np.clip(energy, None, TOTAL_ENERGY)  # Limit energy to total initial energy

    vp_adj = np.sqrt(energy_clip/energy)  # Scale velocity, by energy limiting factor (square rooted)
    #vp *= vp_adj

    # Acc from inverse sq law
    ap = (accel_from_x(xp) + accel_from_x(history[istep-1, 0]))/2

    ang_momentum = rad * vp_speed

    history[istep] = np.array([xp, vp, ap])


# PLOTTING:
plt.figure(1)

plt.scatter(0,0,c='red')
t_seconds = np.arange(0, T_MAX, T_STEP)

plt.scatter(*(history[:, 0, :].T/1e3), c=t_seconds, s=0.1)  # y pos vs. x pos

plt.xlabel('km')
plt.ylabel('km')
plt.xlim(-1.2*R_EARTH/1e3,1.2*R_EARTH/1e3)
plt.ylim(-1.2*R_EARTH/1e3,1.2*R_EARTH/1e3)
plt.gca().set_aspect('equal')

cbar = plt.colorbar(ticks=np.arange(0, T_MAX+0.01, T_MAX/4))
cbar.set_label("time (sec)")

plt.show()

plt.figure(2)

ske = 1/2 * (np.linalg.norm(history[:, 1], axis=1)**2)
gpe = -G*M_EARTH / np.linalg.norm(history[:, 0], axis=1)

plt.plot(t_seconds, ske+gpe)
plt.xlabel('Time (sec)')
plt.ylabel('Total Energy (J)')

plt.show()

