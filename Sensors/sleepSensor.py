from Sensors.sensor import Sensor

class SleepSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Sleep Sensor", env.sleep_detected)

    def update(self, sys, env):
        self.value = env.sleep_detected
