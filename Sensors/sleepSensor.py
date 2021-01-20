from Sensors.singleRoomSensor import SingleRoomSensor


class SleepSensor(SingleRoomSensor):
    def __init__(self, env, room_name):
        SingleRoomSensor.__init__(self, "Sleep Sensor_%s" % (room_name), env.rooms[room_name].sleep_detected, room_name)
        self.room_name = room_name

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].sleep_detected
