from Sensors.sensor import Sensor


class OutdoorBrightnessSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Outdoor Brightness Sensor", env.ambient_light)

    def update(self, sys, env):
        self.value = env.ambient_light
