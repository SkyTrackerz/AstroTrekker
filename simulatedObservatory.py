#from vpython import vector, box, color, cylinder
#import numpy as np
from starTracker import Observatory
from math import pi

class SimulatedObservatory(Observatory):
    def __init__(self, lattitude, longitude):
        super().__init__(lattitude, longitude)

        box(pos=vector(0, 0, 0), size=vector(200, 0, 200), color=color.green)
        box(pos=vector(0, 1, 0), size=vector(25, 2, 12), color=color.cyan)

        leg1 = box(pos=vector(0, 1, 0), size=vector(30, 2, 2), color=color.cyan)
        leg2 = box(pos=vector(0, 1, 0), size=vector(30, 2, 2), color=color.cyan)
        leg1.rotate(angle=pi / 4, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
        leg2.rotate(angle=-pi / 4, axis=vector(0, 1, 0), origin=vector(0, 0, 0))

        turntable = box(pos=vector(0, 3, 0), size=vector(20, 2, 9), color=color.magenta)
        turntableLeftSide = box(pos=vector(0, 7, 5), size=vector(20, 10, 1), color=color.magenta)
        turntableRightSide = box(pos=vector(0, 7, -5), size=vector(20, 10, 1), color=color.magenta)

        track = box(pos=vector(0, 6, 0), size=vector(9, 2, 9), color=color.green)

        pivot = cylinder(pos=vector(0, 7.5, 0), axis=vector(0, 1, 0), radius=4, color=color.orange)
        cameraBody = box(pos=vector(0, 9.25, 0), size=vector(4, 1.5, 6), color=color.gray(0.25))
        cameraLens = cylinder(pos=vector(0, 10, 0), axis=vector(0, 3, 0), radius=1.75, color=color.gray(0.35))

        self.turntableGroup = np.array((turntable, turntableLeftSide, turntableRightSide, track, pivot, cameraBody, cameraLens))
        self.trackGroup = np.array((track, pivot, cameraBody, cameraLens))
        self.pivotGroup = np.array((pivot, cameraBody, cameraLens))

    def move(self):
        for obj in self.turntableGroup:
            obj.rotate(angle=self.targetTurntableAngle - self.turntableAngle,
                       axis=vector(0, 1, 0),
                       origin=vector(0, 0, 0))

        for obj in self.trackGroup:
            obj.rotate(angle=self.targetTrackAngle - self.trackAngle,
                       axis=vector(1, 0, 0),
                       origin=vector(0, 15, 0))

        for obj in self.pivotGroup:
            obj.rotate(angle=self.targetPivotAngle - self.pivotAngle,
                       axis=vector(0, 1, 0),
                       origin=vector(0, 0, 0))
