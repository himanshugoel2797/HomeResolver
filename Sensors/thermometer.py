from Sensors.sensor import Sensor


class Thermometer(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Thermometer", env.temperature)

    def update(self, sys, env):
        self.value = env.temperature
