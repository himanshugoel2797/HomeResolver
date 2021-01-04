from Sensors.sensor import Sensor


class UserLocator(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "User Locator", env.user_location)

    def update(self, sys, env):
        self.value = env.user_location
