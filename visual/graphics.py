import math
import numpy as np

from vispy import scene
from vispy.visuals.transforms import STTransform


class OrbitalGraphics:
    def __setup_trail(self, t):
        self.view.add(t)
        t.set_data(np.array([[0, 0, 0], [0, 0, 0]]), edge_color=None, face_color=(1, 1, 1, .5), size=5)

    def __setup_camera(self):
        self.view.camera.set_range(x=[-55, 55])
        self.view.camera.elevation = 90
        self.view.camera.azimuth = 0

    def __init__(self, bodies):
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                                        size=(800, 600), show=True)

        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'

        self.bodies = []
        self.trails = []

        for b in bodies:
            self.bodies.append(scene.visuals.Sphere(radius=math.pow(b.mass/1e11, 1/3), method='latitude',
                                                    parent=self.view.scene, edge_color=b.color))
            self.trails.append(scene.visuals.Markers())
            self.__setup_trail(self.trails[-1])

        self.__setup_camera()

    '''
    @property
    def earth_transform(self):
        return self.earth.transform

    @earth_transform.setter
    def earth_transform(self, trans):
        self.earth.transform = trans'''

    def draw(self, t=0.1):
        im = self.canvas.render()
        self.canvas.app.sleep(t)
        return t, im
