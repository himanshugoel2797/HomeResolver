from Sensors.sensor import Sensor


class PresenceSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Presence Sensor", env.presence_detected)

    def update(self, sys, env):
        self.value = env.presence_detected
