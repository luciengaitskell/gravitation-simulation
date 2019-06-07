import math

from .body import Body, KEY, np


class Simulation:
    def __init__(self, tstep, tmax, bodies):
        # -- Simulation Vars --:
        self.T_STEP = tstep  # sec
        self.T_MAX = tmax  # sec
        self.T_ITER = math.floor(tmax / tstep)  # number of iterations based on time designation

        self.i_step = 0

        self.bodies = bodies
        for b in self.bodies:
            b.tracking = np.zeros((self.T_ITER, 3))

    def frame(self):
        self.i_step += 1
        for b in self.bodies:
            b.curr_state = b.state

        for i in range(0,5):
            self._calc_accel()
            self._move_frame()

        for b in self.bodies:
            b.history.append(None)
            b.history[self.i_step] = b.curr_state
            b.tracking[self.i_step-1, 0] = b.history[self.i_step-1][KEY.POS, 0]
            b.tracking[self.i_step-1, 1] = b.history[self.i_step-1][KEY.POS, 1]
            b.tracking[self.i_step-1, 2] = 0

    def _calc_accel(self):
        for b in self.bodies:
            b.curr_state[KEY.ACC] = np.array([0.,0.])
            for t in self.bodies:
                if b is t: continue
                old_acc = b.accel_from_pos(t)
                new_acc = b.accel_from_pos(t, pos=b.curr_state[KEY.POS])
                b.curr_state[KEY.ACC] += (old_acc + new_acc)/2

    def _move_frame(self):
        t = self.T_STEP * self.i_step  # (sec) Time at step

        for b in self.bodies:
            self._body_calc_frame(b)

    def flush_frame(self):
        for b in self.bodies:
            b.state = b.curr_state
            b.curr_state = None

    def _body_calc_frame(self, b):
        last = b.history[self.i_step - 1]

        ap = b.curr_state[KEY.ACC]
        vp = last[KEY.VEL] + ap * self.T_STEP
        xp = last[KEY.POS] + (vp) * self.T_STEP

        rad = np.linalg.norm(xp)
        vp_speed = np.linalg.norm(vp)
        ang_momentum = rad * vp_speed

        if len(b.history) > self.i_step+1:
            raise IndexError("Too many history elements")
        b.curr_state[KEY.POS] = xp
        b.curr_state[KEY.VEL] = vp

