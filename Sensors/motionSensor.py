from Sensors.sensor import Sensor


class MotionSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Motion Sensor", env.motion_detected)

    def update(self, sys, env):
        self.value = env.motion_detected
