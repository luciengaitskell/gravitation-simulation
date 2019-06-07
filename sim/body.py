import numpy as np


class KEY:
    POS = 0
    VEL = 1
    ACC = 2


G = 6.67e-11  # m^3 / kg*s^2


class Body:
    def __init__(self, mass, pos, color, lock=False):
        self.history = []
        self.state = pos
        self.mass = mass
        self.LOCK = lock

        self.color = color

        self.curr_state = None

    def accel_from_pos(self, b2, pos=None):
        if self.LOCK: return np.array([0.,0.])
        if pos is None:
            pos = self.history[-1][0]

        diff = pos - b2.state[0]
        r = np.linalg.norm(diff)
        d = -diff / r  # Normalized and inverted x/y direction vector
        a = d * (b2.mass * G) / r ** 2  # Scale based on newton's gravitation equation
        return a

    @property
    def state(self):
        try:
            return self.history[-1]
        except IndexError:
            return None

    @state.setter
    def state(self, state):
        self.history.append(state)
