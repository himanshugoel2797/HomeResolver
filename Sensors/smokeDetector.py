from Sensors.sensor import Sensor

class SmokeDetector(Sensor):
    room_name = None
    def __init__(self, env, name):
        Sensor.__init__(self, "Smoke Detector_%s" % (name), env.rooms[name].smoke_detected)
        self.room_name = name

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].smoke_detected