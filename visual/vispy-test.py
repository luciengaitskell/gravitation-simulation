import numpy as np
import sys
from graphics import OrbitalGraphics, STTransform


if __name__ == '__main__' and sys.flags.interactive == 0:
    g = OrbitalGraphics()

    for i in range(0, 100):
        g.earth_transform = STTransform(translate=[50, 0 + i, 0])
        pos = np.random.normal(size=(100000, 3), scale=10)
        g.trails.set_data(pos, edge_color=None, face_color=(1, 1, 1, .5), size=5)
        g.draw()
        g.earth_transform = STTransform(translate=[50, 0, 0])
