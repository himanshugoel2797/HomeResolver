from Sensors.sensor import Sensor


class PowerMeter(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Power Meter", env.power_consumed_instant)

    def update(self, sys, env):
        self.value = env.power_consumed_instant
