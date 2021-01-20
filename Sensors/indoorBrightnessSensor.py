from Sensors.singleRoomSensor import SingleRoomSensor


class IndoorBrightnessSensor(SingleRoomSensor):
    def __init__(self, env, room_name):
        SingleRoomSensor.__init__(self,
                                  "Indoor Brightness Sensor_%s" % (room_name), env.rooms[room_name].light, room_name)

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].light
