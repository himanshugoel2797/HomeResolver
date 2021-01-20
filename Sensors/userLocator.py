from Sensors.sensor import Sensor


class UserLocator(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "User Locator", "livingroom")

    def update(self, sys, env):
        if env.presence_detected:
            # Check all rooms
            for k, v in env.rooms.items():
                if v.presence_detected:
                    self.value = k
                    break
        else:
            self.value = "outside_1m"