from Sensors.singleRoomSensor import SingleRoomSensor


class SmokeDetector(SingleRoomSensor):
    def __init__(self, env, name):
        SingleRoomSensor.__init__(self, "Smoke Detector_%s" % (name), env.rooms[name].smoke_detected, name)

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].smoke_detected
