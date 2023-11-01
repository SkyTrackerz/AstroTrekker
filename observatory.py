class Observatory:
    def __init__(self):
        self.targetTurntableAngle = 0
        self.targetTrackAngle = 0
        self.targetPivotAngle = 0

        self.turntableAngle = 0
        self.trackAngle = 0
        self.pivotAngle = 0

    def update_target_angles(self, new_turntable_angle, new_track_angle, new_pivot_angle):
        self.targetTurntableAngle = new_turntable_angle
        self.targetTrackAngle = new_track_angle
        self.targetPivotAngle = new_pivot_angle

    def update(self):
        pass
