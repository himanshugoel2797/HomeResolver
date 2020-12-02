from Sensors.sensor import Sensor

class SmokeDetector(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Smoke Detector", env.smoke_detected)

    def update(self, sys, env):
        self.value = env.smoke_detected