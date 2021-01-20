from Sensors.singleRoomSensor import SingleRoomSensor


class Thermometer(SingleRoomSensor):
    def __init__(self, env, room_name):
        SingleRoomSensor.__init__(self, "Thermometer_%s" % (room_name), env.rooms[room_name].temperature, room_name)

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].temperature
