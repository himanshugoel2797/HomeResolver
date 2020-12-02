from Sensors.sensor import Sensor


class PowerRate(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Power Rate", env.electricity_rate)

    def update(self, sys, env):
        self.value = env.electricity_rate
