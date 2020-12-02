from Sensors.sensor import Sensor


class IndoorBrightnessSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Indoor Brightness Sensor", env.light + env.ambient_light * env.ambient_light_mult)

    def update(self, sys, env):
        self.value = env.light + env.ambient_light * env.ambient_light_mult
