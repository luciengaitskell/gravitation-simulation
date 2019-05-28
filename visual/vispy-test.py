import sys
import numpy as np
from vispy import scene
from vispy.visuals.transforms import STTransform

canvas = scene.SceneCanvas(keys='interactive', bgcolor='black',
                           size=(800, 600), show=True)

view = canvas.central_widget.add_view()
view.camera = 'turntable'

sun = scene.visuals.Sphere(radius=20, method='latitude', parent=view.scene,
                               edge_color='white')

earth = scene.visuals.Sphere(radius=1, method='latitude', parent=view.scene,
                               edge_color='white')


trails = scene.visuals.Markers()

view.add(trails)
trails.set_data(np.array([[0,0,0],[0,0,0]]), edge_color=None, face_color=(1, 1, 1, .5), size=5)


sun.transform = STTransform(translate=[0, 0, 0])
i=0

view.camera.set_range(x=[-55, 55])
view.camera.elevation = 90
view.camera.azimuth = 0





pos = np.random.normal(size=(100000, 3), scale=10)

if __name__ == '__main__' and sys.flags.interactive == 0:
    for i in range(0,100):
        earth.transform = STTransform(translate=[50, 0 + i, 0])
        trails.set_data(pos, edge_color=None, face_color=(1, 1, 1, .5), size=5)
        im = canvas.render()
        canvas.app.sleep(0.1)
        earth.transform = STTransform(translate=[50, 0, 0])
        i+=1
#    canvas.app.run()
